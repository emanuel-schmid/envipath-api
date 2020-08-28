# envipath-api
## Installation
pip install envipath-api
## Example
Get all SMIRKS of a particular Biodegradation Rule
```python
from envirest import EnviPathClient
client = EnviPathClient('envipath.org')

# find package by name
EAWAGBBD = client.findpackage('EAWAG-BBD')

# find rule by name
bbd_rules = client.get(f'{EAWAGBBD}/rule')['rule']
BT37 = [rule['id'] for rule in bbd_rules if rule['name'] == 'bt0037'][0]

# collect SMIRKS from simple rules
simple_rules = client.get(BT37)['simpleRules']
smirks = [client.get(rule['id'])['smirks'] for rule in simple_rules]
```
