from tkinter import *
from tkcalendar import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
import tkinter as tk
import datetime
import time
import sqlite3



root = Tk()
root.geometry("1550x850+0+0")
root.title("Hospital Management App")
root.configure(background = "snow")


style = ttk.Style()

style.theme_create( "yummy", parent="alt", settings={
      "TNotebook": {"configure": {"tabmargins": [5, 35, 20, 430] } }, # 5(low value) pushes the tab to the left, 20(low value) pushes the tab to the left also. 35 and 340 control upward and downward movements of the tab
 			"TNotebook.Tab": {
           "configure": {"padding": [10, 10], "foreground":'black'},
            "map":       {"background": [("selected", "snow")],
                          "expand": [("selected", [1, 1, 1, 1])] } } } )


style.theme_use("yummy")
style.configure("lefttab.TNotebook", tabposition = "ws",background = "thistle")
style.configure("TNotebook.Tab", font = "Rockwell 14 bold italic",background = "#f2838e")


notebook = ttk.Notebook(root, style="lefttab.TNotebook")

tab_home = ttk.Frame(notebook )
tab_pdata = ttk.Frame(notebook)
tab_pdata = ttk.Frame(notebook)
tab_app = ttk.Frame(notebook)
tab_pres = ttk.Frame(notebook)
tab_inv= ttk.Frame(notebook)
tab_bill = ttk.Frame(notebook)
tab_fin = ttk.Frame(notebook)
tab_staff = ttk.Frame(notebook)
tab_assess = ttk.Frame(notebook)


notebook.add(tab_home, text = "Home")
notebook.add(tab_pdata, text = "Patient's Data")
notebook.add(tab_app, text = "Patient Appointment")
notebook.add(tab_pres, text = "Prescriptions")
notebook.add(tab_inv, text = "Hospital Inventory")
notebook.add(tab_bill, text = "Patient Billing Record")
notebook.add(tab_fin, text = "Financial Records")
notebook.add(tab_staff, text = "Staff Profile")
notebook.add(tab_assess, text = "Hospital Assessment")

notebook.grid(row = 0, column = 0, sticky = "nw")



#====================== ROOT IMAGE===========================================#
#==============================================================================

b_image = ImageTk.PhotoImage(Image.open("C:\\Users\\KURUS\\Desktop\\Hospital App\\homepage.jpg"))
b_image_label = Label(tab_home, image = b_image, width = 1250, height = 830)
b_image_label.grid(row = 0, column = 0, columnspan = 10, rowspan = 10)


icon = ImageTk.PhotoImage(Image.open("C:\\Users\\KURUS\\Desktop\\Hospital App\\icon_hospital1.jpg"))
icon_label = Label(tab_home, image = icon, width = 100)
icon_label.grid(row = 0, column = 0, sticky = NW, pady = 5)


topic = Label(tab_home, text = "HOSPITAL MANAGEMENT APP", font = "Garamond 32 bold italic underline", fg = "#801722", bg='lightgrey')
topic.grid(row = 0, column = 4, sticky=N)
	
	#--------------------TIME AND DATE----------------#

def tick():
	d = datetime.datetime.now()
	mydate = "{:%B %d %Y}".format(d)
	mytime = time.strftime("%I:%M: %S %p")
	lblInfo.config(text = (mytime +"     " + mydate))
	lblInfo.after(200,tick)
lblInfo = Label(tab_home, font = "calibri 12 bold", fg = "crimson", bg = "lightgrey")
lblInfo.grid(row = 0, column = 6, columnspan = 8, sticky=N, pady = 10)
tick()


#========================PATIENT'S DATA==================================#
#=========================================================================


#========================FUNCTIONS==================================#

def run_query(query,parameters=()):
	conn = sqlite3.connect("medical.db")
	cur = conn.cursor()
	query_result = cur.execute(query,parameters)
	conn.commit()
	return query_result


def view_record_pdata():
	record = tree_pdata.get_children()
	for element in record:
		tree_pdata.delete(element)
	query = "SELECT * FROM hospital"
	connect = run_query(query)
	for data in connect:
		tree_pdata.insert("",10000, text = data[0], values = data[1:])


def validation_pdata():
	return len(entry_date.get())!=0 or len(entry_full.get())!=0 or len(entry_add.get())!=0 or len(entry_phone.get())!=0 or len(entry_gender.get())!=0 or len(entry_age.get())!=0 or len(entry_ill.get())!=0 or len(entry_occ.get())!=0 or len(entry_gen.get())!=0 or len(entry_status.get())

def add_record_pdata():
	if validation_pdata:
		query = "INSERT INTO hospital VALUES(NULL,?,?,?,?,?,?,?,?,?,?)"
		parameters = (entry_date_pdata.get(), entry_full.get(),entry_add.get(),entry_phone.get(),entry_gender.get(),entry_age.get(),entry_ill.get(),entry_occ.get(),entry_gen.get(), entry_status_pdata.get())
		run_query(query,parameters)
		display_pdata["text"] = "New Record Added"

		entry_date_pdata.delete(0,END)
		entry_full.delete(0,END)
		entry_add.delete(0,END)
		entry_phone.delete(0,END)
		entry_gender.delete(0,END)
		entry_age.delete(0,END)
		entry_ill.delete(0,END)
		entry_occ.delete(0,END)
		entry_gen.delete(0,END)
		entry_status_pdata.delete(0,END)

	else:
		display_pdata["text"] = "Please fill all fields"
	view_record_pdata()

def add():
	pop = messagebox.askquestion("Adding New Record","Do you want to add new record?")
	if pop == "yes":
		add_record_pdata()
	else:
		display_pdata["text"] = "Item not added"



def delete_record_pdata():
	pop = messagebox.askquestion("Deleting item","Do you want to delete this record? Action cannot be reversed")
	if pop == "yes":

		try:
			tree_pdata.item(tree_pdata.selection())["values"][1]
		except IndexError as e:
			display_pdata["text"] = "Please select a record to delete"
		query = "DELETE FROM hospital WHERE ID=?"
		number = tree_pdata.item(tree_pdata.selection())["text"]
		run_query(query,(number,))
		display_pdata['text'] = "Record {} has been deleted".format(entry_full.get())
		view_record_pdata()
	else:
		display_pdata["text"] = "Record not deleted"

def edit_box_pdata():
	global new_edit
	tree_pdata.item(tree_pdata.selection())['values'][0]
	date_text = tree_pdata.item(tree_pdata.selection())['values'][0]
	full_text = tree_pdata.item(tree_pdata.selection())['values'][1]
	add_text = tree_pdata.item(tree_pdata.selection())['values'][2]
	phone_text = tree_pdata.item(tree_pdata.selection())['values'][3]
	gender_text = tree_pdata.item(tree_pdata.selection())['values'][4]
	age_text = tree_pdata.item(tree_pdata.selection())['values'][5]
	ill_text = tree_pdata.item(tree_pdata.selection())['values'][6]
	occ_text = tree_pdata.item(tree_pdata.selection())['values'][7]
	gen_text = tree_pdata.item(tree_pdata.selection())['values'][8]
	status_text = tree_pdata.item(tree_pdata.selection())['values'][9]

	new_edit = Toplevel()
	Label(new_edit, text = "Old Date").grid(row = 0, column = 0)
	Entry(new_edit, textvariable = StringVar(new_edit,date_text), state = "readonly").grid(row = 0, column = 1)
	Label(new_edit, text = "New Date").grid(row = 1, column = 0)
	new_date = DateEntry(new_edit)
	new_date.grid(row = 1, column = 1)

	Label(new_edit, text = "Old Full name").grid(row = 2, column = 0)
	Entry(new_edit, textvariable = StringVar(new_edit, full_text),state = "readonly").grid(row = 2, column = 1)
	Label(new_edit, text = "New Full name").grid(row = 3, column = 0)
	new_full = Entry(new_edit)
	new_full.grid(row = 3, column = 1)

	Label(new_edit, text = "Old Address").grid(row = 4, column = 0)
	Entry(new_edit, textvariable = StringVar(new_edit, add_text),state = "readonly").grid(row = 4, column = 1)
	Label(new_edit, text = "New Address").grid(row = 5, column = 0)
	new_add = Entry(new_edit)
	new_add.grid(row = 5, column = 1)

	Label(new_edit, text = "Old Phone number").grid(row = 6, column = 0)
	Entry(new_edit, textvariable = StringVar(new_edit, phone_text),state = "readonly").grid(row = 6, column = 1)
	Label(new_edit, text = "New Phone number").grid(row = 7, column = 0)
	new_phone = Entry(new_edit)
	new_phone.grid(row = 7, column = 1)

	Label(new_edit, text = "Old Gender").grid(row = 8, column = 0)
	Entry(new_edit, textvariable = StringVar(new_edit, gender_text),state = "readonly").grid(row = 8, column = 1)
	Label(new_edit, text = "New Gender").grid(row = 9, column = 0)
	new_gender = ttk.Combobox(new_edit)
	new_gender["values"] = ("Male","Female","I prefer not to say")
	new_gender.grid(row = 9, column = 1)

	Label(new_edit, text = "Old Age").grid(row = 10, column = 0)
	Entry(new_edit, textvariable = StringVar(new_edit, age_text),state = "readonly").grid(row = 10, column = 1)
	Label(new_edit, text = "New Age").grid(row = 11, column = 0)
	new_age = Spinbox(new_edit, from_=0, to=150)
	new_age.grid(row = 11, column = 1)

	Label(new_edit, text = "Old Nature of Illness").grid(row = 12, column = 0)
	Entry(new_edit, textvariable = StringVar(new_edit, ill_text),state = "readonly").grid(row = 12, column = 1)
	Label(new_edit, text = "New Nature of Illness").grid(row = 13, column = 0)
	new_ill = Entry(new_edit)
	new_ill.grid(row = 13, column = 1)

	Label(new_edit, text = "Old Occupation").grid(row = 14, column = 0)
	Entry(new_edit, textvariable = StringVar(new_edit, occ_text),state = "readonly").grid(row = 14, column = 1)
	Label(new_edit, text = "New Occupation").grid(row = 15, column = 0)
	new_occ = Entry(new_edit)
	new_occ.grid(row = 15, column = 1)

	Label(new_edit, text = "Old Genotype").grid(row = 16, column = 0)
	Entry(new_edit, textvariable = StringVar(new_edit, gen_text),state = "readonly").grid(row = 16, column = 1)
	Label(new_edit, text = "New Genotype").grid(row = 17, column = 0)
	new_gen = ttk.Combobox(new_edit)
	new_gen['values'] = ("AA","AS","SS","AC")
	new_gen.grid(row = 17, column = 1)

	Label(new_edit, text = "Old Status").grid(row = 18, column = 0)
	Entry(new_edit, textvariable = StringVar(new_edit, gen_text),state = "readonly").grid(row = 18, column = 1)
	Label(new_edit, text = "New Status").grid(row = 19, column = 0)
	new_status = ttk.Combobox(new_edit)
	new_status['values'] = ("Admitted(In=Patient)","Out-patient","Discharged","Transferred")
	new_status.grid(row = 19, column = 1)

	Button(new_edit, text = "Save Changes", command = lambda:edit_record_pdata(new_date.get(),date_text,new_full.get(),full_text,new_add.get(),add_text, new_phone.get(),phone_text,new_gender.get(),gender_text,new_age.get(),age_text,new_ill.get(),ill_text,new_occ.get(),occ_text,new_gen.get(),gen_text, new_status.get(), status_text)).grid(row = 20, column = 1)
	new_edit.mainloop()

def edit_record_pdata(new_date,date_text,new_full,full_text,new_add,add_text,new_phone,phone_text,new_gender,gender_text,new_age,age_text,new_ill,ill_text,new_occ,occ_text,new_gen,gen_text,new_status,status_text):
	query = "UPDATE hospital SET datee =?, name = ?, address = ?, phone = ?, gender = ?, age = ?, nature = ?, occupation = ?, genotype = ? , status = ? WHERE datee=? AND name=? AND address=? AND phone=? AND gender=? AND age=? AND nature=? AND occupation=? AND genotype=? AND status=?"
	parameters = (new_date,new_full,new_add,new_phone,new_gender,new_age,new_ill,new_occ,new_gen,new_status,date_text,full_text,add_text,phone_text,gender_text,age_text,ill_text,occ_text,gen_text,status_text)
	run_query(query,parameters)
	new_edit.destroy()
	display_pdata["text"] = "Record has been modified"
	view_record_pdata()



#========================IMAGE==================================#

img_pdata = ImageTk.PhotoImage(Image.open("C:\\Users\\KURUS\\Desktop\\Hospital App\\symbol-patnt data1.jpg"))
img_label = Label(tab_pdata, image = img_pdata, height = 400)
img_label.grid(row = 1, column = 3, columnspan=5)

#========================LABEL==================================#


topic = Label(tab_pdata, text = "PATIENTS' RECORDS",font = "Garamond 30 bold italic underline",fg = "chocolate")
topic.grid(row = 0, column = 0, pady = 10, columnspan=10)

frame_pdata= LabelFrame(tab_pdata, text = "Register New Patient",font = "Garamond 10 bold italic", bd = 4,  padx = 10, pady = 10)
frame_pdata.grid(row = 1, column = 0, padx = 50, pady = 10, columnspan=2)

date_pdata = Label(frame_pdata, text = "Date: ", font = "Garamond 13 bold italic")
date_pdata.grid(row = 0, column = 0, pady = 5)

full_name_pdata = Label(frame_pdata, text = "Full name: ", font = "Garamond 13 bold italic")
full_name_pdata.grid(row = 1, column = 0, pady = 5)

address_pdata = Label(frame_pdata, text = "Address: ", font = "Garamond 13 bold italic")
address_pdata.grid(row = 2, column = 0, pady = 5)

phone_pdata = Label(frame_pdata, text = "Phone number: ", font = "Garamond 13 bold italic")
phone_pdata.grid(row = 3, column = 0, pady = 5)

gender = Label(frame_pdata, text = "Gender: ", font = "Garamond 13 bold italic")
gender.grid(row = 4, column = 0, pady = 5)

age_pdata = Label(frame_pdata, text = "Age: ", font = "Garamond 13 bold italic")
age_pdata.grid(row = 5, column = 0, pady = 5)

ill_pdata = Label(frame_pdata, text = "Nature of Illness: ", font = "Garamond 13 bold italic")
ill_pdata.grid(row = 6, column = 0, pady = 5)

occ_pdata = Label(frame_pdata, text = "Occupation: ", font = "Garamond 13 bold italic")
occ_pdata.grid(row = 7, column = 0, pady = 5)

gen_pdata = Label(frame_pdata, text = "Genotype: ", font = "Garamond 13 bold italic")
gen_pdata.grid(row = 8, column = 0, pady = 5)

status_pdata = Label(frame_pdata, text = "Status: ", font = "Garamond 13 bold italic")
status_pdata.grid(row = 9, column = 0, pady = 5)




#========================ENTRIES==================================#

