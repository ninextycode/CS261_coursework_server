import json

user_input = "What is the share price of Apple?"


request = {}

req1 = {
  'type': 'request',
  'keyword': 'Microsoft'
}

s = json.dumps(req1)

print(s)
with open("/Users/richardlumpi/Documents/A Warwick/Year 1/"
          + "06_Software_Eng/project/CS261_coursework_server/business_logic/nlp/request.txt", "w") as f:
  f.write(s)

