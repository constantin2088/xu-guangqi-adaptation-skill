import json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from check_trial import analyze
class TaskToolTests(unittest.TestCase):
 def sample(self):return json.loads((ROOT/'examples/tool-input.json').read_text(encoding='utf-8'))
 def test_pair_by_id_not_order(self):self.assertEqual(analyze(self.sample())['paired_delta'],{'a':-5,'b':-20})
 def test_mismatched_conditions_stop(self):
  p=self.sample();p['trial'][0]['conditions']='high-load'
  with self.assertRaises(ValueError):analyze(p)
 def test_lost_measurement_not_zero(self):
  p=self.sample();p['trial'].pop()
  with self.assertRaises(ValueError):analyze(p)
 def test_nonfinite_measurement_stops(self):
  p=self.sample();p['trial'][0]['value']=float('nan')
  with self.assertRaises(ValueError):analyze(p)
 def test_identical_data_have_zero_difference(self):
  p=self.sample();p['trial']=p['baseline'];self.assertEqual(analyze(p)['mean_delta'],0)

if __name__=='__main__':unittest.main()
