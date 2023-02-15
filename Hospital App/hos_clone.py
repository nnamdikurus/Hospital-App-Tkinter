from tkinter import *
from tkcalendar import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
import datetime
import time
import sqlite3



root = Tk()
root.title("Hospital Management App")
root.geometry("1550x1000+0+0")




#================STYLING THE NOTEBOOK TAB======================================


style = ttk.Style()
style.configure("TNotebook.Tab", font = "Garamond 14 bold")
style.configure("lefttab.TNotebook", tabposition ="ws", background = "lightgrey", tabmargins = (10,10,30,10))

#================NOTEBOOK MANAGEMENT======================================

notebook = ttk.Notebook(root, style = "lefttab.TNotebook")

tab_home = ttk.Frame(notebook)
tab_pdata = ttk.Frame(notebook)
tab_pdata = ttk.Frame(notebook)
tab_app = ttk.Frame(notebook)
tab_pres = ttk.Frame(notebook)
tab_inv= ttk.Frame(notebook)
tab_bill = ttk.Frame(notebook)
tab_fin = ttk.Frame(notebook)
tab_staff = ttk.Frame(notebook)
tab_assess = ttk.Frame(notebook)

notebook.add(tab_home, text = "|Home|")
notebook.add(tab_pdata, text = "Patient's Data")
notebook.add(tab_app, text = "Patient Appointment")
notebook.add(tab_pres, text = "Prescriptions")
notebook.add(tab_inv, text = "Hospital Inventory")
notebook.add(tab_bill, text = "Patient Billing Record")
notebook.add(tab_fin, text = "Financial Records")
notebook.add(tab_staff, text = "Staff Profile")
notebook.add(tab_assess, text = "Hospital Assessment")

notebook.grid(row = 0, column = 0, sticky = 'nw')



#================ CLOCK ======================================

def tick():
	d = datetime.datetime.now()
	myday = "{:%B  %d  %Y}".format(d)
	mytime = time.strftime("%I : %M : %S%p")
	time_label.config(text = (myday + "  " + mytime))
	time_label.after(200,tick)

time_label = Label(root, font = "Arial 13 bold italic", fg = "navy", bg = "lightgrey")
time_label.grid(row = 0, column = 9, sticky = N)
tick()

#====================HEADER===================================

topic_label = Label(tab_home, text = "HOSPITAL MANAGEMENT APP", font = "impact 35 bold", fg = "#8f1e33", bg = "lightgrey")
topic_label.grid(row = 0, column = 1, sticky = N)


#================BACKGROUND IMAGE======================================


home = ImageTk.PhotoImage(Image.open("C:\\Users\\KURUS\\Desktop\\Hospital App\\homepage.jpg"))
home_label = Label(tab_home, image = home, width = 1700, height = 900)
home_label.grid(row = 0, column = 0, columnspan = 2, rowspan = 2)

















root.mainloop()