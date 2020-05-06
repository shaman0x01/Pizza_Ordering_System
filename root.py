from tkinter import *
from tkinter import messagebox as ms
from sqlite3 import *
import main_screen
import admin


with connect('ordering_management.db') as db:
    c = db.cursor()

c.execute('CREATE TABLE IF NOT EXISTS USER (name TEXT, sur_name TEXT, username TEXT, password TEXT, type TEXT);')
db.commit()

class User:
	def __init__(self, name, sur_name, username):
		self.name = name
		self.sur_name = sur_name
		self.username = username


def add_to_table(name, sur_name, username, password):
	with connect('ordering_management.db') as db:
            c = db.cursor()
	c.execute('SELECT * FROM USER WHERE username = ?', (username.get(),))
	if c.fetchall():
		ms.showerror('Error!','Username Taken, Try a Diffrent One!')
	else:
		c.execute('INSERT INTO USER (name,sur_name,username,password,type) VALUES(?,?,?,?, ?)', (name.get(), sur_name.get(), username.get(), password.get(), "user",))
		db.commit()
		ms.showinfo('Success!','Account Created!')

class register():
	def __init__(self, base):
	    self.root = Toplevel(base)
	    self.root.title("Registration")
	    self.root.geometry("500x250")
	    self.fr1 = Frame(self.root, bg = "#f58a42", bd = 5)
	    self.fr1.place(relx=0, rely=0, relwidth=1, relheight=0.2)
	    self.name = StringVar()
	    self.sur_name = StringVar()
	    self.username = StringVar()
	    self.password = StringVar()
	    self.l1 = Label(self.fr1, text="Please enter details below", bg="#42f5bc", width="300", height="2", font=("Verdana", 14))
	    self.l1.pack()
	    self.fr2 = Frame(self.root, bg = "#f58a42", bd = 5)
	    self.fr2.place(relx=0, rely=0.2, relwidth=1, relheight=0.8)
	    self.name_label = Label(self.fr2, text="Name* ", bg = "#f58a42")
	    self.name_label.place(relx=0.1, rely = 0.05, relwidth=0.3, relheight=0.15)
	    self.name_entry = Entry(self.fr2, textvariable=self.name)
	    self.name_entry.place(relx = 0.5, rely = 0.05, relwidth = 0.4, relheight=0.15)
	    self.sur_name_label = Label(self.fr2, text="Surname* ", bg = "#f58a42")
	    self.sur_name_label.place(relx=0.1, rely = 0.25, relwidth=0.3, relheight=0.15)
	    self.sur_name_entry = Entry(self.fr2, textvariable=self.sur_name)
	    self.sur_name_entry.place(relx = 0.5, rely = 0.25, relwidth = 0.4, relheight=0.15)
	    self.username_label = Label(self.fr2, text="Username* ", bg = "#f58a42")
	    self.username_label.place(relx=0.1, rely = 0.45, relwidth=0.3, relheight=0.15)
	    self.username_entry = Entry(self.fr2, textvariable=self.username)
	    self.username_entry.place(relx = 0.5, rely = 0.45, relwidth = 0.4, relheight=0.15)
	    self.password_label = Label(self.fr2, text="Password * ", bg = "#f58a42")
	    self.password_label.place(relx= 0.1, rely = 0.65, relwidth=0.3, relheight=0.15)
	    self.password_entry = Entry(self.fr2, textvariable=self.password, show='*')
	    self.password_entry.place(relx = 0.5, rely = 0.65, relwidth=0.4, relheight=0.15)
	    self.b1 = Button(self.fr2, text="Register", command=lambda: add_to_table(self.name, self.sur_name, self.username, self.password))
	    self.b1.place(relx = 0.3, rely = 0.85, relwidth = 0.4, relheight = 0.15)

class login():
	def __init__(self, base):
		self.base = base
		self.root = Toplevel(base)
		self.root.title("Login")
		self.root.geometry("300x150")
		self.fr1 = Frame(self.root, bg = "#f58a42", bd = 5)
		self.fr1.place(relx=0, rely=0, relwidth=1, relheight=0.2)
		self.username = StringVar()
		self.password = StringVar()
		self.l1 = Label(self.fr1, text="Please enter username and password", bg="#42f5bc", width="300", height="2", font=("Verdana", 11))
		self.l1.pack()
		self.fr2 = Frame(self.root, bg = "#f58a42", bd = 5)
		self.fr2.place(relx=0, rely=0.2, relwidth=1, relheight=0.8)
		self.username_label = Label(self.fr2, text="Username * ", bg = "#f58a42")
		self.username_label.place(relx=0.1, rely = 0.1, relwidth=0.3, relheight=0.2)
		self.username_entry = Entry(self.fr2, textvariable=self.username)
		self.username_entry.place(relx = 0.5, rely = 0.1, relwidth = 0.4, relheight=0.2)
		self.password_label = Label(self.fr2, text="Password * ", bg = "#f58a42")
		self.password_label.place(relx= 0.1, rely = 0.35, relwidth=0.3, relheight=0.2)
		self.password_entry = Entry(self.fr2, textvariable=self.password, show='*')
		self.password_entry.place(relx = 0.5, rely = 0.35, relwidth=0.4, relheight=0.2)
		self.b1 = Button(self.fr2, text="Login", command = lambda: self.fetch_from_table(self.username, self.password))
		self.b1.place(relx = 0.3, rely = 0.75, relwidth = 0.4, relheight = 0.25)

	def close(self):
		self.root.destroy()

	def fetch_from_table(self,username, password):
		if username.get() == '' or password.get() == '':
			ms.showerror("Error!", "Please, enter username and password!")
			return
		with connect('ordering_management.db') as db:
			c = db.cursor()
		c.execute('SELECT * FROM USER WHERE (username, password, type) = (?, ?, ?)', (username.get(),password.get(),"admin",))
		data = c.fetchall()
		if data:
			self.close()
			admin.main(self.base)
		else:
			c.execute('SELECT * FROM USER WHERE (username, password) = (?, ?)', (username.get(),password.get(),))
			data = c.fetchall()
			if data:
				self.close()
				user = User(data[0][0], data[0][1], data[0][2])
				main_screen.main(user)
			else:
				ms.showerror("Error!", "Username or password is incorrect!")

class root():
	def __init__(self):
		self.root = Tk()
		self.root.geometry("450x250")
		self.root.title("Login - Pizza Ordering System")
		self.f1 = Frame(self.root, bg = "#f58a42", bd = 5)
		self.f1.place(relx=0, rely=0, relwidth=1, relheight=0.2)
		self.l1 = Label(self.f1, text="Welcome to Pizza Ordering System!", bg="#42f5bc", width="300", height="2", font=("Verdana", 14))
		self.l1.pack()
		self.f2 = Frame(self.root, bg = "#f58a42", bd = 5)
		self.f2.place(relx=0, rely=0.2, relwidth=1, relheight=0.8)
		self.b1 = Button(self.f2, text="Login", command = lambda:login(self.root))
		self.b1.place(rely = 0.1 , relx = 0.3, relwidth=0.4, relheight=0.2)
		self.l2 = Label(self.f2, text="or", bg = "#f58a42")
		self.l2.place(rely=0.35, relx = 0.3, relwidth=0.4, relheight=0.1)
		self.b2 = Button(self.f2, text="Register", command=lambda: register(self.root))
		self.b2.place(rely = 0.5, relx = 0.3, relwidth=0.4, relheight=0.2)
		self.root.mainloop()
	def close(self):
		self.root.destroy()

def main():
	app = root()


if __name__ == "__main__":
	main()