date_text = StringVar()
entry_date_pdata = DateEntry(frame_pdata, textvariable = date_text, bd = 2, state="readonly", width = 20)
entry_date_pdata.grid(row = 0, column = 1)

full_text = StringVar()
entry_full = Entry(frame_pdata, textvariable = full_text, bd = 2, width = 40)
entry_full.grid(row = 1, column = 1)

add_text = StringVar()
entry_add = Entry(frame_pdata, textvariable = add_text, bd = 2, width = 40)
entry_add.grid(row = 2, column = 1)

phone_text = StringVar()
entry_phone = Entry(frame_pdata, textvariable = phone_text, bd = 2, width = 40)
entry_phone.grid(row = 3, column = 1)

gender_text = StringVar()
entry_gender = ttk.Combobox(frame_pdata, textvariable = gender_text, width = 20)
entry_gender["values"] = ("Male", "Female", "I prefer not to say")
entry_gender.grid(row = 4, column = 1)

age_text = StringVar()
entry_age = Spinbox(frame_pdata, textvariable = age_text, from_= 0, to = 150, bd = 2, width = 10)
entry_age.grid(row = 5, column = 1)

ill_text = StringVar()
entry_ill = Entry(frame_pdata, textvariable = ill_text, bd = 2, width = 40)
entry_ill.grid(row = 6, column = 1)

occ_text = StringVar()
entry_occ = Entry(frame_pdata, textvariable = occ_text, bd = 2, width = 40)
entry_occ.grid(row = 7, column = 1)

gen_text = StringVar()
entry_gen = ttk.Combobox(frame_pdata, textvariable = gen_text, width = 20)
entry_gen["values"] = ("AA","AS","SS","AC")
entry_gen.grid(row = 8, column = 1)

status_text = StringVar()
entry_status_pdata = ttk.Combobox(frame_pdata, textvariable = status_text, width = 20)
entry_status_pdata['values'] = ("Admitted(In=Patient)","Out-patient","Discharged","Transferred")
entry_status_pdata.grid(row = 9, column = 1)




#========================BUTTON==================================#

add_button_pdata = Button(frame_pdata, text = "Add Record",  cursor = "hand2",bg = "#51a66f", fg = "white", font = "Garamond 13 bold italic", bd=3, command = add)
add_button_pdata.grid(row = 10, column = 1, pady = 10)

edit_button_pdata = Button(frame_pdata, text = "Edit Record",  cursor = "hand2",bg = "#13264a",  fg = "white",font = "Garamond 13 bold italic", bd=3, command = edit_box_pdata)
edit_button_pdata.grid(row = 10, column = 0, pady = 10)

del_button_pdata = Button(frame_pdata, text = "Delete Record",  cursor = "hand2",bg = "#8c1c0f",  fg = "white",font = "Garamond 13 bold italic", bd=3, command = delete_record_pdata)
del_button_pdata.grid(row = 10, column = 2, pady = 10)

display_pdata = Label(frame_pdata, text = "", font = "Garamond 10 bold italic", bd=3, fg = "navy")
display_pdata.grid(row = 11, column = 1, pady = 5)


#========================TREEVIEW==================================#

style = ttk.Style()
style.configure("Treeview.Heading", font = "arial 13 bold")
style.configure("Treeview", font = "arial 9 bold")


tree_pdata = ttk.Treeview(tab_pdata, height = 12, column = ["","","","","","","","","",""])
tree_pdata.grid(row = 12, column = 0, columnspan = 10, sticky = W, padx = 5, pady = 10)

tree_pdata.heading("#0", text = "ID")
tree_pdata.column("#0", width = 50, anchor = 'n')

tree_pdata.heading("#1", text = "Date")
tree_pdata.column("#1", width = 60, anchor = 'n')

tree_pdata.heading("#2", text = "Full name")
tree_pdata.column("#2", width = 150, anchor = 'n')

tree_pdata.heading("#3", text = "Address")
tree_pdata.column("#3", width = 200, anchor = 'n')

tree_pdata.heading("#4", text = "Phone number")
tree_pdata.column("#4", width = 160, anchor = 'n')

tree_pdata.heading("#5", text = "Gender")
tree_pdata.column("#5", width = 70, anchor = 'n')

tree_pdata.heading("#6", text = "Age")
tree_pdata.column("#6", width = 70, anchor = 'n')

tree_pdata.heading("#7", text = "Nature of Illness")
tree_pdata.column("#7", width = 130, anchor = 'n')

tree_pdata.heading("#8", text = "Occupation")
tree_pdata.column("#8", width = 140, anchor = 'n')

tree_pdata.heading("#9", text = "Genotype")
tree_pdata.column("#9", width = 100, anchor = 'n')

tree_pdata.heading("#10", text = "Status")
tree_pdata.column("#10", width = 140, anchor = 'n')


scroll = Scrollbar(tab_pdata, command = tree_pdata.yview)
scroll.grid(row = 12, column = 9, sticky=NS, padx = (250,0))
view_record_pdata()



#========================PATIENTS' APPOINTMENT==================================#
#=========================================================================


#==============================FUNCTIONS===========================================

def run_query(query,parameters=()):
	conn = sqlite3.connect("medical.db")
	cur = conn.cursor()
	query_result = cur.execute(query,parameters)
	conn.commit()
	return query_result


def view_record_app():
	record = tree_app.get_children()
	for element in record:
		tree_app.delete(element)
	query = "SELECT * FROM appointment"
	run_query(query)
	connect = run_query(query)
	for data in connect:
		tree_app.insert("",10000, text = data[0], value = data[1:])


def validation():
	return len(entry_name_app.get())!=0 and len(entry_app.get())!=0 and len(entry_time_app.get())!=0 and len(entry_date_app.get())!=0 and len(entry_status_app.get())!=0 

def add_record_app():
	if validation:
		query = "INSERT INTO appointment VALUES(NULL,?,?,?,?,?)"
		parameters = (entry_name_app.get(), entry_app.get(),entry_time_app.get(),entry_date_app.get(),entry_status_app.get())
		run_query(query,parameters)
		display_app["text"] = "New Record added"

		entry_name_app.delete(0,END)
		entry_app.delete(0,END)
		entry_time_app.delete(0,END)
		entry_date_app.delete(0,END)
		entry_status_app.delete(0,END)

	else:
		display_app['text'] = "Please fill all fields"

	view_record_app()

def add():
	pop = messagebox.askquestion("Adding New Record","Do you want to add new record?")
	if pop == "yes":
		add_record_app()
	else:
		display_app["text"] = "Item not added"
	view_record_app()


def delete_record_app():
	try:
		tree_app.item(tree_app.selection())['values'][1]
		query = "DELETE FROM appointment WHERE ID=?"
		number = tree_app.item(tree_app.selection())['text']
		run_query(query,(number,))
		display_app['text'] = "Record {} deleted".format(entry_name.get())
	except IndexError as e:
		display_app["text"] = "Please select a record to delete"

	view_record_app()  

def delete():
	pop = messagebox.askquestion("Deleting Record","Do you want to delete record?, This action cannot be reversed")
	if pop == "yes":
		delete_record_app()
	else:
		display_app["text"] = "Item not deleted"


def edit_box_app():
	global new_edit
	try:
		tree_app.item(tree_app.selection())['values'][0]
	except IndexError as e:
		display_app['text'] = "Please select a record to edit"

	name_text_app = tree_app.item(tree_app.selection())["values"][0]
	app_text = tree_app.item(tree_app.selection())["values"][1]
	time_text_app = tree_app.item(tree_app.selection())["values"][2]
	date_text_app = tree_app.item(tree_app.selection())["values"][3]
	status_text_app = tree_app.item(tree_app.selection())["values"][4]

	new_edit = Toplevel()

	Label(new_edit, text = "Old Full name").grid(row = 0, column = 0)
	Entry(new_edit,textvariable=StringVar(new_edit,name_text_app),state = "readonly").grid(row = 0, column = 1)
	Label(new_edit, text = "New Full name").grid(row = 1, column = 0)
	new_name_app = Entry(new_edit)
	new_name_app.grid(row = 1, column = 1)

	Label(new_edit, text = "Old Appointment with").grid(row = 2, column = 0)
	Entry(new_edit,textvariable=StringVar(new_edit,app_text),state = "readonly").grid(row = 2, column = 1)
	Label(new_edit, text = "New Appointment with").grid(row = 3, column = 0)
	new_app = Entry(new_edit)
	new_app.grid(row = 3, column = 1)

	Label(new_edit, text = "Old Time").grid(row = 4, column = 0)
	Entry(new_edit,textvariable=StringVar(new_edit,time_text_app),state = "readonly").grid(row = 4, column = 1)
	Label(new_edit, text = "New Time").grid(row = 5, column = 0)
	new_time_app = Entry(new_edit)
	new_time_app.grid(row = 5, column = 1)

	Label(new_edit, text = "Old Date").grid(row = 6, column = 0)
	Entry(new_edit,textvariable=StringVar(new_edit,date_text_app),state = "readonly").grid(row = 6, column = 1)
	Label(new_edit, text = "New Date").grid(row = 7, column = 0)
	new_date_app = DateEntry(new_edit,state = "readonly")
	new_date_app.grid(row = 7, column = 1)

	Label(new_edit, text = "Old Status").grid(row = 8, column = 0)
	Entry(new_edit,textvariable=StringVar(new_edit,status_text_app),state = "readonly").grid(row = 8, column = 1)
	Label(new_edit, text = "New Status").grid(row = 9, column = 0)
	new_status_app = ttk.Combobox(new_edit,state = "readonly")
	new_status_app['values'] = ("Completed","Pending","Cancelled","Rescheduled")
	new_status_app.grid(row = 9, column = 1)

	but = Button(new_edit, text = "Save Changes", command = lambda:edit_record_app(new_name_app.get(), name_text_app,new_app.get(),app_text,new_time_app.get(),time_text_app,new_date_app.get(),date_text_app,new_status_app.get(),status_text_app)).grid(row = 11, column = 1)

def edit_record_app(new_name_app,name_text_app,new_app,app_text,new_time_app,time_text_app,new_date_app,date_text_app,new_status_app,status_text_app):
	query = "UPDATE appointment SET name = ?, appointment = ?, timee = ?, datee = ?, status = ? WHERE name=? AND appointment=? AND timee=? AND datee=? AND status=?"
	parameters = (new_name_app,new_app,new_time_app,new_date_app,new_status_app,name_text_app,app_text,time_text_app,date_text_app,status_text_app)
	run_query(query,parameters)
	new_edit.destroy()
	display_app['text'] = "Record has been modified"
	view_record_app()

	new_edit.mainloop()


#==============================IMAGE AND HEADER===========================================

frame_app = LabelFrame(tab_app, text = "Enter New Appointment", font = "Calibri 9 bold")
frame_app.grid(row = 1, column = 0, padx = 50, pady = 20)

image_app = ImageTk.PhotoImage(Image.open("C:\\Users\\KURUS\\Desktop\\Hospital App\\doctors appointment1.jpg"))
image_app_label = Label(tab_app, image = image_app, width = 600, height = 410)
image_app_label.grid(row = 1, column = 3, pady = 20)



#============================LABELS=================================

topic_app = Label(tab_app, text = "HOSPITAL APPOINTMENT", font = "Georgia 35 bold", fg = "firebrick")
topic_app.grid(row = 0, column = 0)


name = Label(frame_app, text = "Full name:", font = "Georgia 12 bold")
name.grid(row = 0, column = 0, pady = 20)

app = Label(frame_app, text = "Appointment with:", font = "Georgia 12 bold")
app.grid(row = 1, column = 0, padx = 10, pady = 20)

time = Label(frame_app, text = "Time:", font = "Georgia 12 bold")
time.grid(row = 2, column = 0, pady = 20)

date = Label(frame_app, text = "Date:", font = "Georgia 12 bold")
date.grid(row = 3, column = 0, pady = 20)

status = Label(frame_app, text = "Status:", font = "Georgia 12 bold")
status.grid(row = 4, column = 0, pady = 20)



#==========================ENTRIES=================================

name_text = StringVar()
entry_name_app = Entry(frame_app, textvariable=name_text,bd=3, width = 40)
entry_name_app.grid(row = 0, column = 1)

app_text = StringVar()
entry_app = Entry(frame_app, textvariable=app_text,bd=3, width = 40)
entry_app.grid(row = 1, column = 1)

time_text = StringVar()
entry_time_app = Entry(frame_app, textvariable=time_text,bd=3, width = 20)
entry_time_app.grid(row = 2, column = 1)

date_text = StringVar()
entry_date_app = DateEntry(frame_app, textvariable=date_text,bd=3, width = 20)
entry_date_app.grid(row = 3, column = 1)

status_text = StringVar()
entry_status_app = ttk.Combobox(frame_app, textvariable=status_text,width = 20)
entry_status_app['values'] = ("Completed","Pending","Cancelled","Rescheduled")
entry_status_app.grid(row = 4, column = 1)


#==========================BUTTONS=================================

but_add = Button(frame_app, text = "Add New Record",  cursor = "hand2", bg = "#51a66f",fg = "white",font = "Georgia 12 bold", bd = 3, command = add)
but_add.grid(row = 5, column = 1, pady = 10)

but_edit = Button(frame_app, text = "Edit Record",  cursor = "hand2",bg = "#13264a",fg = "white",font = "Georgia 12 bold", bd = 3, command = edit_box_app)
but_edit.grid(row = 5, column = 0, pady = 10)

but_del = Button(frame_app, text = "Delete Record",  cursor = "hand2",bg = "#8c1c0f",fg = "white",font = "Georgia 12 bold", bd = 3, command = delete)
but_del.grid(row = 5, column = 2, padx = 10, pady = 10)

display_app = Label(frame_app, text = "", fg = "navy",font = "arial 9 bold italic")
display_app.grid(row = 6, column = 1)



tree_app = ttk.Treeview(tab_app, height = 13, column = ["","","","",""])
tree_app.grid(row = 7, column = 0, columnspan = 10)

style_app = ttk.Style()
style_app.configure("Treeview.Heading", font = "Helvetica 12 bold")
style_app.configure("Treeview", font = "times 9 bold")



tree_app.heading("#0", text = "ID")
tree_app.column("#0", width = 50, anchor = 'n')

tree_app.heading("#1", text = "Full name")
tree_app.column("#1", width = 150, anchor = 'n')

tree_app.heading("#2", text = "Appointment with")
tree_app.column("#2", width = 250, anchor = 'n')

tree_app.heading("#3", text = "Time")
tree_app.column("#3", width = 120, anchor = 'n')

tree_app.heading("#4", text = "Date")
tree_app.column("#4", width = 120, anchor = 'n')

tree_app.heading("#5", text = "Status")
tree_app.column("#5", width = 120, anchor = 'n')

view_record_app()

scroll_app = Scrollbar(tab_app, command = tree_app.yview)
scroll_app.grid(row = 7, column = 3, padx = (145,0), sticky = NS)





#========================PATIENTS' APPOINTMENT==================================#
#=========================================================================
#================================FUNCTIONS=========================================


