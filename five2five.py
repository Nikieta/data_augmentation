import pandas as pd
import re 
import sys
import pickle
from pickle import load
import gzip
from ner import movie_ner
import warnings
import string 
reload(sys)
sys.setdefaultencoding('utf-8')

#
pd.options.mode.chained_assignment = None
fname_input = sys.argv[1] #input file
fname_output = sys.argv[2] #output file
switch_flag = sys.argv[3] #file with or without switch 
movies = None
people = None
genres = None
characters = None
reddit_singles = None
reviews = None
review_titles = None
printable = set(string.printable)

def convert_to_ascii(statement):
	global printable
	return  filter(lambda x: x in printable, statement)
def load_the_full_data():
	global movies,people,genres,characters,reviews,review_titles,reddit_singles

	movies,people,genres,characters = load(gzip.open('data/final_data.pklz'))
	print('Complete')
	reddit_singles = pickle.load(open('data/reddit_singles.pkl','rb'))
	review_titles = pickle.load(open('data/review_titles.pkl' ,'rb' ))
	reviews = pickle.load(open('data/reviews.pkl','rb'))
	print('Data Loading completed')

def get_named_entity_movie(s, mult=True):
		movie_info= movie_ner(s)
		if len(movie_info) == 0:
			return None
		"""
		if len(movie_info) > 1:
			for every_movie in movie_info:
				popularity_score = self.movies[every_movie[1]].popularity_score
				if popularity_score > most_poular_movie:
					most_popular_id = every_movie[1]
			return most_popular_id		
		"""

		
		#print ("Entity", movie_info[0][0])
	

		return movie_info[0][1]

def store_legends():
	global data
	for k in data.itertuples():
		j = k.Index
		for i in range(1,6):
			s =  data.loc[j,'Answer.resource_' + str(i)]
			chosen = s.lower()[0]
			if not (chosen =='s' or chosen =='p' or chosen == 'r' or chosen =='c'):
				chosen = 'n'
			
			data.loc[j,'Input.legend_'+str(i)] = str(data.loc[j,'Input.legend_'+str(i)]) + chosen
	print('Legends Stored')

def change_to_html(array):
	s = ''

	for i in array:
		#st = i.encode('ascii',errors='ignore')
		st = convert_to_ascii(i)
		s = s + ' <p> ' + str(st) + ' </p> '

	return s

def augment_response(source,response):
	new_chat = []

	for s,r in zip(source,response):
		
		count_1 = len(re.findall('<p><b> You: </b>',s))
		count_2 = len(re.findall('<p><b> Friend: </b>',s))
		if ((count_1 + count_2 )%2) == 0: #even utterances completed!
			string = s + ' <p><b> You: </b> ' + r + ' </p> ' 
		else:
			#print('printed')
			string = s + ' <p><b> Friend: </b> ' + r + ' </p> ' 
		new_chat.append(string)
		
	return new_chat	


def change_the_movie_data(): #need a change of name of  variables here
	global data
#DataFrame.set_value(index, col, value, takeable=False)
	for k in data.itertuples():
		j = k.Index
		#print(j)
		for i in range(1,6):
			s = data.loc[j,'Answer.switch_' +str(i)]
			if s[0] == '{':
				continue
			imdb_id = get_named_entity_movie(s)
			'''
			if imdb_id in movies:
				data.loc[j,'Input.wiki_' + str(i)] = 'https://en.wikipedia.org/?curid=' + str(movies[imdb_id].wiki_id)
				data.loc[j,'Input.movie_name_'+str(i)] = movies[imdb_id].title
				data.loc[j,'Input.plot_'+str(i)] = movies[imdb_id].plot
				data.loc[j,'Input.comment_'+str(i)] = ''
				data['Input.review_'+str(i)] = ''
				if imdb_id in reddit_singles:
					data.loc[j,'Input.comment_'+str(i)] = change_to_html(reddit_singles[imdb_id])
				if imdb_id in review_titles :
					data.loc[j,'Input.comment_'+str(i)] = data.loc[j,'Input.comment_'+str(i)] + change_to_html(review_titles[imdb_id])
			
				if imdb_id in reviews:
					data.loc[j,'Input.review_'+str(i)] = reviews[imdb_id][0]
					#print("Updated")
			
			if imdb_id in movies:
				data['Input.wiki_' + str(i)][j] = 'https://en.wikipedia.org/?curid=' + str(movies[imdb_id].wiki_id)
				data['Input.movie_name_'+str(i)][j] = movies[imdb_id].title
				data['Input.plot_'+str(i)][j] = movies[imdb_id].plot
				data['Input.comment_'+str(i)][j] = ''
				data['Input.review_'+str(i)][j] = ''
				if imdb_id in reddit_singles:
					data['Input.comment_'+str(i)][j] = change_to_html(reddit_singles[imdb_id])
				if imdb_id in review_titles :
					data['Input.comment_'+str(i)][j] = data['Input.comment_'+str(i)] + change_to_html(review_titles[imdb_id])
			
				
			'''	

			if imdb_id in movies:
				data.loc[j,'Input.wiki_' + str(i)] = 'https://en.wikipedia.org/?curid=' + str(movies[imdb_id].wiki_id)
				data.loc[j,'Input.movie_name_'+str(i)] = movies[imdb_id].title
				data.loc[j,'Input.plot_'+str(i)] = movies[imdb_id].plot
				data.loc[j,'Input.comment_'+str(i)] = ''
				#data['Input.review_'+str(i)] = ''
				if imdb_id in reddit_singles:
					data.loc[j,'Input.comment_'+str(i)] = change_to_html(reddit_singles[imdb_id])
				if imdb_id in review_titles :
					data.loc[j,'Input.comment_'+str(i)] = data.loc[j,'Input.comment_'+str(i)] + change_to_html(review_titles[imdb_id])
				if imdb_id in reviews:
					data['Input.review_'+str(i)][j] = convert_to_ascii(reviews[imdb_id][0])
					#print("Updated")
			


