import unittest
import re
from requests.exceptions import ReadTimeout

from envirest import EnviPathClient


USER = 'anonymous'
TESTHOST = 'envipath.org:8181'
PACKAGE = 'anonymous'

DIOXANE_PW = 'https://envipath.org/package/32de3cf4-e3e6-4168-956e-32fa5ddb0ce1/pathway/19a53ddd-7bbe-43b3-bd56-c1c35302d185'


class PostTestCase(unittest.TestCase):

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

        for lower, upper, source, comment, model, fit in [
            (2.5, 2.5, '', 'some comment; some more', 'SFO', 'chi2'),
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
        updated = self.client.updaterreaction(reaction,
                name='the little alchemist', related_rule=rule)
        assert updated['rules'][0]['id'] == rule
        assert updated['name'] == 'the little alchemist'
        assert updated['smirks'] == '[Pb]>>[Au]'
        self.client.delete(reaction)
        self.client.delete(rule)


class GetTestCase(unittest.TestCase):
    """Testing GET calls on the productive server
    """

    def test_envi_link(self):
        """check whether get_enviLink is correct"""
        client = EnviPathClient('envipath.org')
        self.assertEqual(len(client.get_enviLink(rule='bt0028')), 1)

    def test_timeout(self):
        """check timeout functionality for plain get calls"""
        client = EnviPathClient('envipath.org')
        with self.assertRaises(ReadTimeout):
            client.get(DIOXANE_PW, 0.1)
        dpw = client.get(DIOXANE_PW, 10)
        self.assertEqual(len(dpw['nodes']), 12)


if __name__ == '__main__':
    unittest.main()
