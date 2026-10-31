from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/'plugin/index.html').read_text()
with sync_playwright() as p:
    browser=p.chromium.launch(args=['--no-sandbox'])
    page=browser.new_page(viewport={'width':360,'height':760})
    page.evaluate('''() => {
      const date = new Date();const key=`${date.getFullYear()}-${String(date.getMonth()+1).padStart(2,'0')}-${String(date.getDate()).padStart(2,'0')}`;
      window.__test={updates:[],counters:[],selected:[]};
      window.PluginAPI={
        Hooks:{TASK_CREATED:'taskCreated',TASK_COMPLETE:'taskComplete',TASK_UPDATE:'taskUpdate',TASK_DELETE:'taskDelete'},
        registerHook:()=>{},
        getTasks:async()=>[{id:'task-1',title:'Hoàn thành báo cáo',isDone:false,projectId:'project-1',dueDay:key}],
        getAllProjects:async()=>[{id:'project-1',title:'Công việc'}],
        getAllSimpleCounters:async()=>[
          {id:'habit-1',title:'Đọc sách 20 phút',isEnabled:true,type:'ClickCounter',isTrackStreaks:true,streakMinValue:1,streakWeekDays:{0:true,1:true,2:true,3:true,4:true,5:true,6:true},countOnDay:{}},
          {id:'habit-2',title:'Uống nước',isEnabled:true,type:'ClickCounter',isTrackStreaks:true,streakMinValue:6,countOnDay:{}},
          {id:'habit-3',title:'Tập thể dục 30 phút',isEnabled:true,type:'StopWatch',isOn:false,isTrackStreaks:true,streakMinValue:1800000,countOnDay:{[key]:600000}},
          {id:'habit-4',title:'Active timer',isEnabled:true,type:'StopWatch',isOn:true,isTrackStreaks:true,streakMinValue:1800000,countOnDay:{[key]:600000}}
        ],
        updateTask:async(id,updates)=>{window.__test.updates.push({id,updates})},
        setCounter:async(id,value)=>{window.__test.counters.push({id,value})},
        selectTask:async(id)=>{window.__test.selected.push(id)}
      };
    }''')
    page.set_content(HTML)
    page.wait_for_timeout(100)
    assert page.locator('.demo-note:not(.hidden)').count()==0
    assert page.locator('.item-task').count()==1
    assert page.locator('#habits .item').count()==4
    page.locator('[data-task="task-1"]').click()
    assert page.evaluate('window.__test.updates[0].updates.isDone') is True
    assert page.locator('.item-task').count()==0 # hidden by default after completion
    page.locator('#completed-filter').click()
    assert page.locator('.item-task').count()==1
    page.locator('[data-task="task-1"]').click()
    assert page.evaluate('window.__test.updates[1].updates.isDone') is False
    page.locator('[data-habit="habit-1"]').click()
    assert page.evaluate('window.__test.counters[0].value')==1
    page.locator('[data-habit="habit-1"]').click()
    assert page.evaluate('window.__test.counters[1].value')==0
    page.locator('[data-more="habit-2"]').click()
    assert page.evaluate('window.__test.counters[2].value')==1
    page.locator('[data-less="habit-2"]').click()
    assert page.evaluate('window.__test.counters[3].value')==0
    page.locator('[data-open="task-1"]').click()
    assert page.evaluate('window.__test.selected[0]')=='task-1'
    # Manual time entry adds 25 minutes (1,500,000 ms) to 10 minutes (600,000 ms).
    assert page.locator('[data-log-time="habit-4"]').is_disabled()
    page.locator('[data-log-time="habit-3"]').click()
    assert page.locator('#time-overlay:not(.hidden)').count()==1
    page.locator('#time-minutes').fill('25')
    page.locator('#time-save').click()
    page.wait_for_timeout(80)
    assert page.locator('#time-overlay.hidden').count()==1
    counters=page.evaluate('window.__test.counters')
    assert counters[-1]=={'id':'habit-3','value':2100000},counters
    assert page.evaluate('document.documentElement.scrollWidth<=document.documentElement.clientWidth')
    print('PASS: tasks, habit toggles, goal counters, stopwatch time logging/disabled running timer, task selection, no horizontal overflow')
    browser.close()
