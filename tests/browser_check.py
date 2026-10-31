from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
with sync_playwright() as p:
    browser=p.chromium.launch(args=['--no-sandbox'])
    for width,height,name in [(1440,900,'desktop'),(390,844,'phone'),(320,568,'small-phone')]:
        pg=browser.new_page(viewport={'width':width,'height':height},device_scale_factor=1)
        pg.set_content((ROOT/'plugin/index.html').read_text(encoding='utf-8'))
        pg.wait_for_timeout(100)
        pg.screenshot(path=str(ROOT/'docs/screenshots'/f'{name}.png'),full_page=True)
        data=pg.evaluate('''() => ({scrollWidth:document.documentElement.scrollWidth,clientWidth:document.documentElement.clientWidth,taskCount:document.querySelectorAll('.item-task').length,habitCount:document.querySelectorAll('#habits .item').length,hero:document.querySelector('.hero h1').textContent, sections:[...document.querySelectorAll('.section')].map(x=>x.getBoundingClientRect().toJSON())})''')
        print(name,data)
        assert data['scrollWidth']<=data['clientWidth']+1, f'horizontal overflow {name}'
        assert data['taskCount']>=3 and data['habitCount']>=2
        pg.close()
    browser.close()