def run_query(query,parameters=()):
	conn = sqlite3.connect("medical.db")
	cur = conn.cursor()
	query_result = cur.execute(query,parameters)
	conn.commit()
	return query_result

def view_record_pres():
	record = tree_pres.get_children()
	for element in record:
		tree_pres.delete(element)
	query = "SELECT * FROM prescription"
	connect = run_query(query)
	for data in connect:
		tree_pres.insert("", 10000, text = data[0], values = data[1:])


def validation():
	return len(entry_pat_name.get())!=0 and len(entry_drug_prescribed.get())!=0 and len(entry_prescribed_by.get())!=0 and len(entry_date_pres.get())!=0 and len(entry_time_pres.get())!=0


def add_record_pres():
	if validation:
		query = "INSERT INTO prescription VALUES(NULL,?,?,?,?,?)"
		parameters = (entry_pat_name.get(),entry_drug_prescribed.get(),entry_prescribed_by.get(),entry_date_pres.get(),entry_time_pres.get())
		run_query(query,parameters)
		display_pres["text"] = "Record {} has been added".format(entry_pat_name.get())

		entry_pat_name.delete(0,END)
		entry_drug_prescribed.delete(0,END)
		entry_prescribed_by.delete(0,END)
		entry_date_pres.delete(0,END)
		entry_time_pres.delete(0,END)

	else:
		display_pres["text"] = "Please fill all fields"

def add():
	pop = messagebox.askquestion("Adding New Record","Do you want to add this record?")
	if pop=="yes":
		add_record_pres()
	else:
		display_pres['text'] = "Record not added"

	view_record_pres()


def delete_record_pres():
	try:
		tree_pres.item(tree_pres.selection())["values"][1]
		query = "DELETE FROM prescription WHERE ID=?"
		number = tree_pres.item(tree_pres.selection())["text"]
		run_query(query,(number,))
		display_pres['text'] = "Record {} has been deleted".format(entry_pat_name.get())

	except IndexError as e:
		display_pres['text'] = "Please select a record to delete"

	view_record_pres()


def delete():
	pop = messagebox.askquestion("Deleting Item???","Do you want to delete this record, this action cannot be reversed")
	if pop == "yes":
		delete_record_pres()
	else:
		display_pres['text'] = "Record not deleted"



def edit_box_pres():
	global new_edit
	try:
		tree_pres.item(tree_pres.selection())['values'][0]
	except IndexError as e:
		display_pres['text'] = "Please select a record to edit"
	pat_text = tree_pres.item(tree_pres.selection())['values'][0]
	drug_text = tree_pres.item(tree_pres.selection())['values'][1]
	pres_text = tree_pres.item(tree_pres.selection())['values'][2]
	time_text = tree_pres.item(tree_pres.selection())['values'][3]
	date_text = tree_pres.item(tree_pres.selection())['values'][4]

	new_edit = Toplevel()
	Label(new_edit, text = "Old Full name").grid(row = 0, column = 0)
	Entry(new_edit, textvariable=StringVar(new_edit,pat_text),state = "readonly").grid(row = 0, column = 1)
	Label(new_edit, text = "New Full name").grid(row = 1, column = 0)
	new_pat = Entry(new_edit)
	new_pat.grid(row = 1, column = 1)

	Label(new_edit, text = "Old Drugs Prescribed").grid(row = 2, column = 0)
	Entry(new_edit, textvariable=StringVar(new_edit,drug_text),state = "readonly").grid(row = 2, column = 1)
	Label(new_edit, text = "New Drugs Prescribed").grid(row = 3, column = 0)
	new_drug = Entry(new_edit)
	new_drug.grid(row = 3, column = 1)

	Label(new_edit, text = "Old Prescribed by").grid(row = 4, column = 0)
	Entry(new_edit, textvariable=StringVar(new_edit,pres_text),state = "readonly").grid(row = 4, column = 1)
	Label(new_edit, text = "New Prescribed by").grid(row = 5, column = 0)
	new_pres = Entry(new_edit)
	new_pres.grid(row = 5, column = 1)

	Label(new_edit, text = "Old Date").grid(row = 6, column = 0)
	Entry(new_edit, textvariable=StringVar(new_edit,time_text),state = "readonly").grid(row = 6, column = 1)
	Label(new_edit, text = "New Date").grid(row = 7, column = 0)
	new_time = DateEntry(new_edit)
	new_time.grid(row = 7, column = 1)

	Label(new_edit, text = "Old Time").grid(row = 8, column = 0)
	Entry(new_edit, textvariable=StringVar(new_edit,date_text),state = "readonly").grid(row = 8, column = 1)
	Label(new_edit, text = "New Time").grid(row = 9, column = 0)
	new_date = Entry(new_edit)
	new_date.grid(row = 9, column = 1)

	Button(new_edit, text = "Save Changes", command = lambda:edit_record_pres(new_pat.get(), pat_text, new_drug.get(), drug_text,new_pres.get(),pres_text,new_time.get(),time_text,new_date.get(),date_text)).grid(row = 10, column = 1)

	new_edit.mainloop()

def edit_record_pres(new_pat,pat_text,new_drug,drug_text,new_pres,pres_text,new_time,time_text,new_date,date_text):
	query = "UPDATE prescription SET name = ?, drugs = ?, prescribe = ?, datee = ?, timee = ? WHERE  name = ? and drugs = ? and prescribe = ? and datee = ? and timee = ?"
	parameters = (new_pat,new_drug,new_pres,new_time,new_date,pat_text,drug_text,pres_text,time_text,date_text)
	run_query(query,parameters)
	new_edit.destroy()
	display_pres['text'] = "Record has been updated"
	view_record_pres()



#==============================IMAGE AND HEADER===========================================

topic_pres = Label(tab_pres, text = "PRESCRIPTIONS", font = "Garamond 35 bold italic underline", fg = "maroon", bg = "lightgrey")
topic_pres.grid(row = 0, column = 0, padx = (170,0))


img_pres = ImageTk.PhotoImage(Image.open("C:\\Users\\KURUS\\Desktop\\Hospital App\\prescription1.jpg"))
img_pres_label = Label(tab_pres, image = img_pres, height = 350)
img_pres_label.grid(row = 1, column = 1, padx = (170,0), pady = 10)


frame_pres = LabelFrame(tab_pres, text = "Add new prescription", bd = 4, bg = "seagreen", padx = 20, pady = 20)
frame_pres.grid(row = 1, column = 0, padx = (70,0), pady = 10)


#================================LABELS=========================================

patient_name = Label(frame_pres, text = "Patient name:", fg = "white", bg = "seagreen",font = "Garamond 13 bold italic")
patient_name.grid(row = 1, column = 0, padx = 10, pady = 10)

drug_prescribed = Label(frame_pres, text = "Drugs Prescribed:",  fg = "white",  bg = "seagreen",font = "Garamond 13 bold italic")
drug_prescribed.grid(row = 2, column = 0, padx = 10, pady = 10)

prescribed_by = Label(frame_pres, text = "Prescribed by:",  fg = "white",  bg = "seagreen",font = "Garamond 13 bold italic")
prescribed_by.grid(row = 3, column = 0, padx = 10, pady = 10)

date_prescribed = Label(frame_pres, text = "Date:",  fg = "white",  bg = "seagreen",font = "Garamond 13 bold italic")
date_prescribed.grid(row = 4, column = 0, padx = 10, pady = 10)

time_prescribed = Label(frame_pres, text = "Time:",  fg = "white",  bg = "seagreen",font = "Garamond 13 bold italic")
time_prescribed.grid(row = 5, column = 0, padx = 10, pady = 10)


#================================ENTRIES=========================================

pat_text = StringVar()
entry_pat_name = Entry(frame_pres, textvariable = pat_text, width = 40, bd=3)
entry_pat_name.grid(row = 1, column = 1)

drug_text = StringVar()
entry_drug_prescribed = Entry(frame_pres, textvariable = drug_text, width = 40, bd=3)
entry_drug_prescribed.grid(row = 2, column = 1)

pres_text = StringVar()
entry_prescribed_by = Entry(frame_pres, textvariable = pres_text, width = 40, bd=3)
entry_prescribed_by.grid(row = 3, column = 1)

date_pres_text = StringVar()
entry_date_pres = DateEntry(frame_pres, textvariable = date_pres_text, width = 20, bd=3)
entry_date_pres.grid(row = 4, column = 1)

time_pres_text = StringVar()
entry_time_pres = Entry(frame_pres, textvariable = time_pres_text, width = 20, bd=3)
entry_time_pres.grid(row = 5, column = 1)


#=============================BUTTONS===================================

add_but_pres = Button(frame_pres, text = "Add Record", cursor = "hand2", bd = 3, bg = "#51a66f", fg = "white", font = "Garamond 13 bold italic", command = add)
add_but_pres.grid(row = 6, column = 1, pady = 5)

edit_but_pres = Button(frame_pres, text = "Edit Record", cursor = "hand2", bd = 3, bg = "#13264a", fg = "white", font = "Garamond 13 bold italic", command = edit_box_pres)
edit_but_pres.grid(row = 6, column = 0, pady = 5)

del_but_pres = Button(frame_pres, text = "Delete Record", cursor = "hand2", bd = 3, bg = "#8c1c0f", fg = "white", font = "Garamond 13 bold italic", command = delete)
del_but_pres.grid(row = 6, column = 2, pady = 5)

display_pres = Label(frame_pres, text = "", bg = "seagreen", fg = "white", font = "Garamond 9 bold italic")
display_pres.grid(row = 7, column = 1, pady = 5)

#=============================TREEVIEW===================================

tree_pres = ttk.Treeview(tab_pres, height = 16, column = ["","","","",""])
tree_pres.grid(row = 8, column = 0, columnspan = 10, padx = (70,0),pady = 10)

tree_pres.heading("#0",text = "ID")
tree_pres.column("#0", width = 80, anchor = 'n')

tree_pres.heading("#1",text = "Patient's name")
tree_pres.column("#1", width = 250, anchor = 'n')

tree_pres.heading("#2",text = "Drugs Prescribed")
tree_pres.column("#2", width = 250, anchor = 'n')

tree_pres.heading("#3",text = "Prescribed by")
tree_pres.column("#3", width = 150, anchor = 'n')

tree_pres.heading("#4",text = "Date")
tree_pres.column("#4", width = 100, anchor = 'n')

tree_pres.heading("#5",text = "Time")
tree_pres.column("#5", width = 100, anchor = 'n')
view_record_pres()

style_pres = ttk.Style(tab_pres)
style_pres.configure("Treeview.Heading", font = "Garamond 14 bold italic")
style_pres.configure("Treeview", font = "Garamond 10 bold italic")

scroll_pres = Scrollbar(tab_pres, command = tree_pres.yview)
scroll_pres.grid(row=8, column = 1, padx = (380,0), sticky=NS)




#========================HOSPITAL INVENTORY==================================#
#=========================================================================

#==============================FUNCTIONS======================================

def run_query(query,parameters=()):
	conn = sqlite3.connect("medical.db")
	cur = conn.cursor()
	query_result = cur.execute(query,parameters)
	conn.commit()
	return query_result

def view_record_inv():
	record = tree_inv.get_children()
	for element in record:
		tree_inv.delete(element)
	query = "SELECT * FROM inventory"
	connect = run_query(query)
	for data in connect:
		tree_inv.insert("", 10000, text = data[0], values = data[1:])


def validation():
	return len(entry_inv.get())!=0 and len(entry_date_inv.get())!=0 and len(entry_qty_inv.get())!=0 and len(entry_price_inv.get())!=0 and len(entry_total_price.get())!=0 and len(entry_qty_left.get())!=0 and len(entry_total_qty.get())!=0


def add_record_inv():
	if validation:
		query = "INSERT INTO inventory VALUES(NULL,?,?,?,?,?,?,?)"
		parameters = (entry_inv.get(),entry_date_inv.get(),entry_qty_inv.get(),entry_price_inv.get(),entry_total_price.get(),entry_qty_left.get(),entry_total_qty.get())
		run_query(query,parameters)
		display_inv["text"] = "Record {} has been added".format(entry_inv.get())

		entry_inv.delete(0,END)
		entry_date_inv.delete(0,END)
		entry_qty_inv.delete(0,END)
		entry_price_inv.delete(0,END)
		entry_total_price.delete(0,END)
		entry_qty_left.delete(0,END)
		entry_total_qty.delete(0,END)

	else:
		display_inv["text"] = "Please fill all fields"

def add():
	pop = messagebox.askquestion("Adding New Record","Do you want to add this record?")
	if pop=="yes":
		add_record_inv()
	else:
		display_inv['text'] = "Record not added"

	view_record_inv()


def delete_record_inv():
	try:
		tree_inv.item(tree_inv.selection())["values"][1]
		query = "DELETE FROM inventory WHERE ID=?"
		number = tree_inv.item(tree_inv.selection())["text"]
		run_query(query,(number,))
		display_inv['text'] = "Record {} has been deleted".format(entry_inv.get())

	except IndexError as e:
		display_inv['text'] = "Please select a record to delete"

	view_record_inv()

def delete():
	pop = messagebox.askquestion("Deleting Record?","Do you want to delete this record? Action cannot be reversed")
	if pop=="yes":
		delete_record_inv()
	else:
		display_inv['text'] = "Record not deleted"

	view_record_inv()

