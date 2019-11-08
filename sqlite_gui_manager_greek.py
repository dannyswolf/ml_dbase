# coding=utf-8
"""
Sqlite Γραφικό περιβάλλον με Python3
******************************************************************
************** ΔΕΝ ΔΗΜΗΟΥΡΓΕΙ ΒΑΣΗ ΟΥΤΕ ΠΙΝΑΚΕΣ*******************
** Οι βάσεις πρέπει να έχουν Id ή id ή ID intiger και NOT NULL  **
******************************************************************

Version Για το μαγαζί                                               8/11/2019
Ολα δουλευουν

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
root.geometry('1200x620+100+100')
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


# ------------------------Style------------------------------------
style = ttk.Style()
# # Modify the font of the body
#style1.theme_create("mystyle.Treeview", parent="alt")
#style.configure("Custom.Treeview.Heading", background="blue", foreground="white", relief="flat")
style.map("Treeview.Heading", relief=[('active', 'groove'), ('pressed', 'sunken')])
style.configure("mystyle.Treeview", highlightthickness=0, width=150, font=('San Serif', 11))  # Εμφάνηση δεδομένων
style.configure("TNotebook.Tab", padding=[50, 1], background="green", foreground="black")  # configure "tabs" background color
#"map": {"background": [("selected", myred)],"expand": [("selected", [1, 1, 1, 0])]}

style.configure("mystyle.Treeview.Heading", font=('San Serif', 13, 'underline'), background="green", foreground="black", relief="groove")  # Modify the font of the headings
style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders
style.configure("mystyle.Treeview", rowheight=40)
#style1.theme_use("mystyle.Treeview")
        # -------------------------New Style--------------------------------
style1 = ttk.Style()
mygreen = "gray"
myred = "green"
# Styles - normal, bold, roman, italic, underline, and overstrike.
style1.theme_create("yummy", parent="alt", settings={
        "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0]}},
        "Treeview": {"configure": {"font": ['San Serif', 13, "normal"]}, "rowhight": 10, "highlightthickness": 10, "background": [("selected", myred)]},
        "Treeview.treearea": {"configure": {'sticky': 'nswe'}},
        "Treeview.Heading": {"configure": {"font": ['San Serif', 11, 'bold']}, "background": "blue",
                            "foreground": "white", "relief": "flat"},
        "TNotebook.Tab": {
            "configure": {"padding": [50, 1], "background": mygreen, "foreground": "white"},
            "map": {"background": [("selected", myred)],
                    "expand": [("selected", [1, 1, 1, 0])]}}})

        #style1.theme_use("yummy")


# Τίτλος προγράμματος
app_title = Label(root, bg="brown", fg="white", text="MLShop Database", font=("Arial Bold", 15), bd=8 )
#app_title.grid(column=0, row=0, sticky="we")


# ------------------------Εμφάνιση δεδομένων σε Frame-------------------------

buttons_frame = Frame(root, bg="#C2C0BD", relief=RAISED)
buttons_frame.grid(column=0, row=1)
search_frame = Frame(root, bg="#C2C0BD")


# =================================ΑΝΑΖΉΤΗΣΗ===================================
search_data = StringVar()
search_entry = Entry(buttons_frame, textvariable=search_data, relief=RAISED)

search_image = PhotoImage(master=search_frame, file="search.png")
search_button = Button(buttons_frame, command=lambda: search(search_data), text="Αναζήτηση",  bg="gray20", fg="white", bd=3, image=search_image, compound=LEFT, relief=RAISED)

# =======================Δημιουργία Tree==========================


#data_frame.grid(column=0, row=3, columnspan=2)
#(column=1, row=1)


# ========================================================================================
# ------------------------------------Κουμπιά--------------------------------------------=
# =======================================================================================
#
# add_button = Button(buttons_frame, command=lambda: add_to(root), text="Προσθήκη", padx=10, pady=10, bg="green",
#                     fg="white", bd=3)
#
#
# del_button = Button(buttons_frame, command=del_from_tree, text="Διαγραφή απο λίστα", padx=10, pady=10,
#                     bg="red", fg="white", bd=3)
#
# edit_button = Button(buttons_frame, command=lambda: edit(root), text="Επεξεργασία", padx=10, pady=10, bg="green",
#                      fg="white", bd=3)
#
#
# file_button = Button(buttons_frame, text="Ανοιγμα αρχείου", padx=10, pady=10, bg="green", fg="white", bd=3,
#                      command=lambda: open_file(root))
#
# backup_button = Button(buttons_frame, padx=10, pady=10, bd=3, text="Αντίγραφο ασφαλείας", command=backup, bg="blue",
#                        fg="white")
# exit_button = Button(buttons_frame, bg="black", fg="white", padx=10, pady=10, bd=3, text='Εξωδος', command=root.destroy)
#

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
search_entry.grid(column=0, row=3,  ipady=10, ipadx=400, sticky="we")
search_entry.focus_force()
search_button.grid(column=1, row=3, ipadx=10, ipady=7)
#search_frame.grid(column=0, row=2)
#data_frame.grid(column=0, row=3)
#tree.grid(column=0, row=3)
#reset_button.grid(column=2, row=2)
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
#filemenu.add_command(label="make tabs", command=lambda: make_tabs(root))
menubar.add_cascade(label="Αρχείο", menu=filemenu)

backup_menu = Menu(menubar, tearoff=0)
backup_menu.add_command(label="===Αντίγραφο ασφαλείας!===", command=backup)
menubar.add_cascade(label="Αντίγραφο ασφαλείας", menu=backup_menu)


root.config(menu=menubar)
# Εμφάνιση των κουμίων που είναι στο frame αριστερά
#buttons_frame.grid(row=2, column=0)


root.mainloop()
