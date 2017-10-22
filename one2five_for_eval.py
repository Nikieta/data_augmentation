import pandas as pd
import sys
import string
import re
reload(sys)
sys.setdefaultencoding('utf-8')

printable = set(string.printable)

def convert_to_ascii(statement):
	global printable
	return  filter(lambda x: x in printable, statement)

def strip_tags(statement):
	statement = re.sub('<p>','',statement)
	statement = re.sub('<b>','',statement)
	statement = re.sub('</b>','',statement)
	statement = re.sub('</p>','\n',statement)
	statement = re.sub('\t','',statement)
	return statement

def combiner(input_chat,chat):
	new_batch = []
	for i,c in zip(input_chat,chat):
		s = '<p>'
		s = s + strip_tags(convert_to_ascii(str(i))) + c
		s = re.sub('\n','</p><p>',s)
		s = s + '</p>'
		new_batch.append(s)
	return new_batch

data = pd.read_csv(sys.argv[1])
print(len(data))
data = data[data.AssignmentStatus=='Approved']
print(len(data))
title = list(data['Input.movie_name_1'])
chat = data['Answer.writing_chats']
input_chat = data['Input.chat_1']
all_chats = combiner(input_chat,chat)
n = len(all_chats)
n = n/5
print(n)
print(len(all_chats[n:2*n]))

d = {'chat_1' : all_chats[0:n] ,'title_1' : title[0:n],'chat_2' : all_chats[n:2*n],'title_2':title[n:2*n],'chat_3':all_chats[2*n:3*n],'title_3':title[2*n:3*n],'chat_4' : all_chats[3*n:4*n],'title_4' : title[3*n:4*n] ,'chat_5' : all_chats[4*n:5*n],'title_5' : title[4*n:5*n]}

df = pd.DataFrame(d)

df.to_csv('self_chat_eval_'+str(sys.argv[2])+'.csv',index = False)