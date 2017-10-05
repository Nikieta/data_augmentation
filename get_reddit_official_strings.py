from __future__ import print_function
import json
from StringIO import StringIO
import pandas as pd
from copy import deepcopy
import itertools
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


f = open('discussionarchive.json','r')
j_f = json.load(f)
all_titles = []
for i in j_f['data']['children'][1:]:
	temp = []
	movie_title = i['data']['title']
	movie_title = re.sub('Official Discussion: ','',movie_title)
	movie_title = re.sub(' \[SPOILERS\]','',movie_title)
	movie_title = re.sub('Official Discussion - ','',movie_title)
	print(movie_title)
	url = i['data']['url']
	temp.append(movie_title)
	temp.append(url)
	all_titles.append(temp)
print(j_f['data']['children'])
#print(all_titles)