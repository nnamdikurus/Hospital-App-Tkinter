import tkinter as tk
import tkinter.ttk as ttk


def my_values_cal():
    sum1 = 0.0
    for child in tree.get_children():
        sum1 += float(tree.item(child, "values")[0])
        lab.config(text=sum1)

        print(sum1)



root = tk.Tk()

tree =ttk.Treeview(root, column=("col1", "col2", "col3"), show="headings")
tree.heading('#1', text='Number')
tree.heading('#2', text='Temp')
tree.heading('#3', text='time')


tree.insert("", tk.END, values=(24, "09", "2:00 AM"))
tree.insert("", tk.END, values=(34, "04", "5:00 AM"))
tree.insert("", tk.END, values=(40, "09", "1:00 PM"))
tree.insert("", tk.END, values=(94, "01", "23:00 PM"))
tree.insert("", tk.END, values=("38", "21", "21:00 AM"))


tree.pack()


children = tree.get_children()
for child in children:
	i = tree.item(child,'values')[2]
	print(len(i))

sum=0
#for child in tree.get_children():
	#sum = sum+float(tree.item(child, "values")[1])
	#print(sum)


lab = tk.Label(root, text=i, font = "garamond 12 bold")
lab.pack()



b = tk.Button(root, text="CALCULATE", command=my_values_cal)
b.pack()


root.mainloop()