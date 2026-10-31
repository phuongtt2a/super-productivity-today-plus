"""Native Won't Do adapter: simulated detail-panel and temporary-route paths.

These are DOM integration tests, not installed Super Productivity integration tests.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
HOST_SCRIPT = (ROOT/'plugin/plugin.js').read_text(encoding='utf-8')
BASE = """
window.__tasks=[{id:'task-1',title:'Exercise',isDone:false,projectId:'project-1'}];
window.__snacks=[];
window.__selectedId=null;
window.PluginAPI={
  onMessage:handler=>{window.__handler=handler;},
  getTasks:async()=>window.__tasks.map(t=>({...t})),
  selectTask:async(id)=>{window.__selectedId=id;},
  getSelectedTask:async()=>window.__tasks.find(t=>t.id===window.__selectedId) || null,
  showSnack:info=>{window.__snacks.push(info);}
};
window.__makeMenu=()=>{
  const container=document.querySelector('.cdk-overlay-container');
  const menu=document.createElement('div');menu.setAttribute('role','menu');
  const btn=document.createElement('button');btn.setAttribute('role','menuitem');
  const icon=document.createElement('mat-icon');icon.textContent='block';
  btn.appendChild(icon);menu.appendChild(btn);
  btn.addEventListener('click',()=>{
    const now=Date.now();
    Object.assign(window.__tasks[0],{isDone:true,doneOn:now,wontDoOn:now});
    menu.remove();
  });
  container.appendChild(menu);
};
"""
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,args=['--no-sandbox'])
    try:
        # Touch/narrow-screen path: use the actual native More button inside
        # the selected task's detail panel instead of exposing a manual fallback.
        mobile=browser.new_page(viewport={'width':390,'height':844},has_touch=True,is_mobile=True)
        mobile.set_content("""
           <style>task-detail-panel{display:block;width:280px;height:100px}</style>
           <task-detail-panel><button class="task-detail-more-btn">More</button></task-detail-panel>
           <div class="cdk-overlay-container"></div>""")
        mobile.evaluate(BASE)
        mobile.evaluate("""() => document.querySelector('.task-detail-more-btn')
            .addEventListener('click',window.__makeMenu)""")
        mobile.add_script_tag(content=HOST_SCRIPT)
        response=mobile.evaluate("""async()=>window.__handler({
          kind:'today-plus:native-wont-do',taskId:'task-1'
        })""")
        assert response['status']=='confirmed',response
        assert mobile.evaluate("window.__tasks[0].doneOn===window.__tasks[0].wontDoOn")
        assert mobile.evaluate("window.__selectedId")== 'task-1'
        print('detail-panel More menu: PASS')
        mobile.close()

        # Desktop path: Today+ fills a plugin page without a native task row.
        # The host-side adapter briefly visits native Today, invokes the native
        # task menu, then restores the plugin route even after its iframe unmounts.
        desktop=browser.new_page(viewport={'width':1200,'height':800})
        desktop.goto('about:blank')
        desktop.set_content('<main id="host"></main><div class="cdk-overlay-container"></div>')
        desktop.evaluate(BASE)
        desktop.evaluate("""() => {
          window.__routeChanges=[];
          window.addEventListener('hashchange',()=>{
            const hash=window.location.hash;
            window.__routeChanges.push(hash);
            document.querySelectorAll('task[data-task-id]').forEach(el=>el.remove());
            if(hash!=='#/tag/TODAY/tasks') return;
            const row=document.createElement('task');
            row.setAttribute('data-task-id','task-1');
            row.style.cssText='display:block;width:300px;height:60px';
            row.textContent='Exercise';
            row.addEventListener('contextmenu',ev=>{
              ev.preventDefault();
              const inner=document.createElement('task-context-menu-inner');
              row.appendChild(inner);
              window.__makeMenu();
            });
            document.querySelector('#host').appendChild(row);
          });
          window.location.hash='#/plugins/sp-today-tasks-habits/index';
        }""")
        desktop.wait_for_function("window.location.hash==='#/plugins/sp-today-tasks-habits/index'")
        desktop.add_script_tag(content=HOST_SCRIPT)
        response=desktop.evaluate("""async()=>window.__handler({
          kind:'today-plus:native-wont-do',taskId:'task-1'
        })""")
        assert response['status']=='confirmed',response
        desktop.wait_for_function("window.location.hash==='#/plugins/sp-today-tasks-habits/index'")
        routes=desktop.evaluate('window.__routeChanges')
        assert '#/tag/TODAY/tasks' in routes,routes
        assert desktop.evaluate('window.__tasks[0].wontDoOn===window.__tasks[0].doneOn')
        snack=desktop.evaluate('window.__snacks.at(-1)')
        assert snack['type']=='SUCCESS',snack
        print('temporary native task route + restore: PASS')
        desktop.close()
    finally:
        browser.close()
