# 
 
import streamlit as st
import time
import plotly.express as px
import pandas as pd
import altair as alt
import datetime
import os
import numpy as np
import gspread

from google.oauth2.service_account import Credentials
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe
import json
import gspread_dataframe as gd


st.title('マーマレード食味分析')

name = st.text_input('ニックネームを入力してください。 ※入力するとボタンが出ます')
sex = st.selectbox(
    '性別',
     (' ','女性', '男性'))
st.write('性別:', sex)
age = st.number_input('年齢を入力してください。',0,100,1)

option = st.selectbox(
    'マーマレードの種類',
     ('ブラッドオレンジ', 'グリーンレモン', 'レッドレモン'))
st.write('マーマレードの種類:', option)

st.sidebar.write("""
# 食味レーダーチャート作成
柑橘味分析レーダーチャートです。食味を指定してください。
""")

st.sidebar.write("""
## 好みを選択してください。
""")

like_mr = st.sidebar.slider('好み', 1, 10, 5)
st.write('好み:', like_mr)

st.sidebar.write("""
## 各食味の数値を選択してください。
""")

sweet = st.sidebar.slider('甘味', 1, 5, 3)
sannmi = st.sidebar.slider('酸味', 1, 5, 3)
nigami = st.sidebar.slider('苦み', 1, 5, 3)
huumi = st.sidebar.slider('風味', 1, 5, 3)
koku = st.sidebar.slider('コク', 1, 5, 3)

data = pd.DataFrame({
    "甘味":[sweet],
    "酸味":[sannmi],
    "苦み":[nigami],
    "風味":[huumi],
    "コク":[koku]
})

#st.write(data)

def radar_chart(): 
    df = pd.DataFrame(dict( 
    r=[sweet,
    sannmi,
    nigami,
    huumi,
    koku],
    theta=['甘味','酸味','苦み',
           '風味', 'コク']))
    fig = px.line_polar(df, r='r', theta='theta', line_close=True)
    placeholder.write(fig)

def csv_output():
    csv_data =pd.DataFrame(data=([name,sex,age,option,like_mr,sweet,sannmi,nigami,huumi,koku]))
    csv_data=csv_data.T

    csv_data.columns =(["名前","性別","年齢", "マーマレード種類", "好み", "甘味","酸味","苦み","風味","コク"])
    d_today = datetime.date.today ( )
    csv_name = name + str(d_today.year) + str(d_today.month) + str(d_today.day) + '.csv'

    # if not os.path.isfile(csv_name):
    #     csv_data.to_csv(csv_name,header=True,encoding='utf_8_sig',
    #                 columns=["名前","マーマレード種類", "好み", "甘味","酸味","苦み","風味","コク"],index=False)
    # else: # else it exists so append without writing the header
    #     csv_data.to_csv(csv_name, mode='a', header=False,encoding='utf_8_sig',index=False)
    scopes = [
                'https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive'
            ]
    SERVICE_ACCOUNT_FILE = 'kankitsu.json'

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        'kankitsu.json', 
        scopes=scopes
    )
    gs = gspread.authorize(credentials)

    SPREADSHEET_KEY ='1s8CEemxoE_HDe0Jhp7yZMwMh0-0xyOCXGAdRk1utf5o'
    worksheet = gs.open_by_key(SPREADSHEET_KEY).worksheet('kankitsu')

    workbook = gs.open_by_key(SPREADSHEET_KEY)
    worksheet = workbook.worksheet('kankitsu')
    # set_with_dataframe(workbook.worksheet('kankitsu'),csv_data,include_index=True,)
 
    ws = gs.open("kankitsu").worksheet("kankitsu")
    existing = pd.DataFrame(ws.get_all_records())
    # existing.drop([''],axis=1,inplace=True)
    updated = existing.append(csv_data)
    gd.set_with_dataframe(ws, updated)
    

# csv_data.to_csv(csv_name,header=True,encoding='utf_8_sig',
#                 columns=["名前","マーマレード種類", "好み", "甘味","酸味","苦み","風味","コク"],index=False)
placeholder = st.empty()
start_button = st.empty()

if name!="":
    if start_button.button('Start',key='start'):
        start_button.empty()
        if st.button('Stop',key='stop'):
            pass
        while True:
            radar_chart()
            csv_output()
                       
            break
