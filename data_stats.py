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
		s = remove_tags(convert_to_ascii(str(i)))  + c
		new_chats.append(s)
	#new_chats = remove_tags(new_chats)
	return new_chats	

def statement_processing(input_chat):
	all_st = []
	all_anno = []
	flag = np.zeros(len(input_chat))
	count = 0
	x_count = 0
	count_p = 0
	count_n = 0
	count_r = 0
	count_c = 0
	for every_chat in input_chat:
		colon_count = re.find_all(every_chat)
		s = input_chat.split('\n')
		flag_count = colon_count		
		st = []
		anno = []
		
		for i in s:
			x = s.partition(':')
			st.append(str(x[2]))
			if 'P' in str(x[0]):
				anno.append('P')
				count_p = count_p + 1
			elif 'R' in str(x[0]):
				anno.append('R')
				count_r = count_r + 1
			elif 'N' in str(x[0]):
				anno.append('N')
				count_n = count_n + 1
			elif 'C' in str(x[0]):
				anno.append('C')
				count_c = count_c + 1
			else:
				anno.append('X')
				x_count = x_count + 1	
		

		all_st.append(st)
		all_anno.append(anno)
		count = count + 1	
	print (x_count)
	print (c_count)
	print (n_count)
	print (r_count)
	print (p_count)
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
d = {'chat':a,'anno':b,'flag':c}
df = pd.DataFrame(d)
df.to_csv('trying.csv',index = False)
