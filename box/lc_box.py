##import requests
##exec(requests.get('https://raw.githubusercontent.com/leo202103/public_area/main/box/lc_box.py').text)
'''
Name: lc_box.py
Path: https://github.com/leo202103/leo202103/new/main/box/
Date: 20230908,1009,1014,1015,1023,1209,1214, 20240128
Desc: lc python tool-box
Test Script:
import sys
sys.path.append('D:\\temp')
import importlib, lc_box
importlib.reload(lc_box)                # Reload the module
'''
import numpy as np, pandas as pd, gc, datetime
import time,json,requests,urllib
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def config():
	'''['gas']['url_load']: google apps script to load spreadsheet data by lc_public.gas(lc_developer01@gmail.com)
		['weather']['url_weather']: OpenWeather API with my key for current weather
		['weather']['url_forecast']: OpenWeather API with my key for forecast weather
	'''
	return {'gas':{'url_load':'https://script.google.com/macros/s/AKfycbwzSMDlB6faBhW7YBtOIYeZeJ-nLE220K3w7XtyEkHNmqyVO1ITnVitWI9TL1Okm-bEQA/exec'}
		, 'weather':{'url_weather':'https://api.openweathermap.org/data/2.5/weather?appid=71fba3326133817a09512ae9c379eeb1&units=metric'
		,'url_forecast':'https://api.openweathermap.org/data/2.5/forecast?appid=71fba3326133817a09512ae9c379eeb1&units=metric'
		}
	}
    
def getJSON2(p_json=None,url=config()['gas']['url_load']):
	if not p_json: print ('''Doc(20230908):
	input:
		json data, e.g. {'table':'t_sample0'}, {'json':json.dumps({'range':'t_sample0'})}
	output:
		json output generated by url
	test script: 
		lc_box.getJSON2({'table':'t_sample0'})
		lc_box.getJSON2({'q':'Hongkong'},lc_box.config()['weather']['url_weather'])
	''')
	if not p_json: return
	import requests, json
	response = requests.get(url,p_json)
	data = json.loads(response.text)
	return data

def getJSON(p_json=None,url=config()['gas']['url_load']):
    import requests, json
    response = requests.get(url,p_json)
    data = json.loads(response.text)
    return data

def postJSON(p_json=None,p_url=config()['gas']['url_load']):
    import requests, json
    response = requests.post(url=p_url,data=p_json)
    data = json.loads(response.text)
    return data
    ## e.g. postJSON(p_json={"json_insert":json.dumps({"range":"t_sample1","data":[{'value':{'C1':1}}]})})
    ## e.g. postJSON(p_json={"json_insert":json.dumps({"range":"t_sample1","rangeTruncate":1,"data":[{'value':{'C1':1}}]})})

def gs2df(p_json=None,v_url=config()['gas']['url_load'],v_note=False):                                 ## load google spreadsheet via gas to panda dataframe
	if not p_json: print ('''Doc(20230908):
	def gs2df(p_json,v_url=config0['gas']['url_load'],v_note=False) ## load google spreadsheet via gas to pandas dataframe
	input:
		json data, e.g. {'table':'t_sample0'}, {'json':json.dumps({'range':'t_sample0'})}
	output:
		pandas dataframe
	test script: 
		lc_box.gs2df({'table':'t_sample0'})
	''')
	if not p_json: return
	import pandas as pd
	v_json =getJSON2(p_json,v_url)
	v_df=pd.DataFrame(list(map(lambda r:list(map(lambda c:r[c]['value'],v_json['cols'])),v_json['rows'])))
	v_df.columns=v_json['cols']
	if v_note:
		v_df1=pd.DataFrame(list(map(lambda r:list(map(lambda c:r[c]['note'],v_json['cols'])),v_json['rows'])))
		v_df1.columns=list(map(lambda c:'note_'+c,v_json['cols']))
		return pd.concat([v_df,v_df1],axis=1)
	return v_df

