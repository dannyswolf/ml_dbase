# coding=utf-8
"""
Sqlite Γραφικό περιβάλλον με Python3
******************************************************************
************** ΔΕΝ ΔΗΜΗΟΥΡΓΕΙ ΒΑΣΗ ΟΥΤΕ ΠΙΝΑΚΕΣ*******************
** Οι βάσεις πρέπει να έχουν Id ή id ή ID intiger και NOT NULL  **
******************************************************************

Version v 0.6 Προσθήκη καρτέλων και η αναζήτηση δουλεύει :-)              6/11/2019

version v 0.5 διαχωρισμός συναρτήσεων  απο το γραφικό περιβάλλων          3/11/2019
Προσθήκη icons και συντόμευση πληκτρολογίου
Η ΑΝΑΖΗΤΗΣΗ ΔΕΝ ΔΟΥΛΕΥΕΙ αν το βάλω να ζηταει να ανοιγει αρχείο απο μόνο του
αρχεία : func.py , sqlite_gui_manager_greek.py

version v 0.4 Προσθήκη menu

version v 0.3 Η αναζήτηση δουλευει για ολες τις Βάσεις και πινακες
Η ΑΝΑΖΗΤΗΣΗ ΔΕΝ ΔΟΥΛΕΥΕΙ ΜΕ ΤΟ ΑΝΟΙΓΜΑ ΤΟΥ ΠΡΩΤΟΥ ΑΡΧΕΙΟΥ
ΧΑΛΑΕΙ ΤΟ ΠΛΑΤΟΣ ΤΟΥ ΠΡΟΓΡΑΜΜΑΤΟΣ ΜΕ ΤΗΝ ΑΝΑΝΕΩΣΗ
===============================ΓΡΑΜΜΗ 405=======================
TO DO LIST   ********* ΠΡΕΠΕΙ ΝΑ ΤΑ ΒΑΛΩ ΟΛΛΑ ΣΕ CLASS ΓΙΑ ΝΑ ΠΕΞΟΥΝ ΣΩΣΤΑ *******************
TO DO LIST  0) Να φιάξω την επεξεργρασία επιλεγμένου απο το treeview  ΝΑ ΠΕΡΝΕΙ column αντι TONER=? κτλπ.------------Εγινε 29/10/2019
TO DO LIST  1) ΝΑ ΦΤΙΑΞΩ ΤΟ BACKUP DIRECTORY------------------------------------------------------------------------ΕΓΙΝΕ
TO DO LIST  2) ΤΟ TREE NA ΕΜΦΑΝΙΖΕΙ OTI ΒΑΣΗ ΚΑΙ ΝΑ ΕΠΙΛΕΞΩ--να εμφανίζει τους πίνακες------------------------------ΕΓΙΝΕ 30/10/2019
TO DO LIST  3) ΝΑ ΒΑΛΩ ΜΕΝΟΥ ---------------------------------------------------------------------------------------Εγινε 1/11/2019
TO DO LIST  4) ο χρήστης να επιλέγει τον πίνακα
TO DO LIST  5) ελεγχος αν ο χρήστης εισάγει αλφαριθμητικό ή αριθμό
TO DO LIST  6) Να βάλω να έχει log αρχείο
TO DO LIST  7) Να κάνει αυτόματα υπολογισμό το σύνολο (όταν έχουμε τιμη και τεμάχια)
TO DO LIST  8) Να βάλω triggers
TO DO LIST  9) Να βάλω στο μενοu RUN SQL
"""

from func import *


# Πρώτα αυτό για το Combobox
from tkinter import ttk

# Μετά αυτο για το Label Διαφορετικά βγαζει error για το font
from tkinter import *


root = Tk()
root.geometry('1200x750+100+100')
root.title('Sqlite γραφικό περιβάλλον')
root.config(bg="#C2C0BD")
# root.resizable(width=1000, height=100)
# width = 1200
# height = 600
# screen_width = root.winfo_screenwidth()
# screen_height = root.winfo_screenheight()
# x = (screen_width / 2) - (width / 2)
# y = (screen_height / 2) - (height / 2)
# root.geometry("%dx%d+%d+%d" % (width, height, x, y))
# Τίτλος προγράμματος


app_title = Label(root, bg="brown", fg="white", text="MLShop Database", font=("Arial Bold", 15), bd=8 )
#app_title.grid(column=0, row=0, sticky="we")

# Εμφανηση Κεφαλίδων του πίνακα



# ------------------------Εμφάνιση δεδομένων σε Frame-------------------------

# =======================Δημηουργεία καρτέλων==========================

#data_frame = Frame(root, width=1024, bg="#C2C0BD", relief=SOLID)
#data_frame.grid(column=0, row=4, columnspan=1)
# tree = ttk.Treeview(data_frame)
#tree = ttk.Treeview(data_frame, selectmode="browse", style="mystyle.Treeview", show="headings", height=10)




#tree.grid(column=1, row=3, columnspan=1)


# Κουμπιά ειναι μερους ενος frame
buttons_frame = Frame(root, relief=RAISED)
buttons_frame.config(bg="#C2C0BD")




