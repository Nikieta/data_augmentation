import pandas as pd

#only possible for the first lines !

def clean_data(data,accept_file_name,reject_file_name):
	movie_name = []
	wiki_link = []
	response = []
	accept = []
	reject = []
	d_movie = data['Input.movie_name']
	d_wiki = data['Input.wiki']
	d_response = data['Answer.response']
	s_movie = []
	s_wiki = []

	for m,w,r in zip(d_movie,d_wiki,d_response):
		flag = True
		if len(r.split()) < 5:
			flag = False

		if flag:
			accept.append('x')
			reject.append('')
			movie_name.append(m)
			wiki_link.append(w)
			response.append('<p> <b>Friend:</b> '+ r + '</p>')

		else:
			accept.append('')
			reject.append('Not as per the instructions')
			s_movie.append(m)
			s_wiki.append(w)

	d = {'movie_name':movie_name ,'wiki': wiki_link, 'chat': response }

	df = pd.DataFrame(d)

	df.to_csv(accept_file_name,index=False)

	d = {'movie_name':s_movie,'wiki': s_wiki }

	df = pd.DataFrame(d)

	df.to_csv(reject_file_name,index=False)

	d = {'Accept':accept,'Reject': reject }

	df = pd.DataFrame(d)

	df.to_csv("accept_reject_this_batch.csv",index=False)




data = pd.read_csv('Batch_2893477_batch_results.csv')
clean_data(data,'AMT_dump/batch_1_accept.csv','AMT_dump/batch_1_reload_1.csv')