def stockPriceAnalysis(code=None,var='Close',history='100d'):
	import yfinance as yf, pandas as pd, datetime, time, math
	from sklearn.linear_model import LinearRegression
	from sklearn.preprocessing import PolynomialFeatures
	from sklearn.metrics import mean_squared_error
	if not code: print ('''Doc(20230908):
	def stockPriceAnalysis(code=.., var='Close', history='100'd)
	e.g. stockPriceAnalysis(code='9988.HK')
	input:
	    code = 4-digirs HK stock code, e.g. '0005.HK','9988.HK'
	    history = period of yahoo history data loaded, e.g. '1d','20d','100d'
		var = data column for regression (division will be added to this var and take log values)
	output:
		dict{df:<pandas dataframe for yahoo finance stock data>
		, 'code': code, 'history':history, 'date_start':<first date>, 'date_end':<last date>
		, 'linear_reg':[model.intercept_[0],model.coef_[0][0],mse]
		, 'quadratic_reg':[model2.intercept_[0],model2.coef_[0][1],model2.coef_[0][2],mse2]
	note:
		mse is mean square of error term
		df columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits', 'code', 'seq', 'acc_div', 'Y', 'Y_pred', 'Y2_pred']
	test script:
		lc_box.stockPriceAnalysis(code='9988.HK')
		}
	''')
	if not code: return
	def acc_dividends(v_list):
		v_out,v_sum=[],0
		for v in v_list:
			v_sum+=v
			v_out.append(v_sum)
		return v_out
	## main process
	df0=yf.Ticker(code).history(history)
	df0['code']=code
	df0['seq']=range(len(df0))
	df0['acc_div']=acc_dividends(df0['Dividends'].values)
	df0['Y']=df0.apply(lambda r:math.log(r['Close']+r['acc_div']),axis=1)
	## linear regression
	X,Y=df0[['seq']],df0[['Y']]
	model = LinearRegression()
	model.fit(X,Y)
	## quadratic regression
	poly_features = PolynomialFeatures(degree=2)
	X2 = poly_features.fit_transform(X)
	model2 = LinearRegression()
	model2.fit(X2,Y)
	## prediction
	Y_pred = model.predict(X)
	mse = mean_squared_error(Y, Y_pred)
	X_new_poly = poly_features.transform(X)
	Y2_pred = model2.predict(X_new_poly)
	mse2 = mean_squared_error(Y, Y2_pred)
	df0['Y_pred']=Y_pred
	df0['Y2_pred']=Y2_pred
	## return
	## return {'df':df0, 'linear_reg':[model.intercept_,model.coef_[0],mse], 'quadratic_reg':[model2.intercept_,model2.coef_[1],model2.coef_[2],mse2]}
	return {'df':df0, 'code':code, 'history':history
	, 'date_start':df0.index.min().strftime('%s-%s-%s' % ('%Y','%m','%d'))
	, 'date_end':df0.index.max().strftime('%s-%s-%s' % ('%Y','%m','%d'))
	, 'linear_reg':[model.intercept_[0],model.coef_[0][0],mse], 'quadratic_reg':[model2.intercept_[0],model2.coef_[0][1],model2.coef_[0][2],mse2]}

def df_from_cards(v_cards,v_dlm=','):
    ##(20230929): create dataframe from multi-line string similiar to SAS cards
    import pandas as pd
    if not v_cards: return None
    return pd.DataFrame(list(map(lambda r:r.split(v_dlm),v_cards.strip().split('\n')[1:])),columns=v_cards.strip().split('\n')[0].split(v_dlm))

def google_geocode(v_addr):  
    ##(20230928) return google geocode (e.g. latitude, longitude) from address
    ## API key definded under developer01.lc@gmail.com of project lc2022-share
    return getJSON(url=f'https://maps.googleapis.com/maps/api/geocode/json?address={v_addr}&key=AIzaSyCxEaArQPHkF-N_NPraPfogdlutQIdYOGU')
    ##e.g. google_geocode('1600 Amphitheatre Parkway, Mountain View, CA')['results'][0]['geometry']['location'] return {'lat': 37.4223878, 'lng': -122.0841877}

def gs_put(p_json=None,p_url=config()['gas']['url_load']):
    ##(20230930)output to saswork.xls (developer01.lc@gmail.com)
    import json
    return postJSON(p_json={"gs_put":json.dumps(p_json)})
    ##e.g. lc_box.gs_put(p_json={"name":"data0X","cols":["X0","X1","X2"],"rows":[[74,0,91],[11,42,20]]})

def gs_df(srcname):
    ##(20231001)load google spreadsheet to pandas dataframe
    import pandas as pd, json
    gs_data=getJSON(p_json={"gs_get":json.dumps({"srcname":srcname})})
    return pd.DataFrame(list(map(lambda r:list(map(lambda c:r.get(c,''),gs_data['cols'])),gs_data['rows']['values'])),columns=gs_data['cols'])

