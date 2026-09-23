import sys,unittest,tempfile,subprocess
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import calibration_client as client
from intelligence.budget import Budget
class TransportDeadlineTests(unittest.TestCase):
    def test_timeout_retains_reservation_and_prevents_resend(self):
        with tempfile.TemporaryDirectory() as temp:
            root=Path(temp);(root/'data').mkdir()
            with patch.object(client,'ROOT',root),patch('check_providers.settings',return_value={'DEEPSEEK_API_KEY':'test-placeholder'}),patch.object(client,'run_bounded',side_effect=subprocess.TimeoutExpired('worker',300)) as dispatch:
                with self.assertRaises(subprocess.TimeoutExpired):client.run_call('test','deepseek','high','system',{'text':'test'},stage_limit=10)
                self.assertEqual(dispatch.call_args.kwargs['timeout'],300)
                for path in [root/'data/test/spend.sqlite',root/'data/spend.sqlite']:
                    b=Budget(path);self.assertEqual(b.summary()['pending_requests'],1);b.close()
                with self.assertRaises(ValueError):client.run_call('test','deepseek','high','system',{'text':'test'},stage_limit=10)
                self.assertEqual(dispatch.call_count,1)
