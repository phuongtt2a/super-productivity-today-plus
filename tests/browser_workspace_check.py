"""Today+ workspace feature tests: ordering, Working Now, native tracking/focus and restore.

Uses an instrumented mock plugin API. Real-host testing is still required.
"""
from pathlib import Path
from datetime import date
import json
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / "plugin/index.html").read_text(encoding="utf-8")
TODAY = date.today().isoformat()
tasks = [
    {"id":"t1","title":"Morning project","projectId":"work","isDone":False,"dueDay":TODAY,"subTaskIds":["c1","c2"]},
    {"id":"c1","title":"Sketch plan","projectId":"work","isDone":False,"parentId":"t1","subTaskIds":[]},
    {"id":"c2","title":"Collect facts","projectId":"work","isDone":False,"parentId":"t1","subTaskIds":[]},
    {"id":"t2","title":"Review design","projectId":"work","isDone":False,"dueDay":TODAY,"subTaskIds":[]},
    {"id":"t3","title":"Write proposal","projectId":"work","isDone":False,"dueDay":TODAY,"subTaskIds":[]}
]
habits = [
    {"id":"h1","title":"Drink enough water","type":"ClickCounter","isEnabled":True,"isTrackStreaks":True,"streakMinValue":8,"countOnDay":{}},
    {"id":"h2","title":"Read","type":"ClickCounter","isEnabled":True,"isTrackStreaks":True,"streakMinValue":1,"countOnDay":{}},
    {"id":"h3","title":"Go jogging","type":"ClickCounter","isEnabled":True,"isTrackStreaks":True,"streakMinValue":1,"countOnDay":{}},
    {"id":"h4","title":"Practice piano","type":"StopWatch","isEnabled":True,"isTrackStreaks":True,"streakMinValue":3600000,"countOnDay":{TODAY:3600000}}
]
API = r"""
window.__dataTasks = __TASKS__;
window.__dataHabits = __HABITS__;
window.__today = "__TODAY__";
window.__saved = __SAVED__;
window.__events = [];
window.__hooks = {};
window.PluginAPI = {
  Hooks:{
    TASK_CREATED:'taskCreated', TASK_UPDATE:'taskUpdate',
    TASK_COMPLETE:'taskComplete', TASK_DELETE:'taskDelete',
    CURRENT_TASK_CHANGE:'currentTaskChange',
    PERSISTED_DATA_CHANGED:'persistedDataChanged',
    DATA_CHANGED:'dataChanged', DAY_CHANGE:'dayChange'
  },
  registerHook:(name,fn)=>{window.__hooks[name]=fn},
  getTasks:async()=>window.__dataTasks.map(t=>({...t})),
  getAllSimpleCounters:async()=>window.__dataHabits.map(h=>({...h})),
  getAllProjects:async()=>[{id:'work',title:'Work'}],
  getDayContext:async()=>({todayStr:window.__today}),
  loadSyncedData:async(key)=>window.__saved[key]??null,
  persistDataSynced:async(data,key)=>{
    window.__events.push({type:'persist',key});
    window.__saved[key]=data;
  },
  updateTask:async(id,updates)=>{
    window.__events.push({type:'update',id,updates});
    Object.assign(window.__dataTasks.find(t=>t.id===id),updates);
  },
  setCounter:async(id,value)=>{
    const habit=window.__dataHabits.find(h=>h.id===id);
    habit.countOnDay[window.__today]=value;
  },
  selectTask:async(id)=>{window.__events.push({type:'select',id})},
  startTracking:async(id)=>{
    window.__events.push({type:'startTracking',id});
    window.__hooks.currentTaskChange?.({current:window.__dataTasks.find(t=>t.id===id),previous:null});
  },
  stopTracking:async()=>{
    window.__events.push({type:'stopTracking'});
    window.__hooks.currentTaskChange?.({current:null,previous:null});
  },
  dispatchAction:action=>window.__events.push({type:'focus',action})
};
void 0;
"""
def install(page,saved=None,without_tracking=False):
    page.goto('about:blank')
    data = (API.replace('__TASKS__',json.dumps(tasks,ensure_ascii=False))
        .replace('__HABITS__',json.dumps(habits,ensure_ascii=False))
        .replace('__TODAY__',TODAY)
        .replace('__SAVED__',json.dumps(saved or {})))
    page.evaluate(data)
    if without_tracking:
        page.evaluate('delete window.PluginAPI.startTracking; delete window.PluginAPI.stopTracking')
    page.set_content(HTML)
    page.wait_for_selector('#tasks [data-sort-id="t1"]')
    page.wait_for_selector('#habits [data-sort-id="h3"]')

