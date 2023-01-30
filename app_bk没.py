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
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT,hnmi TEXT,suryo TEXT,ybn_num TEXT,address TEXT,address2 TEXT,address3 TEXT,add_name TEXT,tel TEXT)')

def add_user(username,password,hnmi,suryo,ybn_num,address,address2,address3,add_name,tel):
	c.execute('INSERT INTO userstable(username,password,hnmi,suryo,ybn_num,address,address2,address3,add_name,tel) VALUES (?,?,?,?,?,?,?,?,?,?)',(username,password,hnmi,suryo,ybn_num,address,address2,address3,add_name,tel))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data

def main():


	st.title("在庫管理")

	menu = ["ホーム","ログイン","管理者メニュー"]
	choice = st.sidebar.selectbox("メニュー",menu)

	if choice == "ホーム":
		st.subheader("ホーム画面です")

		# #ホームに入る度に１行追加
		# c.execute('INSERT INTO userstable(username,password) VALUES (?,?)', ('test', 'test2'))
		# conn.commit()


		c.execute("select * from userstable")
		data = c.fetchall()
		st.info(data)
		#230125追加

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
				st.success("{}さんでログインしました".format(username))

				st.subheader("テストさんの在庫一覧です。")







			else:
				st.warning("ユーザー名かパスワードが間違っています")

	elif choice == "管理者メニュー":
		st.subheader("新しいアカウントを作成します")

		new_user = st.text_input("ユーザー名")
		new_password = st.text_input("パスワード",type='password')

		new_hnmi = st.text_input("品名")
		new_suryo = st.text_input("数量")

		new_ybn_num = st.text_input("郵便番号")
		new_address = st.text_input("住所")
		new_address2 = st.text_input("住所2")
		new_address3 = st.text_input("住所3")
		new_add_name = st.text_input("宛名")
		new_tel = st.text_input("電話番号")

		if st.button("アカウント作成"):

			row = 'SELECT count(*) FROM userstable WHERE username = ?'
			c.execute(row, (new_user,))
			count = c.fetchone()[0]
			print(count)

			if count == 0:
				# アカウントの作成をする
				print('ゼロ件です')

				create_user()
				add_user(new_user, make_hashes(new_password),new_hnmi,new_suryo,new_ybn_num,new_address,new_address2,new_address3,new_add_name,new_tel)
				st.success("アカウントの作成に成功しました")
				st.info("ログイン画面からログインしてください")
			else:
				#アカウントの作成はしない
				print("ゼロ件ではないです")
				st.info("ユーザー名は既にアカウント登録されているため作成できません")

		st.subheader("データ全件削除します。")
		if st.button("全件削除"):
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

			st.info("全件削除しました。")

if __name__ == '__main__':
	main()
