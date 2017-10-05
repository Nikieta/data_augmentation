import numpy as np
from ner import movie_ner, person_ner, genre_ner, movie_person_ner
import pandas as pd
import pickle
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


movie_question_dict = {}
people_question_dict = {}



def get_named_entity_random(s):
		entity = movie_person_ner(s)
		if(len(entity) == 0):
			return None, False
		else:
			imdb_id = entity[0][1]
			if(imdb_id[:2] == 'tt'):
				return imdb_id, True
			else:
				return imdb_id, False

def choose_medium_length_string(l,lmin=5,lmax=18):
		good_strings = filter(lambda x: len(x.split())>=lmin and len(x.split())<=lmax,l)
		if(len(good_strings) == 0):
			return False
		else:
			return True

data = pd.read_csv('data/questions_quora.csv')
data = data['question']
#print(data[0][0])
#print(len(data[0]))
k = 0
for i in data:
	#print(i)
	s = str(str(i).encode(encoding='UTF-8'))

	k = k + 1
	if (k%100==0):
		print(k)
		pickle.dump(movie_question_dict,open('movie_question_dict.pkl','wb'))
		pickle.dump(people_question_dict,open('people_question_dict.pkl','wb'))

	
	imdb_id,flag = get_named_entity_random(s)
	if imdb_id is None:
		continue
	if not choose_medium_length_string([s]):
		continue
	if flag:
		if imdb_id in movie_question_dict:
			movie_question_dict[imdb_id].append(s)
		else:
			movie_question_dict[imdb_id] = [s]
	else:
		if imdb_id in people_question_dict:
			people_question_dict[imdb_id].append(s)
		else:
			people_question_dict[imdb_id] = [s]

print(len(movie_question_dict))
print(len(people_question_dict))

pickle.dump(movie_question_dict,open('movie_question_dict.pkl','wb'))
pickle.dump(people_question_dict,open('people_question_dict.pkl','wb'))
	