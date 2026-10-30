from pathlib import Path
import json, subprocess, unittest, zipfile
ROOT=Path(__file__).resolve().parents[1]
class TestPlugin(unittest.TestCase):
    def test_manifest(self):
        data=json.loads((ROOT/'plugin/manifest.json').read_text())
        self.assertEqual(data['id'],'sp-today-tasks-habits')
        self.assertRegex(data['version'],r'^\d+\.\d+\.\d+$')
        self.assertTrue(data['iFrame'])
        self.assertEqual(data['name'],'Today+')
        self.assertIn('tasks due today',data['description'])
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
    def test_zip(self):
        subprocess.run(['python',str(ROOT/'scripts/package.py')],capture_output=True,check=True)
        with zipfile.ZipFile(ROOT/'dist/today-tasks-habits.zip') as z:
            self.assertEqual(z.namelist(),['manifest.json','plugin.js','index.html','icon.svg'])
            self.assertIsNone(z.testzip())
if __name__=='__main__':unittest.main(verbosity=2)
