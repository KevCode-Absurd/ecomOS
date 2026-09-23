import unittest
from types import SimpleNamespace
from intelligence.creative_retrieval import candidates
class RoutingTests(unittest.TestCase):
 def test_marketing_words_cannot_admit_security_or_staff_permissions(self):
  e=SimpleNamespace(cards={
   'good':dict(domain='ad-copy-deployment',title='Write specific headlines',tags=['copywriting']),
   'security':dict(domain='bot-and-agent-security',title='Protect product page',tags=['landing-page']),
   'staff':dict(domain='ad-copy-deployment',title='Staff permissions for copywriting',tags=['copywriting'])})
  self.assertEqual(candidates(e,'landing_page'),{'good'})
  self.assertEqual(candidates(e,'writing_principles'),{'good'})
 def test_unknown_route_does_not_fall_back_to_everything(self):
  with self.assertRaises(ValueError):candidates(SimpleNamespace(cards={}),'unknown')
