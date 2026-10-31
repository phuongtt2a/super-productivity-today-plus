"""Exercise Today+'s host-side native Won't Do adapter with a DOM menu stub.

This is a contract test for the adapter, NOT proof that Super Productivity
keeps the same DOM structure across app releases.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
HOST_SCRIPT = (ROOT / "plugin/plugin.js").read_text(encoding="utf-8")
DOM_SETUP = """
window.__tasks=[{id:'task-1',title:'Exercise',isDone:false}];
window.__nativeClicks=0;
window.PluginAPI={
  onMessage:handler=>{window.__handler=handler;},
  getTasks:async()=>window.__tasks.map(t=>({...t}))
};
const row=document.querySelector('task[data-task-id="task-1"]');
row.addEventListener('contextmenu',event=>{
  event.preventDefault();
  const inner=document.createElement('task-context-menu-inner');
  row.appendChild(inner);
  const menu=document.createElement('div');
  menu.setAttribute('role','menu');
  const btn=document.createElement('button');
  btn.setAttribute('role','menuitem');
  const icon=document.createElement('mat-icon');
  icon.textContent='block';
  btn.appendChild(icon);
  btn.addEventListener('click',()=>{
    window.__nativeClicks++;
    const t=window.__tasks[0],now=Date.now();
    Object.assign(t,{isDone:true,doneOn:now,wontDoOn:now});
    menu.remove();
  });
  menu.appendChild(btn);
  document.querySelector('.cdk-overlay-container').appendChild(menu);
});
"""
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,args=['--no-sandbox'])
    try:
        page=browser.new_page()
        page.set_content('<style>task{display:block;width:260px;height:50px}</style>'
                         '<task data-task-id="task-1">Exercise</task>'
                         '<div class="cdk-overlay-container"></div>')
        page.evaluate(DOM_SETUP)
        page.add_script_tag(content=HOST_SCRIPT)
        actual=page.evaluate("""async () => window.__handler({
            kind:'today-plus:native-wont-do',taskId:'task-1'
        })""")
        assert actual['status']=='confirmed',actual
        assert page.evaluate('window.__nativeClicks')==1
        task=page.evaluate('window.__tasks[0]')
        assert task['wontDoOn']==task['doneOn']
        assert task['isDone'] is True

        # Replaying a request must not click the native action twice.
        again=page.evaluate("""async () => window.__handler({
            kind:'today-plus:native-wont-do',taskId:'task-1'
        })""")
        assert again['status']=='unavailable',again
        assert page.evaluate('window.__nativeClicks')==1

        # If no matching native task row exists, it must not mutate state.
        page.evaluate("""() => {
           window.__tasks.push({id:'task-2',title:'Hidden',isDone:false})
        }""")
        absent=page.evaluate("""async () => window.__handler({
            kind:'today-plus:native-wont-do',taskId:'task-2'
        })""")
        assert absent['status']=='manual',absent
        assert page.evaluate("window.__tasks.find(x=>x.id==='task-2').isDone") is False

        print('PASS: native menu dispatch, skip verification, duplicate guard, absent-row fallback')
        page.close()
    finally:
        browser.close()
