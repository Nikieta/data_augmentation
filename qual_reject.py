import pandas as pd
import sys

data = pd.read_csv(sys.argv[1])

approve = []
reject = []

data = data[data.AssignmentStatus=='Submitted']
app_rate = list(data['WorkTimeInSeconds'])
print((app_rate[0]))
for i in app_rate:
	if i > 130:

		approve.append('x')
		reject.append('')
	else:
		approve.append('')
		reject.append('It is highly unlikely that the chats have been read and evaluated in this time. Hence the rejection')

data['Approve'] = approve
data['Reject'] = reject

data.to_csv(sys.argv[1])