def edit_box_inv():
	global new_edit
	try:
		tree_inv.item(tree_inv.selection())['values'][0]
	except IndexError as e:
		display_inv['text'] = "Please select a record to edit"
	inv_text = tree_inv.item(tree_inv.selection())['values'][0]
	date_p_text = tree_inv.item(tree_inv.selection())['values'][1]
	qty_p_text = tree_inv.item(tree_inv.selection())['values'][2]
	price_p_text = tree_inv.item(tree_inv.selection())['values'][3]
	total_price_text = tree_inv.item(tree_inv.selection())['values'][4]
	qty_left_text = tree_inv.item(tree_inv.selection())['values'][5]
	total_qty_text = tree_inv.item(tree_inv.selection())['values'][6]

	new_edit = Toplevel()
	Label(new_edit, text = "Old Inventory").grid(row = 0, column = 0)
	Entry(new_edit, textvariable=StringVar(new_edit,inv_text),state = "readonly").grid(row = 0, column = 1)
	Label(new_edit, text = "New Inventory").grid(row = 1, column = 0)
	new_inv = Entry(new_edit)
	new_inv.grid(row = 1, column = 1)

	Label(new_edit, text = "Old Date").grid(row = 2, column = 0)
	Entry(new_edit, textvariable=StringVar(new_edit,date_p_text),state = "readonly").grid(row = 2, column = 1)
	Label(new_edit, text = "New Date").grid(row = 3, column = 0)
	new_date = DateEntry(new_edit)
	new_date.grid(row = 3, column = 1)

	Label(new_edit, text = "Old Quantity Purchased").grid(row = 4, column = 0)
	Entry(new_edit, textvariable=StringVar(new_edit,qty_p_text),state = "readonly").grid(row = 4, column = 1)
	Label(new_edit, text = "New Quantity Purchased").grid(row = 5, column = 0)
	new_qty = Entry(new_edit)
	new_qty.grid(row = 5, column = 1)

	Label(new_edit, text = "Old Price/Qty").grid(row = 6, column = 0)
	Entry(new_edit, textvariable=StringVar(new_edit,price_p_text),state = "readonly").grid(row = 6, column = 1)
	Label(new_edit, text = "New Price/Qty").grid(row = 7, column = 0)
	new_price = Entry(new_edit)
	new_price.grid(row = 7, column = 1)

	Label(new_edit, text = "Old Total Price/Qty").grid(row = 8, column = 0)
	Entry(new_edit, textvariable=StringVar(new_edit,total_price_text),state = "readonly").grid(row = 8, column = 1)
	Label(new_edit, text = "New Total Price/Qty").grid(row = 9, column = 0)
	new_price1 = Entry(new_edit)
	new_price1.grid(row = 9, column = 1)

	Label(new_edit, text = "Old Qty Before").grid(row = 10, column = 0)
	Entry(new_edit, textvariable=StringVar(new_edit,qty_left_text),state = "readonly").grid(row = 10, column = 1)
	Label(new_edit, text = "New Qty Before").grid(row = 11, column = 0)
	new_qty1 = Entry(new_edit)
	new_qty1.grid(row = 11, column = 1)

	Label(new_edit, text = "Old Qty After").grid(row = 12, column = 0)
	Entry(new_edit, textvariable=StringVar(new_edit,total_qty_text),state = "readonly").grid(row = 12, column = 1)
	Label(new_edit, text = "New Qty After").grid(row = 13, column = 0)
	new_qty2 = Entry(new_edit)
	new_qty2.grid(row = 13, column = 1)

	Button(new_edit, text = "Save Changes", command = lambda:edit_record(new_inv.get(), inv_text, new_date.get(), date_p_text,new_qty.get(),qty_p_text,new_price.get(),price_p_text,new_price1.get(),total_price_text, new_qty1.get(), qty_left_text,  new_qty2.get(), total_qty_text)).grid(row = 14, column = 1)

	new_edit.mainloop()

def edit_record(new_inv,inv_text,new_date,date_p_text,new_qty,qty_p_text,new_price,price_p_text,new_price1,total_price_text,new_qty1,qty_left_text,new_qty2,total_qty_text):
	query = "UPDATE inventory SET inventory = ?, datee = ?, qty1 = ?, price1 = ?, price2 = ?, qty2 = ?, qty3 = ? WHERE  inventory = ? and datee = ? and qty1 = ? and price1 = ? and price2 = ? and qty2 = ? and qty3 = ? "
	parameters = (new_inv,new_date,new_qty,new_price,new_price1,new_qty1,new_qty2,inv_text,date_p_text,qty_p_text,price_p_text,total_price_text,qty_left_text,total_qty_text)
	run_query(query,parameters)
	new_edit.destroy()
	display_inv['text'] = "Record has been updated"
	view_record_inv()



#========================IMAGE AND HEADER=========================================

topic_inv = Label(tab_inv, text = "HOSPITAL INVENTORY", fg = "firebrick", font = "Helvetica 30 bold underline")
topic_inv.grid(row = 0, column = 0, pady = 10)

frame_inv = LabelFrame(tab_inv, text = "Add New Inventory",bd = 4, bg = "chartreuse")
frame_inv.grid(row = 1, column = 0, padx = 10)

img_inv = ImageTk.PhotoImage(Image.open("C:\\Users\\KURUS\\Desktop\\Hospital App\\Hospital-Inventory.jpg"))
img_inv_label = Label(tab_inv, image = img_inv, width = 650, height = 430)
img_inv_label.grid(row=1, column = 2)



#========================LABEL=========================================

inv = Label(frame_inv, text = "Inventory:", font = "Rockwell 13 bold",bg = "chartreuse")
inv.grid(row = 0, column = 0, pady = 10)

date_purchased = Label(frame_inv, text = "Date Purchased:", font = "Rockwell 13 bold",bg = "chartreuse")
date_purchased.grid(row = 1, column = 0, pady = 10)

qty_purchased = Label(frame_inv, text = "Quantity Purchased:", font = "Rockwell 13 bold",bg = "chartreuse")
qty_purchased.grid(row = 2, column = 0, pady = 10)

price_per_qty = Label(frame_inv, text = "Price per Qty Purchased:", font = "Rockwell 13 bold",bg = "chartreuse")
price_per_qty.grid(row = 3, column = 0, pady = 10)

total_price = Label(frame_inv, text = "Total Price for Purchase:", font = "Rockwell 13 bold",bg = "chartreuse")
total_price.grid(row = 4, column = 0, pady = 10)

qty_left = Label(frame_inv, text = "Quantity left before Purchase:", font = "Rockwell 13 bold",bg = "chartreuse")
qty_left.grid(row = 5, column = 0, pady = 10)

total_qty = Label(frame_inv, text = "Total Quantity left after Purchase:", font = "Rockwell 13 bold",bg = "chartreuse")
total_qty.grid(row = 6, column = 0, pady = 10)


#========================ENTRIES=========================================

inv_text = StringVar()
entry_inv = Entry(frame_inv,textvariable = inv_text, width = 40, bd = 3)
entry_inv.grid(row = 0, column = 1)

date_p_text = StringVar()
entry_date_inv = DateEntry(frame_inv,textvariable = date_p_text, width = 20, bd = 3)
entry_date_inv.grid(row = 1, column = 1)

qty_p_text = StringVar()
entry_qty_inv = Entry(frame_inv,textvariable = qty_p_text, width = 20, bd = 3)
entry_qty_inv.grid(row = 2, column = 1)


price_p_text = StringVar()
entry_price_inv = Entry(frame_inv,textvariable = price_p_text, width = 20, bd = 3)
entry_price_inv.grid(row = 3, column = 1)

total_price_text = StringVar()
entry_total_price= Entry(frame_inv,textvariable = total_price_text, width = 20, bd = 3)
entry_total_price.grid(row = 4, column = 1)

qty_left_text = StringVar()
entry_qty_left = Entry(frame_inv,textvariable = qty_left_text, width = 20, bd = 3)
entry_qty_left.grid(row = 5, column = 1)

total_qty_text = StringVar()
entry_total_qty = Entry(frame_inv,textvariable = total_qty_text, width = 20, bd = 3)
entry_total_qty.grid(row = 6, column = 1)



#========================BUTTONS=========================================

add_button_inv = Button(frame_inv, text = "Add Record",font = "Rockwell 12 bold",bg = "#51a66f",  fg = "white", bd = 3, cursor = "hand2", command = add)
add_button_inv.grid(row = 7, column = 1 ,padx = (0,90), pady = 10)

edit_button_inv = Button(frame_inv, text = "Edit Record",font = "Rockwell 12 bold",bg = "#13264a",  fg = "white", bd = 3, cursor = "hand2", command = edit_box_inv)
edit_button_inv.grid(row = 7, column = 0 ,pady = 10)

del_button_inv = Button(frame_inv, text = "Delete Record",font = "Rockwell 12 bold",bg = "#8c1c0f", fg = "white", bd = 3, cursor = "hand2", command = delete)
del_button_inv.grid(row = 7, column = 2 ,padx = 10, pady = 10)

display_inv = Label(frame_inv, text = "", font = "Garamond 10 bold italic",bg = "chartreuse", fg = "navy")
display_inv.grid(row = 8, column = 1 ,pady = 10)



#========================TREEVIEW AND SCROLLBAR=========================================

tree_inv = ttk.Treeview(tab_inv, height = 12, column = ["","","","","","",""])
tree_inv.grid(row = 9, column = 0, columnspan = 10, padx = 10,pady = 20, sticky = W)

tree_inv.heading("#0",text = "ID")
tree_inv.column("#0", width = 100, anchor = "n")

tree_inv.heading("#1",text = "Inventory")
tree_inv.column("#1", width = 250, anchor = "n")

tree_inv.heading("#2",text = "Date Purchased")
tree_inv.column("#2", width = 160, anchor = "n")

tree_inv.heading("#3",text = "Qty Purchased")
tree_inv.column("#3", width = 160, anchor = "n")

tree_inv.heading("#4",text = "Price/Qty")
tree_inv.column("#4", width = 100, anchor = "n")

tree_inv.heading("#5",text = "Total Price/Qty")
tree_inv.column("#5", width = 200, anchor = "n")

tree_inv.heading("#6",text = "Qty Before")
tree_inv.column("#6", width = 120, anchor = "n")

tree_inv.heading("#7",text = "Qty After")
tree_inv.column("#7", width = 120, anchor = "n")
view_record_inv()

style_inv = ttk.Style()
style_inv.configure("Treeview.Heading", font = "Rockwell 12 bold")
style_inv.configure("Treeview", font = "Rockwell 9 bold")

scroll_inv = Scrollbar(tab_inv, command = tree_inv.yview)
scroll_inv.grid(row = 9, column = 2, padx = (380,0), sticky=NS)


#========================PATIENT BILLING RECORD==================================#
#=====================================================================================

#==============================FUNCTIONS======================================

def run_query(query,parameters=()):
	conn = sqlite3.connect("medical.db")
	cur = conn.cursor()
	query_result = cur.execute(query,parameters)
	conn.commit()
	return query_result

def view_record_bill():
	record = tree_bill.get_children()
	for element in record:
		tree_bill.delete(element)
	query = "SELECT * FROM billing"
	connect = run_query(query)
	for data in connect:
		tree_bill.insert("", 10000, text = data[0], values = data[1:])


def validation():
	return len(entry_name_bill.get())!=0 and len(entry_amount_paid.get())!=0 and len(entry_paid_for.get())!=0 and len(entry_mode.get())!=0 and len(entry_issued_by.get())!=0 and len(entry_date_bill.get())!=0 and len(entry_status_bill.get())!=0


def add_record_bill():
	if validation:
		query = "INSERT INTO billing VALUES(NULL,?,?,?,?,?,?,?)"
		parameters = (entry_name_bill.get(),entry_amount_paid.get(),entry_paid_for.get(),entry_mode.get(),entry_issued_by.get(),entry_date_bill.get(),entry_status_bill.get())
		run_query(query,parameters)
		display_bill["text"] = "Record {} has been added".format(entry_name_bill.get())

		entry_name_bill.delete(0,END)
		entry_amount_paid.delete(0,END)
		entry_paid_for.delete(0,END)
		entry_mode.delete(0,END)
		entry_issued_by.delete(0,END)
		entry_date_bill.delete(0,END)
		entry_status_bill.delete(0,END)

	else:
		display_bill["text"] = "Please fill all fields"

def add():
	pop = messagebox.askquestion("Adding New Record","Do you want to add this record?")
	if pop=="yes":
		add_record_bill()
	else:
		display_bill['text'] = "Record not added"

	view_record_bill()


def delete_record_bill():
	try:
		tree_bill.item(tree_bill.selection())["values"][1]
		query = "DELETE FROM billing WHERE ID=?"
		number = tree_bill.item(tree_bill.selection())["text"]
		run_query(query,(number,))
		display_bill['text'] = "Record {} has been deleted".format(entry_inv.get())

	except IndexError as e:
		display_bill['text'] = "Please select a record to delete"

	view_record_bill()

def delete():
	pop = messagebox.askquestion("Deleting Record?","Do you want to delete this record? Action cannot be reversed")
	if pop=="yes":
		delete_record_bill()
	else:
		display_bill['text'] = "Record not deleted"

	view_record_inv()

def edit_box_bill():
	global new_edit
	try:
		tree_bill.item(tree_bill.selection())['values'][0]
	except IndexError as e:
		display_bill['text'] = "Please select a record to edit"
	name_text = tree_bill.item(tree_bill.selection())['values'][0]
	amount_text = tree_bill.item(tree_bill.selection())['values'][1]
	items_text = tree_bill.item(tree_bill.selection())['values'][2]
	mode_text = tree_bill.item(tree_bill.selection())['values'][3]
	issued_text = tree_bill.item(tree_bill.selection())['values'][4]
	date_text = tree_bill.item(tree_bill.selection())['values'][5]
	status_text = tree_bill.item(tree_bill.selection())['values'][6]

	new_edit = Toplevel()
	Label(new_edit, text = "Old Full name").grid(row = 0, column = 0)
	Entry(new_edit, textvariable=StringVar(new_edit,name_text),state = "readonly").grid(row = 0, column = 1)
	Label(new_edit, text = "New Full name").grid(row = 1, column = 0)
	new_name = Entry(new_edit)
	new_name.grid(row = 1, column = 1)

	Label(new_edit, text = "Old Amount Paid").grid(row = 2, column = 0)
	Entry(new_edit, textvariable=StringVar(new_edit,amount_text),state = "readonly").grid(row = 2, column = 1)
	Label(new_edit, text = "New Amount Paid").grid(row = 3, column = 0)
	new_amount = Entry(new_edit)
	new_amount.grid(row = 3, column = 1)

	Label(new_edit, text = "Old Items Paid For").grid(row = 4, column = 0)
	Entry(new_edit, textvariable=StringVar(new_edit,items_text),state = "readonly").grid(row = 4, column = 1)
	Label(new_edit, text = "New Items Paid For").grid(row = 5, column = 0)
	new_items = Entry(new_edit)
	new_items.grid(row = 5, column = 1)

	Label(new_edit, text = "Old Mode of Payment").grid(row = 6, column = 0)
	Entry(new_edit, textvariable=StringVar(new_edit,mode_text),state = "readonly").grid(row = 6, column = 1)
	Label(new_edit, text = "New Mode of Payment").grid(row = 7, column = 0)
	new_mode = ttk.Combobox(new_edit)
	new_mode['values'] = ("Cash","POS","Bank Transfer")
	new_mode.grid(row = 7, column = 1)

	Label(new_edit, text = "Old Bill Issued By").grid(row = 8, column = 0)
	Entry(new_edit, textvariable=StringVar(new_edit,issued_text),state = "readonly").grid(row = 8, column = 1)
	Label(new_edit, text = "New Bill Issued By").grid(row = 9, column = 0)
	new_issued = Entry(new_edit)
	new_issued.grid(row = 9, column = 1)

	Label(new_edit, text = "Old Date").grid(row = 10, column = 0)
	Entry(new_edit, textvariable=StringVar(new_edit,date_text),state = "readonly").grid(row = 10, column = 1)
	Label(new_edit, text = "New Date").grid(row = 11, column = 0)
	new_date = DateEntry(new_edit)
	new_date.grid(row = 11, column = 1)

	Label(new_edit, text = "Old Status of Payment").grid(row = 12, column = 0)
	Entry(new_edit, textvariable=StringVar(new_edit,status_text),state = "readonly").grid(row = 12, column = 1)
	Label(new_edit, text = "New Status of Payment").grid(row = 13, column = 0)
	new_status = ttk.Combobox(new_edit)
	new_status['values'] = ("Paid", "Outstanding")
	new_status.grid(row = 13, column = 1)

	Button(new_edit, text = "Save Changes", command = lambda:edit_record(new_name.get(), name_text, new_amount.get(), amount_text,new_items.get(),items_text,new_mode.get(),mode_text,new_issued.get(),issued_text, new_date.get(), date_text,  new_status.get(), status_text)).grid(row = 14, column = 1)

	new_edit.mainloop()

