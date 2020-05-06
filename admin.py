from tkinter import *
from tkinter import messagebox as ms
from functools import partial
from tkinter import ttk
from sqlite3 import *

class BuilderFacade:
	def __init__(self):
		self.pb = None

	def update(self, l1, l2, flag, name, price):
		if flag == 1:
			self.pb.add_extention(name)
		elif flag == 2:
			self.pb.remove_extention(name)
		else:
			self.pizza = Pizza(name, price)
			self.pb = PizzaBuilder(name, price, self.pizza)
		l1["text"] = self.pb.get_name()
		l2['text'] = "Total: {0:.2f}$".format(self.pb.get_price())


class Pizza:
	def __init__(self, name, price):
		self.name = name
		self.price = price

	def get_price(self):
		return self.price

	def get_name(self):
		return self.name

class PizzaDecorator(Pizza):
	def __init__(self, pizza):
		self.pizza = pizza

	def get_price(self):
		return self.pizza.get_price()

	def get_name(self):
		return self.pizza.get_name()

class Tomato(PizzaDecorator):
	def __init__(self, pizza):
		super(Tomato, self).__init__(pizza)
		self.__tomato_price = 0.6

	@property
	def price(self):
		return self.__tomato_price

	def get_price(self):
		return super(Tomato, self).get_price() + self.__tomato_price

	def get_name(self):
		return super(Tomato, self).get_name()+"Tomato "

class Cheese(PizzaDecorator):
	def __init__(self, pizza):
		super(Cheese, self).__init__(pizza)
		self.__cheese_price = 0.4

	@property
	def price(self):
		return self.__cheese_price

	def get_price(self):
		return super(Cheese, self).get_price() + self.__cheese_price

	def get_name(self):
		return super(Cheese, self).get_name() + "Cheese "

class Chicken(PizzaDecorator):
	def __init__(self, pizza):
		super(Chicken, self).__init__(pizza)
		self.__chicken_price = 0.8

	@property
	def price(self):
		return self.__chicken_price

	def get_price(self):
		return super(Chicken, self).get_price() + self.__chicken_price

	def get_name(self):
		return super(Chicken, self).get_name() + "Chicken "


class PizzaBuilder:
	def __init__(self, pizza_type, pizza_price, pizza):
		self.pizza_type = pizza_type
		self.pizza_price = pizza_price
		self.pizza = pizza
		self.extentions_list = []

	def add_extention(self, extention):
		self.pizza = eval(extention)(self.pizza)
		self.extentions_list.append(extention)

	def remove_extention(self, extention):
		if extention in self.extentions_list:
			self.extentions_list.remove(extention)
		temp_pizza = Pizza(self.pizza_type, self.pizza_price)
		for ex in self.extentions_list:
			temp_pizza = eval(ex)(temp_pizza)
		self.pizza = temp_pizza

	def get_price(self):
		return self.pizza.get_price()
	def get_name(self):
		return self.pizza.get_name()

class change_admin():
	def __init__(self, base):
		self.root = Toplevel(base)
		self.root.title("Change Admin Details")
		self.root.geometry("350x150")
		self.fr1 = Frame(self.root, bg = "#f58a42", bd = 5)
		self.fr1.place(relx=0, rely=0, relwidth=1, relheight=0.2)
		self.username = StringVar()
		self.password = StringVar()
		self.l1 = Label(self.fr1, text="Please enter new username and password", bg="#42f5bc", width="300", height="2", font=("Verdana", 11))
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
		self.b1 = Button(self.fr2, text="Confirm", command = lambda: self.add_to_table(self.username, self.password))
		self.b1.place(relx = 0.3, rely = 0.75, relwidth = 0.4, relheight = 0.25)

	def add_to_table(self,username, password):
		with connect('ordering_management.db') as db:
			c = db.cursor()
		c.execute('UPDATE USER SET username = ? WHERE type = ?', (username.get(), "admin"))
		c.execute('UPDATE USER SET password = ? WHERE type = ?', (password.get(), "admin"))
		db.commit()
		ms.showinfo('Success!','Changes saved!')

