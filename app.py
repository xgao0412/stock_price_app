import os
from flask import Flask, render_template, request, redirect

from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8

import datetime as dt
import pandas as pd
import numpy as np



app = Flask(__name__)

@app.route('/index',methods=['GET','POST'])
def index_lulu():
	if request.method == 'GET':
		return render_template('userinfo_lulu.html')
	else:
		n1 = request.form['name_lulu']

		api_url = 'https://www.quandl.com/api/v3/datasets/WIKI/%s.csv' % n1
		df = pd.read_csv(api_url, nrows=100)
		aapl_dates = np.array(df['Date'], dtype=np.datetime64)


		# create a new plot with a a datetime axis type
		p = figure(width=600, height=500, x_axis_type="datetime")

		if request.form.get('close_price'):
			aapl = np.array(df['Close'])
			p.line(aapl_dates, aapl, color='darkgrey',legend='close')

		if request.form.get('high_price'):
			aapl = np.array(df['High'])
			p.line(aapl_dates, aapl, color='red',legend='high')

		if request.form.get('open_price'):
			aapl = np.array(df['Open'])
			p.line(aapl_dates, aapl, color='blue',legend='open')

		if request.form.get('low_price'):
			aapl = np.array(df['Low'])
			p.line(aapl_dates, aapl, color='green',legend='low')




		# NEW: customize by setting attributes
		p.title.text = n1
		p.legend.location = "top_left"
		p.grid.grid_line_alpha = 0
		p.xaxis.axis_label = 'Date'
		p.yaxis.axis_label = 'Price'
		p.ygrid.band_fill_color = "olive"
		p.ygrid.band_fill_alpha = 0.1

	    # grab the static resources
		js_resources = INLINE.render_js()
		css_resources = INLINE.render_css()

	    # render template
		script, div = components(p)
		html = render_template(
		    'chart.html',
	        plot_script=script,
	        plot_div=div,
	        js_resources=js_resources,
	        css_resources=css_resources,
	    )
		return encode_utf8(html)


if __name__ == '__main__':
	port = int(os.environ.get('PORT',5000))	
	app.run(host='0.0.0.0',port=port)