def edit_record(new_name,name_text,new_amount,amount_text,new_items,items_text,new_mode,mode_text,new_issued,issued_text,new_date,date_text,new_status,status_text):
	query = "UPDATE billing SET name = ?, amount = ?, items = ?, mode = ?, bill_by = ?, datee = ?, status = ? WHERE  name = ? and amount = ? and items = ? and mode = ? and bill_by = ? and datee = ? and status = ?"
	parameters = (new_name,new_amount,new_items,new_mode,new_issued,new_date,new_status,name_text,amount_text,items_text,mode_text,issued_text,date_text,status_text)
	run_query(query,parameters)
	new_edit.destroy()
	display_bill['text'] = "Record has been updated"
	view_record_bill()



#========================IMAGE AND HEADER=========================================

topic_bill = Label(tab_bill, text = "PATIENT BILLING RECORD", fg = "firebrick", font = "Helvetica 30 bold underline")
topic_bill.grid(row = 0, column = 0, pady = 10)

frame_bill = LabelFrame(tab_bill, text = "Add New Billing Record",bd = 4, bg = "darkkhaki")
frame_bill.grid(row = 1, column = 0, padx = 10)

img_bill = ImageTk.PhotoImage(Image.open("C:\\Users\\KURUS\\Desktop\\Hospital App\\hospital-bill.jpg"))
img_bill_label = Label(tab_bill, image = img_bill, width = 650, height = 450)
img_bill_label.grid(row=1, column = 2)



#========================LABEL=========================================

name_bill = Label(frame_bill, text = "Full name:", font = "Rockwell 13 bold",bg = "darkkhaki")
name_bill.grid(row = 0, column = 0, pady = 10)

amount_paid = Label(frame_bill, text = "Amount Paid:", font = "Rockwell 13 bold",bg = "darkkhaki")
amount_paid.grid(row = 1, column = 0, pady = 10)

paid_for = Label(frame_bill, text = "Items Paid For:", font = "Rockwell 13 bold",bg = "darkkhaki")
paid_for.grid(row = 2, column = 0, pady = 10)

mode = Label(frame_bill, text = "Mode of Payment:", font = "Rockwell 13 bold",bg = "darkkhaki")
mode.grid(row = 3, column = 0, pady = 10)

issued_by = Label(frame_bill, text = "Bill Issued By:", font = "Rockwell 13 bold",bg = "darkkhaki")
issued_by.grid(row = 4, column = 0, pady = 10)

date_bill = Label(frame_bill, text = "Date:", font = "Rockwell 13 bold",bg = "darkkhaki")
date_bill.grid(row = 5, column = 0, pady = 10)

status_bill = Label(frame_bill, text = "Status of Payment:", font = "Rockwell 13 bold",bg = "darkkhaki")
status_bill.grid(row = 6, column = 0, pady = 10)


#========================ENTRIES=========================================

name_bill_text = StringVar()
entry_name_bill = Entry(frame_bill,textvariable = name_bill_text, width = 40, bd = 3)
entry_name_bill.grid(row = 0, column = 1)

amount_paid_text = StringVar()
entry_amount_paid = Entry(frame_bill,textvariable = amount_paid_text, width = 20, bd = 3)
entry_amount_paid.grid(row = 1, column = 1)

paid_for_text = StringVar()
entry_paid_for = Entry(frame_bill,textvariable = paid_for_text, width = 40, bd = 3)
entry_paid_for.grid(row = 2, column = 1)

mode_text = StringVar()
entry_mode = ttk.Combobox(frame_bill,textvariable = mode_text, width = 20)
entry_mode['values'] = ("Cash","POS","Bank Transfer")
entry_mode.grid(row = 3, column = 1)

issued_by_text = StringVar()
entry_issued_by= Entry(frame_bill,textvariable = issued_by_text, width = 30, bd = 3)
entry_issued_by.grid(row = 4, column = 1)

date_bill_text = StringVar()
entry_date_bill = DateEntry(frame_bill,textvariable = date_bill_text, width = 20, bd = 3)
entry_date_bill.grid(row = 5, column = 1)

status_bill_text = StringVar()
entry_status_bill = ttk.Combobox(frame_bill,textvariable = status_bill_text, width = 20)
entry_status_bill['values'] = ("Paid","Outstanding")
entry_status_bill.grid(row = 6, column = 1)



#========================BUTTONS=========================================

add_button_bill = Button(frame_bill, text = "Add Record",font = "Rockwell 12 bold",bg = "#51a66f",  fg = "white", bd = 3, cursor = "hand2", command = add)
add_button_bill.grid(row = 7, column = 1 ,padx = (0,20), pady = 10)

edit_button_bill = Button(frame_bill, text = "Edit Record",font = "Rockwell 12 bold",bg = "#13264a",  fg = "white", bd = 3, cursor = "hand2", command = edit_box_bill)
edit_button_bill.grid(row = 7, column = 0 ,pady = 10)

del_button_bill = Button(frame_bill, text = "Delete Record",font = "Rockwell 12 bold",bg = "#8c1c0f", fg = "white", bd = 3, cursor = "hand2", command = delete)
del_button_bill.grid(row = 7, column = 2 ,padx = 10, pady = 10)

display_bill = Label(frame_bill, text = "", font = "Garamond 10 bold italic",bg = "darkkhaki", fg = "navy")
display_bill.grid(row = 8, column = 1 ,pady = 10)



#========================TREEVIEW AND SCROLLBAR=========================================

tree_bill = ttk.Treeview(tab_bill, height = 12, column = ["","","","","","",""])
tree_bill.grid(row = 9, column = 0, columnspan = 10, padx = 10,pady = 20, sticky = W)

tree_bill.heading("#0",text = "ID")
tree_bill.column("#0", width = 50, anchor = "n")

tree_bill.heading("#1",text = "Full name")
tree_bill.column("#1", width = 250, anchor = "n")

tree_bill.heading("#2",text = "Amount Paid")
tree_bill.column("#2", width = 130, anchor = "n")

tree_bill.heading("#3",text = "Items Paid For")
tree_bill.column("#3", width = 160, anchor = "n")

tree_bill.heading("#4",text = "Mode of Payment")
tree_bill.column("#4", width = 160, anchor = "n")

tree_bill.heading("#5",text = "Bill Issued By")
tree_bill.column("#5", width = 200, anchor = "n")

tree_bill.heading("#6",text = "Date")
tree_bill.column("#6", width = 70, anchor = "n")

tree_bill.heading("#7",text = "Status of Payment")
tree_bill.column("#7", width = 170, anchor = "n")
view_record_bill()

style_bill = ttk.Style()
style_bill.configure("Treeview.Heading", font = "Rockwell 12 bold")
style_bill.configure("Treeview", font = "Rockwell 9 bold")

scroll_bill = Scrollbar(tab_bill, command = tree_bill.yview)
scroll_bill.grid(row = 9, column = 1, columnspan = 10, padx = (590,0), sticky=NS)





#========================FINANCIAL RECORDS==================================#
#=====================================================================================



topic_fin = Label(tab_fin, text = "FINANCIAL RECORDS", fg = "firebrick", font = "Helvetica 30 bold underline")
topic_fin.grid(row = 0, column = 0, padx = (160,0), pady = 10)

frame_rev = LabelFrame(tab_fin, text = "Add New Revenue Record",bd = 4, bg = "darkolivegreen")
frame_rev.grid(row = 1, column = 0, padx = 10, sticky=N)

frame_exp = LabelFrame(tab_fin, text = "Add New Expense Record",bd = 4, fg = "white", bg = "darkred")
frame_exp.grid(row = 2, column = 0, padx = 10, sticky=N)

frame_net = LabelFrame(tab_fin, text = "Add New Net Record",bd = 4, bg = "darkorange")
frame_net.grid(row = 2, column = 1, padx = 10, sticky=N, columnspan=10)

img_fin = ImageTk.PhotoImage(Image.open("C:\\Users\\KURUS\\Desktop\\Hospital App\\Financial-Reports.png"))
img_fin_label = Label(tab_fin, image = img_fin, width = 650, height = 347)
img_fin_label.grid(row=1, column = 2, columnspan=10)

#============================REVENUE SECTION=========================================================


#==========================FUNCTIONS===========================================================


def run_query(query,parameters=()):
	conn = sqlite3.connect("medical.db")
	cur = conn.cursor()
	query_result = cur.execute(query,parameters)
	conn.commit()
	return query_result

def view_record_rev():
	record = tree_rev.get_children()
	for element in record:
		tree_rev.delete(element)
	query = "SELECT * FROM revenue"
	connect = run_query(query)
	for data in connect:
		tree_rev.insert("", 10000, text = data[0], values = data[1:])


def validation():
	return len(entry_date_rev.get())!=0 and len(entry_amount_rev.get())!=0 and len(entry_mode_rev.get())!=0


def add_record_rev():
	if validation:
		query = "INSERT INTO revenue VALUES(NULL,?,?,?)"
		parameters = (entry_date_rev.get(),entry_amount_rev.get(),entry_mode_rev.get())
		run_query(query,parameters)
		display_rev["text"] = "New Record has been added"

		entry_date_rev.delete(0,END)
		entry_amount_rev.delete(0,END)
		entry_mode_rev.delete(0,END)


	else:
		display_rev["text"] = "Please fill all fields"

def add():
	pop = messagebox.askquestion("Adding New Record","Do you want to add this record?")
	if pop=="yes":
		add_record_rev()
	else:
		display_rev['text'] = "Record not added"

	view_record_rev()


def delete_record_rev():
	try:
		tree_rev.item(tree_rev.selection())["values"][1]
		query = "DELETE FROM revenue WHERE ID=?"
		number = tree_rev.item(tree_rev.selection())["text"]
		run_query(query,(number,))
		display_rev['text'] = "Record {} has been deleted".format(entry_date_rev.get())

	except IndexError as e:
		display_rev['text'] = "Please select a record to delete"

	view_record_rev()

def delete():
	pop = messagebox.askquestion("Deleting Record?","Do you want to delete this record? Action cannot be reversed")
	if pop=="yes":
		delete_record_rev()
	else:
		display_rev['text'] = "Record not deleted"

	view_record_rev()

def edit_box_rev():
	global new_edit
	try:
		tree_rev.item(tree_rev.selection())['values'][0]
	except IndexError as e:
		display_rev['text'] = "Please select a record to edit"
	date_text_rev = tree_rev.item(tree_rev.selection())['values'][0]
	rev_text_rev = tree_rev.item(tree_rev.selection())['values'][1]
	mode_text_rev = tree_rev.item(tree_rev.selection())['values'][2]

	new_edit = Toplevel()
	Label(new_edit, text = "Old Date").grid(row = 0, column = 0)
	Entry(new_edit, textvariable=StringVar(new_edit,date_text_rev),state = "readonly").grid(row = 0, column = 1)
	Label(new_edit, text = "New Date").grid(row = 1, column = 0)
	new_date_rev = DateEntry(new_edit)
	new_date_rev.grid(row = 1, column = 1)

	Label(new_edit, text = "Old Revenue Amount").grid(row = 2, column = 0)
	Entry(new_edit, textvariable=StringVar(new_edit,rev_text_rev),state = "readonly").grid(row = 2, column = 1)
	Label(new_edit, text = "New Revenue Amount").grid(row = 3, column = 0)
	new_amount_rev = Entry(new_edit)
	new_amount_rev.grid(row = 3, column = 1)

	Label(new_edit, text = "Old Mode of Payment").grid(row = 4, column = 0)
	Entry(new_edit, textvariable=StringVar(new_edit,mode_text_rev),state = "readonly").grid(row = 4, column = 1)
	Label(new_edit, text = "New Mode of Payment").grid(row = 5, column = 0)
	new_mode_rev = ttk.Combobox(new_edit)
	new_mode_rev['values'] = ("Cash","POS","Bank Transfer")
	new_mode_rev.grid(row = 5, column = 1)


	Button(new_edit, text = "Save Changes", command = lambda:edit_record_rev(new_date_rev.get(),date_text_rev,new_amount_rev.get(),rev_text_rev,new_mode_rev.get(),mode_text_rev)).grid(row = 14, column = 1)

	new_edit.mainloop()

def edit_record_rev(new_date_rev,date_text_rev,new_amount_rev,rev_text_rev,new_mode_rev,mode_text_rev):
	query = "UPDATE revenue SET datee = ?, revenue = ?, mode = ? WHERE  datee = ? and  revenue = ? and mode = ?"
	parameters = (new_date_rev,new_amount_rev,new_mode_rev,date_text_rev,rev_text_rev,mode_text_rev)
	run_query(query,parameters)
	new_edit.destroy()
	display_rev['text'] = "Record has been updated"
	view_record_rev()



#==========================REV_LABEL===========================================================

date_rev = Label(frame_rev, text = "Date:", font = "Cambria 11 bold",bg = "darkolivegreen",fg = "white")
date_rev.grid(row = 0, column = 0, pady = 5)

amount_rev = Label(frame_rev, text = "Revenue Amount:", font = "Cambria 11 bold",bg = "darkolivegreen",fg = "white")
amount_rev.grid(row = 1, column = 0, pady = 5)

date_rev = Label(frame_rev, text = "Mode of Payment:", font = "Cambria 11 bold",bg = "darkolivegreen",fg = "white")
date_rev.grid(row = 2, column = 0, pady = 5)


#==========================REV_ENTRIES===========================================================

date_text_rev = StringVar()
entry_date_rev = DateEntry(frame_rev, textvariable = date_text_rev, bd = 3, width=15)
entry_date_rev.grid(row = 0, column = 1)

rev_text_rev = StringVar()
entry_amount_rev = Entry(frame_rev, textvariable = rev_text_rev, bd = 3, width=25)
entry_amount_rev.grid(row = 1, column = 1)

mode_text_rev = StringVar()
entry_mode_rev = ttk.Combobox(frame_rev, textvariable = mode_text_rev, width=22)
entry_mode_rev["values"] = ("Cash","POS","Bank Transfer")
entry_mode_rev.grid(row = 2, column = 1)

#==========================BUTTON_ENTRIES===========================================================


rev_but = Button(frame_rev, text = "Add Record", font = "Cambria 11 bold",bg = "#51a66f", fg = "white",command = add)
rev_but.grid(row = 3, column = 1, padx = 5, pady = 5)

rev_but1 = Button(frame_rev, text = "Edit Record", font = "Cambria 11 bold",bg = "#13264a",fg = "white",command = edit_box_rev)
rev_but1.grid(row = 3, column = 0, padx = 5, pady = 5)

