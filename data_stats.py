import pandas as pd
import pickle
import glob
import numpy as np
import re
import string
printable = set(string.printable)
#movie name movie id dict id wiki plot(get full plot) review plot_part comment chat annotations

#movie stats - how many disctinct movies , movie count

def convert_to_ascii(statement):
	if statement == None:
		return ''
	global printable
	return  filter(lambda x: x in printable, statement)

def remove_tags(source_string):
	source_string = re.sub('<p>','',source_string)
	source_string = re.sub('</p>','\n',source_string)
	source_string = re.sub('<b>','',source_string)
	source_string = re.sub('</b>','',source_string)
	return source_string

def augment_response(input_,chat):
	new_chats = []
	for i,c in zip(input_,chat):
		s = remove_tags(convert_to_ascii(str(i)))  + str(c)
		new_chats.append(s)
	#new_chats = remove_tags(new_chats)
	return new_chats	

def statement_processing(input_chat):
	all_st = []
	all_anno = []
	flag = np.zeros(len(input_chat))
	count = 0
	x_count = 0
	chat_len = []
	for every_chat in input_chat:
		colon_count = re.findall(':',every_chat)
		every_chat = re.sub('\n\n','\n',every_chat)
		every_chat = every_chat.strip()
		s = every_chat.split('\n')
		for i in s:
			if s =='':
				s.remove(i)
		if len(s) != colon_count:
			flag[count] = len(colon_count)
		st = []
		anno = []
		
		for i in s:
			x = i.partition(':')
			st.append(str(x[2]))
			if 'P' in str(x[0]):
				anno.append('P')
			elif 'R' in str(x[0]):
				anno.append('R')
			elif 'N' in str(x[0]):
				anno.append('N')
			elif 'C' in str(x[0]):
				anno.append('C')
			else:
				anno.append('X')
				x_count = x_count + 1	
		

		all_st.append(st)
		all_anno.append(anno)
		count = count + 1	
	print (x_count)
	return all_st, all_anno, flag

def movie_stats(data):
	id_ = data['Input.imdb_id_1']
	id_ = np.array(id)
	unique, counts = numpy.unique(id_, return_counts=True)
	print(np.av)
chat_dict = {}

count = 0

f = '/home/nikita/Downloads/So_Far_Chats.csv'
data = pd.read_csv(f)
data = data[data.AssignmentStatus=='Approved']
input_chat = data['Input.chat_1']
answer_chat = data['Answer.writing_chats']
chat = augment_response(input_chat,answer_chat)
a,b,c = statement_processing(chat)
d = {'chat':a,'anno':b,'flag':c,'chat_og':answer_chat}
df = pd.DataFrame(d)
df.to_csv('trying.csv',index = False)