# =================================ΑΝΑΖΉΤΗΣΗ===================================
search_data = StringVar()
search_entry = Entry(buttons_frame, textvariable=search_data, relief=RAISED)

search_image = PhotoImage(master = root, file="search.png")

search_button = Button(buttons_frame, command=lambda: search(search_data), text="Αναζήτηση",  bg="gray20", fg="white", bd=3, image=search_image, compound=LEFT, relief=RAISED)


#===============================Επιλογή πίνακα================================
choices = ["ΕΠΙΛΟΓΗ ΠΗΝΑΚΑ", "s", "c"]
table_var = StringVar(root)
table_var.set("ΕΠΙΛΟΓΗ ΠΗΝΑΚΑ")
table_menu = OptionMenu(buttons_frame, table_var, *choices)

select_table_button = Button(buttons_frame, text="Επιλογή πίνακα", command=lambda: select_table(root))

# ========================================================================================
# ------------------------------------Κουμπιά--------------------------------------------=
# ========================================================================================
reset_image = PhotoImage(master = root, file="refresh.png")

reset_button = Button(buttons_frame, text="Ανανέωση",  bg="gray15", fg="white", bd=3, command=lambda: update_view(root),
                      image=reset_image, compound=LEFT, relief=RAISED)


add_button = Button(buttons_frame, command=lambda: add_to(root), text="Προσθήκη", padx=10, pady=10, bg="green",
                    fg="white", bd=3)


del_button = Button(buttons_frame, command=del_from_tree, text="Διαγραφή απο λίστα", padx=10, pady=10,
                    bg="red", fg="white", bd=3)

edit_button = Button(buttons_frame, command=lambda: edit(root), text="Επεξεργασία", padx=10, pady=10, bg="green",
                     fg="white", bd=3)


file_button = Button(buttons_frame, text="Ανοιγμα αρχείου", padx=10, pady=10, bg="green", fg="white", bd=3,
                     command=lambda: open_file(root))


backup_button = Button(buttons_frame, padx=10, pady=10, bd=3, text="Αντίγραφο ασφαλείας", command=backup, bg="blue",
                       fg="white")
exit_button = Button(buttons_frame, bg="black", fg="white", padx=10, pady=10, bd=3, text='Εξωδος', command=root.destroy)


#======================Πληκτολόγιο=====================
def search_event(event):
    search(search_data)


search_entry.bind('<Return>', search_event)


#ΑΝΑΝΕΩΣΗ
def reset_event(event):

    update_view(root)


root.bind('<F5>', reset_event)


#ΕΞΩΔΟΣ
def quit(event):

    root.destroy()


root.bind('<Escape>', quit)


#FOCUS ΣΤΗΝ ΑΝΑΖΗΤΗΣΗ
def focus_search(event):

    search_entry.focus()


root.bind('<Control_L>', focus_search)


#ΠΡΟΣΘΗΚΗ
def add_event(event):

    add_to(root)


root.bind('<F1>', add_event)


#ΕΠΕΞΕΡΓΑΣΙΑ
def edit_event(event):

    edit(root)


root.bind('<F3>', edit_event)


# Εμφάνιση κουμιών και Logo
image = PhotoImage(master = root, file="logo-small-orange.png")
label_image = Label(root, image=image)
#label_image.grid(column=0, row=0, sticky="w")
#Δεν χρειάζεται το εμνφανίζει το func.py
#table_menu.grid(column=0, row=1, ipady=3, sticky="w")
#select_table_button.grid(column=0, row=1, ipady=3, sticky="e")
# Το file_button κάνει αυτόματα και ενημέρωση στο treeview
search_entry.grid(column=0, row=2,  ipady=3, ipadx=100, sticky="we")
search_entry.focus()
search_button.grid(column=1, row=2, )
reset_button.grid(column=2, row=2)
#file_button.grid(column=3, row=0)
#add_button.grid(column=4, row=0)
#edit_button.grid(column=5, row=0)
#backup_button.grid(column=6, row=0)
# Εχω βάλει απο πανω αλλο Το file_button κάνει αυτόματα και ενημέρωση στο treeview
# update_button.grid(sticky="we")
#del_button.grid(column=7, row=0)
#exit_button.grid(column=8, row=0)



##############################################   MENU    ##########################################
menubar = Menu(root)

filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Ανοιγμα αρχείου", command=lambda: open_file(root))

filemenu.add_command(label="Προσθήκη --> F1", command=lambda: add_to(root))
filemenu.add_command(label="Επεξεργασία --> F3", command=lambda: edit(root))
filemenu.add_separator()
filemenu.add_command(label="Διαγραφή", command=del_from_tree)
filemenu.add_command(label ="Εξωδος --> Esc", command=root.quit)
filemenu.add_command(label="make tabs", command=lambda: make_tabs(root))
menubar.add_cascade(label="Αρχείο", menu=filemenu)

backup_menu = Menu(menubar, tearoff=0)
backup_menu.add_command(label="===Αντίγραφο ασφαλείας!===", command=backup)
menubar.add_cascade(label="Αντίγραφο ασφαλείας", menu=backup_menu)


root.config(menu=menubar)
# Εμφάνιση των κουμίων που είναι στο frame αριστερά
buttons_frame.grid(row=2, column=0)


root.mainloop()
