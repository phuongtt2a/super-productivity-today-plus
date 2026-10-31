"""Today+ native Won't Do adapter: popup-free UI route integration tests.

These tests simulate the host task list; real installed-host behavior must still
be verified. No pathway may automatically select a task or open task details.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
HOST_SCRIPT = (ROOT/'plugin/plugin.js').read_text(encoding='utf-8')
PLUGIN_ROUTE = '#/plugins/sp-today-tasks-habits/index'
SETUP = """
window.__tasks=[{id:'task-1',title:'Exercise',isDone:false,projectId:'project-1'}];
window.__snacks=[];
window.__selectedCalls=0;
window.__routeChanges=[];
window.__menuOpacityAtOpen=[];
window.__dialogOpacityAtOpen=[];
window.PluginAPI={
  onMessage:handler=>{window.__handler=handler;},
  getTasks:async()=>window.__tasks.map(t=>({...t})),
  selectTask:async()=>{window.__selectedCalls++;throw new Error('No task detail popup allowed');},
  showSnack:info=>{window.__snacks.push(info);}
};
window.__makeMenu=()=>{
  const container=document.querySelector('.cdk-overlay-container');
  const pane=document.createElement('div');pane.className='cdk-overlay-pane';
  const menu=document.createElement('div');menu.setAttribute('role','menu');
  const btn=document.createElement('button');btn.setAttribute('role','menuitem');
  const icon=document.createElement('mat-icon');icon.textContent='block';
  btn.appendChild(icon);menu.appendChild(btn);
  btn.addEventListener('click',()=>{
    const now=Date.now();
    Object.assign(window.__tasks[0],{isDone:true,doneOn:now,wontDoOn:now});
    pane.remove();
  });
  pane.appendChild(menu);
  container.appendChild(pane);
  window.__menuOpacityAtOpen.push(getComputedStyle(pane).opacity);
  window.__dialogOpacityAtOpen.push(getComputedStyle(document.querySelector('#unrelated-dialog-pane')).opacity);
};
void 0;
"""
def setup_route(page, mode):
    page.goto('about:blank')
    page.set_content('<main id="host"></main><div class="cdk-overlay-container"><div class="cdk-overlay-pane" id="unrelated-dialog-pane"><div role="dialog">Other host dialog</div></div></div>')
    page.evaluate(SETUP)
    page.evaluate("""mode=>{
      window.addEventListener('hashchange',()=>{
        const hash=window.location.hash;
        window.__routeChanges.push(hash);
        document.querySelectorAll('task[data-task-id]').forEach(el=>el.remove());
        if(hash!=='#/tag/TODAY/tasks' || mode==='missing')return;
        const row=document.createElement('task');
        row.setAttribute('data-task-id','task-1');
        row.style.cssText='display:block;width:300px;height:60px';
        row.setAttribute('tabindex','0');
        row.textContent='Exercise';
        function openMenu(ev){
          ev.preventDefault();
          const inner=document.createElement('task-context-menu-inner');
          row.appendChild(inner);
          window.__makeMenu();
        }
        // The native host accepts the menu key on touch; on desktop the contextmenu
        // event also works as a second path.
        if(mode==='touch')row.addEventListener('keydown',ev=>{
          if(ev.key==='ContextMenu')openMenu(ev);
        });
        if(mode==='desktop')row.addEventListener('contextmenu',openMenu);
        document.querySelector('#host').appendChild(row);
      });
      window.location.hash='#/plugins/sp-today-tasks-habits/index';
    }""",mode)
    page.wait_for_function("location.hash==='#/plugins/sp-today-tasks-habits/index'")
    page.add_script_tag(content=HOST_SCRIPT)

with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,args=['--no-sandbox'])
    try:
        for mode in ['touch','desktop']:
            is_touch=(mode=='touch')
            page=browser.new_page(viewport={'width':390 if is_touch else 1200,'height':844 if is_touch else 800},
                                  has_touch=is_touch,is_mobile=is_touch)
            setup_route(page,mode)
            outcome=page.evaluate("""async()=>window.__handler({
              kind:'today-plus:native-wont-do',taskId:'task-1'
            })""")
            assert outcome['status']=='confirmed',(mode,outcome)
            page.wait_for_function("location.hash==='#/plugins/sp-today-tasks-habits/index'")
            routes=page.evaluate('window.__routeChanges')
            assert '#/tag/TODAY/tasks' in routes,(mode,routes)
            assert page.evaluate('window.__selectedCalls')==0,mode
            assert page.evaluate('window.__menuOpacityAtOpen')==['0'],mode
            assert page.evaluate('window.__dialogOpacityAtOpen')==['1'],mode
            assert page.evaluate("document.querySelector('[data-today-plus-wont-do-style]')") is None,mode
            assert page.evaluate("document.documentElement.classList.contains('today-plus-wont-do-menu-automation')") is False,mode
            task=page.evaluate('window.__tasks[0]')
            assert task['isDone'] and task['wontDoOn']==task['doneOn']
            assert page.evaluate("window.__snacks.at(-1).type")=='SUCCESS'
            print(f'{mode}: PASS native Won’t Do, route restored, task detail never selected')
            page.close()

        # If native rows do not exist, refuse to mutate or open task details.
        page=browser.new_page()
        setup_route(page,'missing')
        outcome=page.evaluate("""async()=>window.__handler({
          kind:'today-plus:native-wont-do',taskId:'task-1'
        })""")
        assert outcome['status']=='manual',outcome
        assert page.evaluate('window.__selectedCalls')==0
        assert page.evaluate("document.querySelector('[data-today-plus-wont-do-style]')") is None
        assert page.evaluate("document.documentElement.classList.contains('today-plus-wont-do-menu-automation')") is False
        assert page.evaluate('window.__tasks[0].isDone') is False
        page.wait_for_function("location.hash==='#/plugins/sp-today-tasks-habits/index'")
        print('missing row: PASS no popup, no mutation, original route restored')
        page.close()
    finally:
        browser.close()