def sample_large_df(nrows=10000,ncols=100):
    ## (20231003-8)create sample large data file
    import numpy as np, pandas as pd, random
    ##return pd.DataFrame(list(map(lambda c:list(map(lambda c:random.random(),range(ncols))),range(nrows))),columns=list(map(lambda c:"C"+str(c),range(ncols))))
    return pd.DataFrame(np.random.standard_normal((int(nrows),ncols)),columns=list(map(lambda c:'C'+str(c),range(ncols))))
    
def sample_benchmark(nrows=10000):
    ## (20231003)benchmark for client environment
    ##sample_benchmark()                      ## (20231003)Total = 0:00:24.985146 for nrows=10000 (acer i7), Total = 0:04:27.356350 for nrows=1000000
    import pandas as pd, datetime
    d0=datetime.datetime.now()
    print(datetime.datetime.now(),f' Start (nrows={nrows})')
    df1=sample_large_df(nrows=nrows)
    print(datetime.datetime.now(),' Create')
    df1.sort_values(list(map(lambda c:"C"+str(c),range(100))),inplace=True)
    print(datetime.datetime.now(),' Sort')
    df1.to_csv('//app/data/sample_large_df.zip',index=False)
    print(datetime.datetime.now(),' to CSV')
    df2=pd.read_csv('//app/data/sample_large_df.zip')
    print(datetime.datetime.now(),' read CSV')
    print(f'Total = {datetime.datetime.now()-d0} for nrows={nrows}')

def df_get(gs=None,csv=None,pickle=None,fwf=None,sas=None,sep=",",colspecs=[(1,10)], header=None, names=None):
    ##(20231003)load google spreadsheet or csv to pandas dataframe
    import pandas as pd, json
    if gs: 
        gs_data=getJSON(p_json={"gs_get":json.dumps({"srcname":gs})})
        return pd.DataFrame(list(map(lambda r:list(map(lambda c:r.get(c,''),gs_data['cols'])),gs_data['rows']['values'])),columns=gs_data['cols'])
    if csv: return pd.read_csv(csv,sep=sep)
    if pickle: return pd.read_pickle(pickle)
    if fwf: return pd.read_fwf(fwf,colspecs=colspecs, header=header, names=names)                    ## fix-column width file
    if sas: return pd.read_sas(sas)
    return "err: Neither parameter gs, csv, pickle, fwf or excel parameter not found"
    ## lc_box.df_get(gs='sashelp.class')
    ## lc_box.df_get(csv='//app/data/sample_large_df.zip')
    ## lc_box.df_get(fwf='//app/data/sample.txt',colspecs=[(0,10),(10,15)],names=['A','B'])
    ## lc_box.df_get(sas='//app/data/airline.sas7bdat')

def df_put(df, gs=None,csv=None,pickle=None,fwf=None,sep=",",colspecs=[(1,10)], header=None, names=None,index=False):
    ##(20231003)load pandas dataframe to google spreadsheet or csv
    import pandas as pd, json
    if gs: return gs_put(p_json={"name":gs,"cols":list(df.columns),"rows":df.values.tolist()})
    if csv: 
        df.to_csv(csv,sep=sep,index=index)
        return {'msg':f'output to csv {csv}'}
    if pickle:
        df.to_pickle(pickle)
        return {'msg':f'output to pickle {pickle}'}        
    if fwf: 
        df.to_fwf(fwf,colspecs=colspecs, header=header, names=names)                    ## fix-column width file
        return {'msg':f'output to fwf(fix-width file) {fwf}'}
    return "err: Neither parameter gs, csv, pickle or fwf parameter not found"
    ## lc_box.df_get(gs='sashelp.class').pipe(lc_box.df_put,csv='//app/data/sashelp_class.zip')
    ## lc_box.df_get(gs='sashelp.class').pipe(lc_box.df_put,gs='saswork.test3')

def date_put(dt,tz='Asia/Hong_Kong'):
    ##(20231004) put datetime.datetime to str in format of '%Y-%m-%d %H:%M:%S.%f%z'
    import datetime, pytz
    return datetime.datetime.strftime(dt.astimezone(pytz.timezone(tz)),'%Y-%m-%d %H:%M:%S.%f%z')

