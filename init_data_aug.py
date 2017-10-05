from strings_for_data_aug import *
import numpy as np
import pandas as pd
import re
#from ner import movie_ner, person_ner, genre_ner, movie_person_ner
from pickle import load
import gzip
import math
import pickle
from numpy.random import choice as ch
import string
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
#review,critic review, plot based, do you remember , fav scene ,fav character, trivia , trivia person, reddit, aspect-specific, aspect generic
printable = set(string.printable)
'''
Appending after conversation

1. Trivia done
2. Opinion - user done
3. Fav scene done
4. Fav character done
5. Trivia person
6. critic done 
7. aspect (??)

This plus for active

1. Quora
2. Reddit
3. Do you remember
4. Synthetic
'''


def convert_to_ascii(statement):
	global printable
	return  filter(lambda x: x in printable, statement)

def change_to_html(array):
	s = ''

	for i in array:
		#st = i.encode('ascii',errors='ignore')
		st = convert_to_ascii(i)
		s = s + ' <p> ' + str(st) + ' </p> '

	return s
movies = None
people = None
genres = None
characters = None
reddit_singles = None
reviews = None
review_titles = None


count = 0
breakpoint = 2
movie2charac = load(open('data/character_list.pkl','rb'))
movies,people,genres,characters = load(gzip.open('data/final_data.pklz'))
questions = load(open('data/movie_question_dict.pkl'))
reddit_singles = pickle.load(open('data/reddit_singles.pkl','rb'))
review_titles = pickle.load(open('data/review_titles.pkl' ,'rb' ))
reviews = pickle.load(open('data/reviews.pkl','rb'))

def statement_processing(start,end=None):
	x = '<p><b> You: </b> '+ start + '</p>'

	if end ==None:
		return 	
	
	else:
		return x + '<p><b> Friend: </b> '+ end + '</p>'
	

def check_if_exists(movie_id,key): #call augmentation directly from here refined logic for breakpoint
	
	conversation = None
	i = -1
	l = -1

	if key =='scene':
		if movies[movie_id].fav_scene:
			i = ch(np.arange(len(movies[movie_id].fav_scene)))
			chosen = movies[movie_id].fav_scene[i]
			conversation = statement_processing(ch(fav_scene_open_statements),chosen)
			l = 2			

	if key == 'character':
		if movies[movie_id].fav_character:
			i = ch(np.arange(len(movies[movie_id].fav_character)))
			chosen = movies[movie_id].fav_character[i]
			conversation = statement_processing(ch(fav_character_open_statements),chosen)
			l = 4			
			
	
	'''		

	if key == 'movie_trivia':
		trivias = movies[movie_id].trivia
		trivia_chosen = choose_medium_length_string(trivias)
		if trivia_chosen is not None:
			conversation = movie_trivia_augmentation(movie_id,conversation,breakpoint,trivia_chosen)
	'''		

	if key == 'critical_review':
		critical_reviews = movies[movie_id].critical_reviews
		selected_review = choose_medium_length_string(critical_reviews)
		if selected_review is not None:
			if selected_review[0].islower():
				processed_review = "This movie is " + selected_review
				conversation = statement_processing(ch(review_intro_statements),processed_review)
				i = critical_reviews.index(selected_review)			
				l = 8			
				

	if key == 'opinion':
		if movies[movie_id].opinion:
			i = ch(np.arange(len(movies[movie_id].opinion)))
			chosen = movies[movie_id].opinion[i]
			conversation = statement_processing(ch(opinion_open_statements),chosen)
			l = 3		


				
	if key == 'question':
		if movie_id in questions:
			if questions[movie_id]:
				i = ch(np.arange(len(questions[movie_id])))
				chosen = questions[movie_id][i]
				conversation = statement_processing(chosen)
				l = 7

	if key == 'remember':
		if movies[movie_id].do_you_remember:
			i = ch(np.arange(len(movies[movie_id].do_you_remember)))
			chosen = movies[movie_id].do_you_remember[i]
			conversation = statement_processing(chosen)
			l = 5			


	'''		
	if conversation:
		 chat.append(conversation)              
		 index.append(i)
		 legend.append(l)
	'''

	return conversation , i ,l


	
def breakpoint_showstoppers(conversation,breakpoint):
	current_string = conversation[breakpoint-1]
	flag = True
	if re.findall('\?',current_string): #determines if a question
		flag = False

	return flag
	#dst remaning!


def choose_medium_length_string(l,lmin=5,lmax=18):
		good_strings = filter(lambda x: len(x.split())>=lmin and len(x.split())<=lmax,l)
		if(len(good_strings) == 0):
			return None
		else:
			return ch(good_strings)

def person_detector(movie_id,conversation): #function for people trivia incomplete
	person =  movies[movie_id].cast
	broken_person = []
	for every_person in person:
		broken_person = broken_person + people[every_person].name.lower().split()
	flag = look_for_words(conversation,broken_person)
	if not flag:
		count = 0
		for sentence in conversation:
			given_words = sentence.lower().split()
			breakpoint = count
	
	return flag



def look_for_words(conversation,word_list):
	for sentence in conversation:
		given_words = sentence.lower().split()
		if not set(given_words).isdisjoint(word_list):
			return False
	return True	


def fav_character_detector(movie_id,conversation):
	character_list = movie2charac[movie_id]
	broken_person = []
	for every_person in character_list:
		broken_person = broken_person + every_person.lower().split()
	flag = look_for_words(conversation,fav_character_look_for_words+broken_person)
	return flag
	


def augment_the_conversation(conversation,breakpoint,statements):
	pre_conversation = conversation[0:breakpoint]
	post_conversation = conversation[breakpoint:] #change the sequence here
	conversation = pre_conversation + statements + post_conversation
	return conversation




