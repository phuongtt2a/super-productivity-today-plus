from pathlib import Path
import json
from datetime import date,timedelta
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
TODAY=date.today().isoformat(); YESTERDAY=(date.today()-timedelta(days=1)).isoformat()
TASKS=[
 {'id':'p1','title':'Viết báo cáo tiến độ dự án','projectId':'work','dueDay':TODAY,'isDone':False,'subTaskIds':['c1','c2']},
 {'id':'c1','parentId':'p1','title':'Soạn nội dung chi tiết','projectId':'work','isDone':False,'subTaskIds':[]},
 {'id':'c2','parentId':'p1','title':'Kiểm tra phần trình bày','projectId':'work','isDone':False,'subTaskIds':[]},
 {'id':'old','title':'Overdue task','projectId':'work','dueDay':YESTERDAY,'isDone':False,'subTaskIds':[]},
 {'id':'done','title':'Completed task','projectId':'work','dueDay':TODAY,'isDone':True,'subTaskIds':[]},
 {'id':'timed','title':'Timed appointment today','projectId':'work','dueWithTime':int(__import__('datetime').datetime.combine(date.today(),__import__('datetime').time(12,0)).timestamp()*1000),'remindAt':1800000000000,'isDone':False,'subTaskIds':[]},
 {'id':'repeating','title':'Recurring work today','projectId':'work','dueDay':TODAY,'repeatCfgId':'r1','isDone':False,'subTaskIds':[]},
]
API="""
window.__actions=[]; window.__tasks=__DATA__;
window.PluginAPI={
  getTasks:async()=>window.__tasks.map(x=>({...x})),
  getAllProjects:async()=>[{id:'work',title:'Work'}],
  getAllSimpleCounters:async()=>[],
  updateTask:async(id,values)=>{window.__actions.push({kind:'update',id,values});Object.assign(window.__tasks.find(t=>t.id===id),values);},
  selectTask:async(id)=>{window.__actions.push({kind:'select',id});},
};
""".replace('__DATA__',json.dumps(TASKS))
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,args=['--no-sandbox'])
 try:
  for width,height in [(320,568),(390,844),(1200,800)]:
   page=browser.new_page(viewport={'width':width,'height':height},device_scale_factor=1)
   page.goto("about:blank")
   page.evaluate(API)
   page.set_content((ROOT/'plugin/index.html').read_text(encoding="utf8"))
   page.wait_for_selector('[data-not-today="p1"]')
   # Hero messaging and button affordance must match the current design.
   assert page.locator('.hero h1').inner_text() == 'Focus on what matters.'
   assert page.locator('.hero p').inner_text() == 'Not another endless checklist.'
   btn=page.locator('[data-not-today="p1"]')
   assert btn.evaluate("el => getComputedStyle(el).borderTopWidth") == '1px', (width,'button border')
   assert btn.evaluate("el => getComputedStyle(el).backgroundColor") != 'rgba(0, 0, 0, 0)', (width,'button background')
   assert btn.locator('svg').count()==1,(width,'calendar-x icon')
   assert not btn.inner_text().strip(),(width,'icon only')
   assert btn.get_attribute('aria-label').startswith('Not Today: '),(width,'accessible label')
   assert btn.get_attribute('title')=='Not Today',(width,'plain tooltip')
   assert btn.bounding_box()['width']>=40,(width,'touch target')
   assert page.locator('[data-not-today="c2"]').count()==0,(width,'no button for unscheduled subtask')

   assert page.locator('.task-children .item').count()==2,(width,'subtask count')
   assert page.get_by_text('Overdue task').count()==0,(width,'overdue hidden')
   assert page.get_by_text('Completed task').count()==0,(width,'finished hidden')
   assert page.locator('#overdue-filter').get_attribute('aria-pressed')=='false'
   assert page.locator('#completed-filter').get_attribute('aria-pressed')=='false'
   assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth'),(width,'overflow')
   if width==390:
    page.screenshot(path=str(ROOT/'docs/screenshots/today-plus-tasks-phone-v1.1.0.png'),type='png',full_page=True)
   if width==1200:
    page.screenshot(path=str(ROOT/'docs/screenshots/today-plus-tasks-desktop-v1.1.0.png'),type='png',full_page=True)
   page.locator('[data-task="c1"]').click()
   acts=page.evaluate('window.__actions')
   assert acts[-1]=={'kind':'update','id':'c1','values':{'isDone':True}},(width,acts)
   # Reproduce an iframe regaining focus while the user presses the action.
   # The focus listener starts a fast refresh; it must not replace the button
   # between pointerdown and click (the old code needed a second tap).
   page.evaluate("window.__simulateFocus=()=>window.dispatchEvent(new Event('focus'));document.addEventListener('pointerdown',window.__simulateFocus,true)")
   page.locator('[data-not-today="p1"]').click()
   page.evaluate("document.removeEventListener('pointerdown',window.__simulateFocus,true)")
   acts=page.evaluate('window.__actions')
   assert acts[-1]=={'kind':'update','id':'p1','values':{'dueDay':None,'dueWithTime':None}},(width,acts)
   assert 'remains open in its project' in page.locator('#task-action-note').text_content(),width
   assert page.evaluate("window.__tasks.find(t=>t.id==='p1').isDone") is False
   # Parent disappears when unscheduled, unless a child still has its own due date.
   assert page.locator('[data-open="p1"]').count()==0
   assert page.get_by_text('Soạn nội dung chi tiết').count()==0
   # A timed task must lose its date/time AND related time reminder.
   page.locator('[data-not-today="timed"]').click()
   acts=page.evaluate('window.__actions')
   assert acts[-1]=={'kind':'update','id':'timed','values':{'dueDay':None,'dueWithTime':None,'remindAt':None}},(width,acts)
   assert page.evaluate("window.__tasks.find(t=>t.id==='timed').isDone") is False
   # Recurring tasks require explicit acknowledgement; cancel preserves schedule.
   dialog_handler=lambda dialog:dialog.dismiss()
   page.on('dialog',dialog_handler)
   page.locator('[data-not-today="repeating"]').click()
   assert page.evaluate("window.__tasks.find(t=>t.id==='repeating').dueDay") == TODAY
   assert page.locator('[data-not-today="repeating"]').count()==1
   page.remove_listener('dialog',dialog_handler)
   page.on('dialog',lambda dialog:dialog.accept())
   page.locator('[data-not-today="repeating"]').click()
   assert page.evaluate("window.__tasks.find(t=>t.id==='repeating').dueDay") is None
   page.locator('#overdue-filter').click()
   assert page.get_by_text('Overdue task').count()==1,(width,'overdue filter')
   page.locator('#completed-filter').click()
   assert page.get_by_text('Completed task').count()==1,(width,'finished filter')
   print(f'{width}x{height}: PASS')
   page.close()
  # Real touch gesture: first tap must work even if focus triggers a refresh.
  mobile=browser.new_page(viewport={'width':390,'height':844},has_touch=True,is_mobile=True)
  mobile.goto('about:blank')
  mobile.evaluate(API)
  mobile.set_content((ROOT/'plugin/index.html').read_text(encoding='utf8'))
  mobile.wait_for_selector('[data-not-today="timed"]')
  mobile.evaluate("window.__simulateFocus=()=>window.dispatchEvent(new Event('focus'));document.addEventListener('pointerdown',window.__simulateFocus,true)")
  mobile.locator('[data-not-today="timed"]').tap()
  mobile.wait_for_timeout(250)
  actions=mobile.evaluate('window.__actions')
  assert actions==[{'kind':'update','id':'timed','values':{'dueDay':None,'dueWithTime':None,'remindAt':None}}],actions
  assert mobile.locator('[data-not-today="timed"]').count()==0
  print('390x844 touch-first-tap: PASS')
  mobile.close()
 finally:
  browser.close()
