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
#review,critic review, plot based, do you remember , fav scene ,fav character, trivia , trivia person, reddit, aspect-specific, aspect generic

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

count = 0
breakpoint = 2
movie2charac = load(open('data/character_list.pkl','rb'))
movies,people,genres,characters = load(gzip.open('data/final_data.pklz'))

def add_pre_template(breakpoint):
	if breakpoint%2 == 0:
		return '<b>You:</b> ' 
	return '<b>Friend:</b> '

def check_if_exists(movie_id,conversation,key): #call augmentation directly from here refined logic for breakpoint
	breakpoint = breakpoint_detector(conversation,key)	

	if key =='scene':
		if look_for_words(conversation,fav_scene_look_for_words) and movies[movie_id].fav_scene:
			if breakpoint_showstoppers(conversation,breakpoint):
				conversation = fav_scene_augmentation(movie_id,conversation,breakpoint)
			

	if key == 'character':
		if fav_character_detector(movie_id,conversation) and movies[movie_id].fav_character:
			if breakpoint_showstoppers(conversation,breakpoint):
				conversation = fav_character_augmentation(movie_id,conversation,breakpoint)
			

	if key == 'movie_trivia':
		trivias = movies[movie_id].trivia
		trivia_chosen = choose_medium_length_string(trivias)
		if trivia_chosen is not None:
			if breakpoint_showstoppers(conversation,breakpoint):
				conversation = movie_trivia_augmentation(movie_id,conversation,breakpoint,trivia_chosen)
			

	if key == 'critical_review':
		critical_reviews = movies[movie_id].critical_reviews
		selected_review = choose_medium_length_string(critical_reviews)
		if selected_review is not None:
			if selected_review[0].islower():
				selected_review = "This movie is " + selected_review
			if breakpoint_showstoppers(conversation,breakpoint):
				conversation = movie_review_augmentation(movie_id,conversation,breakpoint,selected_review,s=" ")
			

	if key == 'opinion':
		if look_for_words(conversation,opinion_look_for_words) and movies[movie_id].opinion:
			if breakpoint_showstoppers(conversation,breakpoint):
				conversation = opinion_augmentation(movie_id,conversation,breakpoint)
			

	return conversation


	
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
	

def breakpoint_detector(conversation,key): #debug remains
	breakpoint = 0
	
	if key=='opinion' or key=='critical_review':
		#print(2)
		breakpoint = 2 #change to 0
	if key=='movie_trivia' or key=='scene' or key=='character':
		#print(8)
		breakpoint =  8
	
	return breakpoint	

def augment_the_conversation(conversation,breakpoint,statements):
	pre_conversation = conversation[0:breakpoint]
	post_conversation = conversation[breakpoint:] #change the sequence here
	conversation = pre_conversation + statements + post_conversation
	return conversation

###Club to one function only

def fav_scene_augmentation(movie_id,conversation,breakpoint):
	starting_template = add_pre_template(breakpoint) + ch(fav_scene_open_statements)
	fav_scene = add_pre_template(breakpoint+1) + ch(movies[movie_id].fav_scene) 
	return augment_the_conversation(conversation,breakpoint,[starting_template,fav_scene])

def fav_character_augmentation(movie_id,conversation,breakpoint):
	fav_scene = add_pre_template(breakpoint+1) + ch(movies[movie_id].fav_character) 
	starting_template = add_pre_template(breakpoint) + ch(fav_character_open_statements)
	return augment_the_conversation(conversation,breakpoint,[starting_template,fav_scene])
	
def movie_trivia_augmentation(movie_id,conversation,breakpoint,trivia_chosen,s=" "):
	s = add_pre_template(breakpoint) + ch(mid_trivia_open_statements) + trivia_chosen 
	answer = add_pre_template(breakpoint+1) + ch(mid_trivia_accept)
	return augment_the_conversation(conversation,breakpoint,[s,answer]) #change to s after first batch		

def movie_review_augmentation(movie_id,conversation,breakpoint,selected_review,s=" "):
	s = add_pre_template(breakpoint) + ch(review_intro_statements) + selected_review 
	answer = add_pre_template(breakpoint+1) + ch(mid_review_accept)
	return augment_the_conversation(conversation,breakpoint,[s,answer])			

def opinion_augmentation(movie_id,conversation,breakpoint):
	starting_template = add_pre_template(breakpoint) + ch(opinion_open_statements)
	fav_scene = add_pre_template(breakpoint+1) + ch(movies[movie_id].opinion) 
	return augment_the_conversation(conversation,breakpoint,[starting_template,fav_scene])

###

def dict_creator():
	movie = ["Interstellar","The Despicable Me","You Have Got Mail","Ace Ventura","Star Trek","Rush Hour","Speed","The Notebook","Liar Liar","Ice Age","Gone in Sixty Seconds","Serendipity","Boss Baby","Matrix","X men","Bride Wars","Bruce Almighty","The Avengers","Inception","Titanic","Superman","Home Alone","Avataar","Iron Man","Finding Nemo","The Fast and the Furious","Transporter","The Wedding Singer","The Incredibles","The Dark Knight"]
	movie_id = ['tt0816692','tt1323594','tt0128853','tt0109040','tt0796366','tt0120812','tt0111257','tt0332280','tt0119528','tt0268380','tt0187078','tt0240890','tt3874544','tt0133093','tt0120903','tt0901476','tt0315327','tt0118661','tt1375666','tt0046435','tt0078346','tt0099785','tt0499549','tt0371746','tt0266543','tt0232500','tt0293662','tt0120888','tt0317705','tt0468569']
	_dict = {}
	for m,m_id in zip(movie,movie_id):
		_dict[m] = m_id
	return _dict

movie_list = dict_creator() 
def begin_augmentation (conversation):
	global count
	keys = ['scene','character','opinion','critical_review','movie_trivia']
	p = [0.25,0.25,0.25,0.125,0.125]
	l = len(conversation)
	s = re.sub("<b>You:</b> Umm, let's talk about ",'',conversation[0])
	#print(s)
	#print(type(movie_list))
	movie_id = movie_list[s]
	#print(movie_id)
	#print(movies[movie_id].title)
	while(len(conversation)==l):
		if not keys:
			#print("Didn't")
			count = count + 1
			break
		key = ch(keys)
		conversation = check_if_exists(movie_id,conversation,key)
		keys.remove(key)
		
	return conversation



def main():
	global count
	data = pd.read_csv('AMT_Chats - Sheet1.csv')
	all_conversations = []
	conversation = []
	data = np.array(data)
	for i in data:
		if isinstance(i[0],float):
			if math.isnan(i[0]):
				#print(i[0])
				all_conversations.append(conversation)
				conversation = []
				continue
		if isinstance(i[4],str):
			conversation.append(i[4])

	all_conversations = all_conversations[1:]
	k = 0
	store_conversations = []
	problem_conversations = []
	for conversation in all_conversations:
		conversation = begin_augmentation(conversation)
		if(len(conversation)==8):
			problem_conversations.append(conversation)
		else:
			store_conversations.append(conversation)	
		#print(conversation)
		
	print(count)

	pickle.dump(store_conversations,open('aug_540.pkl','wb'))
	pickle.dump(problem_conversations,open('didn_aug_540.pkl','wb'))


if __name__ == "__main__":
    main()

