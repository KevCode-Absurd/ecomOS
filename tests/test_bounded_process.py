import subprocess,sys,time,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from bounded_process import run_bounded
class BoundedProcessTests(unittest.TestCase):
    def test_actual_child_that_never_reads_large_stdin_is_stopped(self):
        started=time.monotonic()
        with self.assertRaises(subprocess.TimeoutExpired):
            run_bounded([sys.executable,'-c','import time; time.sleep(60)'],'x'*2_000_000,timeout=.25)
        self.assertLess(time.monotonic()-started,8)
    def test_captures_completed_output(self):
        result=run_bounded([sys.executable,'-c','import sys; print(len(sys.stdin.read()))'],'hello',timeout=5)
        self.assertEqual(result.returncode,0)
        self.assertEqual(result.stdout.strip(),'5')
