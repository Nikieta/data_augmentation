import pandas as pd
import sys
import numpy as np

fname = sys.argv[1]

def plot_update(plot):
	_plot = plot
	plot = str(plot).split('.')
	ten_len = len(plot)/11
	if ten_len > 0:
		r_plot = np.array_split(plot,ten_len)
	else:
		return str(_plot)
	s = ''
	np.random.shuffle(r_plot)
	for i in r_plot[0]:
		s = s + i + ". "
	print(len(s))

	return s

def plot_array(input_array):
	output_array = []
	for plot in input_array:
		output_array.append(plot_update(plot))
	return output_array

data = pd.read_csv(fname)

data['plot_1'] = plot_array(data['plot_1'])

data['plot_2'] = plot_array(data['plot_2'])
#data['plot_3'] = plot_array(data['plot_3'])
#data['plot_4'] = plot_array(data['plot_4'])
#data['plot_5'] = plot_array(data['plot_5'])

data.to_csv('updated_'+fname,index = False)