def order(page,selector):
    return page.locator(selector).evaluate_all(
        "(rows)=>rows.map(row=>row.getAttribute('data-sort-id'))"
    )

with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,args=['--no-sandbox'])
    try:
        page=browser.new_page(viewport={'width':1200,'height':820})
        install(page)
        assert order(page,'#tasks [data-sort-kind="task"]')==['t1','t2','t3']
        page.locator('#arrange-tasks').click()
        page.locator('#tasks [data-order-kind="task"][data-order-id="t3"][data-move="top"]').click()
        assert order(page,'#tasks [data-sort-kind="task"]')[0]=='t3'
        page.locator('#tasks [data-order-kind="child"][data-order-id="c2"][data-move="top"]').click()
        assert order(page,'#tasks .task-children [data-sort-kind="child"]')[:2]==['c2','c1']
        print('tasks and nested subtasks move-to-top: PASS')

        page.locator('#arrange-habits').click()
        page.locator('#habits [data-order-kind="habit"][data-order-id="h3"][data-move="top"]').click()
        assert order(page,'#habits [data-sort-kind="habit"]')[0]=='h3'
        print('recurring habit order: PASS')

        # Selecting a task does not automatically start its time tracker.
        page.locator('#tasks [data-work="t3"]').click()
        assert page.locator('#working-card [data-sort-id="t3"]').count()==1
        assert page.locator('#tasks [data-sort-id="t3"]').count()==0
        assert page.evaluate("window.__events.filter(e=>e.type==='startTracking').length")==0
        page.locator('#working-card [data-track-start]').click()
        page.wait_for_selector('#working-card [data-track-stop]')
        assert page.evaluate("window.__events.filter(e=>e.type==='startTracking')[0].id")=='t3'
        page.locator('#working-card [data-focus-open]').click()
        assert page.evaluate("window.__events.filter(e=>e.type==='focus').at(-1).action.type")=='[FocusMode] Show Overlay'
        page.locator('#working-card [data-track-stop]').click()
        page.wait_for_selector('#working-card [data-track-start]')
        assert page.evaluate("window.__events.some(e=>e.type==='stopTracking')")
        print('Working Now selection, native tracking and Focus overlay: PASS')

        # Persistent, versioned and scoped to Today+: no global task reorder.
        page.wait_for_function("!!window.__saved['todayplus.workspace.v1']")
        page.wait_for_function(
            "JSON.parse(window.__saved['todayplus.workspace.v1']).workingId==='t3'"
        )
        prefs=page.evaluate("JSON.parse(window.__saved['todayplus.workspace.v1'])")
        assert prefs['taskOrder'][0]=='t3',prefs
        assert prefs['childOrder']['t1'][0]=='c2',prefs
        assert prefs['habitOrder'][0]=='h3',prefs
        assert prefs['workingId']=='t3',prefs
        assert page.evaluate("window.__events.some(e=>e.type==='update')") is False
        saved=page.evaluate('window.__saved')

        # Reload with a fresh iframe, reusing the mock host's synced state.
        restored=browser.new_page(viewport={'width':390,'height':844},has_touch=True,is_mobile=True)
        install(restored,saved)
        assert restored.locator('#working-card [data-sort-id="t3"]').count()==1
        assert restored.locator('#tasks [data-sort-id="t3"]').count()==0
        assert order(restored,'#habits [data-sort-kind="habit"]')[0]=='h3'
        restored.locator('#working-card [data-work-clear]').click()
        assert restored.locator('#working-card .working-empty').count()==1
        assert restored.locator('#tasks [data-sort-id="t3"]').count()==1
        restored.wait_for_function("JSON.parse(window.__saved['todayplus.workspace.v1']).workingId===null")
        before=restored.evaluate("window.__events.filter(e=>e.type==='persist').length")
        restored.evaluate("""() => {
          const key='todayplus.workspace.v1';
          const prefs=JSON.parse(window.__saved[key]);
          prefs.habitOrder=['h2','h1','h3'];
          window.__saved[key]=JSON.stringify(prefs);
          window.__hooks.persistedDataChanged?.({key});
        }""")
        restored.wait_for_function("document.querySelector('#habits [data-sort-kind=habit]').dataset.sortId==='h2'")
        assert restored.evaluate("window.__events.filter(e=>e.type==='persist').length")==before
        print('persistence, rehydrate and remote-sync refresh without write loop: PASS')

        # Drag-and-drop is a convenience in addition to tap targets and
        # keyboard-accessible top/up/down buttons.
        restored.locator('#arrange-tasks').click()
        handle=restored.locator('#tasks [data-drag-kind="task"][data-drag-id="t2"]')
        target=restored.locator('#tasks [data-sort-kind="task"][data-sort-id="t1"] .item-copy')
        restored.evaluate("window.scrollTo(0, document.querySelector('#tasks').getBoundingClientRect().top+window.scrollY-12)")
        a=handle.bounding_box()
        b=target.bounding_box()
        restored.mouse.move(a['x']+a['width']/2,a['y']+a['height']/2)
        restored.mouse.down()
        restored.mouse.move(b['x']+b['width']/2,b['y']+3,steps=12)
        restored.mouse.up()
        assert order(restored,'#tasks [data-sort-kind="task"]')[:3]==['t3','t2','t1'],order(restored,'#tasks [data-sort-kind="task"]')
        assert restored.evaluate('document.documentElement.scrollWidth<=window.innerWidth')
        assert restored.locator('#tasks [data-drag-kind="task"]').first.bounding_box()['height']>=40
        print('pointer drag, touch layout and no horizontal overflow: PASS')
        restored.close()
        page.close()

        # Compact 320px layout must retain independent task and habit buttons.
        tiny=browser.new_page(viewport={'width':320,'height':620},has_touch=True,is_mobile=True)
        install(tiny)
        tiny.locator('#arrange-habits').click()
        tiny.locator('#habits [data-order-id="h3"][data-move="top"]').click()
        assert order(tiny,'#habits [data-sort-kind="habit"]')[0]=='h3'
        assert tiny.evaluate('document.documentElement.scrollWidth<=window.innerWidth')
        tiny.close()
        print('320px keyboard-accessible reorder controls: PASS')

        # Arrange is a deliberately different action from the two filter chips.
        ui=browser.new_page(viewport={'width':320,'height':640},has_touch=True,is_mobile=True)
        install(ui)
        assert ui.locator('#arrange-tasks.arrange-toggle').count()==1
        assert ui.locator('#arrange-habits.arrange-toggle').count()==1
        assert ui.locator('#overdue-filter.arrange-toggle').count()==0
        # Verify visual DOM order, independent of CSS or responsive wrapping.
        assert ui.locator('#task-heading').locator('xpath=../..').locator('.section-actions button').evaluate_all(
            "(buttons)=>buttons.map(b=>b.id)"
        ) == ['overdue-filter','completed-filter','arrange-tasks']
        assert ui.locator('#habit-caption').locator('xpath=..').locator('button').last.get_attribute('id')=='arrange-habits'
        assert ui.evaluate('document.documentElement.scrollWidth<=innerWidth')
        ui.locator('#habits [data-work-habit="h3"]').click()
        assert ui.locator('#working-card [data-sort-id="h3"]').count()==1
        assert ui.locator('#working-card.has-priority').count()==1
        assert ui.locator('#habits [data-sort-id="h3"]').count()==0
        assert ui.locator('#working-card [data-track-start]').count()==0
        assert ui.locator('#working-card [data-focus-open]').count()==0
        assert ui.evaluate("window.__events.filter(e=>e.type==='startTracking').length")==0
        prefs=ui.evaluate("JSON.parse(window.__saved['todayplus.workspace.v1'])")
        assert prefs['workingKind']=='habit' and prefs['workingId']=='h3',prefs
        ui.locator('#working-card [data-habit="h3"]').click()
        ui.wait_for_selector('#working-card [data-sort-id="h3"].is-done')
        assert ui.locator('#working-card [data-sort-id="h3"]').count()==1
        assert ui.locator('#habits [data-sort-id="h3"]').count()==0
        assert ui.locator('#working-card [data-work-clear]').count()==1
        assert ui.evaluate('document.documentElement.scrollWidth<=innerWidth')
        print('completed habit stays in Working Now until manually removed: PASS')

        # A habit that already reached its 60-minute goal can still be
        # selected, and its native time log can exceed the daily goal.
        ui.locator('#working-card [data-work-clear]').click()
        assert ui.locator('#habits [data-sort-id="h3"] .check.is-done').count()==1
        ui.locator('#habits [data-work-habit="h4"]').click()
        assert ui.locator('#working-card [data-sort-id="h4"].is-done').count()==1
        assert ui.locator('#habits [data-sort-id="h4"]').count()==0
        assert 'Goal reached' in ui.locator('#working-card .working-habit-note').inner_text()
        assert ui.locator('#working-card [data-log-time="h4"]').is_enabled()
        completed_before=ui.locator('#done-count').inner_text()
        ui.locator('#working-card [data-log-time="h4"]').click()
        ui.wait_for_selector('#time-overlay:not(.hidden)')
        ui.locator('#time-minutes').fill('30')
        ui.locator('#time-save').click()
        ui.wait_for_selector('#time-overlay.hidden')
        ui.wait_for_function("document.querySelector('#working-card [data-sort-id=h4] .item-meta').textContent.includes('1h 30m')")
        assert ui.locator('#working-card [data-sort-id="h4"].is-done').count()==1
        assert ui.locator('#habits [data-sort-id="h4"]').count()==0
        assert ui.evaluate("window.__dataHabits.find(h=>h.id==='h4').countOnDay[window.__today]") == 5400000
        assert ui.locator('#done-count').inner_text()==completed_before
        ui.locator('#working-card [data-work-clear]').click()
        assert ui.locator('#habits [data-sort-id="h4"]').count()==1
        print('met-goal stopwatch habit can be selected, extended and removed: PASS')

        ui.locator('#habits [data-work-habit="h1"]').click()
        assert ui.locator('#working-card [data-more="h1"]').count()==1
        ui.locator('#working-card [data-more="h1"]').click()
        ui.wait_for_function("document.querySelector('#working-card .counter-value')?.textContent==='1'")
        ui.locator('#working-card [data-work-clear]').click()
        assert ui.locator('#habits [data-sort-id="h1"]').count()==1
        ui.close()
        print('counter habit progress and remove: PASS')

        # Some installed hosts expose the approved task action but not the
        # newer startTracking/stopTracking API. No disabled dead-end controls.
        older=browser.new_page(viewport={'width':390,'height':800})
        install(older,without_tracking=True)
        older.locator('#tasks [data-work="t3"]').click()
        assert older.locator('#working-card [data-track-start]').is_enabled()
        older.locator('#working-card [data-track-start]').click()
        older.wait_for_selector('#working-card [data-track-stop]')
        assert older.evaluate("window.__events.some(e=>e.action?.type==='[Task] SetCurrentTask'&&e.action.id==='t3')")
        older.locator('#working-card [data-track-stop]').click()
        older.wait_for_selector('#working-card [data-track-start]')
        assert older.evaluate("window.__events.some(e=>e.action?.type==='[Task] SetCurrentTask'&&e.action.id===null)")
        older.locator('#working-card [data-focus-open]').click()
        older.wait_for_function("window.__events.some(e=>e.action?.type==='[FocusMode] Show Overlay')")
        actions=older.evaluate("window.__events.filter(e=>e.action).map(e=>e.action)")
        assert actions[-2:]==[
            {'type':'[Task] SetCurrentTask','id':'t3'},
            {'type':'[FocusMode] Show Overlay'}
        ],actions
        assert older.evaluate("window.__events.some(e=>e.type==='select')") is False
        older.close()
        print('older host fallback and selected task activated before Focus: PASS')
    finally:
        browser.close()
