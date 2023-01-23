import streamlit as st

st.title('サプーアプリ')
st.caption('あああこれはサプーの動画用のテストアプリです')
st.subheader('自己紹介')
st.text('Pythonに関する情報')

code = '''
import streamlit as st

st.title('サプーアプリ')
'''
st.code(code, language='python')

#テキストボックス
name = st.text_input('名前')
print(name)

#ボタン
submit_btn = st.button('送信')
cancel_btn = st.button('キャンセル')

print(f'submit_btn:{submit_btn}')
print(f'cancel_btn:{cancel_btn}')
