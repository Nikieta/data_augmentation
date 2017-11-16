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
import sys
import string
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
fname_input = 'new_1000_movies.csv' #hardcoding here
ind = sys.argv[1]
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
extra_data = pickle.load(open('data/extra_data.pkl','rb'))


def array_to_html(input):
	s = ''
	for i in input:
		s = s + '<p>' + str(i) + '</p>'
	return s
def movies_like_list(input):
	global movies
	s = ''
	for i in input:
		 s = s +'<p>'+ i.title + '</p>'
	return s

def convert_to_ascii(statement):
	if statement == None:
		return ''
	global printable
	return  filter(lambda x: x in printable, statement)

def change_to_html(array):
	s = ''

	for i in array:
		#st = i.encode('ascii',errors='ignore')
		st = convert_to_ascii(i)
		s = s + ' <p> ' + str(st) + ' </p> '

	return s

def statement_processing(start,end=None):
	x = '<p><b> Speaker1 (N): </b> '+ str(start) + '</p>'

	if end ==None:
		return 	
	
	else:
		return x + '<p><b> Speaker2 (C): </b> '+ str(end) + '</p>'
	

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
		elif movie_id in extra_data:	
			chosen = extra_data[movie_id]['fav_scene']
			conversation = statement_processing(ch(fav_scene_open_statements),chosen)
			l = 2
		

	if key == 'character':
		if movies[movie_id].fav_character:
			i = ch(np.arange(len(movies[movie_id].fav_character)))
			chosen = movies[movie_id].fav_character[i]
			conversation = statement_processing(ch(fav_character_open_statements),chosen)
			l = 4
		elif movie_id in extra_data:	
			chosen = extra_data[movie_id]['fav_character']
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
		elif movie_id in extra_data:	
			chosen = extra_data[movie_id]['opinion']
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
		elif movie_id in extra_data:	
			chosen = extra_data[movie_id]['do_you_remember']
			conversation = statement_processing(chosen)
			l = 5			


	'''		
	if conversation:
		 chat.append(conversation)              
		 index.append(i)
		 legend.append(l)
	'''

	return conversation , i ,l

'''
	
def breakpoint_showstoppers(conversation,breakpoint):
	current_string = conversation[breakpoint-1]
	flag = True
	if re.findall('\?',current_string): #determines if a question
		flag = False

	return flag
	#dst remaning!
'''

def choose_medium_length_string(l,lmin=5,lmax=18):
		good_strings = filter(lambda x: len(x.split())>=lmin and len(x.split())<=lmax,l)
		if(len(good_strings) == 0):
			return None
		else:
			return ch(good_strings)
'''
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
	
'''

def augment_the_conversation(conversation,breakpoint,statements):
	pre_conversation = conversation[0:breakpoint]
	post_conversation = conversation[breakpoint:] #change the sequence here
	conversation = pre_conversation + statements + post_conversation
	return conversation

def plot_update(plot):
	_plot = convert_to_ascii(plot)
	plot = str(plot).split('.')
	ten_len = len(plot)/10
	if ten_len > 0:
		s = ''
		arr = np.arange(ten_len)
		np.random.shuffle(arr)	
		for i in plot[arr[0]*10:arr[0]*10+10]:
			s = s + i + ". "
			s = convert_to_ascii(s)
		return s,arr[0]	
	
	return convert_to_ascii(str(_plot)),0
	
	#print(len(s))

	

def plot_array(input_array):
	output_array = []
	output_array_legend = []
	for plot in input_array:
		a,b = plot_update(plot)
		output_array.append(a)
		output_array_legend.append(b)
	
	return output_array,output_array_legend


''''
def i_softmax(a):
	b = np.ones(len(a))
	b = b - (np.exp(a) / np.sum(np.exp(a), axis=0))
	return b

def normalise(a):
	return a/np.linalg.norm(a)
'''
def main():
	data = pd.read_csv(fname_input) # change file_name here
	x = np.arange(len(data)) 
	np.random.shuffle(x)#number of movies you want to give
	x = x[0:int(sys.argv[2])	]
	keys = ['scene','character','opinion']
	count = np.ones(len(keys))
	movie_name =np.array(data['title'])
	movie_name = movie_name[x]
	#wiki = data['wiki']
	imdb_id = np.array(data['imdb_id'])
	imdb_id = imdb_id[x]
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
	s_rev_lengend = []
	awards = []
	box_office = []
	movies_like = []
	taglines = []

	for m,id_ in zip(movie_name,imdb_id):
		conversation = None
		keys = ['scene','character','opinion']
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
			s_wiki.append('https://en.wikipedia.org/?curid='+str(movies[id_].wiki_id))
			s_chat.append(conversation)
			s_imdb_id.append(id_)
			s_movie_name.append(m)
			index_.append(i)
			legend.append(l)
			m_plot.append(movies[id_].plot)
			awards.append(array_to_html(movies[id_].awards[0:3]))
			box_office.append(movies[id_].net_gross)
			movies_like.append(movies_like_list(movies[id_].movies_like[0:5]))
			taglines.append(array_to_html(movies[id_].taglines[0:3]))
			temp = ""
			if id_ in reddit_singles:
				temp = temp + change_to_html(reddit_singles[id_])
			if id_ in review_titles :
				temp  = temp + change_to_html(review_titles[id_])
			m_comment.append(temp)
			if id_ in reviews:
				m_review.append(convert_to_ascii(reviews[id_][1]))
				s_rev_lengend.append(1)
			else:
				m_review.append("")
				s_rev_lengend.append(-1)

			

		else:
			did_not.append(id_)
	print(did_not)
	'''
	for i in did_not:
		conversation,i_m,l = check_if_exists(i,'scene')
		s_wiki.append('https://en.wikipedia.org/?curid='+str(movies[i].wiki_id))
		s_chat.append(conversation)
		s_imdb_id.append(i)
		s_movie_name.append(movies[i].title)
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
			s_rev_lengend.append(0)
		else:
			m_review.append("")
			s_rev_lengend.append(-1)	
	'''	
	m_plot,s_plot_legend = plot_array(m_plot)
	
	print(len(s_wiki))

	d = {'comment_1': m_comment,'plot_1':m_plot,'review_1':m_review ,'chat_1': s_chat, 'wiki_1':s_wiki, 'imdb_id_1': s_imdb_id, 'movie_name_1': s_movie_name, 'legend_1': legend, 'used_index_1': index_,
	'review_legend_1': s_rev_lengend,'plot_legend_1':s_plot_legend,'award_1':awards,'tagline_1':taglines,'box_office_1':box_office,'similar_movies_1':movies_like}
	df = pd.DataFrame(d)
	df.to_csv('self_chat_batch_'+str(ind) + '.csv',index=False,encoding = 'utf-8')
	#pickle.dump(did_not,open('augmented_start_failed_batch_1.csv','wb'))


		


if __name__ == "__main__":
	main()