rev_but2 = Button(frame_rev, text = "Delete Record", font = "Cambria 11 bold",bg = "#8c1c0f",fg = "white",command = delete)
rev_but2.grid(row = 3, column = 2, padx = 5, pady = 5)

display_rev = Label(frame_rev, text = "",  font = "Cambria 8 bold italic",bg = "darkolivegreen",fg = "white")
display_rev.grid(row = 4, column = 1, pady = 3)


tree_rev = ttk.Treeview(frame_rev, height = 8, column = ["","",""])
tree_rev.grid(row = 5, column = 0, columnspan = 10, padx = 15, pady = 5)

tree_rev.heading("#0",text = "ID")
tree_rev.column("#0", width = 50, anchor = "n")

tree_rev.heading("#1",text = "Date")
tree_rev.column("#1", width = 70, anchor = "n")

tree_rev.heading("#2",text = "Revenue Amount")
tree_rev.column("#2", width = 150, anchor = "n")

tree_rev.heading("#3",text = "Mode of Payment")
tree_rev.column("#3", width = 170, anchor = "n")
view_record_rev()

scroll_rev = ttk.Scrollbar(frame_rev, command = tree_rev.yview)
scroll_rev.grid(row = 5, column = 9,padx = (50,0), sticky=NS)



#============================EXPENSE SECTION=========================================================


#==========================FUNCTIONS===========================================================


def run_query(query,parameters=()):
	conn = sqlite3.connect("medical.db")
	cur = conn.cursor()
	query_result = cur.execute(query,parameters)
	conn.commit()
	return query_result

def view_record_exp():
	record = tree_exp.get_children()
	for element in record:
		tree_exp.delete(element)
	query = "SELECT * FROM expenses"
	connect = run_query(query)
	for data in connect:
		tree_exp.insert("", 10000, text = data[0], values = data[1:])


def validation():
	return len(entry_date_exp.get())!=0 and len(entry_expense_exp.get())!=0 and len(entry_amount_exp.get())!=0


def add_record_exp():
	if validation:
		query = "INSERT INTO expenses VALUES(NULL,?,?,?)"
		parameters = (entry_date_exp.get(),entry_expense_exp.get(),entry_amount_exp.get())
		run_query(query,parameters)
		display_exp["text"] = "Record {} has been added".format(entry_date_exp.get())

		entry_date_exp.delete(0,END)
		entry_expense_exp.delete(0,END)
		entry_amount_exp.delete(0,END)

	else:
		display_exp["text"] = "Please fill all fields"

def add():
	pop = messagebox.askquestion("Adding New Record","Do you want to add this record?")
	if pop=="yes":
		add_record_exp()
	else:
		display_exp['text'] = "Record not added"

	view_record_exp()


def delete_record_exp():
	try:
		tree_exp.item(tree_exp.selection())["values"][1]
		query = "DELETE FROM expenses WHERE ID=?"
		number = tree_exp.item(tree_exp.selection())["text"]
		run_query(query,(number,))
		display_exp['text'] = "Record {} has been deleted".format(entry_date_rev.get())

	except IndexError as e:
		display_exp['text'] = "Please select a record to delete"

	view_record_exp()

def delete():
	pop = messagebox.askquestion("Deleting Record?","Do you want to delete this record? Action cannot be reversed")
	if pop=="yes":
		delete_record_exp()
	else:
		display_exp['text'] = "Record not deleted"

	view_record_exp()

def edit_box_exp():
	global new_edit
	try:
		tree_exp.item(tree_exp.selection())['values'][0]
	except IndexError as e:
		display_exp['text'] = "Please select a record to edit"
	date_text_exp = tree_exp.item(tree_exp.selection())['values'][0]
	exp_text = tree_exp.item(tree_exp.selection())['values'][1]
	amount_text_exp = tree_exp.item(tree_exp.selection())['values'][2]

	new_edit = Toplevel()
	Label(new_edit, text = "Old Date").grid(row = 0, column = 0)
	Entry(new_edit, textvariable=StringVar(new_edit,date_text_exp),state = "readonly").grid(row = 0, column = 1)
	Label(new_edit, text = "New Date").grid(row = 1, column = 0)
	new_date_exp = DateEntry(new_edit)
	new_date_exp.grid(row = 1, column = 1)

	Label(new_edit, text = "Old Expense").grid(row = 2, column = 0)
	Entry(new_edit, textvariable=StringVar(new_edit,exp_text),state = "readonly").grid(row = 2, column = 1)
	Label(new_edit, text = "New Expense").grid(row = 3, column = 0)
	new_expense_exp = Entry(new_edit)
	new_expense_exp.grid(row = 3, column = 1)

	Label(new_edit, text = "Old Expense Amount").grid(row = 4, column = 0)
	Entry(new_edit, textvariable=StringVar(new_edit,amount_text_exp),state = "readonly").grid(row = 4, column = 1)
	Label(new_edit, text = "New Expense Amount").grid(row = 5, column = 0)
	new_amount_exp = Entry(new_edit)
	new_amount_exp.grid(row = 5, column = 1)


	Button(new_edit, text = "Save Changes", command = lambda:edit_record_exp(new_date_exp.get(),date_text_exp,new_expense_exp.get(),exp_text,new_amount_exp.get(),amount_text_exp)).grid(row = 14, column = 1)

	new_edit.mainloop()

def edit_record_exp(new_date_exp,date_text_exp,new_expense_exp,exp_text,new_amount_exp,amount_text_exp):
	query = "UPDATE expenses SET datee = ?, expense = ?, amount = ? WHERE  datee = ? and  expense = ? and amount = ?"
	parameters = (new_date_exp,new_expense_exp,new_amount_exp,date_text_exp,exp_text,amount_text_exp)
	run_query(query,parameters)
	new_edit.destroy()
	display_exp['text'] = "Record has been updated"
	view_record_exp()


#==========================EXP_LABEL===========================================================

date_exp = Label(frame_exp, text = "Date:", font = "Cambria 11 bold",bg = "darkred",fg = "white")
date_exp.grid(row = 0, column = 0, pady = 10)

expense = Label(frame_exp, text = "Expense:", font = "Cambria 11 bold",bg = "darkred",fg = "white")
expense.grid(row = 1, column = 0, pady = 10)

amount = Label(frame_exp, text = "Amount:", font = "Cambria 11 bold",bg = "darkred",fg = "white")
amount.grid(row = 2, column = 0, pady = 10)


#==========================EXP_ENTRIES===========================================================

date_text_exp = StringVar()
entry_date_exp = DateEntry(frame_exp, textvariable = date_text_exp, bd = 3, width=15)
entry_date_exp.grid(row = 0, column = 1)

expense_text_exp = StringVar()
entry_expense_exp = Entry(frame_exp, textvariable = expense_text_exp, bd = 3, width=25)
entry_expense_exp.grid(row = 1, column = 1, padx = 5)

amount_text_exp = StringVar()
entry_amount_exp = Entry(frame_exp, textvariable = amount_text_exp, width=22)
entry_amount_exp.grid(row = 2, column = 1, padx = 5)

#==========================BUTTON_ENTRIES===========================================================


exp_but = Button(frame_exp, text = "Add Record", font = "Cambria 11 bold",bg = "#51a66f", fg = "white", command = add)
exp_but.grid(row = 3, column = 1, padx = 5)

exp_but1 = Button(frame_exp, text = "Edit Record", font = "Cambria 11 bold",bg = "#13264a",fg = "white", command = edit_box_exp)
exp_but1.grid(row = 3, column = 0, padx = (50,0))

exp_but2 = Button(frame_exp, text = "Delete Record", font = "Cambria 11 bold",bg = "#8c1c0f",fg = "white", command = delete)
exp_but2.grid(row = 3, column = 2, padx = 5)

display_exp = Label(frame_exp, text = "", font = "Cambria 8 bold italic", bg = "darkred", fg = "white")
display_exp.grid(row = 4, column = 1, pady = 3)

tree_exp = ttk.Treeview(frame_exp, height = 6, column = ["","",""])
tree_exp.grid(row = 5, column = 0, columnspan = 10, padx = 15, pady = 5)

tree_exp.heading("#0",text = "ID")
tree_exp.column("#0", width = 50, anchor = "n")

tree_exp.heading("#1",text = "Date")
tree_exp.column("#1", width = 70, anchor = "n")

tree_exp.heading("#2",text = "Expense ")
tree_exp.column("#2", width = 150, anchor = "n")

tree_exp.heading("#3",text = "Amount")
tree_exp.column("#3", width = 100, anchor = "n")

view_record_exp()

scroll_exp = ttk.Scrollbar(frame_exp, command = tree_exp.yview)
scroll_exp.grid(row = 5, column = 9,padx = (10,0), sticky=NS)





#============================NET SECTION=========================================================#============================NET SECTION=========================================================#============================NET SECTION=========================================================
#==========================FUNCTIONS===========================================================


def run_query(query,parameters=()):
	conn = sqlite3.connect("medical.db")
	cur = conn.cursor()
	query_result = cur.execute(query,parameters)
	conn.commit()
	return query_result

def view_record_net():
	record = tree_net.get_children()
	for element in record:
		tree_net.delete(element)
	query = "SELECT * FROM net"
	connect = run_query(query)
	for data in connect:
		tree_net.insert("", 10000, text = data[0], values = data[1:])


def validation():
	return len(entry_date_net.get())!=0 and len(entry_trev.get())!=0 and len(entry_texp.get())!=0 and len(entry_net.get())!=0


def add_record_net():
	if validation():
		query = "INSERT INTO net VALUES(NULL,?,?,?,?)"
		parameters = (entry_date_net.get(),entry_trev.get(),entry_texp.get(),entry_net.get())
		run_query(query,parameters)
		display_net["text"] = "Record {} has been added".format(entry_date_net.get())

		entry_date_net.delete(0,END)
		entry_trev.delete(0,END)
		entry_texp.delete(0,END)
		entry_net.delete(0,END)


	else:
		display_net["text"] = "Please fill all fields"

def add():
	pop = messagebox.askquestion("Adding New Record","Do you want to add this record?")
	if pop=="yes":
		add_record_net()
	else:
		display_net['text'] = "Record not added"

	view_record_net()


def delete_record_net():
	try:
		tree_net.item(tree_net.selection())["values"][1]
		query = "DELETE FROM net WHERE ID=?"
		number = tree_net.item(tree_net.selection())["text"]
		run_query(query,(number,))
		display_net['text'] = "Record {} has been deleted".format(entry_date_net.get())

	except IndexError as e:
		display_net['text'] = "Please select a record to delete"

	view_record_net()

def delete():
	pop = messagebox.askquestion("Deleting Record?","Do you want to delete this record? Action cannot be reversed")
	if pop=="yes":
		delete_record_net()
	else:
		display_net['text'] = "Record not deleted"

	view_record_net()

def edit_box_net():
	global new_edit
	try:
		tree_net.item(tree_net.selection())['values'][0]
	except IndexError as e:
		display_net['text'] = "Please select a record to edit"
	date_text_net = tree_net.item(tree_net.selection())['values'][0]
	trev_text_net = tree_net.item(tree_net.selection())['values'][1]
	texp_text_net = tree_net.item(tree_net.selection())['values'][2]
	net_text_net = tree_net.item(tree_net.selection())['values'][3]

	new_edit = Toplevel()
	Label(new_edit, text = "Old Date").grid(row = 0, column = 0)
	Entry(new_edit, textvariable=StringVar(new_edit,date_text_net),state = "readonly").grid(row = 0, column = 1)
	Label(new_edit, text = "New Date").grid(row = 1, column = 0)
	new_date_net = DateEntry(new_edit)
	new_date_net.grid(row = 1, column = 1)

	Label(new_edit, text = "Old Total Revenue Amount").grid(row = 2, column = 0)
	Entry(new_edit, textvariable=StringVar(new_edit,trev_text_net),state = "readonly").grid(row = 2, column = 1)
	Label(new_edit, text = "New Total Revenue Amount").grid(row = 3, column = 0)
	new_trev = Entry(new_edit)
	new_trev.grid(row = 3, column = 1)

	Label(new_edit, text = "Old Total Expense Amount").grid(row = 4, column = 0)
	Entry(new_edit, textvariable=StringVar(new_edit,texp_text_net),state = "readonly").grid(row = 4, column = 1)
	Label(new_edit, text = "New Total Expense Amount").grid(row = 5, column = 0)
	new_texp = Entry(new_edit)
	new_texp.grid(row = 5, column = 1)

	Label(new_edit, text = "Old Net Amount").grid(row = 6, column = 0)
	Entry(new_edit, textvariable=StringVar(new_edit,net_text_net),state = "readonly").grid(row = 6, column = 1)
	Label(new_edit, text = "New Net Amount").grid(row = 7, column = 0)
	new_net = Entry(new_edit)
	new_net.grid(row = 7, column = 1)


	Button(new_edit, text = "Save Changes", command = lambda:edit_record_net(new_date_net.get(),date_text_net,new_trev.get(),trev_text_net,new_texp.get(),texp_text_net,new_net.get(),net_text_net)).grid(row = 14, column = 1)

	new_edit.mainloop()

def edit_record_net(new_date_net,date_text_net,new_trev,trev_text_net,new_texp,texp_text_net,new_net,net_text_net):
	query = "UPDATE net SET datee = ?, trev = ?,texp = ?,net = ? WHERE  datee = ? AND trev = ? AND texp = ? AND net = ?"
	parameters = (new_date_net,new_trev,new_texp,new_net,date_text_net,trev_text_net,texp_text_net,net_text_net)
	run_query(query,parameters)
	new_edit.destroy()
	display_net['text'] = "Record has been updated"
	view_record_net()



#==========================NET_LABEL===========================================================

date_exp = Label(frame_net, text = "Date:", font = "Cambria 11 bold",bg = "darkorange",fg = "white")
date_exp.grid(row = 0, column = 0, pady = 5)

total_rev = Label(frame_net, text = "Total Revenue:", font = "Cambria 11 bold",bg = "darkorange",fg = "white")
total_rev.grid(row = 1, column = 0, pady = 5)

total_expense = Label(frame_net, text = "Total Expense:", font = "Cambria 11 bold",bg = "darkorange",fg = "white")
total_expense.grid(row = 2, column = 0, pady = 5)

net = Label(frame_net, text = "Net Summary:", font = "Cambria 11 bold",bg = "darkorange",fg = "white")
net.grid(row = 3, column = 0, pady = 5)


#==========================NET_ENTRIES===========================================================

date_text = StringVar()
entry_date_net = DateEntry(frame_net, textvariable = date_text, bd = 3, width=15)
entry_date_net.grid(row = 0, column = 1)

trev_text = StringVar()
entry_trev = Entry(frame_net, textvariable = trev_text, bd = 3, width=25)
entry_trev.grid(row = 1, column = 1, padx = 5)

texp_text = StringVar()
entry_texp = Entry(frame_net, textvariable = texp_text, bd = 3, width=25)
entry_texp.grid(row = 2, column = 1, padx = 5)

