import pandas as pd
import sys
fname = sys.argv[1] #insert file name here

data = pd.read_csv(fname) 

approve = []
reject = []

resource_1 = data['Answer.resource_1']
resource_2 = data['Answer.resource_2']
resource_3 = data['Answer.resource_3']
resource_4 = data['Answer.resource_4']
resource_5 = data['Answer.resource_5']

response_1 = data['Answer.response_1']
response_2 = data['Answer.response_2']
response_3 = data['Answer.response_3']
response_4 = data['Answer.response_4']
response_5 = data['Answer.response_5']


def check_none(s1):
	if "never saw" in s1.lower() or "have never seen" in s1.lower() or "have never seen" in s1.lower() or "didn't see" in s1.lower():
		return True
	return False 

for r1,r2,r3,r4,r5,s1,s2,s3,s4,s5 in zip(resource_1,resource_2,resource_3,resource_4,resource_5,response_1,response_2,response_3,response_4,response_5):
	flag = False
	x  = len(r1.split()) + len(r2.split()) + len(r3.split()) + len(r4.split()) + len (r5.split())
	if x > 5:
		flag = True
	if r1[0] == '{' or s1[0] == '{' or r2[0] == '{' or s2[0] == '{' or r3[0] == '{' or s3[0] == '{' or r4[0] == '{' or s4[0] == '{' or r5[0] == '{' or s5[0] == '{':
		flag = True

	if check_none(r1) or check_none(r2) or check_none(r3) or check_none(r4) or check_none(r5):
		flag = True

	if flag:
		approve.append("")
		reject.append("Not as per instructions")
	else:
		approve.append("x")
		reject.append("")

		
data['Approve'] = approve
data['Reject'] = reject
#fname = "update_" + fname
data.to_csv(fname,index = False)		