"""Today+ UI contract tests with a simulated host message bridge.

These tests do NOT prove native Super Productivity menu automation. Live-host
verification of the real context menu, recurrence and metrics is still required.
"""
from pathlib import Path
import json
from datetime import date, timedelta
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
TODAY = date.today().isoformat()
YESTERDAY = (date.today() - timedelta(days=1)).isoformat()
TASKS = [
    {'id': 'p1', 'title': 'Viết báo cáo tiến độ dự án', 'projectId': 'work', 'dueDay': TODAY, 'isDone': False, 'subTaskIds': ['c1','c2']},
    {'id': 'c1', 'parentId': 'p1', 'title': 'Soạn nội dung chi tiết', 'projectId': 'work', 'isDone': False, 'subTaskIds': []},
    {'id': 'c2', 'parentId': 'p1', 'title': 'Kiểm tra phần trình bày', 'projectId': 'work', 'isDone': False, 'subTaskIds': []},
    {'id': 'old', 'title': 'Overdue task', 'projectId': 'work', 'dueDay': YESTERDAY, 'isDone': False, 'subTaskIds': []},
    {'id': 'done', 'title': 'Completed task', 'projectId': 'work', 'dueDay': TODAY, 'isDone': True, 'subTaskIds': []},
    {'id': 'timed', 'title': 'Timed appointment today', 'projectId': 'work', 'dueDay': TODAY, 'isDone': False, 'subTaskIds': []},
    {'id': 'repeating', 'title': 'Recurring work today', 'projectId': 'work', 'dueDay': TODAY, 'repeatCfgId': 'r1', 'isDone': False, 'subTaskIds': []},
]
API = """
window.__actions=[];window.__tasks=__DATA__;window.__bridgeMode='confirmed';
window.PluginAPI={
  getTasks:async()=>window.__tasks.map(t=>({...t})),
  getAllProjects:async()=>[{id:'work',title:'Work'}],
  getAllSimpleCounters:async()=>[],
  updateTask:async(id,updates)=>{window.__actions.push({kind:'update',id,updates});Object.assign(window.__tasks.find(t=>t.id===id),updates);},
  selectTask:async(id)=>{window.__actions.push({kind:'select',id});}
};

""".replace('__DATA__', json.dumps(TASKS))
BRIDGE = """\nwindow.addEventListener('message',event=>{
  if(event.data?.type!=='PLUGIN_MESSAGE')return;
  const id=event.data.message.taskId;
  window.__actions.push({kind:'native-request',id});
  const task=window.__tasks.find(t=>t.id===id);
  const mode=window.__bridgeMode;
  if(mode==='confirmed'){
    const timestamp=Date.now();
    Object.assign(task,{isDone:true,doneOn:timestamp,wontDoOn:timestamp});
  }
  window.postMessage({type:'PLUGIN_MESSAGE_RESPONSE',messageId:event.data.messageId,
    result:{status:mode}},'*');
});\n"""

with sync_playwright() as playwright:
    browser = playwright.chromium.launch(headless=True,args=['--no-sandbox'])
    try:
        for width, height in [(320, 568), (390, 844), (1200, 800)]:
            page=browser.new_page(viewport={'width':width,'height':height})
            page.goto('about:blank')
            page.evaluate(API)
            page.set_content((ROOT/'plugin/index.html').read_text(encoding='utf8'))
        page.evaluate(BRIDGE)
            page.wait_for_selector('[data-wont-do="p1"]')
            assert page.locator('.task-group').count()==1
            assert page.locator('.task-children .item-task').count()==2
            assert page.locator('[data-wont-do="c2"]').count()==1
            assert page.get_by_text('Overdue task').count()==0
            assert page.get_by_text('Completed task').count()==0
            btn=page.locator('[data-wont-do="p1"]')
            assert btn.get_attribute('aria-label').startswith('Won’t Do:')
            assert btn.get_attribute('title').startswith('Won’t Do')
            assert btn.bounding_box()['width']>=40
            assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),width

            # Mocked host confirms genuine Won't Do; Today+ must not fake a Done
            # update or change the current occurrence's due date.
            btn.click()
            page.wait_for_function("document.querySelector('#task-action-note').textContent.includes('Skipped')")
            events=page.evaluate('window.__actions')
            assert events==[{'kind':'native-request','id':'p1'}],events
            task=page.evaluate("window.__tasks.find(t=>t.id==='p1')")
            assert task['isDone'] and task['wontDoOn']==task['doneOn']
            assert task['dueDay']==TODAY
            page.locator('#completed-filter').click()
            assert page.locator('[data-task="p1"]').inner_text().strip()=='×'
            assert page.get_by_text("Won't Do").count()>=1
            # The displayed daily completion count excludes skipped tasks.
            assert page.locator('#done-count').inner_text().startswith('1 of ')

            # Missing native row => host requests manual intervention.
            page.evaluate("window.__bridgeMode='manual'")
            page.locator('[data-wont-do="timed"]').click()
            page.wait_for_function("document.querySelector('#task-action-note').textContent.includes('Task opened')")
            events=page.evaluate('window.__actions')
            assert events[-2:]==[{'kind':'native-request','id':'timed'}, {'kind':'select','id':'timed'}],events
            assert page.evaluate("window.__tasks.find(t=>t.id==='timed').dueDay")==TODAY
            assert page.evaluate("window.__tasks.find(t=>t.id==='timed').isDone") is False

            # Recurring instances are never unscheduled by the plugin.
            page.locator('[data-wont-do="repeating"]').click()
            page.wait_for_function("document.querySelector('#task-action-note').textContent.includes('Task opened')")
            repeat=page.evaluate("window.__tasks.find(t=>t.id==='repeating')")
            assert repeat['repeatCfgId']=='r1' and repeat['dueDay']==TODAY and repeat['isDone'] is False
            assert not any(e['kind']=='update' for e in page.evaluate('window.__actions'))
            print(f'{width}x{height}: PASS (mock host + responsive + fallback)')
            page.close()

        # Touch-first tap must work even if focus triggers a refresh.
        page=browser.new_page(viewport={'width':390,'height':844},has_touch=True,is_mobile=True)
        page.goto('about:blank')
        page.evaluate(API)
        page.set_content((ROOT/'plugin/index.html').read_text(encoding='utf8'))
            page.evaluate(BRIDGE)
        page.wait_for_selector('[data-wont-do="timed"]')
        page.evaluate("window.__simulateFocus=()=>window.dispatchEvent(new Event('focus'));document.addEventListener('pointerdown',window.__simulateFocus,true)")
        page.locator('[data-wont-do="timed"]').tap()
        page.wait_for_function("document.querySelector('#task-action-note').textContent.includes('Skipped')")
        assert page.evaluate("window.__actions.filter(e=>e.kind==='native-request').length")==1
        assert page.evaluate("window.__tasks.find(t=>t.id==='timed').dueDay")==TODAY
        print('390x844 touch-first-tap: PASS (mock host)')
        page.close()
    finally:
        browser.close()