net_text = StringVar()
entry_net = Entry(frame_net, textvariable = net_text, bd = 3, width=25)
entry_net.grid(row = 3, column = 1, padx = 5)


#==========================BUTTON_ENTRIES===========================================================


net_but = Button(frame_net, text = "Add Record", font = "Cambria 11 bold",bg = "#51a66f", fg = "white", command = add)
net_but.grid(row = 4, column = 1, padx = 5)

net_but1 = Button(frame_net, text = "Edit Record", font = "Cambria 11 bold",bg = "#13264a",fg = "white", command = edit_box_net)
net_but1.grid(row = 4, column = 0, padx = (50,0))

net_but2 = Button(frame_net, text = "Delete Record", font = "Cambria 11 bold",bg = "#8c1c0f",fg = "white", command = delete)
net_but2.grid(row = 4, column = 2, padx = 5)

display_net = Label(frame_net, text = "", font = "Cambria 9 bold italic", bg = "darkorange", fg = "white")
display_net.grid(row = 5, column = 1)

tree_net = ttk.Treeview(frame_net, height = 7, column = ["","","",""])
tree_net.grid(row = 6, column = 0, columnspan = 10, padx = 15, pady = 10)

tree_net.heading("#0",text = "ID")
tree_net.column("#0", width = 50, anchor = "n")

tree_net.heading("#1",text = "Date")
tree_net.column("#1", width = 70, anchor = "n")

tree_net.heading("#2",text = "Total Revenue ")
tree_net.column("#2", width = 150, anchor = "n")

tree_net.heading("#3",text = "Total Expense")
tree_net.column("#3", width = 150, anchor = "n")

tree_net.heading("#4",text = "Net Summary")
tree_net.column("#4", width = 150, anchor = "n")
view_record_net()

scroll_net = ttk.Scrollbar(frame_net, command = tree_net.yview)
scroll_net.grid(row = 6, column = 9,padx = (10,0), sticky=NS)




#==========================STAFF DETAILS===========================================================
#==========================================================================================


#==========================FUNCTIONS================================================================
#==========================================================================================

def run_query(query,parameters=()):
	conn = sqlite3.connect("medical.db")
	cur = conn.cursor()
	query_result = cur.execute(query,parameters)
	conn.commit()
	return query_result

def view_record_staff():
	record = tree_staff.get_children()
	for element in record:
		tree_staff.delete(element)
	query = "SELECT * FROM staff"
	connect = run_query(query)
	for data in connect:
		tree_staff.insert("", 10000, text = data[0], values = data[1:])


def validation():
	return len(entry_staff_date.get())!=0 and len(entry_staff_id.get())!=0 and len(entry_staff_name.get())!=0 and len(entry_staff_gender.get())!=0 and len(entry_staff_address.get())!=0 and len(entry_staff_phone.get())!=0 and len(entry_staff_position.get())!=0 and len(entry_staff_status.get())!=0


def add_record_staff():
	if validation:
		query = "INSERT INTO staff VALUES(NULL,?,?,?,?,?,?,?,?)"
		parameters = (entry_staff_date.get(),entry_staff_id.get(),entry_staff_name.get(),entry_staff_gender.get(),entry_staff_address.get(),entry_staff_phone.get(),entry_staff_position.get(),entry_staff_status.get())
		run_query(query,parameters)
		display_staff["text"] = "Record {} has been added".format(entry_staff_name.get())

		entry_staff_date.delete(0,END)
		entry_staff_id.delete(0,END)
		entry_staff_name.delete(0,END)
		entry_staff_gender.delete(0,END)
		entry_staff_address.delete(0,END)
		entry_staff_phone.delete(0,END)
		entry_staff_position.delete(0,END)
		entry_staff_status.delete(0,END)

	else:
		display_staff["text"] = "Please fill all fields"

def add():
	pop = messagebox.askquestion("Adding New Record","Do you want to add this record?")
	if pop=="yes":
		add_record_staff()
	else:
		display_staff['text'] = "Record not added"

	view_record_staff()


def delete_record_staff():
	try:
		tree_staff.item(tree_staff.selection())["values"][1]
		query = "DELETE FROM staff WHERE ID=?"
		number = tree_staff.item(tree_staff.selection())["text"]
		run_query(query,(number,))
		display_staff['text'] = "Record {} has been deleted".format(entry_staff_id.get())

	except IndexError as e:
		display_staff['text'] = "Please select a record to delete"

	view_record_staff()

def delete():
	pop = messagebox.askquestion("Deleting Record?","Do you want to delete this record? Action cannot be reversed")
	if pop=="yes":
		delete_record_staff()
	else:
		display_staff['text'] = "Record not deleted"

	view_record_staff()

def edit_box_staff():
	global new_edit
	try:
		tree_staff.item(tree_staff.selection())['values'][0]
	except IndexError as e:
		display_staff['text'] = "Please select a record to edit"
	date_text_staff = tree_staff.item(tree_staff.selection())['values'][0]
	id_text_staff = tree_staff.item(tree_staff.selection())['values'][1]
	name_text_staff = tree_staff.item(tree_staff.selection())['values'][2]
	gender_text_staff = tree_staff.item(tree_staff.selection())['values'][3]
	address_text_staff = tree_staff.item(tree_staff.selection())['values'][4]
	phone_text_staff = tree_staff.item(tree_staff.selection())['values'][5]
	position_text_staff = tree_staff.item(tree_staff.selection())['values'][6]
	status_text_staff = tree_staff.item(tree_staff.selection())['values'][7]

	new_edit = Toplevel()
	Label(new_edit, text = "Old Date").grid(row = 0, column = 0)
	Entry(new_edit, textvariable=StringVar(new_edit,date_text_staff),state = "readonly").grid(row = 0, column = 1)
	Label(new_edit, text = "New Date").grid(row = 1, column = 0)
	new_date_staff = DateEntry(new_edit)
	new_date_staff.grid(row = 1, column = 1)

	Label(new_edit, text = "Old Staff ID").grid(row = 2, column = 0)
	Entry(new_edit, textvariable=StringVar(new_edit,id_text_staff),state = "readonly").grid(row = 2, column = 1)
	Label(new_edit, text = "New Staff ID").grid(row = 3, column = 0)
	new_staff_id = Entry(new_edit)
	new_staff_id.grid(row = 3, column = 1)

	Label(new_edit, text = "Old Full name").grid(row = 4, column = 0)
	Entry(new_edit, textvariable=StringVar(new_edit,name_text_staff),state = "readonly").grid(row = 4, column = 1)
	Label(new_edit, text = "New Full name").grid(row = 5, column = 0)
	new_name_staff = Entry(new_edit)
	new_name_staff.grid(row = 5, column = 1)

	Label(new_edit, text = "Old Gender").grid(row = 6, column = 0)
	Entry(new_edit, textvariable=StringVar(new_edit,gender_text_staff),state = "readonly").grid(row = 6, column = 1)
	Label(new_edit, text = "New Gender").grid(row = 7, column = 0)
	new_gender_staff = ttk.Combobox(new_edit)
	new_gender_staff["values"] = ("Male","Female")
	new_gender_staff.grid(row = 7, column = 1)

	Label(new_edit, text = "Old Contact Address").grid(row = 8, column = 0)
	Entry(new_edit, textvariable=StringVar(new_edit,address_text_staff),state = "readonly").grid(row = 8, column = 1)
	Label(new_edit, text = "New Contact Address").grid(row = 9, column = 0)
	new_address_staff = Entry(new_edit)
	new_address_staff.grid(row = 9, column = 1)

	Label(new_edit, text = "Old Phone number").grid(row = 10, column = 0)
	Entry(new_edit, textvariable=StringVar(new_edit,phone_text_staff),state = "readonly").grid(row = 10, column = 1)
	Label(new_edit, text = "New Phone number").grid(row = 11, column = 0)
	new_phone_staff = Entry(new_edit)
	new_phone_staff.grid(row = 11, column = 1)

	Label(new_edit, text = "Old Position").grid(row = 12, column = 0)
	Entry(new_edit, textvariable=StringVar(new_edit,position_text_staff),state = "readonly").grid(row = 12, column = 1)
	Label(new_edit, text = "New Position").grid(row = 13, column = 0)
	new_position_staff = Entry(new_edit)
	new_position_staff.grid(row = 13, column = 1)

	Label(new_edit, text = "Old Status").grid(row = 14, column = 0)
	Entry(new_edit, textvariable=StringVar(new_edit,status_text_staff),state = "readonly").grid(row = 14, column = 1)
	Label(new_edit, text = "New Status").grid(row = 15, column = 0)
	new_status_staff = ttk.Combobox(new_edit)
	new_status_staff["values"] = ("Employed","Resigned", "On Leave","Suspended","Laid-Off")
	new_status_staff.grid(row = 15, column = 1)


	Button(new_edit, text = "Save Changes", command = lambda:edit_record_staff(new_date_staff.get(),date_text_staff,new_staff_id.get(),id_text_staff,new_name_staff.get(),name_text_staff,new_gender_staff.get(),gender_text_staff,new_address_staff.get(),address_text_staff,new_phone_staff.get(),phone_text_staff,new_position_staff.get(),position_text_staff,new_status_staff.get(),status_text_staff)).grid(row = 16, column = 1)

	new_edit.mainloop()

def edit_record_staff(new_date_staff,date_text_staff,new_staff_id,id_text_staff,new_name_staff,name_text_staff,new_gender_staff,gender_text_staff,new_address_staff,address_text_staff,new_phone_staff,phone_text_staff,new_position_staff,position_text_staff,new_status_staff,status_text_staff):
	query = "UPDATE staff SET datee = ?, staff_id = ?,name = ?,gender = ?,address = ?,phone = ?,position = ?,status = ? WHERE  datee = ? and staff_id = ? and name = ?  and gender = ?  and address = ?  and phone = ?  and position = ?  and status = ?"
	parameters = (new_date_staff,new_staff_id,new_name_staff,new_gender_staff,new_address_staff,new_phone_staff,new_position_staff,new_status_staff,date_text_staff, id_text_staff,name_text_staff,gender_text_staff,address_text_staff,phone_text_staff,position_text_staff,status_text_staff)
	run_query(query,parameters)
	new_edit.destroy()
	display_staff['text'] = "Record has been updated"
	view_record_staff()



topic_staff = Label(tab_staff, text = "STAFF PROFILE", fg = "crimson", bg = "lightgrey", font = "Helvetica 35 bold underline") 
topic_staff.grid(row=0,column=0, padx = 50, pady = 10, columnspan = 2, sticky=N)

#=================================IMAGE, FRAME=========================================================


img_staff = ImageTk.PhotoImage(Image.open("C:\\Users\\KURUS\\Desktop\\Hospital App\\staff_profile.jpg"))
img_staff_label = Label(tab_staff, image = img_staff, width = 770, height = 450)
img_staff_label.grid(row=1, column = 1, sticky=W)

frame_staff = LabelFrame(tab_staff, text = "Add New Staff Details", bg = "saddlebrown", font = "arial 11 bold", bd = 3, padx = 10)
frame_staff.grid(row = 1, column = 0, sticky=N, rowspan = 10)


#================================LABELS========================================

staff_date = Label(frame_staff, text = "Date Employed", font = "times 12 bold", bg = "saddlebrown",fg = "white")
staff_date.grid(row = 1, column = 0)

staff_id = Label(frame_staff, text = "Staff ID", font = "times 12 bold", bg = "saddlebrown",fg = "white")
staff_id.grid(row = 2, column = 0)

staff_name = Label(frame_staff, text = "Full name", font = "times 12 bold", bg = "saddlebrown",fg = "white")
staff_name.grid(row = 3, column = 0)

staff_gender = Label(frame_staff, text = "Gender", font = "times 12 bold", bg = "saddlebrown",fg = "white")
staff_gender.grid(row = 4, column = 0)

staff_address = Label(frame_staff, text = "Contact Address", font = "times 12 bold", bg = "saddlebrown",fg = "white")
staff_address.grid(row = 5, column = 0)

staff_phone = Label(frame_staff, text = "Phone number", font = "times 12 bold", bg = "saddlebrown",fg = "white")
staff_phone.grid(row = 6, column = 0)

staff_position = Label(frame_staff, text = "Position", font = "times 12 bold", bg = "saddlebrown",fg = "white")
staff_position.grid(row = 7, column = 0)

staff_status = Label(frame_staff, text = "Status", font = "times 12 bold", bg = "saddlebrown",fg = "white")
staff_status.grid(row = 8, column = 0)


#================================ENTRIES========================================

date_text_staff = StringVar()
entry_staff_date = DateEntry(frame_staff, textvariable = date_text_staff, state="readonly", bd = 3, width = 20)
entry_staff_date.grid(row = 1, column = 1, padx = 20, pady = 10)

id_text_staff = StringVar()
entry_staff_id = Entry(frame_staff, textvariable = id_text_staff, bd = 3, width = 20)
entry_staff_id.grid(row = 2, column = 1, padx = 20, pady = 10)

name_text_staff = StringVar()
entry_staff_name = Entry(frame_staff, textvariable = name_text_staff, bd = 3, width = 40)
entry_staff_name.grid(row = 3, column = 1, padx = 20, pady = 10)

gender_text_staff = StringVar()
entry_staff_gender = ttk.Combobox(frame_staff, textvariable = gender_text_staff,state="readonly", width = 20)
entry_staff_gender['values'] = ("Male", "Female")
entry_staff_gender.grid(row = 4, column = 1, padx = 20, pady = 10)

address_text_staff = StringVar()
entry_staff_address = Entry(frame_staff, textvariable = address_text_staff, bd = 3, width = 40)
entry_staff_address.grid(row = 5, column = 1, padx = 20, pady = 10)

phone_text_staff = StringVar()
entry_staff_phone = Entry(frame_staff, textvariable = phone_text_staff, bd = 3, width = 25)
entry_staff_phone.grid(row = 6, column = 1, padx = 20, pady = 10)

position_text_staff = StringVar()
entry_staff_position = Entry(frame_staff, textvariable = position_text_staff, bd = 3, width = 30)
entry_staff_position.grid(row = 7, column = 1, padx = 20, pady = 10)

status_text_staff = StringVar()
entry_staff_status = ttk.Combobox(frame_staff, textvariable = status_text_staff, state="readonly", width = 20)
entry_staff_status['values'] = ("Employed","Resigned", "On Leave","Suspended","Laid-Off")
entry_staff_status.grid(row = 8, column = 1, padx = 20, pady = 10)



#================================BUTTONS========================================

staff_add = Button(frame_staff, text = "Add Record", font = "Cambria 12 bold italic", bg = "#51a66f", fg = "white", command = add)
staff_add.grid(row = 9, column = 1, pady=10)

staff_edit = Button(frame_staff, text = "Edit Record",  font = "Cambria 12 bold italic",bg = "#13264a", fg = "white", command = edit_box_staff)
staff_edit.grid(row = 9, column = 0, pady=10)

