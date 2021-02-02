import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import streamlit as st
import pandas_datareader.data as web
import datetime as dt
from datetime import date
from matplotlib import rcParams


start = dt.datetime(2020,1,1)
end = date.today()
tick = ""
df = pd.DataFrame()
st.title("Stock Analytics App")

def get_stock(tick):
	  global df
	  df = web.DataReader(tick,'yahoo',start,end)
	  return df

def plot_pct_change(df):
	df["% Change"] = df["Adj Close"].pct_change()
	df.dropna(axis=0, inplace=True)
	rcParams["figure.figsize"] = 15,7
	df.set_index("Date",inplace=True)
	df["% Change"].plot()
	plt.title(tick + " % Change", fontsize=25)
	plt.xlabel("Date", fontsize=20)
	plt.show()
	return st.pyplot()

def layout(df):
	df.reset_index(inplace=True)
	# 10 days moving average
	fig = px.line(x = df["Date"],y=df.loc[:,"MA for 10 days"], title=tick,
		labels={
		"x" :"Date",
		"y" :"Price"
		})
	fig['data'][0]['showlegend']=True
	fig['data'][0]['name']='MA for 10 days'

	# 20 days moving average
	fig.add_scatter(x=df['Date'], y=df['MA for 20 days'], mode='lines')
	fig['data'][1]['showlegend']=True
	fig['data'][1]['name']='MA for 20 days'

	# 30 days moving average
	fig.add_scatter(x=df['Date'], y=df['MA for 30 days'], mode='lines')
	fig['data'][2]['showlegend']=True
	fig['data'][2]['name']='MA for 30 days'

	#Close Price
	fig.add_scatter(x=df['Date'], y=df['Close'], mode='lines')
	fig['data'][2]['showlegend']=True
	fig['data'][2]['name']='Close Price'

	fig.update_layout(width=1500,height=600)


	st.plotly_chart(fig)
	st.write(df)
	plot_pct_change(df)



def moving_average(df):
	ma_day = [10, 20, 30]

	for ma in ma_day:
	        column_name = f"MA for {ma} days"
	        df[column_name] = df["Adj Close"].rolling(ma).mean()
	return layout(df)

def write(tick):
	data = get_stock(tick)
	return moving_average(data)

def app():
	global tick
	tick = st.text_input("Enter the tick!")
	button = st.button('Search')
	if tick:
		write(tick)
	
	elif button:
		write(tick)
	
app()





