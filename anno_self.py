import pandas as pd
import sys
import re
import numpy as np

def remove_tags(source_string):
	source_string = re.sub('<p>','',source_string)
	source_string = re.sub('</p>','\n',source_string)
	source_string = re.sub('<b>','',source_string)
	source_string = re.sub('</b>','',source_string)
	return source_string

def augment_response(input_,chat):
	new_chats = []
	for i,c in zip(input_,chat):
		s = remove_tags(i)  + c
		new_chats.append(s)
	#new_chats = remove_tags(new_chats)
	return new_chats	

fname = sys.argv[1]
data = pd.read_csv(fname)
if "AssignmentStatus" in data:
	data = data[data.AssignmentStatus!='Rejected']

m = len(data)
input_chat = data['Input.chat_1']
chat_1 = data['Answer.writing_chats']
all_chats = augment_response(input_chat,chat_1)
movie_name_1 = data['Input.movie_name_1']
wiki_1 = data['Input.wiki_1']

batch = 40
n = m/batch

for i in range (0,batch*n,batch):
	chat = all_chats[i:i+batch]
	name = movie_name_1[i:i+batch]
	wiki = wiki_1[i:i+batch]
	df = { 'Movie Name': name,'Wiki Link': wiki , 'Chats': chat}
	df = pd.DataFrame(df)
	df ['Intelligble'] = 5  
	df ['Coherent'] = 5 
	df ['On Topic'] = 5
	df ['Grammar'] = 5
	df ['Two-Person Chat'] = 5 
	df ['Other Comments'] = ''
	
	fname_csv = 'annotation_s_2/annotation_batch_'+str(i/batch)+'.csv'
	df.to_csv(fname_csv,index = False)
