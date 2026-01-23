from flask import Flask, render_template, request
import requests
from waitress import serve
import os
from datetime import datetime, timezone
import csv

def read_data(cesta):
    f = open(cesta, 'r', encoding='utf-8', newline='')
    reader = csv.reader(f, delimiter = ';')
    data = []
    for row in reader:
        data.append(row)
    return data

def data_write(cesta, data):
    g = open(cesta, 'w', encoding='utf-8')
    for row in data:
        s = ''
        for cell in row:
            s+=f'{cell};'
        if s.endswith(';'): 
            s = s[:-1]
        s+='\n'
        g.write(s)
    g.close()

app = Flask(__name__)
@app.route('/')
def get_main_page():
    return render_template('index.html')

@app.route('/edit')
def get_edit_page():
    return render_template('edit.html')

@app.route('/getdata')
def get_data():
    data1 = read_data('./bezne.csv')
    data2 = read_data('./vector.csv')
    data = []
    for i in range(len(data1)):
        radek = data1[i] + data2[i]
        data.append(radek)
    f = open('./navic.txt', 'r', encoding='utf-8')
    lines = f.readlines()
    lines_text = '\n'.join(lines)
    f.close()
    return {'data': data, 'added': lines_text}

@app.route('/subbutclicked', methods = ['POST'])
def put_bezne():
    js = request.get_json()
    data = js['data']
    data_write('./vector.csv', data)
    return {}

@app.route('/obnovuj')
def obnov():
    data = read_data('./vectordef.csv')
    data_write('./vector.csv', data)
    g = open('./navic.txt', 'w', encoding='utf-8')
    g.close()
    return {}

@app.route('/submit', methods = ['POST'])
def zmen_oznameni():
    js = request.get_json()
    added = js['added']
    g = open('./navic.txt', 'w', encoding='utf-8')
    g.write(added)
    g.close()
    data2 = js['data']
    data = []
    for elem in data2:
        data.append([elem]) 
    data_write('./vector.csv', data)
    return {}

@app.route('/getall')
def get_all_data():
    top = ''
    data = read_data('./bezne.csv')
    vec = read_data('./vector.csv')
    for i in range(len(vec)):
        if vec[i] == ['1']:
            udalost = data[i]
            if len(udalost) > 3:
                top += f'{udalost[0]} v {udalost[1]}:{udalost[2]} - {udalost[3]} \n'


    f = open('./navic.txt', 'r', encoding='utf-8')
    lines = f.readlines()
    left = ''.join(lines)
    f.close()

    right = ''
    zadyl = read_data('./zadyl.csv')
    tsp_now = datetime.now(timezone.utc).timestamp()
    for line in zadyl:  
        if len(line) == 5:
            day, month, year = int(line[0]), int(line[1]), int(line[2])
            dt = datetime(year, month, day+1, tzinfo=timezone.utc)
            tsp = dt.timestamp()
            if tsp_now < tsp:
                right += f'{line[3]} - {line[4]} \n'

    return {'top': top, 'left': left, 'right': right}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    serve(app, host="0.0.0.0", port=port)