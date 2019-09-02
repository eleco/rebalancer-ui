from app import app
import redis
import json
import os
from flask import Flask, Markup, render_template

redis_url = os.getenv('REDISTOGO_URL')
redis = redis.from_url(redis_url)


@app.route('/')
@app.route('/index')
def index():
    

    encoding='utf-8'
    out = {}
    for key in redis.scan_iter('*'):
        out[key.decode(encoding)]=redis.get(key).decode(encoding)
    
    line_labels=list(out.keys())
    line_values=out.values()

    values_btc = []
    values_gbp = []
    values_total = []

    for line in line_values:
        j=json.loads(line)
        values_btc.append(j['rate']* j['qty_btc'])
        values_gbp.append(j['qty_gbp'])
        values_total.append(j['rate']* j['qty_btc']+j['qty_gbp'])


    return render_template('chart.html', labels=line_labels, values_btc=values_btc, values_gbp=values_gbp, values_total=values_total)
