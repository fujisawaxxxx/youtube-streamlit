import streamlit as st
import pandas as pd
import pandas.io.sql as psql
import sqlite3
import hashlib
import webbrowser

conn = sqlite3.connect('database.db')
c = conn.cursor()



def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False

def create_user():
	# カラムの追加
	# c.execute('ALTER TABLE userstable ADD hinmei text')
	# c.execute('ALTER TABLE userstable ADD suryo  text')
	# c.execute('ALTER TABLE userstable ADD yu_no  text')
	# c.execute('ALTER TABLE userstable ADD ad  text')
	# c.execute('ALTER TABLE userstable ADD ad2  text')
	# c.execute('ALTER TABLE userstable ADD ad3  text')
	# c.execute('ALTER TABLE userstable ADD atena  text')
	# c.execute('ALTER TABLE userstable ADD tel  text')
	# c.execute('ALTER TABLE userstable DROP ad2  text')
	# c.execute('ALTER TABLE userstable DROP ad3  text')
	# c.execute('ALTER TABLE userstable ADD omosa  text')
	# c.execute('ALTER TABLE userstable ADD other  text')
	# c.execute('ALTER TABLE userstable ADD other2  text')
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT,hinmei TEXT,suryo TEXT,yu_no TEXT,ad TEXT,atena TEXT,tel TEXT,omosa text,other text)')

#アカウント作成
def add_user(username,password,hinmei,suryo,yu_no,ad,atena,tel,omosa,other):
	c.execute('INSERT INTO userstable(username,password,hinmei,suryo,yu_no,ad,atena,tel,omosa,other) VALUES (?,?,?,?,?,?,?,?,?,?)',(username,password,hinmei,suryo,yu_no,ad,atena,tel,omosa,other))
	conn.commit()

#ログイン
def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data

#ユーザー名と品名が重複していないか確認
def add_check(new_user,new_hinmei):
	c.execute('SELECT count(*) FROM userstable WHERE username = ? AND hinmei = ? ', (new_user,new_hinmei))
	data = c.fetchone()[0]
	return data

#アカウントの上書き
def add_Update(username,hinmei,suryo):
    c.execute('UPDATE userstable SET suryo = ? WHERE username=? AND hinmei = ?', (suryo, username, hinmei))
    conn.commit()
    st.success("データを更新しました")


def kanri():
	st.header("管理者メニュー")
	st.subheader("新規アカウント作成")
	
	new_user = st.text_input("ユーザー名")
	new_password = st.text_input("パスワード",type='password')

	new_hinmei = st.text_input("品名")
	new_suryo = st.text_input("数量")
	new_yu_no = st.text_input("郵便")
	
	new_ad = st.text_input("住所")
	new_atena = st.text_input("宛名")
	new_tel = st.text_input("電話")
	new_omosa = st.text_input("１冊の重さ")
	new_other = st.text_input("備考")

	#初期化（何もなければ0を入れる）
	if 'key' not in st.session_state:
		st.session_state['key'] = '0'
		print('keyの初期化')

	

	if st.button("アカウント作成"):

		#ユーザー名と品名が重複していないか確認
		result = add_check(new_user,new_hinmei)
		if result == 0:
			print('ゼロ件なのでアカウントの作成')

			create_user()
			add_user(new_user, new_password,new_hinmei,new_suryo,new_yu_no,new_ad,new_atena,new_tel,new_omosa,new_other)
			st.success("アカウントの作成に成功しました")
		else:
			print("ゼロ件ではないです")
			st.info("ユーザー名は既にアカウント登録されています。数量を上書きしますか")
	

			#更新保存
			st.session_state['key'] = '1'
			print("keyに1")

	#アカウント作成のボタンが押されたら「はい」「いいえ」を表示	
	if st.session_state['key'] == '1':
		if st.button("はい"):
			st.success("更新しました。")
			print("更新しました。")

			#更新保存(初期化)
			st.session_state['key'] = '0'
			
			#以下に更新作業を記載↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
			add_Update(new_user,new_hinmei,new_suryo)

		if st.button("いいえ"):
			st.warning("キャンセルしました。")
			print("キャンセルしました。")

			#更新保存(初期化)
			st.session_state['key'] = '0'

	#全件表示
	st.subheader("データベース全件")

	#ユーザーのDBを表示
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	df = pd.DataFrame(data)
	df.columns = ['ユーザー名', 'パスワード','品名','数量', '郵便番号','住所１','氏名', '電話番号','1冊の重さ','備考']
	st.dataframe(df.style.set_properties(**{'text-align': 'left', 'width': '100px'}))


	#全件削除
	st.subheader("データ全件削除します。")
	if st.button("削除"):
		sql = 'DELETE FROM userstable'
		c.execute(sql)

		# コミット
		conn.commit()

		# データ（レコード）取得
		sql = 'select * from userstable'
		for row in c.execute(sql):
			print(row)

		# クローズ
		conn.close()

def open_google():
    webbrowser.open("https://www.google.com/")
	
def success_login(username):
	#ユーザーのDBを表示
	c.execute('SELECT * FROM userstable WHERE username =?', (username,))
	data = c.fetchall()
	df = pd.DataFrame(data)
	df.columns = ['ユーザー名', 'パスワード','品名','数量', '郵便番号','住所１','氏名', '電話番号','1冊の重さ','備考']
	st.dataframe(df.style.set_properties(**{'text-align': 'left', 'width': '100px'}))
	#st.markdown(df.to_html(), unsafe_allow_html=True)
	
	
	c.execute('SELECT hinmei FROM userstable WHERE username =?', (username,))
	item_names = [item[0] for item in c.fetchall()]
	# Streamlitでプルダウンを追加する
	selected_item_name = st.selectbox('発送する品名を選択してください', item_names)

	st.info("発送先情報を入力してください")
	
	ha_yu_no = st.text_input("郵便")
	ha_ad = st.text_input("住所")
	ha_atena = st.text_input("宛名")
	ha_tel = st.text_input("電話")
	ha_suryo = st.text_input("数量")

	st.button("Open Google", open_google)

def main():

	#初期化（何もなければ0を入れる）
	if 'key2' not in st.session_state:
		st.session_state['key2'] = '0'
		print('key2の初期化')
	
	st.title("在庫管理")

	menu = ["ログイン"]
	choice = st.sidebar.selectbox("",menu)

	if choice == "ログイン":
		print("ログイン")
		

		username = st.sidebar.text_input("ユーザー名を入力してください")
		password = st.sidebar.text_input("パスワードを入力してください",type='password')

		if username =="a" and  password=="a":
			print("管理者メニューに飛ぶ★初期状態")
			kanri()
		else:
			print("管理者メニューじゃない★初期状態")
			
			#ログインボタンが押されたまたはkey2が保持されているとき
			if st.sidebar.button("ログイン") or st.session_state['key2'] == '1':
				#更新保存
				st.session_state['key2'] = '1'
				print("key2に1")

				print("ユーザーログインしようとする★ログイン後")
				create_user()

				result = login_user(username,password)
				if st.session_state['key2'] == '1':
					if result:
						print(username)
						st.success("{}さんでログインしました".format(username))

						success_login(username)
					
						
					else:
						st.warning("ユーザー名かパスワードが間違っています")
						





if __name__ == '__main__':
	
	main()
