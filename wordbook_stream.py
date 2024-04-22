import streamlit as st
import pandas as pd
import random

# Excelファイルから単語リストを読み込む関数
def load_vocabularies(url):
    df = pd.read_excel(url, header=None, usecols="A:B")
    return list(df.itertuples(index=False, name=None))

# 単語リストの読み込み
vocabularies = {
    'basic': load_vocabularies('https://try20240422.github.io/basic.xlsx'),
    'standard': load_vocabularies('https://try20240422.github.io/standard.xlsx'),
    'advanced': load_vocabularies('https://try20240422.github.io/advanced.xlsx')
}

# セッションステートの初期化
if 'words' not in st.session_state:
    st.session_state.words = []
if 'current_word' not in st.session_state:
    st.session_state.current_word = None
if 'current_meaning' not in st.session_state:
    st.session_state.current_meaning = None
if 'level' not in st.session_state:
    st.session_state.level = 'basic'

def init_words():
    # レベルに応じて単語リストを初期化
    st.session_state.words = vocabularies[st.session_state.level][:]
    get_next_word()

def get_next_word():
    # 次の単語を取得する処理
    if st.session_state.words:
        st.session_state.current_word, st.session_state.current_meaning = random.choice(st.session_state.words)
    else:
        st.session_state.current_word = "All words learned!"
        st.session_state.current_meaning = ""

# Streamlit アプリのレイアウト設定
st.title("Vocabulary Game")

# レベル選択
level = st.selectbox("Choose your level", ('basic', 'standard', 'advanced'), index=('basic', 'standard', 'advanced').index(st.session_state.level))
if level != st.session_state.level:
    st.session_state.level = level
    init_words()

# 単語と意味を表示する部分
if st.button("Next Word"):
    get_next_word()

# 単語と意味を表示
if st.session_state.current_word:
    st.header(f"Word: {st.session_state.current_word}")
    if st.button("Show Meaning"):
        st.write(f"Meaning: {st.session_state.current_meaning}")

# 単語を覚えた場合の処理
if st.button("Mark as Learned") and st.session_state.words:
    st.session_state.words.remove((st.session_state.current_word, st.session_state.current_meaning))
    get_next_word()

# 残りの単語数を表示
st.write(f"Remaining Words: {len(st.session_state.words)}")
