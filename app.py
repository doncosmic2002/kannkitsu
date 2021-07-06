# 
import streamlit as st
import time

import pandas as pd
import altair as alt
import streamlit as st
import datetime
import os
import numpy as np

st.title('マーマレード食味分析')

name = st.text_input('ニックネームを入力してください。 ※入力するとボタンが出ます')

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
    csv_data =pd.DataFrame(data=([name,option,like_mr,sweet,sannmi,nigami,huumi,koku]))
    csv_data=csv_data.T

    csv_data.columns =(["名前", "マーマレード種類", "好み", "甘味","酸味","苦み","風味","コク"])
    d_today = datetime.date.today ( )
    csv_name = name + str(d_today.year) + str(d_today.month) + str(d_today.day) + '.csv'

    if not os.path.isfile(csv_name):
        csv_data.to_csv(csv_name,header=True,encoding='utf_8_sig',
                    columns=["名前","マーマレード種類", "好み", "甘味","酸味","苦み","風味","コク"],index=False)
    else: # else it exists so append without writing the header
        csv_data.to_csv(csv_name, mode='a', header=False,encoding='utf_8_sig',index=False)

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

