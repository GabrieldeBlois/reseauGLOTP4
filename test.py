

import json

with open("./gaby/emaillist.json") as infp:
    rawContent = infp.read()
    contentDeserialized = json.loads(rawContent)
    subjectList = list((x["subject"] for x in contentDeserialized))
    print(subjectList)
