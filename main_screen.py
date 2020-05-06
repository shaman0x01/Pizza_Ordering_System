from tkinter import *
from tkinter import messagebox as ms
from tkinter import ttk
from sqlite3 import *
from functools import partial
import datetime
import time

class BuilderFacade:
	def __init__(self):
		self.pb = None

	def update(self, flag, name, price, label):
		if flag == 1:
			self.pb.add_extention(name)
		elif flag == 2:
			self.pb.remove_extention(name)
		else:
			self.pizza = Pizza(name, price)
			self.pb = PizzaBuilder(name, price, self.pizza)
		label['text'] = "Total: {0:.2f}$".format(self.pb.get_price())


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


class Order:
	def __init__(self, pizza, price, orderer):
		self.pizza = pizza
		self.date_of_order = ""
		self.orderer = orderer
		self.price = price
		self.number = 1

class User:
	def __init__(self, flag, name, sur_name, username):
		self.name = name
		self.sur_name = sur_name
		self.username = username

class confirm_order():
	def __init__(self, base, order):
		with connect ('ordering_management.db') as db:
			c = db.cursor()
		self.order = order
		self.price1 = self.order.price
		self.root = Toplevel(base)
		self.root.geometry("500x250")
		self.root.title("Confirm order")
		self.f1 = Frame(self.root, bg = "#f58a42", bd = 5)
		self.f1.place(relx=0, rely=0, relwidth=1, relheight=0.2)
		self.l1 = Label(self.f1, text= order.pizza + " - number: 1", bg="#42f5bc",font=("Verdana", 10))
		self.l1.place(relx = 0, rely = 0, relwidth = 1, relheight = 1)
		self.f2 = Frame(self.root, bg = "#f58a42", bd = 5)
		self.f2.place(relx=0, rely=0.2, relwidth=1, relheight=0.8)
		self.total_label = Label(self.f2, text = "Total price: {0:.2f}$".format(self.order.price), bg="#42f5bc", font=("Verdana", 14))
		self.total_label.place(relx = 0.38, rely = 0)
		self.increase_number = Button(self.f2, text = "Increase number", command = lambda: self.set_number(1))
		self.increase_number.place(relx = 0.1, rely = 0.3, relwidth = 0.4, relheight=0.2)
		self.decrease_number = Button(self.f2, text = "Decrease number", command = lambda: self.set_number(0))
		self.decrease_number.place(relx = 0.55, rely = 0.3, relwidth = 0.4, relheight=0.2)
		self.confirm_button = Button(self.f2, text = "Confirm!", bg = "red", command = self.add_to_table)
		self.confirm_button.place(relx = 0.25, rely = 0.6, relwidth = 0.5, relheight = 0.3)

	def set_number(self, flag):
		if flag:
			self.order.number += 1
		else:
			self.order.number -= 1
		if self.order.number < 1:
			self.order.number = 1
		else: 
			self.order.price = self.price1*self.order.number
			self.total_label["text"] = "Total price: {0:.2f}$".format(self.order.price)
			self.l1["text"] = self.order.pizza + " - number: "+str(self.order.number)

	def add_to_table(self):
		self.order.date_of_order = str(datetime.datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S"))
		with connect('ordering_management.db') as db:
			c = db.cursor()
		c.execute('INSERT INTO ORDERS (pizza,date_of_order,price,orderer,number) VALUES(?,?,?,?,?)', (self.order.pizza, self.order.date_of_order, self.order.price, self.order.orderer, self.order.number))
		db.commit()
		ms.showinfo('Success!','Order confirmed!')


class new_order():
		def __init__(self, base, user):
			with connect('ordering_management.db') as db:
				c = db.cursor()
			c.execute('SELECT * FROM DEFAULT_PIZZAS')
			data1 = c.fetchall()
			CheckVar1 = IntVar()
			self.user = user
			self.bf = BuilderFacade()
			self.root = Toplevel(base)
			self.root.geometry("800x400")
			self.root.title("New Order - Pizza Ordering System")
			self.f1 = Frame(self.root, bg = "#f58a42", bd = 5)
			self.f1.place(relx=0, rely=0, relwidth=1, relheight=0.2)
			self.l1 = Label(self.f1, text="Total: 0", bg="#42f5bc",font=("Verdana", 14))
			self.l1.place(relx = 0, rely = 0, relwidth = 0.8, relheight = 1)
			self.order_button = Button(self.f1, text = "Order!", bg = "red", command = self.confirm_order_util)
			self.order_button.place(relx = 0.8, rely = 0, relwidth = 0.2, relheight = 1)
			self.f2 = Frame(self.root, bg = "#f58a42", bd = 5)
			self.f2.place(relx=0, rely=0.2, relwidth=1, relheight=0.8)
			self.f3 = Frame(self.f2, bg = "#f58a42", bd = 5)
			self.f3.place(relx = 0.1, rely = 0, relwidth = 0.5, relheight = 1)
			Label(self.f3, text = "Default options:", bg="#f58a42", font=("Verdana", 14)).pack(side = TOP, anchor = W)
			self.f4 = Frame(self.f2, bg = "#f58a42", bd = 5)
			self.f4.place(relx = 0.7, rely = 0, relwidth = 0.3, relheight = 1)
			Label(self.f4, text = "Add:", bg="#f58a42", font=("Verdana", 14)).pack(side = TOP, anchor = W)
			var = IntVar()
			Radiobutton(self.f3, text = "Pizza Dough", variable = var, value = "Pizza Dough", indicatoron = 0, command = partial(self.bf.update, 0, "Pizza Dough ", 1.0, self.l1)).pack(fill = X)
			for pizza in data1:
				Radiobutton(self.f3, text = pizza[1]+" - " + "{0:.2f}$".format(pizza[2]), variable = var, value = pizza, command = partial(self.bf.update, 0, pizza[1]+ " ", pizza[2], self.l1), indicatoron=0).pack(fill = X)
			for ingredient in [["Cheese", 0.4], ["Tomato", 0.6], ["Chicken", 0.8]]:
				Button(self.f4, text = ingredient[0]+" - +"+str(ingredient[1])+"$", command = partial(self.bf.update,1, ingredient[0], ingredient[1], self.l1)).pack(fill = X)
			Label(self.f4, text = "Remove:", bg="#f58a42", font=("Verdana", 14)).pack(side = TOP, anchor = W)
			for ingredient in [["Cheese", 0.4], ["Tomato", 0.6], ["Chicken", 0.8]]:
				Button(self.f4, text = ingredient[0]+" - -"+str(ingredient[1])+"$", command = partial(self.bf.update,2, ingredient[0], ingredient[1], self.l1)).pack(fill = X)

		def confirm_order_util(self):
			if self.bf.pb == None:
				ms.showerror("Error!", "Please, select pizza first!")
			else:
				order = Order(self.bf.pb.get_name(), self.bf.pb.get_price(), self.user.username)
				confirm_order(self.root, order)



class main():
	def __init__(self, user):
		with connect('ordering_management.db') as db:
			c = db.cursor()
		c.execute("CREATE TABLE IF NOT EXISTS ORDERS (id INTEGER PRIMARY KEY AUTOINCREMENT,pizza TEXT, date_of_order TEXT, price REAL,orderer TEXT, number INTEGER)")
		c.execute('SELECT * FROM ORDERS WHERE orderer = ?', (user.username,))
		data = c.fetchall()
		self.user = user
		self.root = Tk()
		self.root.geometry("800x400")
		self.root.title("Main - Pizza Ordering System")
		self.f1 = Frame(self.root, bg = "#f58a42", bd = 5)
		self.f1.place(relx=0, rely=0, relwidth=1, relheight=0.2)
		self.l1 = Label(self.f1, text="Welcome, "+self.user.name+ " " + self.user.sur_name+ "!", bg="#42f5bc", width="300", height="2", font=("Verdana", 14))
		self.l1.pack()
		self.f2 = Frame(self.root, bg = "#f58a42", bd = 5)
		self.f2.place(relx=0, rely=0.2, relwidth=1, relheight=0.8)
		self.l1 = Label(self.f2, text="Order history", bg = "#f58a42")
		self.l1.place(rely = 0.02 , relx = 0.1)
		self.t1 = ttk.Treeview(self.f2, height=10, columns=('#0', '#1', '#2'))
		self.t1.grid(row = 5, column = 3, columnspan = 5)
		self.t1.heading('#0', text = "Order NO", anchor = W)
		self.t1.heading('#1', text = "Pizza", anchor = W)
		self.t1.heading('#2', text = "Date of order", anchor = W)
		self.t1.heading('#3', text = "Price", anchor = W)
		records = self.t1.get_children()
		for x in records:
			self.t1.delete(x)
		for x in data:
			self.t1.insert('', 0, text = x[0], values = (x[1], x[2], "{0:.2f}$".format(float(x[3]))))
		self.t1.place(rely = 0.15, relx = 0.1, relwidth = 0.8, relheight = 0.8)
		self.b2 = Button(self.f2, text="New Order*", command = self.new_order_util)
		self.b2.place(rely = 0.02, relx = 0.7, relwidth=0.2, relheight=0.1)
		self.root.mainloop()

	def new_order_util(self):
		new_order(self.root, self.user)
