"""Generate current Today+ documentation screenshots using synthetic Vietnamese data."""
from pathlib import Path
from datetime import date, timedelta
from io import BytesIO
import json
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"docs/screenshots"
OUT.mkdir(parents=True,exist_ok=True)
HTML=(ROOT/"plugin/index.html").read_text(encoding="utf-8")
TODAY=date.today().isoformat()
TASKS=[
 {"id":"report","title":"Hoàn thiện báo cáo tiến độ dự án","projectId":"work","dueDay":TODAY,"isDone":False,"subTaskIds":["research","review"]},
 {"id":"research","title":"Tổng hợp số liệu và nội dung quan trọng","parentId":"report","projectId":"work","isDone":False,"subTaskIds":[]},
 {"id":"review","title":"Kiểm tra định dạng báo cáo","parentId":"report","projectId":"work","isDone":False,"subTaskIds":[]},
 {"id":"design","title":"Kiểm tra giao diện ứng dụng trên điện thoại","projectId":"work","dueDay":TODAY,"isDone":False,"subTaskIds":[]},
 {"id":"meeting","title":"Chuẩn bị cuộc họp với nhóm phát triển","projectId":"work","dueDay":TODAY,"isDone":False,"subTaskIds":[]},
 {"id":"old","title":"Gửi biên bản làm việc tuần trước","projectId":"work","dueDay":(date.today()-timedelta(days=2)).isoformat(),"isDone":False,"subTaskIds":[]}
]
API="""window.PluginAPI={
 getTasks:async()=>__TASKS__,
 getAllProjects:async()=>[{id:'work',title:'Công việc'}],
 getAllSimpleCounters:async()=>[
  {id:'read',title:'Đọc sách 20 phút',isEnabled:true,type:'ClickCounter',isTrackStreaks:true,streakMinValue:1,streakWeekDays:{0:true,1:true,2:true,3:true,4:true,5:true,6:true},countOnDay:{}},
  {id:'water',title:'Uống đủ nước',isEnabled:true,type:'ClickCounter',isTrackStreaks:true,streakMinValue:6,countOnDay:{}},
  {id:'exercise',title:'Tập thể dục 30 phút',isEnabled:true,type:'StopWatch',isOn:false,isTrackStreaks:true,streakMinValue:1800000,countOnDay:{[__DATE__]:600000}}
 ],
 updateTask:async()=>{},selectTask:async()=>{},setCounter:async()=>{},
 loadSyncedData:async()=>null,persistDataSynced:async()=>{},
 getDayContext:async()=>({todayStr:__DATE__}),
 startTracking:async()=>{},stopTracking:async()=>{},dispatchAction:()=>{}
};""".replace("__TASKS__",json.dumps(TASKS,ensure_ascii=False)).replace("__DATE__",json.dumps(TODAY))
WALLPAPER="""html::before{
 content:'';position:fixed;pointer-events:none;inset:0;z-index:-1;
 background:linear-gradient(140deg,rgba(97,158,125,.25),transparent 55%),
 linear-gradient(20deg,rgba(118,150,190,.13),transparent 65%),#edf4eb;
}"""
with sync_playwright() as playwright:
 browser=playwright.chromium.launch(headless=True,args=["--no-sandbox"])
 for width,height,filename in [
  (1440,900,"today-plus-tasks-desktop-v1.1.0.webp"),
  (390,844,"today-plus-tasks-phone-v1.1.0.webp"),
  (320,568,"small-phone.webp"),
 ]:
  page=browser.new_page(viewport={"width":width,"height":height},device_scale_factor=1,reduced_motion="reduce")
  page.goto("about:blank")
  page.evaluate(API)
  page.set_content(HTML)
  page.add_style_tag(content=WALLPAPER)
  page.evaluate("""() => {
    const root=document.documentElement;
    root.style.setProperty('--font-primary-stack','"Segoe UI",Arial,sans-serif');
    root.style.setProperty('--card-bg','#f3f7f1');
    root.style.setProperty('--text-color','#25382d');
    root.style.setProperty('--text-color-muted','#566c5e');
  }""")
  page.wait_for_selector(".task-group")
  assert page.evaluate("getComputedStyle(document.body).backgroundColor")=="rgba(0, 0, 0, 0)"
  assert page.evaluate("getComputedStyle(document.documentElement).backgroundColor")=="rgba(0, 0, 0, 0)"
  assert page.evaluate("document.documentElement.scrollWidth<=innerWidth+1"),width
  png=page.screenshot(type="png",full_page=True,animations="disabled")
  Image.open(BytesIO(png)).convert("RGB").save(OUT/filename,format="WEBP",quality=86,method=6)
  if width==1440:
   page.locator('[data-log-time="exercise"]').click()
   page.wait_for_selector('#time-overlay:not(.hidden)')
   pic=page.screenshot(type="png",full_page=False,animations="disabled")
   Image.open(BytesIO(pic)).convert("RGB").save(OUT/"log-time.webp",format="WEBP",quality=86,method=6)
   page.locator('#time-close').click()
   page.locator('[data-work="report"]').click()
   page.wait_for_selector('#working-card [data-sort-id="report"]')
   assert page.locator('#tasks [data-sort-id="report"]').count()==0
   shot=page.screenshot(type="png",full_page=True,animations="disabled")
   Image.open(BytesIO(shot)).convert("RGB").save(OUT/"working-now-active.webp",format="WEBP",quality=86,method=6)
  if width==390:
   page.locator('#arrange-tasks').click()
   page.locator('#arrange-habits').click()
   assert page.locator('#tasks [data-move="top"]').count()>0
   assert page.evaluate("document.documentElement.scrollWidth<=innerWidth+1")
   shot=page.screenshot(type="png",full_page=True,animations="disabled")
   Image.open(BytesIO(shot)).convert("RGB").save(OUT/"arrange-mode-phone.webp",format="WEBP",quality=86,method=6)
  print("captured",filename)
  page.close()
 browser.close()
