from flask import Flask, render_template, request
import requests
from waitress import serve
import os
import random
import csv
import hashlib

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

@app.route('/getbezne')
def get_bezne():
    data1 = read_data('./bezne.csv')
    data2 = read_data('./vector.csv')
    print(data1)
    print(data2)
    data = []
    for i in range(len(data1)):
        radek = []
        for j in range(len(data1[i])):
            radek.append(data1[i][j])
        for k in range(len(data2[i])):
            radek.append(data2[i][k])
        data.append(radek)
    return {'data': data}

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
    return {}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    serve(app, host="0.0.0.0", port=port)