import pandas as pd
import sys
import re

fname = sys.argv[1]

def check_eight(sent):
	m = re.findall(':',sent)
	if len(m) > 5:
		return True
	return False

def check_annotation(sent):
	if sent[0] == 'P' or sent[0] == 'N' or sent[0] == 'R' or sent[0] == 'C':
		return True
	m = sent.split()[0]
	# Add a check for < You >

	if 'you' in m.lower() or 'friend' in m.lower():
		return True

	return False

def check_mud (m):
	if m=='Mud':
		return False
	return True

def check_assn_status(m):
	if m=='Submitted':
		return True
	return False
def check_instruction_copy(sent):
	if 'oh the one with the heroic mission where french, british, belgian and dutch soldiers' in sent.lower():
		return False
	return True
data = pd.read_csv(fname)
print(len(data))

accept = []
reject = []

answers = data['Answer.writing_chats']
movie_name = data['Input.movie_name_1']
assn_status = data['AssignmentStatus']
for m,a,an in zip(movie_name,answers,assn_status):
	flag = False
	flag = check_annotation(a) and check_eight(a) and check_mud(m) and check_instruction_copy(a)
	if check_assn_status(an):
		if flag:
			accept.append('x')
			reject.append('')
		else:
			accept.append('')
			reject.append('Not submitted as per the instructions. Sorry!')
	else:
		accept.append('')
		reject.append('')
print(reject)
data['Approve'] = accept
data['Reject'] = reject
uname = fname[:-4] +'_review.csv'
d = {'title':movie_name,'assn_status':assn_status,'writing_chats':answers,'Approve':accept,'Reject':reject}
df = pd.DataFrame(d)
fname = fname[:-4] +'_updated.csv'
data.to_csv(fname,index = False)
df.to_csv(uname,index = False)