staff_del = Button(frame_staff, text = "Delete Record", font = "Cambria 12 bold italic", bg = "#8c1c0f", fg = "white", command = delete)
staff_del.grid(row = 9, column = 2, padx = 10, pady=10)

display_staff = Label(frame_staff, text = "", font = "Cambria 9 bold italic", bg = "saddlebrown", fg = "white")
display_staff.grid(row = 10, column = 1, pady=10)


#================================TREEVIEW========================================

tree_staff = ttk.Treeview(tab_staff, height = 13, column = ["","","","","","","",""])
tree_staff.grid(row = 11, column = 0, pady = 10, columnspan = 15)


tree_staff.heading("#0", text = "ID")
tree_staff.column("#0", width = 50, anchor = "n")


tree_staff.heading("#1", text = "Date Employed")
tree_staff.column("#1", width = 130, anchor = "n")


tree_staff.heading("#2", text = "Staff ID")
tree_staff.column("#2", width = 80, anchor = "n")


tree_staff.heading("#3", text = "Full name")
tree_staff.column("#3", width = 200, anchor = "n")


tree_staff.heading("#4", text = "Gender")
tree_staff.column("#4", width = 100, anchor = "n")


tree_staff.heading("#5", text = "Address")
tree_staff.column("#5", width = 230, anchor = "n")


tree_staff.heading("#6", text = "Phone number")
tree_staff.column("#6", width = 150, anchor = "n")


tree_staff.heading("#7", text = "Position")
tree_staff.column("#7", width = 150, anchor = "n")


tree_staff.heading("#8", text = "Status")
tree_staff.column("#8", width = 150, anchor = "n")

view_record_staff()

scroll_staff = Scrollbar(tab_staff, command = tree_staff.yview)
scroll_staff.grid(row = 11, column = 1, padx = (680,0), sticky = NS)



#================================HOSPITAL ASSESSMENTB========================================
#==========================FUNCTIONS===========================================================


def run_query(query,parameters=()):
	conn = sqlite3.connect("medical.db")
	cur = conn.cursor()
	query_result = cur.execute(query,parameters)
	conn.commit()
	return query_result

def view_record_ass():
	record = tree_ass.get_children()
	for element in record:
		tree_ass.delete(element)
	query = "SELECT * FROM assessment"
	connect = run_query(query)
	for data in connect:
		tree_ass.insert("", 10000, text = data[0], values = data[1:])


def validation():
	return len(entry_date_ass.get())!=0 and len(entry_status_ass.get())!=0 and len(entry_name_ass.get())!=0 and len(entry_con_ass.get())!=0


def add_record_ass():
	if validation():
		query = "INSERT INTO assessment VALUES(NULL,?,?,?,?)"
		parameters = (entry_date_ass.get(),entry_status_ass.get(),entry_name_ass.get(),entry_con_ass.get())
		run_query(query,parameters)
		display_ass["text"] = "Record {} has been added".format(entry_name_ass.get())

		entry_date_ass.delete(0,END)
		entry_status_ass.delete(0,END)
		entry_name_ass.delete(0,END)
		entry_con_ass.delete(0,END)


	else:
		display_ass["text"] = "Please fill all fields"

def add():
	pop = messagebox.askquestion("Adding New Record","Do you want to add this record?")
	if pop=="yes":
		add_record_ass()
	else:
		display_ass['text'] = "Record not added"

	view_record_ass()


def delete_record_ass():
	try:
		tree_ass.item(tree_ass.selection())["values"][1]
		query = "DELETE FROM assessment WHERE ID=?"
		number = tree_ass.item(tree_ass.selection())["text"]
		run_query(query,(number,))
		display_ass['text'] = "Record {} has been deleted".format(entry_date_net.get())

	except IndexError as e:
		display_ass['text'] = "Please select a record to delete"

	view_record_ass()

def delete():
	pop = messagebox.askquestion("Deleting Record?","Do you want to delete this record? Action cannot be reversed")
	if pop=="yes":
		delete_record_ass()
	else:
		display_ass['text'] = "Record not deleted"

	view_record_ass()

def edit_box_ass():
	global new_edit
	try:
		tree_ass.item(tree_ass.selection())['values'][0]
	except IndexError as e:
		display_ass['text'] = "Please select a record to edit"
	date_text_ass = tree_ass.item(tree_ass.selection())['values'][0]
	status_text_ass = tree_ass.item(tree_ass.selection())['values'][1]
	name_text_ass = tree_ass.item(tree_ass.selection())['values'][2]
	con_text_ass = tree_ass.item(tree_ass.selection())['values'][3]

	new_edit = Toplevel()
	Label(new_edit, text = "Old Date").grid(row = 0, column = 0)
	Entry(new_edit, textvariable=StringVar(new_edit,date_text_ass),state = "readonly").grid(row = 0, column = 1)
	Label(new_edit, text = "New Date").grid(row = 1, column = 0)
	new_date_ass = DateEntry(new_edit)
	new_date_ass.grid(row = 1, column = 1)

	Label(new_edit, text = "Old Status").grid(row = 2, column = 0)
	Entry(new_edit, textvariable=StringVar(new_edit,status_text_ass),state = "readonly").grid(row = 2, column = 1)
	Label(new_edit, text = "New Status").grid(row = 3, column = 0)
	new_status_ass = ttk.Combobox(new_edit, values = ["Status","Admitted","Discharged","Transferred","Deceased"])
	new_status_ass.grid(row = 3, column = 1)
	new_status_ass.current(0)

	Label(new_edit, text = "Old Name").grid(row = 4, column = 0)
	Entry(new_edit, textvariable=StringVar(new_edit,name_text_ass),state = "readonly").grid(row = 4, column = 1)
	Label(new_edit, text = "New Name").grid(row = 5, column = 0)
	new_name_ass = Entry(new_edit)
	new_name_ass.grid(row = 5, column = 1)

	Label(new_edit, text = "Old Condition").grid(row = 6, column = 0)
	Entry(new_edit, textvariable=StringVar(new_edit,con_text_ass),state = "readonly").grid(row = 6, column = 1)
	Label(new_edit, text = "New Condition").grid(row = 7, column = 0)
	new_con_ass = Entry(new_edit)
	new_con_ass.grid(row = 7, column = 1)


	Button(new_edit, text = "Save Changes", command = lambda:edit_record_ass(new_date_ass.get(),date_text_ass,new_status_ass.get(),status_text_ass,new_name_ass.get(),name_text_ass,new_con_ass.get(),con_text_ass)).grid(row = 14, column = 1)

	new_edit.mainloop()

def edit_record_ass(new_date_ass,date_text_ass,new_status_ass,status_text_ass,new_name_ass,name_text_ass,new_con_ass,con_text_ass):
	query = "UPDATE assessment SET datee = ?, status = ?,name = ?,condition = ? WHERE  datee = ? AND status = ? AND name = ? AND condition = ?"
	parameters = (new_date_ass,new_status_ass,new_name_ass,new_con_ass,date_text_ass,status_text_ass,name_text_ass,con_text_ass)
	run_query(query,parameters)
	new_edit.destroy()
	display_ass['text'] = "Record has been updated"
	view_record_ass()



#================================IMAGE, HEADER========================================

frame_ass = LabelFrame(tab_assess, text = "Add New Assessment Record",bd = 3, bg = "cadetblue")
frame_ass.grid(row = 1, column = 0)

frame_ass1 = LabelFrame(tab_assess, text = "Patient Summary",bd = 3, bg = "firebrick", pady = 15)
frame_ass1.grid(row = 3, column = 0, columnspan = 3, sticky=W, pady = 15)

frame_ass2 = LabelFrame(tab_assess, text = "Finance Summary",bd = 3, bg = "mediumvioletred", padx = 25, pady = 15)
frame_ass2.grid(row = 3, column = 0,  sticky=W, padx = (425,0))

frame_ass3 = LabelFrame(tab_assess, text = "Staff Summary",bd = 3, bg = "lightyellow", padx = 15, pady = 35)
frame_ass3.grid(row = 3, column = 2 ,sticky=W, padx = (10,0))

img_ass = ImageTk.PhotoImage(Image.open("C:\\Users\\KURUS\\Desktop\\Hospital App\\hospital_assessment1.jpg"))
img_ass_label = Label(tab_assess,image = img_ass, height = 400)
img_ass_label.grid(row = 1, column = 1, padx = (50,0), columnspan = 10, sticky=W)

#==========================LABEL===========================================================

topic_ass = Label(tab_assess, text= "HOSPITAL ASSESSMENT", bg = "crimson", font = "Georgia 30 bold underline")
topic_ass.grid(row = 0, column = 0, pady = 5)

topic_summary = Label(tab_assess, text = "HOSPITAL SUMMARY", bg = "crimson", font = "Georgia 30 bold underline")
topic_summary.grid(row = 2, column = 0, pady = 5)

date_ass = Label(frame_ass, text = "Date:", font = "Cambria 11 bold",bg = "cadetblue",fg = "white")
date_ass.grid(row = 0, column = 0, pady = 5)

status_ass = Label(frame_ass, text = "Status", font = "Cambria 11 bold",bg = "cadetblue",fg = "white")
status_ass.grid(row = 1, column = 0, pady = 5)

name_ass = Label(frame_ass, text = "Name:", font = "Cambria 11 bold",bg = "cadetblue",fg = "white")
name_ass.grid(row = 2, column = 0, pady = 5)

con_ass = Label(frame_ass, text = "Condition:", font = "Cambria 11 bold",bg = "cadetblue",fg = "white")
con_ass.grid(row = 3, column = 0, pady = 5)


#==========================NET_ENTRIES===========================================================

date_text_ass = StringVar()
entry_date_ass = DateEntry(frame_ass, textvariable = date_text_ass, bd = 3, width=15)
entry_date_ass.grid(row = 0, column = 1)

status_ass_text = StringVar()
entry_status_ass = ttk.Combobox(frame_ass, text = "Status:", state = "readonly", textvariable = status_ass_text, width = 11, font="arial 10 bold", values = ["Status","Admitted","Discharged","Transferred","Deceased"])
entry_status_ass.grid(row = 1, column = 1, padx = 5)
entry_status_ass.current(0)

name_text_ass = StringVar()
entry_name_ass = Entry(frame_ass, textvariable = name_text_ass, bd = 3, width=25)
entry_name_ass.grid(row = 2, column = 1, padx = 5)

con_text_ass = StringVar()
entry_con_ass = Entry(frame_ass, textvariable = con_text_ass, bd = 3, width=25)
entry_con_ass.grid(row = 3, column = 1, padx = 5)


#==========================BUTTON_ENTRIES===========================================================


ass_but = Button(frame_ass, text = "Add Record", font = "Cambria 11 bold",bg = "#51a66f", fg = "white", command = add)
ass_but.grid(row = 4, column = 1, padx = 5,pady = 4)

ass_but1 = Button(frame_ass, text = "Edit Record", font = "Cambria 11 bold",bg = "#13264a",fg = "white", command = edit_box_ass)
ass_but1.grid(row = 4, column = 0, padx = (50,0),pady = 4)

ass_but2 = Button(frame_ass, text = "Delete Record", font = "Cambria 11 bold",bg = "#8c1c0f",fg = "white", command = delete)
ass_but2.grid(row = 4, column = 2, padx = 5,pady = 4)

display_ass = Label(frame_ass, text = "", font = "Cambria 9 bold italic", bg = "cadetblue", fg = "white")
display_ass.grid(row = 5, column = 1)

tree_ass = ttk.Treeview(frame_ass, height = 7, column = ["","","",""])
tree_ass.grid(row = 6, column = 0, columnspan = 10, padx = 15, pady = 10)

tree_ass.heading("#0",text = "ID")
tree_ass.column("#0", width = 50, anchor = "n")

tree_ass.heading("#1",text = "Date")
tree_ass.column("#1", width = 70, anchor = "n")

tree_ass.heading("#2",text = "Status ")
tree_ass.column("#2", width = 150, anchor = "n")

tree_ass.heading("#3",text = "Name")
tree_ass.column("#3", width = 200, anchor = "n")

tree_ass.heading("#4",text = "Condition")
tree_ass.column("#4", width = 200, anchor = "n")
view_record_ass()

scroll_ass = ttk.Scrollbar(frame_ass, command = tree_ass.yview)
scroll_ass.grid(row = 6, column = 9,padx = (19,0), sticky=NS)

#======================PATIENT SUMMARY=========================================

in_patients = Label(frame_ass1, text = "Total In-Patients:", font = "Cambria 20 bold",bg = "firebrick", fg = "white")
in_patients.grid(row = 0, column = 0, pady = 10)

out_patients = Label(frame_ass1, text = "Total Out-Patients:", font = "Cambria 20 bold" ,bg = "firebrick", fg = "white")
out_patients.grid(row = 1, column = 0, pady = 10)

discharged_patients = Label(frame_ass1, text = "Total Discharged Patients:", font = "Cambria 20 bold" ,bg = "firebrick", fg = "white")
discharged_patients.grid(row = 2, column = 0, pady = 10)

deaths = Label(frame_ass1, text = "Total Deaths:", font = "Cambria 20 bold" ,bg = "firebrick", fg = "white")
deaths.grid(row = 3, column = 0, pady = 10)

#======================FINANCE SUMMARY=========================================

revenue_label = Label(frame_ass2, text = "Total Revenue:", font = "Cambria 20 bold", bg = "mediumvioletred", fg = "white")
revenue_label.grid(row = 0, column = 0, pady = 10)

expense_label = Label(frame_ass2, text = "Total Expense:", font = "Cambria 20 bold" ,bg = "mediumvioletred", fg = "white")
expense_label.grid(row = 1, column = 0, pady = 10)

net_labels = Label(frame_ass2, text = "Total Net:", font = "Cambria 20 bold" ,bg = "mediumvioletred", fg = "white")
net_labels.grid(row = 2, column = 0, pady = 10)

days_label = Label(frame_ass2, text = "Total Days:", font = "Cambria 20 bold" ,bg = "mediumvioletred", fg = "white")
days_label.grid(row = 3, column = 0, pady = 10)


#======================STAFF SUMMARY=========================================

total_employed = Label(frame_ass3, text = "Total Currently Employed:", font = "Cambria 20 bold" , bg = "lightyellow")
total_employed.grid(row = 1, column = 0)

total_resigned = Label(frame_ass3, text = "Total Resigned:", font = "Cambria 20 bold" , bg = "lightyellow")
total_resigned.grid(row = 2, column = 0)

total_suspended = Label(frame_ass3, text = "Suspended:", font = "Cambria 20 bold" , bg = "lightyellow")
total_suspended.grid(row = 3, column = 0)

total_laidoff = Label(frame_ass3, text = "Laid-Off:", font = "Cambria 20 bold" , bg = "lightyellow")
total_laidoff.grid(row = 4, column = 0)

total_onleave = Label(frame_ass3, text = "On Leave:", font = "Cambria 20 bold" , bg = "lightyellow")
total_onleave.grid(row = 5, column = 0)































root.mainloop()



