def date_get(dt_str,tz='+0800'):
    ##(20231004) get datetime.datetime from str in format of '%Y-%m-%d %H:%M:%S.%f%z'
    import datetime, pytz
    vformat='%Y-%m-%d %H:%M:%S.%f%z'
    if len(dt_str.split('+')[0])==8: vformat='%y-%m-%d%z'
    if len(dt_str.split('+')[0])==10: vformat='%Y-%m-%d%z'
    if len(dt_str.split('+')[0])==13: vformat='%Y-%m-%d %H%z'
    if len(dt_str.split('+')[0])==16: vformat='%Y-%m-%d %H:%M%z'
    if len(dt_str.split('+')[0])==19: vformat='%Y-%m-%d %H:%M:%S%z'
    if len(dt_str.split('+')[0])>19: vformat='%Y-%m-%d %H:%M:%S.%f%z'
    if len(dt_str.split('+'))<2: dt_str=dt_str+tz
    return datetime.datetime.strptime(dt_str,vformat)
    '''lc_box.date_get('2023-10-04 00:55:56.327675+0800'), lc_box.date_put(date_get('2023-10-04+0800'))\
    , lc_box.date_put(date_get('23-10-04+0800')), lc_box.date_put(date_get('2023-10-04 13+0800'))\
    , lc_box.date_put(date_get('2023-10-04 13:12+0800')), lc_box.date_put(date_get('2023-10-04 13:12:44.55+0800'))
    '''
def ods_put(df,file,titles=[]):
    ##(20231004) simulate SAS ODS output table to html
    v_title=''
    if len(titles)>0: v_title=f'<h1>{titles[0]}</h1>'
    v_html=f'''
    <html><body>
    
    {v_title}
    {df.to_html(index=False)}
    </body></html>
    '''
    f1=open(file,'w')
    f1.write(v_html)
    f1.close()
    return {'msg':f'ods output to file {file}'}
    ## ods_put(lc_box.df_get(gs='sashelp.class')[:5],'//app/data/class5.html')

def logmsg(p_msg):
    import datetime
    print(date_put(datetime.datetime.now())[:19],p_msg)

