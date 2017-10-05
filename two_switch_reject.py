import pandas as pd
import sys
fname = sys.argv[1] #insert file name here

data = pd.read_csv(fname) 

approve = []
reject = []

resource_1 = data['Answer.resource_1']
resource_2 = data['Answer.resource_2']
'''
resource_3 = data['Answer.resource_3']
resource_4 = data['Answer.resource_4']
resource_5 = data['Answer.resource_5']
'''
response_1 = data['Answer.response_1']
response_2 = data['Answer.response_2']
'''
response_3 = data['Answer.response_3']
response_4 = data['Answer.response_4']
response_5 = data['Answer.response_5']
'''

def check_none(s1):
	if "none" in s1.lower():
		return True
	return False 

for r1,r2,s1,s2 in zip(resource_1,resource_2,response_1,response_2):
	flag = False
	x  = len(r1.split()) + len(r2.split()) 
	if x > 3:
		flag = True
	if r1[0] == '{' or s1[0] == '{' or r2[0] == '{' or s2[0] == '{' :
		flag = True

	if check_none(r1) or check_none(r2):
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
