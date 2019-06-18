import unittest
import re
from envirest import EnviPathClient
from getpass import getpass
USER = 'admin'
PASS = getpass()
HOST = 'envipath.org'
TESTHOST = 'envipath.org:8181'
PACKAGE = 'EAWAG-SOIL'


class MyTestCase(unittest.TestCase):

    def test_something(self):
        client = EnviPathClient(host=TESTHOST, username=USER, password=PASS, secure=False, verify=False)
        scenariourl = "http://envipath.org:8181/package/b4c33235-b30d-4d7c-a8b0-5d1a1d2aff48/scenario/c97a868d-59c6-4cdb-982a-a2492dd031f1"

        for lower, upper, source, comment, model, fit in [(2.5, 2.5, '', 'some comment; some more', 'SFO', 'chi2'),
                                                          ('4.0E-12', 2.6, '', 'some comment; some more', 'SFO+', '')]:

            whatyouget = client.updatescenario(scenariourl, halflife={
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


if __name__ == '__main__':
    unittest.main()
