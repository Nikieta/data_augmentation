import pandas as pd
import sys


fname_input = sys.argv[1]

data = pd.read_csv(fname_input)
if "RequesterFeedback" in data:
	data = data[data.RequesterFeedback.isnull()] #Filtering rejected responses
if "AssignmentStatus" in data:
	data = data[data.AssignmentStatus!='Rejected']

total = len(data) * 5
print(total)
new_col = []
new_col = list(data['Answer.resource_1']) + list(data['Answer.resource_2']) + list(data['Answer.resource_3']) + list(data['Answer.resource_4']) + list(data['Answer.resource_5'])
p = r = s = n = c = 0
for i in new_col:
	if i.lower()[0] == 's':
		s = s + 1
	elif i.lower()[0] == 'r':
		r = r + 1
	elif i.lower()[0] == 'c':
		c = c + 1
	elif i.lower()[0] == 'p':
		p = p + 1
	else:
		n = n + 1

print("%d \t %d \t %f \t %d \t %f \t %d \t %f \t %d \t %f \t %d \t %f" % (total,c,float(c) / float (total),r,float(r) / float (total),p,float(p) / float (total),s,float(s) / float (total),n,float(n) / float (total)) )

