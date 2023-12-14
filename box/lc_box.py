##import requests
##exec(requests.get('https://raw.githubusercontent.com/leo202103/public_area/main/box/lc_box.py').text)
'''
Name: lc_box.py
Path: https://github.com/leo202103/leo202103/new/main/box/
Date: 20230908,1009,1014,1015,1023,1209,1214
Desc: lc python tool-box
Test Script:
import sys
sys.path.append('D:\\temp')
import importlib, lc_box
importlib.reload(lc_box)                # Reload the module
'''
import numpy as np, pandas as pd, gc, datetime
import time,json,requests,urllib

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
    return pd.DataFrame(list(map(lambda r:r.split(v_dlm),v_cards.split('\n')[1:])),columns=v_cards.split('\n')[0].split(v_dlm))

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
		import urllib,time,ssl
		self.context = ssl.create_default_context()
		self.context.set_ciphers('DEFAULT@SECLEVEL=1')
		self.chunk_size=userparm.get('chunk_size',50000)                                       ## limit to 500000 rows for each chunk
		self.lib={'work':userparm.get('work','./work'), 'user':userparm.get('user','./user')}
		self.libname=lambda s: 'work' if len(s.split('.'))<2 else s.split('.')[0]
		self.dsname =lambda s: s if len(s.split('.'))<2 else s.split('.')[1]
		self.empty('work')
		print(self)
	def readme(self):
		print('''readme: lc_session().readme()
by: Leo CHAN
version: 20231209
test script:
import sys,requests
exec(requests.get('https://raw.githubusercontent.com/leo202103/public_area/main/box/lc_box.py').text)
sys.path.append('D:\\temp\\0806')
import importlib, lc_box
importlib.reload(lc_box)                # Reload the module
lc_box1 =lc_box.lc_session()
lc_box1.readme()
lc_box1.get_keys('user')
lc_box1.df_get(gs='sashelp.class')
lc_box1.df_get(csv='//app/data/sample_large_df.zip')
lc_box1.df_get(fwf='//app/data/sample.txt',colspecs=[(0,10),(10,15)],names=['A','B'])
lc_box1.df_get(sas='//app/data/airline.sas7bdat')
lc_box.sample_large_df(90000)
lc_box.google_geocode('1600 Amphitheatre Parkway, Mountain View, CA')['results'][0]['geometry']['location']
		''')
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
	def get_keys(self,libref):
		v_store =pd.HDFStore(self.lib[libref])
		v_keys =v_store.keys()
		v_store.close()
		return v_keys
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
	def empty(self,libref):                                           ## empty a library (store)
		import numpy as np, pandas as pd
		v_store=pd.HDFStore(self.lib[libref],'w')
		for k in v_store.keys(): v_store.remove(k)
		v_store.close()
		logmsg(f'Store {libref} is cleared')
	def close_all_stores(self):
		for x in filter(lambda x:isinstance(x,pd.HDFStore),gc.get_objects()): x.close()
		logmsg(f'close all HDFStore')
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
	def date_put(self,dt,tz='Asia/Hong_Kong'):
		##(20231004) put datetime.datetime to str in format of '%Y-%m-%d %H:%M:%S.%f%z'
		import datetime, pytz
		return datetime.datetime.strftime(dt.astimezone(pytz.timezone(tz)),'%Y-%m-%d %H:%M:%S.%f%z')
	def logmsg(self,p_msg):
		import datetime
		print(self.date_put(datetime.datetime.now())[:19],p_msg)
'''
s=lc_session()
s.readme()
'''
