import pandas as pd
import sys
import re
from nltk import ngrams
from difflib import SequenceMatcher

fname = sys.argv[1]

def check_eight(sent):
	m = re.findall(':',sent)
	if len(m) > 5:
		return True
	return False

def process_data(Input):
	new_array = []
	for i in Input:
		new_array.append(str(i))
	return new_array



def check_annotation(sent): #convert to ascii / printable characters first
	if sent[0] == 'P' or sent[0] == 'N' or sent[0] == 'R' or sent[0] == 'C' or sent[0] == '(':
		return True
	m = sent.split()[0]
	# Add a check for < You >
	if '< Speaker 1' in sent or '< Speaker 2' in sent or '< Speaker1' in sent or '< Speaker2' in sent:
		return True

	if 'speaker1' in m.lower() or 'Speaker2' in m.lower() or 'speaker' in m.lower():
		return True

	return False

def compare(string1,string2): #change to return indices
	
	match = SequenceMatcher(None, string1.lower(), string2.lower()).find_longest_match(0, len(string1), 0, len(string2))

	if match.size > 2:
		#print (match.size)
		return True
	return False

def check_resource_usage(sent,comment,review):
	m = re.sub('\n\n','\n',str(sent))
	m = m.split('\n')
	
	for i in m:
		anno = i.partition(':')
		
		if 'C' in str(anno[0]):
			flag = compare(comment,i)
			if flag:
				continue
			else:
				return False

		if 'R' in str(anno[0]):
			flag = compare(review,i)
			if flag:
				continue
			else:
				return False
		
	return True	

def check_none(sent):
	m = re.findall('(N)',sent)
	if len(m) < 3:
		return True
	return False

def check_assn_status(m):
	if m=='Submitted':
		return True
	return False

def check_instruction_copy(sent):
	if 'oh the one with the heroic mission where french, british, belgian and dutch soldiers' in sent.lower():
		return False
	return True

def check_sort_of(sent):
	if 'what sort of movie is' in sent.lower():
		return False
	return True


data = pd.read_csv(fname)
print(len(data))

rejection_string = "Missing annotation of resources or copied from the instructions or submiited less than 8 sentences or more than 2 Nones used. Hence the rejection. Sorry"
accept = []
reject = []

answers = data['Answer.writing_chats']
movie_name = data['Input.movie_name_1']
assn_status = data['AssignmentStatus']
comment = data['Input.comment_1']
review = data['Input.review_1']
for m,a,an,c,r in zip(movie_name,answers,assn_status,comment,review):
	flag = False
	flag = check_annotation(a) and check_eight(a)  and check_instruction_copy(a) and check_assn_status(an) and check_resource_usage(a,c,r) and check_sort_of(a)
	if check_assn_status(an):
		if flag:
			accept.append('x')
			reject.append('')
		else:
			accept.append('')
			reject.append(rejection_string)
	else:
		accept.append('')
		reject.append('')
	
	

#print(reject)
data['Approve'] = accept
data['Reject'] = reject
uname = fname[:-4] +'_review.csv'
d = {'title':movie_name,'assn_status':assn_status,'writing_chats': process_data(answers),'Approve':accept,'Reject':reject}
df = pd.DataFrame(d)
fname = fname[:-4] +'_updated.csv'
data.to_csv(fname,index = False)
df.to_csv(uname,index = False)
