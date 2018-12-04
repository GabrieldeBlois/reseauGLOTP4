

import json


def test(msg):
    msg["key"] = "toto"

dictTest = {}
test(dictTest)
print(json.dumps(dictTest))