class lc_session():
	def __init__(self,userparm={}):
		import urllib,time,ssl,re
		self.context = ssl.create_default_context()
		self.context.set_ciphers('DEFAULT@SECLEVEL=1')
		self.chunk_size=userparm.get('chunk_size',50000)                                       ## limit to 500000 rows for each chunk
		self.lib={'work':userparm.get('work','./work'), 'user':userparm.get('user','./user')}
		self.libname=lambda s: 'work' if len(s.split('.'))<2 else s.split('.')[0]
		self.dsname =lambda s: s if len(s.split('.'))<2 else s.split('.')[1]
		self.regx=lambda r,s,pos=0: [[c.group(),pos+c.start(),pos+c.end()] for c in re.finditer(r,s[pos:],re.IGNORECASE)]
		self.empty('work')
		print(self)
	def date_put(self,dt,tz='Asia/Hong_Kong'):
		##(20231004) put datetime.datetime to str in format of '%Y-%m-%d %H:%M:%S.%f%z'
		import datetime, pytz
		return datetime.datetime.strftime(dt.astimezone(pytz.timezone(tz)),'%Y-%m-%d %H:%M:%S.%f%z')
	def logmsg(self,p_msg):
		import datetime
		print(self.date_put(datetime.datetime.now())[:19],p_msg)
	def get_keys(self,libref):
		v_store =pd.HDFStore(self.lib[libref])
		v_keys =v_store.keys()
		v_store.close()
		return v_keys
	def empty(self,libref):                                           ## empty a library (store)
		import numpy as np, pandas as pd
		v_store=pd.HDFStore(self.lib[libref],'w')
		for k in v_store.keys(): v_store.remove(k)
		v_store.close()
		logmsg(f'Store {libref} is cleared')
	def close_all_stores(self):
		for x in filter(lambda x:isinstance(x,pd.HDFStore),gc.get_objects()): x.close()
		logmsg(f'close all HDFStore')
	def select(self,df_name, where=None, start=None, stop=None, columns=None):
		v_store =pd.HDFStore(self.lib[self.libname(df_name)])
		v_df=v_store.select('/'+self.dsname(df_name), where, start, stop, columns)
		v_store.close()
		return v_df
	def df(self,df_name, where=None, start=None, stop=None, columns=None):
		return self.select(df_name, where=where, start=start, stop=stop, columns=columns)
	def get_df(self,df_name):
		v_store =pd.HDFStore(self.lib[self.libname(df_name)])
		v_df=v_store.get('/'+self.dsname(df_name))
		v_store.close()
		return v_df
	def print_df(self,df_name):
		v_store =pd.HDFStore(self.lib[self.libname(df_name)])
		v_df=v_store.get('/'+self.dsname(df_name))
		v_store.close()
		print(v_df)
		logmsg(f'NOTE: Printing of data {df_name} completes successfully.')
		return 0
	def put_df(self,df_name,p_df):
		##print(self.lib[self.libname(df_name)])
		v_store =pd.HDFStore(self.lib[self.libname(df_name)],'a')
		v_df=v_store.put(self.dsname(df_name),p_df)
		v_store.close()
		return p_df
	def sort(self,df_name,by=None,out=None):
		v_df=self.get_df(df_name)
		v_df=v_df.sort_values(by)
		## self.put_df(out if out else df_name,v_df.sort_values(by,ignore_index=True))
		self.put_df(out if out else df_name,v_df)
		logmsg(f'NOTE: Sorting data {df_name} by {by} completes successfully.')
		return 0
	def sample_csv(self,p_file='sample_file.csv',nobs=None):
		v_size,v_mode,v_header=nobs if nobs else self.chunk_size,'w',True
		while v_size>0:
			sample_large_df(min(v_size,self.chunk_size)).to_csv(p_file,index=False,mode=v_mode,header=v_header,chunksize=10000)
			v_size,v_mode,v_header=v_size-min(v_size,self.chunk_size),'a',False
			##print(f'{v_size} rows being process')
	def get_csv(self,p_file,df_name):
		v_store =pd.HDFStore(self.lib[self.libname(df_name)],'a')
		v_df =pd.read_csv(p_file)
		v_store.put(self.dsname(df_name), v_df)
		print(f'Get CSV from file={p_file} to df_name={df_name}')
		v_store.close()
		return v_df
	def xget_csv(self,p_file,df_name):                               ##read in chunk
		import numpy as np, pandas as pd
		v_store =pd.HDFStore(self.lib[self.libname(df_name)],'a')
		v_chunks =pd.read_csv(p_file,chunksize=self.chunk_size)
		v_df=[]
		for i,chunk in enumerate(v_chunks):
			name0=self.dsname(df_name)+'_chunk_'+str(i)
			v_store.put(name0, chunk, format='table')
			v_df.append(name0)
		v_store.put(self.dsname(df_name),pd.Series(v_df))
		v_store.close()
		return v_df
	def load_url(self,url):
		headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36'}
		return urllib.request.urlopen(urllib.request.Request(url, headers=headers), context=self.context).read()
	def gs_get(self,gs_name):
		import requests, json
		v_url='https://script.google.com/macros/s/AKfycbwzSMDlB6faBhW7YBtOIYeZeJ-nLE220K3w7XtyEkHNmqyVO1ITnVitWI9TL1Okm-bEQA/exec'
		response = requests.get(v_url,{"gs_get":json.dumps({"srcname":gs_name})})
		return json.loads(response.text)
	def df_get(self,gs=None,csv=None,pickle=None,fwf=None,sas=None,sep=",",colspecs=[(1,10)], header=None, names=None):
		##(20231003)load google spreadsheet or csv to pandas dataframe
		import pandas as pd, json
		if gs: 
			gs_data=self.gs_get(gs)
			return pd.DataFrame(list(map(lambda r:list(map(lambda c:r.get(c,''),gs_data['cols'])),gs_data['rows']['values'])),columns=gs_data['cols'])
		if csv: return pd.read_csv(csv,sep=sep)
		if pickle: return pd.read_pickle(pickle)
		if fwf: return pd.read_fwf(fwf,colspecs=colspecs, header=header, names=names)                    ## fix-column width file
		if sas: return pd.read_sas(sas)
		return "err: Neither parameter gs, csv, pickle, fwf or excel parameter not found"
		## lc_box.df_get(gs='sashelp.class')
		## lc_box.df_get(csv='//app/data/sample_large_df.zip')
		## lc_box.df_get(fwf='//app/data/sample.txt',colspecs=[(0,10),(10,15)],names=['A','B'])
		## lc_box.df_get(sas='//app/data/airline.sas7bdat')
	def spotify(self):
		import spotipy
		from spotipy.oauth2 import SpotifyOAuth
		CLIENT_ID = 'a7aa531b72d64e1999dcbf3e87ff78da'
		CLIENT_SECRET = input('CLIENT_SECRET:')  ### 
		scopes = ["user-follow-read", 'ugc-image-upload', 'user-read-playback-state',
		          'user-modify-playback-state', 'user-read-currently-playing', 'user-read-private',
		          'user-read-email', 'user-follow-modify', 'user-follow-read', 'user-library-modify',
		          'user-library-read', 'streaming', 'app-remote-control', 'user-read-playback-position',
		          'user-top-read', 'user-read-recently-played', 'playlist-modify-private', 'playlist-read-collaborative',
		          'playlist-read-private', 'playlist-modify-public']
		return spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
		                                               client_secret=CLIENT_SECRET,
		                                               redirect_uri='http://localhost:8887/callback',
		                                               scope=scopes, open_browser=False))
	def data(self,df_name=None,cards=None,v_dlm=','):
		##(20240124): load data from cards and save to store
		import pandas as pd
		if not cards: return None
		df0 =pd.DataFrame(list(map(lambda r:r.split(v_dlm),cards.strip().split('\n')[1:])),columns=cards.strip().split('\n')[0].split(v_dlm))
		if df_name: return self.put_df(df_name,df0)
		return df0
	def ods_put(self,df_name,file,titles=[]):
		##(20231004) simulate SAS ODS output table to html
		v_title=''
		if len(titles)>0: v_title=f'<h1>{titles[0]}</h1>'
		df0 =self.df(df_name)
		v_html=f'''
		<html><body>
		
		{v_title}
		{df0.to_html(index=False)}
		</body></html>
		'''
		f1=open(file,'w')
		f1.write(v_html)
		f1.close()
		return {'msg':f'ods output to file {file}'}
		## ods_put(lc_box.df_get(gs='sashelp.class')[:5],'//app/data/class5.html')
	def date_put(self,dt,tz='Asia/Hong_Kong'):
		##(20231004) put datetime.datetime to str in format of '%Y-%m-%d %H:%M:%S.%f%z'
		import datetime, pytz
		return datetime.datetime.strftime(dt.astimezone(pytz.timezone(tz)),'%Y-%m-%d %H:%M:%S.%f%z')

	def date_get(self,dt_str,tz='+0800'):
		##(20231004) get datetime.datetime from str in format of '%Y-%m-%d %H:%M:%S.%f%z'
		import datetime, pytz
		vformat='%Y-%m-%d %H:%M:%S.%f%z'
		if len(dt_str.split('+')[0])==8: vformat='%y-%m-%d%z'
		if len(dt_str.split('+')[0])==10: vformat='%Y-%m-%d%z'
		if len(dt_str.split('+')[0])==13: vformat='%Y-%m-%d %H%z'
		if len(dt_str.split('+')[0])==16: vformat='%Y-%m-%d %H:%M%z'
		if len(dt_str.split('+')[0])==19: vformat='%Y-%m-%d %H:%M:%S%z'
		if len(dt_str.split('+')[0])>19: vformat='%Y-%m-%d %H:%M:%S.%f%z'
		if len(dt_str.split('+'))<2: dt_str=dt_str+tz
		return datetime.datetime.strptime(dt_str,vformat)
		'''lc_box.date_get('2023-10-04 00:55:56.327675+0800'), lc_box.date_put(date_get('2023-10-04+0800'))\
		, lc_box.date_put(date_get('23-10-04+0800')), lc_box.date_put(date_get('2023-10-04 13+0800'))\
		, lc_box.date_put(date_get('2023-10-04 13:12+0800')), lc_box.date_put(date_get('2023-10-04 13:12:44.55+0800'))
		'''
	def getJSON(self,p_json=None,url=config()['gas']['url_load']):
		import requests, json
		response = requests.get(url,p_json)
		data = json.loads(response.text)
		return data
	def google_geocode(self,v_addr):  
		##(20230928) return google geocode (e.g. latitude, longitude) from address
		## API key definded under developer01.lc@gmail.com of project lc2022-share
		return self.getJSON(url=f'https://maps.googleapis.com/maps/api/geocode/json?address={v_addr}&key=AIzaSyCxEaArQPHkF-N_NPraPfogdlutQIdYOGU')
		##e.g. google_geocode('1600 Amphitheatre Parkway, Mountain View, CA')['results'][0]['geometry']['location'] return {'lat': 37.4223878, 'lng': -122.0841877}
	def sample_large_df(self,nrows=10000,ncols=100):
		## (20231003-8)create sample large data file
		import numpy as np, pandas as pd, random
		##return pd.DataFrame(list(map(lambda c:list(map(lambda c:random.random(),range(ncols))),range(nrows))),columns=list(map(lambda c:"C"+str(c),range(ncols))))
		return pd.DataFrame(np.random.standard_normal((int(nrows),ncols)),columns=list(map(lambda c:'C'+str(c),range(ncols))))
	def regx_sql3(self,sqlcode):
		## (20240128)sql parser using regular expression
		import re
		sql_keywords=['create table', 'as select', 'select','from','left join','inner join','right join','where','order by', 'group by', 'having']
		re_key =lambda k: r"\s*\b"+k.strip().replace(" ",r"\s+")+r"\s+"
		pos, pos_to, out=0, 0, []
		for k in sql_keywords:
			m=re.search(re_key(k), sqlcode[pos:], re.IGNORECASE)
			if m:
				if len(out)>0: out[-1][-1]=sqlcode[p_to:pos+m.start()]
				pos, p_to =pos+m.start(), pos+m.end()
				out.append([k,pos,p_to,m.group(),sqlcode[p_to:]])
		return {'sql_code':sqlcode, 'sql_tokens':out}
		''' unit-test
		s.regx_sql3("  Select\nname,age  from sashelp.class   WHERE SEX='F' order  By age")
		{'sql_code': "  Select\nname,age  from sashelp.class   WHERE SEX='F' order  By age",
		 'sql_tokens': [['select', 0, 9, '  Select\n', 'name,age'],
		  ['from', 17, 24, '  from ', 'sashelp.class'],
		  ['where', 37, 46, '   WHERE ', "SEX='F'"],
		  ['order by', 53, 64, ' order  By ', 'age']]}
		'''
	def regx_sql2(self,sqlcode):
		## (20240127)sql parser using regular expression
		import re
		sql_keywords=['create table', 'as select', 'select','from','left join','inner join','right join','where','order by', 'group by', 'having']
		sqlcode ="  Select name,age  from sashelp.class   WHERE SEX='F' order  By age"
		re_sql=r'\b'+r'\b|\b'.join(map(lambda c:c.replace(' ',r'\s+'),sql_keywords))+r'\b'
		sql_tokens =[{'sql':c.group().upper().replace(' ','').strip(),'start':c.start(),'end':c.end()} for c in re.finditer(re_sql,sqlcode,re.IGNORECASE)]
		for c in enumerate(sql_tokens):
			c[1]['next']=sql_tokens[c[0]+1]['start'] if c[0]+1<len(sql_tokens) else len(sqlcode)
			c[1]['tokens'] =[x.strip() for x in sqlcode[c[1]['end']:c[1]['next']].split(',')]
		return {'sql_code':sqlcode, 'sql_tokens':sql_tokens}
		''' unit-test
		s.regx_sql2("  Select\nname,age  from sashelp.class   WHERE SEX='F' order  By age")
		{'sql_code': "  Select name,age  from sashelp.class   WHERE SEX='F' order  By age",
		 'sql_tokens': [{'sql': 'SELECT',
		   'start': 2,
		   'end': 8,
		   'next': 19,
		   'tokens': ['name', 'age']},
		  {'sql': 'FROM',
		   'start': 19,
		   'end': 23,
		   'next': 40,
		   'tokens': ['sashelp.class']},
		  {'sql': 'WHERE', 'start': 40, 'end': 45, 'next': 54, 'tokens': ["SEX='F'"]},
		  {'sql': 'ORDERBY', 'start': 54, 'end': 63, 'next': 67, 'tokens': ['age']}]}
		'''
	def regx_sql(self,sqlcode):
		## (20240127)sql parser using regular expression
		import re
		sql_keywords=['create table', 'as select', 'select','from','left join','inner join','right join','where','order by', 'group by', 'having']
		regx=lambda r,s,pos=0: [[c.group(),pos+c.start(),pos+c.end()] for c in re.finditer(r,s[pos:],re.IGNORECASE)]
		re_key =lambda k: r"\s*\b"+k.strip().replace(" ",r"\s+")+r"\s+"
		sql_parser, pos =[], 0
		for k in sql_keywords:
			regx0 = regx(re_key(k), sqlcode,pos)
			regx1 =[k]
			if len(regx0)>0:
				regx1.extend(regx0[0])
				sql_parser[-1].append(regx1[2]) if len(sql_parser)>0 else None
				sql_parser.append(regx1)
		return sql_parser
		''' unit-test
		s.regx_sql("  Select\nname,age  from sashelp.class   WHERE SEX='F' order  By age")
		[['select', '  Select\n', 0, 9, 17],
		 ['from', '  from ', 17, 24, 37],
		 ['where', '   WHERE ', 37, 46, 53],
		 ['order by', ' order  By ', 53, 64]]
		'''
	def regx_brackets(self,s,debug=False):
		import re
		regx=lambda r,s,pos=0: [[c.start(),c.end(),c.group()] for c in re.finditer(r,s[pos:],re.IGNORECASE)]
		re_quote   =r'"[^"]*"'+'|'+r"'[^']*'"
		re_bracket =r'\(([^\(\)x"]*?)+\)'.replace('x',"'")
		s0 =list(s)
		out ={'src':s, 'quote':regx(re_quote,s), 'bracket':[]}                         ## locate the quote ('..', "..")
		for c in regx(re_quote,s):
			for i in range(c[0],c[1]): s0[i]=' '
		while (len(regx(re_bracket,''.join(s0)))>0):                                   ## locate brackets ((..)..(..))
			out['bracket'].append(regx(re_bracket,''.join(s0)))
			for c in regx(re_bracket,''.join(s0)):
				for i in range(c[0],c[1]): s0[i]=' '
		chk1 =regx(r'[\(\)]',''.join(s0))
		chk2 =regx(r'["\']',''.join(s0))
		out['rc']=[1,f'ERR: unmatch bracket at {chk1[0]}'] if len(chk1)>0 \
		else [2,f'ERR: unmatch quote at {chk2[0]}'] if len(chk2)>0 \
		else [0, 'MSG: success']
		if debug:
			print(s)
			print(''.join(s0))
			print(out)
			print(''.join(s0))
		return out
		''' unit-test
		>>> s=lc_box.lc_session()
		>>> s.regx_brackets('test "hello" world. it "s good." so ...(((A))+("B"))=("C")...')
		{'src': 'test "hello" world. it "s good." so ...(((A))+("B"))=("C")...',
		 'quote': [[5, 12, '"hello"'],
		  [23, 32, '"s good."'],
		  [47, 50, '"B"'],
		  [54, 57, '"C"']],
		 'bracket': [[[41, 44, '(A)'], [46, 51, '(   )'], [53, 58, '(   )']],
		  [[40, 45, '(   )']],
		  [[39, 52, '(     +     )']]],
		 'rc': [0, 'MSG: success']}
		'''
	def readme(self):
		print('''readme: lc_session().readme()
by: Leo CHAN
version: 20231209-20240127
test script:
import sys,requests
exec(requests.get('https://raw.githubusercontent.com/leo202103/public_area/main/box/lc_box.py').text)
s =lc_session()
sys.path.append('D:\\temp')
import importlib, lc_box
importlib.reload(lc_box)                # Reload the module
s =lc_box.lc_session()
s.readme()
s.get_keys('user')
s.df_get(gs='sashelp.class')
s.df_get(csv='//app/data/sample_large_df.zip')
s.df_get(fwf='//app/data/sample.txt',colspecs=[(0,10),(10,15)],names=['A','B'])
s.df_get(sas='//app/data/airline.sas7bdat')
s.print_df('user.df_test')
s.sort('user.df_test',by=['C2','C3'])
s.select('user.df_test',start=n-6)
s.df('user.df_test',start=n-6)
s.spotify().search(q='I\'m Tied, To You', type='album')
s.data('test',cards='A,B\n1,2\n3,4')
s.ods_put('user.class')
s.date_get('2023-10-04 00:55:56.327675+0800')
s.date_put(datetime.datetime.now())
s.google_geocode('1600 Amphitheatre Parkway, Mountain View, CA')['results'][0]['geometry']['location']
s.sample_large_df(90000)
s.regx_brackets('locating brackets and quotes like "hello".. \'world\' or X+((A+B)*C/(Y+Z)).',debug=True)
s.regx_sql("  Select\nname,age  from sashelp.class   WHERE SEX='F' order  By age")
s.regx_sql2("  Select\nname,age  from sashelp.class   WHERE SEX='F' order  By age")
s.regx_sql3("  Select\nname,age  from sashelp.class   WHERE SEX='F' order  By age")
s.regx(r'\w+ \w+','Hello World')
lc_box.sample_large_df(90000)
lc_box.google_geocode('1600 Amphitheatre Parkway, Mountain View, CA')['results'][0]['geometry']['location']
		''')

'''
s=lc_session()
s.readme()
'''