class new_default_pizza():
	def __init__(self, base):
		self.bf = BuilderFacade()
		self.root = Toplevel(base)
		self.root.geometry("800x400")
		self.root.title("New Default Pizza:")
		self.f1 = Frame(self.root, bg = "#f58a42", bd = 5)
		self.f1.place(relx=0, rely=0, relwidth=1, relheight=0.2)
		self.l1 = Label(self.f1, text="", bg="#42f5bc",font=("Verdana", 10))
		self.l1.place(relx = 0, rely = 0, relwidth = 0.8, relheight = 1)
		self.f3 = Frame(self.root, bg = "#f58a42", bd = 5)
		self.f3.place(relx = 0, rely = 0.2, relwidth = 1, relheight = 0.1)
		self.l2 = Label(self.f3, text = "Price: 0$", bg="#42f5bc",font=("Verdana", 14))
		self.l2.place(rely = 0, relx = 0, relwidth = 1, relheight = 1)
		self.f2 = Frame(self.root, bg = "#f58a42", bd = 5)
		self.f2.place(relx=0, rely=0.3, relwidth=1, relheight=0.7)
		self.bf.update(self.l1, self.l2, 0, "Pizza Dough ", 1.0)
		for ingredient in [["Cheese", 0.4], ["Tomato", 0.6], ["Chicken", 0.8]]:
			Button(self.f2, text = ingredient[0]+" - "+str(ingredient[1])+"$", command = partial(self.bf.update, self.l1, self.l2, 1, ingredient[0], ingredient[1])).pack(fill = X)
		self.add_button = Button(self.f1, text = "ADD", bg = "red", command = partial(self.add_to_table))
		self.add_button.place(relx = 0.8, rely = 0, relwidth = 0.2, relheight = 1)

	def add_to_table(self):
		with connect('ordering_management.db') as db:
			c = db.cursor()
		c.execute('INSERT INTO DEFAULT_PIZZAS (Name,Price) VALUES(?,?)', (self.l1["text"], self.bf.pb.get_price()))
		db.commit()
		ms.showinfo('Success!','Default pizza added!')

	
 
class main():
	def __init__(self, base):
		with connect('ordering_management.db') as db:
			c = db.cursor()
		c.execute("CREATE TABLE IF NOT EXISTS ORDERS (id INTEGER PRIMARY KEY AUTOINCREMENT,pizza TEXT, date_of_order TEXT, price REAL,orderer TEXT, number INTEGER)")
		db.commit()
		c.execute('SELECT * FROM ORDERS')
		data = c.fetchall()
		self.root = Toplevel(base)
		self.root.geometry("800x400")
		self.root.title("Admin page - Pizza Ordering System")
		self.f1 = Frame(self.root, bg = "#f58a42", bd = 5)
		self.f1.place(relx=0, rely=0, relwidth=1, relheight=0.2)
		self.profit = 0
		for i in data:
			self.profit += i[3]
		self.l1 = Label(self.f1, text= "Total profit: {0:.2f}$".format(self.profit), bg="#42f5bc", width="300", height="2", font=("Verdana", 14))
		self.l1.pack()
		self.f2 = Frame(self.root, bg = "#f58a42", bd = 5)
		self.f2.place(relx=0, rely=0.2, relwidth=1, relheight=0.8)
		self.l1 = Label(self.f2, text="All the orders:", bg = "#f58a42")
		self.l1.place(rely = 0.02 , relx = 0.1)
		self.t1 = ttk.Treeview(self.f2, height=10, columns=('#0', '#1', '#2', '#3'))
		self.t1.grid(row = 5, column = 3, columnspan = 5)
		self.t1.heading('#0', text = "Order NO", anchor = W)
		self.t1.heading("#1", text = "Orderer", anchor = W)
		self.t1.heading('#2', text = "Pizza", anchor = W)
		self.t1.heading('#3', text = "Date of order", anchor = W)
		self.t1.heading('#4', text = "Price", anchor = W)
		records = self.t1.get_children()
		for x in records:
			self.t1.delete(x)
		for x in data:
			self.t1.insert('', 0, text = x[0], values = (x[4], x[1], x[2], "{0:.2f}$".format(float(x[3]))))
		self.t1.place(rely = 0.15, relx = 0.1, relwidth = 0.8, relheight = 0.8)
		self.b1 = Button(self.f2, text = "Change Admin Details*", command = self.change_admin_util)
		self.b1.place(rely = 0.02, relx = 0.4, relwidth = 0.25, relheight = 0.1)
		self.b2 = Button(self.f2, text="New Default Pizza*", command = self.new_pizza_util)
		self.b2.place(rely = 0.02, relx = 0.7, relwidth=0.2, relheight=0.1)
		self.root.mainloop()

	def new_pizza_util(self):
		new_default_pizza(self.root)

	def change_admin_util(self):
		change_admin(self.root)

