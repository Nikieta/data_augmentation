import pandas as pd
import pickle 
from pickle import load
import gzip
import string
#detail reddit(get count) review plot review title (get count) remember opinion fav char fav scene
printable = set(string.printable)
reddit = []
review = []
review_titles_list = []
plot = []
title = []
remember = []
opinion = []
fav_char = []
fav_scene = []
critical_reviews = []
quora = []
data_id = pd.read_csv('1000_imdb_id.csv')
imdb_id = data_id['imdb_id']
print(len(imdb_id))
print(imdb_id[0])
final_imdb_id = []
print('Pre-reading')
movies,people,genres,characters = load(gzip.open('data/final_data.pklz'))
print('Complete')
reddit_singles = pickle.load(open('data/reddit_singles.pkl','rb'))
review_titles = pickle.load(open('data/review_titles.pkl' ,'rb' ))
reviews = pickle.load(open('data/reviews.pkl','rb'))
questions = pickle.load(open('data/movie_question_dict.pkl'))
print('Data Loading completed')

def check_if(a):
	if len(a) > 0:
		return 1
	return 0
def convert_to_ascii(statement):
	global printable
	return  filter(lambda x: x in printable, statement)

count = 0
for i in imdb_id:
	if i in movies:
		final_imdb_id.append(i)
		title.append(str(convert_to_ascii(movies[i].title)))
		if movies[i].plot == "":
			plot.append(0)
		else:
			plot.append(1)	
		remember.append(check_if(movies[i].do_you_remember))	
		opinion.append(check_if(movies[i].opinion))	
		fav_scene.append(check_if(movies[i].fav_scene))	
		fav_char.append(check_if(movies[i].fav_character))	
		critical_reviews.append(len(movies[i].critical_reviews))
		if i in reddit_singles:
			reddit.append(len(reddit_singles[i]))
		else:
			reddit.append(0)
		if i in review_titles :
			review_titles_list.append(1)
		else:
			review_titles_list.append(0)
		if i in reviews:
			review.append(1)
		else:
			review.append(0)
		if i in questions:
			quora.append(1)
		else:
			quora.append(0)

	else:
		pass

df = {'imdb_id': final_imdb_id, 'title':title, 'questions from quora':quora,'plot':plot, 'review': review,'reddit singles': reddit,'review titles':review_titles_list,'critical reviews':critical_reviews,'do you remember':remember,'opinion':opinion,'favourite character':fav_char,'favourite_scene':fav_scene}

for i in df:
	print(i)
	print(len(i))

movie_df = pd.DataFrame(df)
movie_df.to_csv('movie_data_stats.csv',index = False)