data = pd.read_csv(fname_input)
store_legends()
#Input.chat_1	Input.comment_1	Input.imdb_id_1	Input.legend_1	Input.movie_name_1	Input.plot_1	Input.review_1	Input.wiki_1
#print(data['Input.review_1'])
if switch_flag =='True':
	load_the_full_data()
	change_the_movie_data()
if "RequesterFeedback" in data:
	data = data[data.RequesterFeedback.isnull()] #Filtering rejected responses
if "AssignmentStatus" in data:
	data = data[data.AssignmentStatus!='Rejected']



worker_id = data['WorkerId']
chat_1 = data['Input.chat_1']
comment_1 = data['Input.comment_1']
imdb_id_1 = data['Input.imdb_id_1']
legend_1 = data['Input.legend_1']
movie_name_1 = data['Input.movie_name_1']
plot_1 = data['Input.plot_1']
review_1 = data['Input.review_1']
wiki_1 = data['Input.wiki_1']
response_1 = data['Answer.response_1']

chat_2 = data['Input.chat_2']
comment_2 = data['Input.comment_2']
imdb_id_2 = data['Input.imdb_id_2']
legend_2 = data['Input.legend_2']
movie_name_2 = data['Input.movie_name_2']
plot_2 = data['Input.plot_2']
review_2 = data['Input.review_2']
wiki_2 = data['Input.wiki_2']
response_2 = data['Answer.response_2']

chat_3 = data['Input.chat_3']
comment_3 = data['Input.comment_3']
imdb_id_3 = data['Input.imdb_id_3']
legend_3 = data['Input.legend_3']
movie_name_3 = data['Input.movie_name_3']
plot_3 = data['Input.plot_3']
review_3 = data['Input.review_3']
wiki_3 = data['Input.wiki_3']
response_3 = data['Answer.response_3']

chat_4 = data['Input.chat_4']
comment_4 = data['Input.comment_4']
imdb_id_4 = data['Input.imdb_id_4']
legend_4 = data['Input.legend_4']
movie_name_4 = data['Input.movie_name_4']
plot_4 = data['Input.plot_4']
review_4 = data['Input.review_4']
wiki_4 = data['Input.wiki_4']
response_4 = data['Answer.response_4']

chat_5 = data['Input.chat_5']
comment_5 = data['Input.comment_5']
imdb_id_5 = data['Input.imdb_id_5']
legend_5 = data['Input.legend_5']
movie_name_5 = data['Input.movie_name_5']
plot_5 = data['Input.plot_5']
review_5 = data['Input.review_5']
wiki_5 = data['Input.wiki_5']
response_5 = data['Answer.response_5']

chat_1 = augment_response(chat_1,response_1)
chat_2 = augment_response(chat_2,response_2)
chat_3 = augment_response(chat_3,response_3)
chat_4 = augment_response(chat_4,response_4)
chat_5 = augment_response(chat_5,response_5)


d = {'WorkerId': worker_id , 'chat_1' : chat_1 ,'comment_1' : comment_1 ,'imdb_id_1' : imdb_id_1 ,'legend_1' : legend_1 ,'movie_name_1' : movie_name_1 ,'plot_1' : plot_1 ,'review_1' : review_1 ,'wiki_1' : wiki_1 ,'chat_2' : chat_2 ,'comment_2' : comment_2 ,'imdb_id_2' : imdb_id_2 ,'legend_2' : legend_2 ,'movie_name_2' : movie_name_2 ,'plot_2' : plot_2 ,'review_2' : review_2 ,'wiki_2' : wiki_2 ,'chat_3' : chat_3 ,'comment_3' : comment_3 ,'imdb_id_3' : imdb_id_3 ,'legend_3' : legend_3 ,'movie_name_3' : movie_name_3 ,'plot_3' : plot_3 ,'review_3' : review_3 ,'wiki_3' : wiki_3 ,'chat_4' : chat_4 ,'comment_4' : comment_4 ,'imdb_id_4' : imdb_id_4 ,'legend_4' : legend_4 ,'movie_name_4' : movie_name_4 ,'plot_4' : plot_4 ,'review_4' : review_4 ,'wiki_4' : wiki_4 ,'chat_5' : chat_5 ,'comment_5' : comment_5 ,'imdb_id_5' : imdb_id_5 ,'legend_5' : legend_5 ,'movie_name_5' : movie_name_5 ,'plot_5' : plot_5 ,'review_5' : review_5 ,'wiki_5' : wiki_5 }

df = pd.DataFrame(d)
df.to_csv(fname_output,index = False,encoding = 'utf-8')
print('See your file')
