import streamlit as st
import pandas as pd
import sqlite3
import hashlib

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

	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT,hinmei TEXT,suryo TEXT,yu_no TEXT,ad TEXT,ad2 TEXT,ad3 TEXT,atena TEXT,tel TEXT)')

def add_user(username,password,hinmei,suryo,yu_no,ad,ad2,ad3,atena,tel):
	c.execute('INSERT INTO userstable(username,password,hinmei,suryo,yu_no,ad,ad2,ad3,atena,tel) VALUES (?,?,?,?,?,?,?,?,?,?)',(username,password,hinmei,suryo,yu_no,ad,ad2,ad3,atena,tel))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data

def main():

	btn_flg = False
	
	st.title("在庫管理")

	menu = ["ホーム","ログイン","管理者メニュー","管理者メニュー(database)"]
	choice = st.sidebar.selectbox("メニュー",menu)

	if choice == "ホーム":
		st.subheader("ホーム画面です")


	elif choice == "ログイン":
		st.subheader("ログイン画面です")

		username = st.sidebar.text_input("ユーザー名を入力してください")
		password = st.sidebar.text_input("パスワードを入力してください",type='password')
		
		if st.sidebar.button("ログインあああ"):
		#if st.sidebar.checkbox("ログイン"):
			create_user()
			hashed_pswd = make_hashes(password)

			result = login_user(username,check_hashes(password,hashed_pswd))
			if result:
				print(username)
				search=username
				st.success("{}さんでログインしました".format(username))

				c.execute("select * from userstable WHERE username = search")
				data = c.fetchall()
				st.markdown(data)

			else:
				st.warning("ユーザー名かパスワードが間違っています")


	elif choice == "管理者メニュー":
		
		st.subheader("新しいアカウントを作成します")

		new_user = st.text_input("ユーザー名")
		new_password = st.text_input("パスワード",type='password')
		
		new_hinmei = st.text_input("品名")
		new_suryo = st.text_input("数量")
		new_yu_no = st.text_input("郵便")
		
		new_ad = st.text_input("住所")
		new_ad2 = st.text_input("住所2")
		new_ad3 = st.text_input("住所3")
		new_atena = st.text_input("宛名")
		new_tel = st.text_input("電話")


		if st.button("アカウント作成"):

			row = 'SELECT count(*) FROM userstable WHERE username = ?'
			c.execute(row, (new_user,))
			count = c.fetchone()[0]
			print(count)

			if count == 0:
				print('ゼロ件です')

				create_user()
				add_user(new_user, make_hashes(new_password),new_hinmei,new_suryo,new_yu_no,new_ad,new_ad2,new_ad3,new_atena,new_tel)
				st.success("アカウントの作成に成功しました")
			else:
				print("ゼロ件ではないです")
				st.info("ユーザー名は既にアカウント登録されています。上書きしますか")
				btn_flg = True

		if btn_flg:
			print("フラグがtrueになりました")
			st.button("はい") 
			st.button("いいえ")
		
		if btn_flg==True and st.button("はい"):
			print("はいが押されました")
	




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

	elif choice == "管理者メニュー(database)":
		
		st.subheader("データベース全件")

		c.execute("select * from userstable")
		data = c.fetchall()
		st.markdown(data)

if __name__ == '__main__':
	main()
