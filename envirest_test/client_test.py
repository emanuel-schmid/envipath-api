import unittest
import re

from envirest import EnviPathClient
from getpass import getpass


USER = 'anonymous'
TESTHOST = 'envipath.org:8181'
PACKAGE = 'anonymous'


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.client = EnviPathClient(host=TESTHOST, username=USER, secure=False, verify=False)
        self.package = self.client.findpackage(PACKAGE)

    def test_scenario(self):
        
        scenariourl = self.client.createscenario(self.package, halflife={
            'lower': 0,
            'upper': 0,
            'source': '',
            'comment': '',
            'model': '',
            'fit': ''
        })

        for lower, upper, source, comment, model, fit in [(2.5, 2.5, '', 'some comment; some more', 'SFO', 'chi2'),
                                                          ('4.0E-12', 2.6, '', 'some comment; some more', 'SFO+', '')]:

            whatyouget = self.client.updatescenario(scenariourl, halflife={
                'lower': lower,
                'upper': upper,
                'source': source,
                'comment': comment,
                'model': model,
                'fit': fit
            })
            halflife = whatyouget['collection']['halflife']
            print(halflife)
            m,f,c,lu,s = re.split(r'(?<!\\);', halflife['value'])
            assert m == model
            assert f == fit
            assert c == comment.replace(';', '\\;')
            assert lu == ' - '.join([str(_) for _ in [lower, upper]])
            assert s == source.replace(';', '\\;')

        self.client.delete(scenariourl)

    def test_reaction(self):
        rule = self.client.createrule(self.package, smirks='[Pb]>>[Au]')['id']
        reaction = self.client.createreaction(self.package, smirks='[Pb]>>[Au]')['id']
        updated = self.client.updaterreaction(reaction, name='the little alchemist', related_rule=rule)
        assert updated['rules'][0]['id'] == rule
        assert updated['name'] == 'the little alchemist'
        assert updated['smirks'] == '[Pb]>>[Au]'
        self.client.delete(reaction)
        self.client.delete(rule)

    def test_enviLink(self):
        client = EnviPathClient('envipath.org')
        assert len(client.get_enviLink(rule='bt0028')) == 1
        

if __name__ == '__main__':
    unittest.main()
