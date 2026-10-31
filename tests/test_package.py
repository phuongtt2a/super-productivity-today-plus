from pathlib import Path
import json, subprocess, unittest, zipfile
ROOT=Path(__file__).resolve().parents[1]
class TestPlugin(unittest.TestCase):
    def test_manifest(self):
        data=json.loads((ROOT/'plugin/manifest.json').read_text())
        self.assertEqual(data['id'],'sp-today-tasks-habits')
        self.assertEqual(data['version'],'1.1.0')
        self.assertTrue(data['iFrame'])
        self.assertEqual(data['name'],'Today+')
        self.assertIn('tasks due today',data['description'])
    def test_logo_consistency(self):
        import re
        icon=(ROOT/'plugin/icon.svg').read_text()
        html=(ROOT/'plugin/index.html').read_text()
        header=html.split('<div class="brand-mark">', 1)[1].split('</svg>', 1)[0] + '</svg>'
        self.assertNotIn('<div class="brand-mark">✓</div>', html)
        self.assertIn('viewBox="0 0 64 64"', header)
        icon_shapes=re.findall(r'<(?:rect|path)\b[^>]*>', icon)
        for shape in icon_shapes:
            self.assertIn(shape, header)
    def test_api_contract(self):
        s=(ROOT/'plugin/index.html').read_text()
        for api in ('getTasks()', 'getAllSimpleCounters()', 'getAllProjects()', 'updateTask(', 'setCounter('):
            self.assertIn(api,s)
        self.assertIn('background:transparent!important',s)
        self.assertIn('data-log-time',s)
        self.assertIn('time-minutes',s)
    def test_syntax(self):
        text=(ROOT/'plugin/index.html').read_text().split('<script>',1)[1].split('</script>',1)[0]
        result=subprocess.run(['node','--check'],input=text,text=True,capture_output=True)
        self.assertEqual(result.returncode,0,result.stderr)
    def test_task_hierarchy_and_action_guard(self):
        html=(ROOT/'plugin/index.html').read_text()
        host=(ROOT/'plugin/plugin.js').read_text()
        self.assertIn('showOverdue:false, showFinished:false',html)
        self.assertIn('function taskGroups()',html)
        self.assertIn('group.children=childIds.map(',html)
        self.assertIn('class="task-skip"',html)
        self.assertIn('data-wont-do=',html)
        self.assertIn('aria-label="Won’t Do:',html)
        self.assertIn('const action=context||t.isDone?',html)
        self.assertIn('async function wontDo(id)',html)
        self.assertIn('requestNativeWontDo(id)',html)
        self.assertIn("isWontDo(t)",html)
        self.assertIn("state.pointerActive",html)
        self.assertNotIn('data-not-today=',html)
        self.assertNotIn('async function removeFromToday',html)
        self.assertNotIn('dueDay:null,dueWithTime:null',html)
        self.assertNotIn('isDone:true',html.split('async function wontDo(id)',1)[1])
        self.assertIn("PluginAPI.onMessage(",host)
        self.assertIn('contextmenu',host)
        self.assertIn('wontDoOn === current.doneOn',host)
        self.assertNotIn('PluginAPI.updateTask(',host)
        result=subprocess.run(['node','--check',str(ROOT/'plugin/plugin.js')],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)
    def test_release_automation(self):
        workflow=(ROOT/'.github/workflows/release.yml').read_text()
        self.assertIn('branches: [main]',workflow)
        self.assertIn("if: github.ref == 'refs/heads/main'",workflow)
        self.assertIn('cancel-in-progress: false',workflow)
        self.assertIn('gh release upload "$TAG" "$ASSET" --clobber',workflow)
        self.assertIn('gh release create "$TAG" "$ASSET"',workflow)
        self.assertIn('cmp "$ASSET" "$VERIFY/$NAME"',workflow)
        self.assertNotIn("startsWith(github.event.head_commit.message, 'release:')",workflow)
        guide=(ROOT/'docs/RELEASING.md').read_text()
        self.assertIn('issue → PR → merge → published ZIP',guide)
        self.assertIn('same version',guide.lower())
    def test_neo_zen_theme_and_documentation(self):
        html=(ROOT/'plugin/index.html').read_text()
        self.assertIn('width:min(1220px,100%)',html)
        self.assertIn('font-family:var(--font-primary-stack',html)
        self.assertIn('html,body,.app{background:transparent!important}',html)
        self.assertIn('#tasks>.item-task{',html)
        self.assertIn('.task-group{',html)
        self.assertIn('#habits .item{',html)
        self.assertIn('box-shadow:3px 3px 0 var(--neo-stroke)',html)
        for filename in ('today-plus-tasks-desktop-v1.1.0.webp','today-plus-tasks-phone-v1.1.0.webp','small-phone.webp','log-time.webp'):
            self.assertTrue((ROOT/'docs/screenshots'/filename).is_file(),filename)
        self.assertTrue((ROOT/'docs/NEO-ZEN-DESIGN.md').is_file())

    def test_zip(self):
        subprocess.run(['python',str(ROOT/'scripts/package.py')],capture_output=True,check=True)
        with zipfile.ZipFile(ROOT/'dist/today-plus-super-productivity.zip') as z:
            self.assertEqual(z.namelist(),['manifest.json','plugin.js','index.html','icon.svg'])
            self.assertIsNone(z.testzip())
if __name__=='__main__':unittest.main(verbosity=2)