###

def begin_augmentation ():
	global count
		

def i_softmax(a):
	b = np.ones(len(a))
	b = b - (np.exp(a) / np.sum(np.exp(a), axis=0))
	return b

def normalise(a):
	return a/np.linalg.norm(a)

def main():
	
	data = pd.read_csv('/home/nikita/Downloads/50 movies - Sheet2.csv') # change file_name here
	keys = ['scene','character','opinion','critical_review','question','remember']
	count = np.ones(len(keys))
	movie_name = data['title']
	wiki = data['wiki']
	imdb_id = data['imdb_id']
	s_movie_name = []
	s_wiki = []
	s_imdb_id = []
	s_chat = []
	did_not = []
	legend = []
	index_ = []
	m_plot = []
	m_review = []
	m_comment = []

	for m,w,id_ in zip(movie_name,wiki,imdb_id):
		conversation = None
		keys = ['scene','character','opinion','critical_review','question','remember']
		flag = True
		while(conversation == None):
			if not keys:
				flag = False
				break
			key = ch(keys)
			conversation,i,l = check_if_exists(id_,key)
			inx = keys.index(key)
			keys.remove(key)

		if flag:
			s_wiki.append(w)
			s_chat.append(conversation)
			s_imdb_id.append(id_)
			s_movie_name.append(m)
			index_.append(i)
			legend.append(l)
			m_plot.append(movies[id_].plot)
			temp = ""
			if id_ in reddit_singles:
				temp = temp + change_to_html(reddit_singles[id_])
			if id_ in review_titles :
				temp  = temp + change_to_html(review_titles[id_])
			m_comment.append(temp)
			if id_ in reviews:
				m_review.append(convert_to_ascii(reviews[id_][0]))
			else:
				m_review.append("")

			keys = ['scene','character','opinion','critical_review','question','remember']
			inx = keys.index(key)
			count[inx] = count[inx] + 1

		else:
			did_not.append(id_)
	print(did_not)
	for i in did_not:
		conversation,i_m,l = check_if_exists(i,'scene')
		s_wiki.append(w)
		s_chat.append(conversation)
		s_imdb_id.append(id_)
		s_movie_name.append(m)
		index_.append(i_m)
		legend.append(l)
		m_plot.append(movies[i].plot)
		temp = ""
		if i in reddit_singles:
				temp = temp + change_to_html(reddit_singles[i])
		if id_ in review_titles :
			temp  = temp + change_to_html(review_titles[i])
		m_comment.append(temp)
		if id_ in reviews:
			m_review.append(convert_to_ascii(reviews[i][0]))
		else:
			m_review.append("")

	print(len(s_wiki))
	print(len(s_chat))
	print(len(s_imdb_id))
	print(did_not)
	'''
	d = {'chat_1': s_chat[0:10], 'wiki_1' : s_wiki[0:10], 'imdb_id_1': s_imdb_id[0:10], 'movie_name_1': s_movie_name[0:10], 'legend_1': legend[0:10], 'used_index_1': index_[0:10],
	'chat_2': s_chat[10:20], 'wiki_2' : s_wiki[10:20], 'imdb_id_2': s_imdb_id[10:20], 'movie_name_2': s_movie_name[10:20], 'legend_2': legend[10:20], 'used_index_2': index_[10:20],
	'chat_3': s_chat[20:30], 'wiki_3' : s_wiki[20:30] ,'imdb_id_3': s_imdb_id[20:30], 'movie_name_3': s_movie_name[20:30], 'legend_3': legend[20:30], 'used_index_3': index_[20:30],
	'chat_4': s_chat[30:40], 'wiki_4' : s_wiki[30:40], 'imdb_id_4': s_imdb_id[30:40], 'movie_name_4': s_movie_name[30:40], 'legend_4': legend[30:40], 'used_index_4': index_[30:40],
	'chat_5': s_chat[40:], 'wiki_5' : s_wiki[40:], 'imdb_id_5': s_imdb_id[40:], 'movie_name54': s_movie_name[40:], 'legend_5': legend[40:], 'used_index_5': index_[40:],
	'plot_1': m_plot[0:10], 'plot_2' : m_plot[10:20], 'plot_3': m_plot[20:30], 'plot_4': m_plot[30:40], 'plot_5': m_plot[40:],
	'review_1': m_review[0:10], 'review_2' : m_review[10:20], 'review_3': m_review[20:30], 'review_4': m_review[30:40], 'review_5': m_review[40:],
	'comment_1': m_comment[0:10], 'comment_2' : m_comment[10:20], 'comment_3': m_comment[20:30], 'comment_4': m_comment[30:40], 'comment_5': m_comment[40:]
	}

'''
	d = {'chat_1': s_chat[0:25], 'wiki_1' : s_wiki[0:25], 'imdb_id_1': s_imdb_id[0:25], 'movie_name_1': s_movie_name[0:25], 'legend_1': legend[0:25], 'used_index_1': index_[0:25],
	'chat_2': s_chat[25:], 'wiki_2' : s_wiki[25:], 'imdb_id_2': s_imdb_id[25:], 'movie_name_2': s_movie_name[25:], 'legend_2': legend[25:], 'used_index_2': index_[25:],	'plot_1': m_plot[0:25], 'plot_2' : m_plot[25:], 
	'review_1': m_review[0:25], 'review_2' : m_review[25:], 'comment_1': m_comment[0:25], 'comment_2' : m_comment[25:]}

	df = pd.DataFrame(d)
	df.to_csv('augmented_start_batch_50_2_1.csv',index=False)
	print('Complete')

		


if __name__ == "__main__":
	main()

