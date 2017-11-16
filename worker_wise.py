import pandas as pd

workers =["A1CCPY0X91V3M3","A3UMDMF589FDPZ","A1ZOBEBY6RQT5W","A1E3136XMOCQ1W","A22S6XK123QWC1","A2SC6UVH1MJ9OE","A5WO8I5J92HHI","A23T8768HQHS0U","A1ZOBEBY6RQT5W","A199QE5OP988XH","ANKVD3FR8CCQ8","ACBF2MWKBONEZ","A364YMZIYPA6LC"]


data = pd.read_csv("/home/nikita/Downloads/Modified Chats 2 - Sheet1.csv")

for w in workers:
	chat = data[data['WorkerId']==w]
	chat.to_csv('batch_2/Worker_'+str(w) + '.csv',index = False)

