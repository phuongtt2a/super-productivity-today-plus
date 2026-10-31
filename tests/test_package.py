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
        self.assertIn('showOverdue:false, showFinished:false', html)
        self.assertIn('function taskGroups()', html)
        self.assertIn('group.children=childIds.map(', html)
        self.assertIn('class="task-skip"', html)
        self.assertIn('aria-label="Not Today:', html)
        self.assertIn('title="Not Today"', html)
        self.assertNotIn('Remove scheduled date', html)
        self.assertIn('state.pointerActive', html)
        self.assertIn('const action=context||t.isDone||!d?', html)
        self.assertIn('data-not-today=', html)
        self.assertIn('async function removeFromToday(id)', html)
        self.assertIn('dueDay:null,dueWithTime:null', html)
        self.assertNotIn('data-wont-do=', html)
        self.assertNotIn('wontDoOn:', html)
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
    def test_zip(self):
        subprocess.run(['python',str(ROOT/'scripts/package.py')],capture_output=True,check=True)
        with zipfile.ZipFile(ROOT/'dist/today-plus-super-productivity.zip') as z:
            self.assertEqual(z.namelist(),['manifest.json','plugin.js','index.html','icon.svg'])
            self.assertIsNone(z.testzip())
if __name__=='__main__':unittest.main(verbosity=2)
