"""
Sqlite Γραφικό περιβάλλον με Python3
version v 0.2 Το Edit δουλευει για όλες τις βάσεις
Πρεπει να φιάκω την επαναφορα γραμμη 624
===============================ΓΡΑΜΜΗ 405=======================
TO DO LIST   ********* ΠΡΕΠΕΙ ΝΑ ΤΑ ΒΑΛΩ ΟΛΛΑ ΣΕ CLASS ΓΙΑ ΝΑ ΠΕΞΟΥΝ ΣΩΣΤΑ *******************
TO DO LIST  0) Να φιάξω την επεξεργρασία επιλεγμένου απο το treeview  ΝΑ ΠΕΡΝΕΙ column αντι TONER=? κτλπ.------------Εγινε 29/10/2019
TO DO LIST  1) ΝΑ ΦΤΙΑΞΩ ΤΟ BACKUP DIRECTORY------------------------------------------------------------------------ΕΓΙΝΕ
TO DO LIST  2) ΤΟ TREE NA ΕΜΦΑΝΙΖΕΙ OTI ΒΑΣΗ ΚΑΙ ΝΑ ΕΠΙΛΕΞΩ--να εμφανίζει τους πίνακες------------------------------ΕΓΙΝΕ 30/10/2019
TO DO LIST  3) ΝΑ ΒΑΛΩ ΜΕΝΟΥ ---------------------------
TO DO LIST  4) ο χρήστης να επιλέγει τον πίνακα
TO DO LIST  5) ελεγχος αν ο χρήστης εισάγει αλφαριθμητικό ή αριθμό
TO DO LIST  6) Να βάλω να έχει log αρχείο
TO DO LIST  7) Να κάνει αυτόματα υπολογισμό το σύνολο (όταν έχουμε τιμη και τεμάχια)
TO DO LIST  8) Να βάλω triggers
"""

# Πρώτα αυτό για το Combobox
from tkinter import ttk

# Μετά αυτο για το Label Διαφορετικά βγαζει error για το font
from tkinter import *

# Για να επιλεξει ο χρήστης το αρχείο (ποια βάση δεδομένων θελει να ανοιξει)
from tkinter import filedialog

import sqlite3
# datetime για backup την βαση πριν κάθε αλλαγή
from datetime import datetime

# Import os για να κάνουμε τον φακελο backup
import os

# Για επιβεβέωση διαγραφής
import tkinter.messagebox


# Κουμπί να ανοιξει το αρχείο (βαση δεδομένων)
def open_file():
    dbase = filedialog.askopenfilename(initialdir=os.getcwd(), title="Επιλογή βάση δεδομένων", filetypes=(("db files",
                                                                                                           "*.db"), (
                                                                                                          "all files",
                                                                                                          "*.*")))
    return dbase


# ========================================Ενημέρωση εμφάνησεις δεδομένων=============================
table = ""  # Για να ορίσουμε πιο κάτω τον πίνακα σαν global
# Αδεία λίστα για να πάρουμε τα header απο τον πίνακα της βάσης δεδομένων
headers = []


def update_view(open_new_file="yes"):
    # Αν τρέξει απο το κουμπί προσθήκη του παραθύρου προσθήκη να μήν ανοιξει άλλο αρχείο
    # διαφορετικα να ανοιξει αρχείο
    if open_new_file == "yes":
        global dbase
        dbase = open_file()
    # Να σβήσει πρώτα τα δεδομένω για να πάρει τα καινούρια
    # map(tree.delete, tree.get_children())
    for i in tree.get_children():
        # Εμφάνηση το τι σβήνηει
        print("DELETED ΑΠΟ ΤΟ TREE ", i)
        tree.delete(i)

    up_conn = sqlite3.connect(dbase)
    print("=============Σύνδεση με Βαση Δεδομένων τώρα============= ", dbase)
    print()
    up_cursor = up_conn.cursor()

    # =======================Ανάγνωριση πίνκα δεδομένων=============
    up_cursor = up_conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_name = up_cursor.fetchall()
    dont_used_tables = ["sqlite_master", "sqlite_sequence", "sqlite_temp_master"]
    for name in table_name:
        if name[0] not in dont_used_tables:
            global table
            table = name[0]
            print("TABLE ", name[0])

    print("=========ΟΝΟΜΑ ΠΙΝΑΚΑ===========LINE 155 ", table)
    print()
    up_cursor.execute("SELECT * FROM " + table)
    global headers
    headers = list(map(lambda x: x[0], up_cursor.description))
    print("headers at line 80 ", headers)
    up_data = up_cursor.fetchall()
    print("up_data line 162 ", up_data)
    up_index = len(up_data)
    for n in range(len(up_data)):
        tree.insert("", up_index - 1, values=up_data[n])

    tree.grid(column=1, row=7)
    return dbase


root = Tk()
#root.geometry('1500x600+0+0')
root.title('Sqlite γραφικό περιβάλλον')
root.config(bg="#C2C0BD")
root.resizable(width=100, height=100)
# width = 1200
# height = 600
# screen_width = root.winfo_screenwidth()
# screen_height = root.winfo_screenheight()
# x = (screen_width / 2) - (width / 2)
# y = (screen_height / 2) - (height / 2)
# root.geometry("%dx%d+%d+%d" % (width, height, x, y))
# Τίτλος προγράμματος

app_title = Label(bg="brown", fg="white", text="MLShop Database", font=("Arial Bold", 15), bd=8, padx=8, )
app_title.grid(column=0, row=0)

# Περιοχη για παρουσήαση του πινακα της βασης
# Δεν χρειάζεται αφου ο χρήστης πρεπει να επιλέξει πρώτα αρχείο (dbase)
# cursor.execute('SELECT * FROM ΠΙΝΑΚΑΣ_ΑΝΑΛΩΣΙΜΑ')
# data = cursor.fetchall()

# Εμφανηση Κεφαλίδων του πίνακα
# ΠΡΩΤΟΣ τροπος ΕΔΩ χρησιμοποιώ ΤΟΝ ΔΕΥΤΕΡΟ ΤΡΟΠΟ ΑΠΟ ΚΑΤΩ
"""
headers = list(map(lambda x: x[0], cursor.description))
view_headers = Button(root, text=headers)
view_headers.grid(column=1, row=3)

for n in range(len(data)):
    view_colum = Label(root, text=data[n], bg="black", fg='white')
    view_colum.grid(column=1,  row=n+4, sticky=W)
"""
# Δευτερος  τροπος εμφανησεις των δεδομενων

# ------------------------Style------------------------------------
style = ttk.Style()
# Modify the font of the body
style.configure("mystyle.Treeview", highlightthickness=10, bd=10, font=('San Serif', 11))
style.configure("mystyle.Treeview.Heading", font=('San Serif', 13, 'bold'))  # Modify the font of the headings
style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders
style.configure("mystyle.Treeview", fg="red", rowheight=40, background="red")

# ------------------------Εμφάνιση δεδομένων σε Frame-------------------------
data_frame = Frame(root, bd=3, bg="#C2C0BD", relief="raise")
data_frame.grid(column=0, row=4)
# tree = ttk.Treeview(data_frame)
tree = ttk.Treeview(data_frame, selectmode="browse", style="mystyle.Treeview", show="headings")

# scrolls
scrolly = ttk.Scrollbar(root, orient='vertical', command=tree.yview)
scrolly.grid(column=1, row=4, sticky="ns")
tree.configure(yscrollcommand=scrolly.set)
scrollx = ttk.Scrollbar(root, orient='horizontal', command=tree.xview)
scrollx.grid(sticky='we', column=0, row=8)
tree.configure(xscrollcommand=scrollx.set)



# ΔΕΝ ΧΡΕΙΑΖΕΤΑΙ ΑΦΟΥ ΠΡΩΤΑ ΑΝΟΙΓΕΙ Ο ΧΡΗΣΤΗΣ ΤΟ ΑΡΧΕΙΟ (dbase)
# και κανει insert τα δεδομένω με function
# index = len(data)
# for n in range(len(data)):
#    tree.insert("", index - 1, values=data[n])

# tree.grid(column=1, row=7)


# Δήνουμε σαν παράμετρο "yes" για να ανοίξει νέο αρχείο
dbase = update_view("yes")
print("************DBASE NOW************** line 172", dbase)



print("**********************head, for head in headers************* Line 162", headers)
# tree["columns"] = sqlite3.Row
tree["columns"] = [head for head in headers]
#tree["columns"] = ["id", "TONER", "ΜΟΝΤΕΛΟΣ", "ΚΩΔΙΚΟΣ", "ΤΕΜΑΧΙΑ", "ΤΙΜΗ", "ΣΥΝΟΛΟ", "ΣΕΛΙΔΕΣ"]
#tree["show"] = "headings"
for head in headers:
    tree.column(head, anchor="center", width=150, stretch=True)
#tree.column("id", width=50, minwidth=50, anchor='center', stretch=True)
#tree.column("TONER", width=200, minwidth=100, anchor='center')
#tree.column("ΜΟΝΤΕΛΟΣ", width=670, minwidth=200, anchor='center')
#tree.column("ΚΩΔΙΚΟΣ", width=90, minwidth=90, anchor='center')
#tree.column("ΤΕΜΑΧΙΑ", width=90, minwidth=90, anchor='center')
#tree.column("ΤΙΜΗ", width=50, minwidth=50, anchor='center')
#tree.column("ΣΥΝΟΛΟ", width=70, minwidth=70, anchor='center')
#tree.column("ΣΕΛΙΔΕΣ", width=70, minwidth=70, anchor='center')
    tree.heading(head, text=head)
#tree.heading("id", text="id")
#tree.heading("TONER", text="TONER")
#tree.heading("ΜΟΝΤΕΛΟΣ", text="ΜΟΝΤΕΛΟ")
#tree.heading("ΚΩΔΙΚΟΣ", text="ΚΩΔΙΚΟΣ")
#tree.heading("ΤΕΜΑΧΙΑ", text="ΤΕΜΑΧΙΑ")
#tree.heading("ΤΙΜΗ", text="ΤΙΜΗ")
#tree.heading("ΣΥΝΟΛΟ", text="ΣΥΝΟΛΟ")
#tree.heading("ΣΕΛΙΔΕΣ", text="ΣΕΛΙΔΕΣ")


# Συνδεση με sqlite
conn = sqlite3.connect(dbase)
# Δημηουργεια κερσορα για να κοινουμαστε στην βάση
cursor = conn.cursor()


# ====================================================================================
# ================================Συναρτήσεις για τα κουμπιά==========================
# ------------------------------------------------------------------------------------
# --------------------------------Δημηουργία νεου παραθύρου---------------------------
def add_to():
    add_window = Toplevel()
    add_window.title("Προσθήκη δεδομένων")
    # Τίτλος παραθύρου
    add_window_title = Label(add_window, bg="brown", fg="white", text="Προσθήκη αναλώσιμου", font=("Arial Bold", 15),
                             bd=8, padx=3, )
    add_window_title.grid(column=1, row=0)

    # ------------------------------Να πάρουμε τις κεφαλίδες---------------------------

    conn = sqlite3.connect(dbase)
    cursor = conn.execute("SELECT * FROM " + table)

    headers = list(map(lambda x: x[0], cursor.description))
    print("HEADERS ============= Line 220 ", headers)

    # ===========================Εμφάνιση κεφαλίδων======================================
    # ΟΙ ΚΕΦΑΛΊΔΕΣ ΕΊΝΑΙ ΤΑ COLUMNS ΤΟΥ ΠΊΝΑΚΑ
    count_headers = 0  # Για να μετρίσουμε πόσες κεφαλίδες έχει ο πίνακας  χωρίς τα " ID " γιατι μας χρειάζεται για τα entry που θα κάνει ο χρήστης
    data_to_add = []
    for index, header in enumerate(headers):
        if header == "ID" or header == "id" or header == "Id":
            continue
        else:
            count_headers += 1
            toner_label = Label(add_window, text=header, width=10, padx=1, pady=1, font=("San Serif", 12, "bold"), bd=3)
            toner_label.grid(row=index + 1)
            var = StringVar()
            data_to_add.append(var)

            entry = Entry(add_window, textvariable=var, bd=2).grid(column=1, row=index + 1)

    # model_laber = Label(add_window, text=headers[1 if headers[0] != "ID" else 2], padx=3, pady=3,  font=("San Serif", 12, "bold"), bd=3)
    # model_laber.grid(row=3)
    # kodikos_label = Label(add_window, text=headers[2 if headers[0] != "ID" else 3], padx=3, pady=3,  font=("San Serif", 12, "bold"), bd=3)
    # kodikos_label.grid(row=4)
    # temaxia_label = Label(add_window, text=headers[3 if headers[0] != "ID" else 4], padx=3, pady=3,  font=("San Serif", 12, "bold"), bd=3)
    # temaxia_label.grid(row=5)
    # timi_laber = Label(add_window, text=headers[4 if headers[0] != "ID" else 5], padx=3, pady=3,  font=("San Serif", 12, "bold"), bd=3)
    # timi_laber.grid(row=6)
    # synolo_label = Label(add_window, text=headers[5 if headers[0] != "ID" else 6], padx=3, pady=3,  font=("San Serif", 12, "bold"), bd=3)
    # synolo_label.grid(row=7)
    # selides_label = Label(add_window, text=headers[6 if headers[0] != "ID" else 7], padx=3, pady=3,  font=("San Serif", 12, "bold"), bd=3)
    # selides_label.grid(row=8)

    # ===============Εισοδος δεδομένων στο παράθυρο add_windows==========================
    # ------------------------------Ορισμός μεταβλητών --------------------------------

    # for i in range(count_headers):
    #     headers[i] = StringVar()
    # Entry(add_window, textvariable=headers[i], bd=2).grid(column=1, row=[i if headers[0] == "id" else i+2])
    # ΑΠΟΘΗΚΕΥΣΗ ΔΕΔΟΜΕΝΩΝ ΠΟΥ ΕΙΣΑΓΕΙ Ο ΧΡΗΣΤΗΣ ΣΕ ΛΙΣΤΑ
    # data_to_add.append(headers[i].get())
    #     print("(headers[i].get()==========line 233 ", headers[i].get())
    # print("=================data to add =============== line 234 ", data_to_add)
    # # toner = StringVar()
    # model = StringVar()
    # kodikos = StringVar()
    # temaxia = IntVar()
    # timi = DoubleVar()
    # synolo = timi.get() * temaxia.get()
    # selides = StringVar()
    # #-----------------------------Ορισμός εμφάνησεις εισόδου χρήστη-------------------

    # Entry(add_window, textvariable=toner, bd=2).grid(column=1, row=2)
    # Entry(add_window, textvariable=model, bd=2).grid(column=1, row=3)
    # Entry(add_window, textvariable=kodikos, bd=2).grid(column=1, row=4)
    # Entry(add_window, textvariable=temaxia, bd=2).grid(column=1, row=5)
    # Entry(add_window, textvariable=timi, bd=2).grid(column=1, row=6)
    # Label(add_window, textvariable=synolo, bd=2).grid(column=1, row=7)
    # Entry(add_window, textvariable=selides, bd=2).grid(column=1, row=8)
    # toner_entry.grid(column=1, row=2)
    # toner = toner_entry.get()

    # model_entry = Entry(add_window, textvariable=model)
    # model_entry.grid(column=1, row=3)
    # model = model_entry.get()

    # kodikos_entry = Entry(add_window, textvariable=kodikos)
    # kodikos_entry.grid(column=1, row=4)
    # kodikos = kodikos_entry.get()

    # temaxia_entry = Entry(add_window, textvariable=temaxia)
    # temaxia_entry.grid(column=1, row=5)
    # temaxia = temaxia_entry.get()
    #
    # timi_entry = Entry(add_window, textvariable=timi)
    # timi_entry.grid(column=1, row=6)
    # timi = timi_entry.get()
    #
    # synolo_entry = Entry(add_window, textvariable=synolo)
    # synolo_entry.grid(column=1, row=7)
    # synolo =  synolo_entry.get()
    #
    # selides_entry = Entry(add_window, textvariable=selides)
    # selides_entry.grid(column=1, row=8)
    # selides = synolo_entry.get()

    # ------------------------------------Προσθήκη δεδομένων στην βάση------------------
    def add_to_db():
        global headers
        culumns = ",".join(headers)
        # Να ορίσουμε τα VALUES ΤΗΣ SQL οσα είναι και τα culumns
        # values είναι πόσα ? να έχει ανάλογα τα culumns
        values_var = []

        for header in headers:
            if header == "ID" or header == "id" or header == "Id":
                values_var.append("NULL")
            else:
                values_var.append('?')
        values = ",".join(values_var)
        print("============values_var============line 295", values)
        # print("==========culumns===========", culumns)
        data = []
        for i in range(len(data_to_add)):
            data.append(data_to_add[i].get())
        # data = tuple(data_to_add)
        print("===========DATA TO ADD AFTER LOOP =========LINE 294 ", data)
        # data_to_add = (toner.get(), model.get(), kodikos.get(),
        #               temaxia.get(), str(timi.get()) + " €", str(timi.get() * temaxia.get()) + " €", selides.get())

        # ΒΑΖΟΥΜΕ ΤΟ ΠΡΩΤΟ NULL ΓΙΑ ΝΑ ΠΆΡΕΙ ΜΟΝΟ ΤΟΥ ΤΟ ID = PRIMARY KEY
        # H ΣΥΝΤΑΞΗ ΕΙΝΑΙ ΑΥΤΉ
        # INSERT        INTO         table(column1, column2,..)        VALUES(value1, value2, ...);  TA  VALUES πρεπει να είναι tuple
        # sql_insert = "INSERT INTO  " + table + "(" + culumns + ")" + "VALUES(NULL, ?, ?, ?, ?, ?, ?, ?);"
        sql_insert = "INSERT INTO  " + table + "(" + culumns + ")" + "VALUES(" + values + ");"  # values είναι πόσα ? να έχει ανάλογα τα culumns
        print("===============sql_insert==========\n", sql_insert)
        print("=======DATA TO ADD===== LINE 291 \n", data_to_add)

        cursor.execute(sql_insert, tuple(data))

        conn.commit()
        # Ενημέρωση του tree με τα νέα δεδομένα
        open_new_file = "no"
        update_view(open_new_file)

        print("Εγινε η προσθήκη")
        print(data)

    # ----------------------------------Κουμπί για να γίνει η προσθήκη-------------------
    enter_button = Button(add_window, text="Προσθήκη", bg="green", fg="White", bd=8, padx=5, pady=8, command=add_to_db)
    enter_button.grid(column=1, row=9)


# Κουμπιά ειναι μερους ενος frame
buttons_frame = Frame(root, relief='raised')
buttons_frame.config(bg="#C2C0BD")


# ========================================================================================
# ------------------------------------- ΕΠΕΞΕΡΓΑΣΙΑ -------------------------------------=
# ========================================================================================
def edit():
    # ===============ΠΡΩΤΑ BACKUP =========
    backup()
    print("tree.selection()", (tree.set(tree.selection(), '#1')))
    selected_item = (tree.set(tree.selection(), '#1'))
    edit_conn = sqlite3.connect(dbase)
    edit_cursor = edit_conn.cursor()
    edit_cursor.execute("SELECT * FROM " + table + " WHERE ID = ?", (selected_item,))
    selected_data = edit_cursor.fetchall()
    selected_data = list(selected_data[0])
    print("selected_data line 349 ", selected_data)
    # δεν χρειάζεται το πέρνει απο το global headers
    # headers = list(map(lambda x: x[0], edit_cursor.description()),)
    print("headers[0] γραμμή 333 = ", headers[0])
    edit_window = Toplevel()
    edit_window.title("Επεξεργασία δεδομέμων")
    edit_window_title = Label(edit_window, bg="brown", fg="white", text="Επεξεργασία αναλώσιμου",
                              font=("Arial Bold", 15),
                              bd=8, padx=3, )
    edit_window_title.grid(column=1, row=0)
    Label(edit_window, text=tree.selection()).grid(column=0, row=0)
    # ===========================Εμφάνιση κεφαλίδων======================================
    count_headers = 0
    data_to_add = []
    for index, header in enumerate(headers):
        if header == "ID" or header == "id" or header == "Id":
            continue
        else:
            count_headers += 1
            toner_label = Label(edit_window, text=header, width=10, padx=1, pady=1, font=("San Serif", 12, "bold"), bd=3)
            toner_label.grid(row=index + 1)
            var = StringVar(edit_window, value=selected_data[index])
            data_to_add.append(var)
            print("------------ΜΗ ΕΠΕΞΕΡΓΑΣΜΈΝΑ ΔΕΔΟΜΈΝΑ------------", var.get())
            entry = Entry(edit_window, textvariable=var, bd=2, width=len(var.get())).grid(column=1, row=index + 1, sticky="we")
            ########################################################################################
            ################################  LAST COMMENT START #########################################
            ########################################################################################
    # toner_label = Label(edit_window, text=headers[1], width=10, padx=1, pady=1, font=("San Serif", 12, "bold"), bd=3)
    # toner_label.grid(row=2)
    # model_laber = Label(edit_window, text=headers[2], padx=3, pady=3, font=("San Serif", 12, "bold"), bd=3)
    # model_laber.grid(row=3)
    # kodikos_label = Label(edit_window, text=headers[3], padx=3, pady=3, font=("San Serif", 12, "bold"), bd=3)
    # kodikos_label.grid(row=4)
    # temaxia_label = Label(edit_window, text=headers[4], padx=3, pady=3, font=("San Serif", 12, "bold"), bd=3)
    # temaxia_label.grid(row=5)
    # timi_laber = Label(edit_window, text=headers[5], padx=3, pady=3, font=("San Serif", 12, "bold"), bd=3)
    # timi_laber.grid(row=6)
    # synolo_label = Label(edit_window, text=headers[6], padx=3, pady=3, font=("San Serif", 12, "bold"), bd=3)
    # synolo_label.grid(row=7)
    # selides_label = Label(edit_window, text=headers[7], padx=3, pady=3, font=("San Serif", 12, "bold"), bd=3)
    # selides_label.grid(row=8)
    # # -------------------------Εμφάνηση τιμών απο το επιλεγμένο στοιχείο-----------------
    # toner_data = StringVar(edit_window, value=selected_data[1])
    # toner_entry = Entry(edit_window, textvariable=toner_data, width=100, font=("San Serif", 12, "bold"), bd=3)
    # toner_entry.grid(column=1, row=2, sticky="w")
    #
    # model_data = StringVar(edit_window, value=selected_data[2])
    # model_entry = Entry(edit_window, textvariable=model_data, width=100, font=("San Serif", 12, "bold"), bd=3)
    # model_entry.grid(column=1, row=3, sticky="w")
    #
    # kodikos_data = StringVar(edit_window, value=selected_data[3])
    # kodikos_entry = Entry(edit_window, textvariable=kodikos_data, font=("San Serif", 12, "bold"), bd=3)
    # kodikos_entry.grid(column=1, row=4, sticky="w")
    #
    # temaxia_data = IntVar(edit_window, value=selected_data[4])
    # temaxia_entry = Entry(edit_window, textvariable=temaxia_data, font=("San Serif", 12, "bold"), bd=3)
    # temaxia_entry.grid(column=1, row=5, sticky="w")
    #
    # timi_data = DoubleVar(edit_window, value=selected_data[5])
    # timi_entry = Entry(edit_window, textvariable=timi_data, font=("San Serif", 12, "bold"), bd=3)
    # timi_entry.grid(column=1, row=6, sticky="w")
    #
    # # Το σύνολο μόνο θα το εμφανίζει δεν χρειάζεται να το αλλάξει ο χρήστης
    # synolo_label = Label(edit_window, text=selected_data[6], padx=3, pady=3, font=("San Serif", 12, "bold"), bd=3)
    # synolo_label.grid(column=1, row=7, sticky="w")
    #
    # selides_data = StringVar(edit_window, value=selected_data[7])
    # selides_entry = Entry(edit_window, textvariable=selides_data, font=("San Serif", 12, "bold"), bd=3)
    # selides_entry.grid(column=1, row=8, sticky="w")

    ########################################################################################
    ################################  LAST COMMENT  END   #########################################
    ########################################################################################


    # test_data = StringVar(edit_window, value=selected_data[1])
    # test_entry = Entry(edit_window, textvariable=test_data).grid(column=2, row=2)

    # --------------------   Προσθήκη δεδομένων στην βάση -------------------------------
    # ---------------------- μετά την επεξεργασία   -------------------------------------
    def update_to_db():

        #culumns = ",".join(headers)
        #print("==========culumns=========== line 436 ", culumns)
        #Τα culumns ειναι της μορφής ID, ΤΟΝΕΡ, ΜΟΝΤΕΛΟ, ΚΩΔΙΚΟΣ κτλπ.
        #Πρεπει να γίνουν ΤΟΝΕΡ=?, ΜΟΝΤΕΛΟ=?, ΚΩΔΙΚΟΣ=? κτλπ για την σύνταξη της sql
        #Ευκολο άν μπουν σε νεα λίστα παρά να τροποποιησω την υπάρχουσα λίστα
        edited_culumns = []
        for culumn in headers:
            if culumn == "id" or culumn == "ID":
                continue
            else:
                edited_culumns.append(culumn + "=?")
        culumns = ",".join(edited_culumns)
        print("-------------edited_culumns--------------", edited_culumns)
        # ====================ΕΠΙΛΕΓΜΈΝΟ ID =================
        selected_item = tree.selection()
        selected_id = tree.set(selected_item, "#1")
        print("==========selected_id==========LINE 447 \n", selected_id)

        # Θα βάζει το data_to_add απο πάνω γραμμη 371
        #βαζουμε και το id που χρειάζεται για το WHERE ID=?
        edited_data = []
        for data in data_to_add:
            edited_data.append(data.get())
        edited_data.append(selected_id)
        # data_to_add = (toner_data.get(), model_data.get(), kodikos_data.get(),
        #                temaxia_data.get(), str(timi_data.get()) + " €",
        #                str(timi_data.get() * temaxia_data.get()) + " €", selides_data.get(), selected_id)
        print("========edited data ======line 482", tuple(edited_data))
        # H ΣΥΝΤΑΞΗ ΕΙΝΑΙ ΑΥΤΉ
        # sql_insert = "INSERT INTO  " + table + "(" + culumns + ")" + "VALUES(NULL, ?, ?, ?, ?, ?, ?, ?);"
        # sqlite_update_query = """Update new_developers set salary = ?, email = ? where id = ?"""
        edit_cursor.execute("UPDATE " + table + "  SET " + culumns + " WHERE ID=? ",
            (tuple(edited_data)))
        print(60 * "*")
        print(50 * "*", "UPDATED", 50 * "*")
        print(60 * "*")
        edit_conn.commit()
        print("===============Το προΐον ενημερώθηκε με επιτυχία ==========LINE 411")
        print("==========Παλιά δεδομένα===========LINE 472 \n", selected_data)

        print("==========Νέα δεδομένα============ LINE 474 \n", edited_data)

        # Ενημέρωση του tree με τα νέα δεδομένα
        open_new_file = "no"
        update_view(open_new_file)

        print("Εγινε η προσθήκη")
        print(data_to_add)

    update_button = Button(edit_window, command=update_to_db, text="Ενημέρωση πρωιόντος", padx=10, pady=10, bg="red",
                           fg="white", bd=3)
    update_button.grid(column=1, row=9)


# ========================================================================================
# -------------------------------------BACK UP ------------------------------------------=
# ========================================================================================
# Αντιγραφα ασφαλείας βασης δεδομένων
def progress(status, remainig, total):
    print(f"{status} Αντιγράφηκαν {total - remainig} απο {total} σελίδες...")


def backup():
    try:
        now = datetime.now().strftime("%d %m %Y %H %M %S")
        today = datetime.today().strftime("%d %m %Y")
        back_dir = "backups" + "\\" + today + "\\"

        backup_file = os.path.join(back_dir, os.path.basename(dbase[:-3]) + " " + now + ".db")
        print("============BACKUP FILE============\n", backup_file, "\n")
        if not os.path.exists(back_dir):
            os.makedirs(back_dir)
        else:
            pass
        # Υπάρχουσα βάση
        conn = sqlite3.connect(dbase)
        print("===========Υπάρχουσα βάση============\n ", dbase, "\n")

        # Δημιουργία νέας βάσης και αντίγραφο ασφαλείας
        back_conn = sqlite3.connect(backup_file)
        with back_conn:
            conn.backup(back_conn, pages=10, progress=progress)
            back_conn.close()
            text = "Η βάση αντιγράφηκε :  "
            result = text + os.path.realpath(backup_file)
            print("=====Αποτέλεσμα ====\n", result)
            show_backup.configure(text=result)
    except FileNotFoundError as file_error:
        print("File Error", file_error)
        backup()
    except sqlite3.Error as error:
        if os.path.exists(backup_file):
            result = os.path.abspath(backup_file)
        else:
            result = "Σφάλμα κατα την αντιγραφή : ", error
    finally:
        try:
            if back_conn:
                back_conn.close()
                print("Συνδεση με ", backup_file, " διακόπηκε")
        except UnboundLocalError as error:
            print(f"Η σύνδεση με {backup_file} δεν έγινε ποτέ {error}")


# ================================Συνάρτηση για διαγραφή  =================
# να τα βαλω σε μια λιστα για επιβεβαιωση διαγραφής
def del_from_tree():
    backup()
    selected_item = (tree.set(tree.selection(), '#1'))

    del_conn = sqlite3.connect(dbase)
    del_cursor = del_conn.cursor()
    del_cursor.execute("SELECT * FROM " + table + " WHERE ID = ?", (selected_item,))
    selected_data = del_cursor.fetchall()
    selected_data = list(selected_data[0])

    # ======================ΕΠΙΒΕΒΑΙΩΣΗ ΔΙΑΓΡΑΦΗΣ============
    answer = tkinter.messagebox.askquestion("Θα πραγματοποιηθεί διαγραφή!",
                                            " Είστε σήγουρος για την διαγραφή του {};".format(selected_data))
    if answer == 'yes':
        tkinter.messagebox.showinfo('Διαγραφή...', "Το {} διαγράφηκε!".format(selected_data))

        pass
    else:
        tkinter.messagebox.showinfo('Ακύρωση διαγραφής', " Τίποτα δεν διαγράφηκε  ")
        print("=================ΑΚΥΡΟΣΗ ΔΙΑΓΡΑΦΗΣ===============line 509\n", selected_data)
        print()
        return

    # del_conn = sqlite3.connect(dbase)
    # del_cursor = del_conn.cursor()
    # cursor.execute("DELETE FROM ΠΙΝΑΚΑΣ_ΑΝΑΛΩΣΙΜΑ WHERE ΚΩΔΙΚΟΣ IS 'None'") #Διαγραφή άδειων γραμμών που δεν έχουν κωδικο προιοντος
    del_cursor.execute("DELETE FROM " + table + " WHERE ID=?", (selected_item,))
    del_conn.commit()
    del_conn.close()
    print("===============ΠΡΑΓΜΑΤΟΠΟΙΗΘΗΚΕ ΔΙΑΓΡΑΦΉ ΤΟΥ===============\n", selected_data)
    print()

    try:
        tree.delete(tree.selection())
        print("=============================ΕΓΙΝΕ ΔΙΑΓΡΑΦΗ ΑΠΟ ΤΟ TREE====================================line 524 ")
        return selected_item
    except TclError as error:
        print("ΣΦΑΛΜΑ", error)


#=====================================ΑΝΑΖΗΤΗΣΗ=========================================
def Search():
    if search_data.get() != "":
        tree.delete(*tree.get_children())
        search_conn = sqlite3.connect(dbase)
        search_cursor = search_conn.cursor()
        #idea = SELECT * FROM tablename WHERE name or email or address or designation = 'nagar';

        search_cursor.execute("SELECT * FROM " + table + " WHERE ΤΟΝΕΡ LIKE ? OR ΜΟΝΤΕΛΟ LIKE ? OR ΚΩΔΙΚΟΣ LIKE ? OR TEMAXIA LIKE ? OR ΤΙΜΗ LIKE ? OR  ΣΥΝΟΛΟ LIKE ? OR ΣΕΛΙΔΕΣ LIKE ?",
                       ('%' + str(search_data.get()) + '%', '%' + str(search_data.get()) + '%', '%' + str(search_data.get()) + '%', '%' + str(search_data.get()) + '%', '%' + str(search_data.get()) + '%', '%' + str(search_data.get()) + '%', '%' + str(search_data.get()) + '%'))
        fetch = search_cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
        search_cursor.close()
        search_conn.close()
# ------------------------------------Κουμπιά------------------------------------------------------------------------
# δεν χρειάζεται αυτο γιατί έχω βάλει απο κάτω αλλο Το file_button κάνει αυτόματα και ενημέρωση στο treeview
# file_button = Button(buttons_frame, bg="gray10", text="Ανοιγμα αρχείου", padx=10, pady=10, bd=3, fg="white", command=open_file)


# =================================ΑΝΑΖΉΤΗΣΗ===================================
search_data = StringVar()
search_entry = Entry(buttons_frame, textvariable=search_data)
search_button = Button(buttons_frame, command=Search, text="Αναζήτηση", padx=10, pady=10, bg="green", fg="white", bd=3)
open_new_file = "no"
reset_button = Button(buttons_frame, text="Επαναφορά", padx=10, pady=10, bg="green", fg="white", bd=3, command=update_view(open_new_file))

add_button = Button(buttons_frame, command=add_to, text="Προσθήκη", padx=10, pady=10, bg="green", fg="white", bd=3)
del_button = Button(buttons_frame, command=del_from_tree, text="Διαγραφή απο λίστα", padx=10, pady=10, bg="red",
                    fg="white", bd=3)
edit_button = Button(buttons_frame, command=edit, text="Επεξεργασία", padx=10, pady=10, bg="green", fg="white", bd=3)
file_button = Button(buttons_frame, text="Ανοιγμα αρχείου", padx=10, pady=10, bg="green", fg="white", bd=3,
                     command=update_view)
backup_button = Button(buttons_frame, padx=10, pady=10, bd=3, text="Αντίγραφο ασφαλείας", command=backup, bg="blue",
                       fg="white")
exit_button = Button(buttons_frame, bg="black", fg="white", padx=10, pady=10, bd=3, text='Εξωδος', command=root.destroy)

# update_text1 = Button(root, text='Ενημέρωση', command=text1_update, bg='green', fg='white')
show_backup = Label(root, text="", bg="#C2C0BD", fg="black", font=("Arial Bold", 15))

# Εμφάνιση κουμιών και Logo
image = PhotoImage(file="logo-small-orange.png")
label_image = Label(root, image=image)
label_image.grid(column=0, row=0, sticky="w")

# Το file_button κάνει αυτόματα και ενημέρωση στο treeview
search_button.grid(column=3, row=2)
search_entry.grid(column=2, row=2,  ipady=3, ipadx=100)
search_entry.focus()
reset_button.grid(column=4, row=2)
file_button.grid(column=3, row=0)
add_button.grid(column=4, row=0)
edit_button.grid(column=5, row=0)
backup_button.grid(column=6, row=0)
# Εχω βάλει απο πανω αλλο Το file_button κάνει αυτόματα και ενημέρωση στο treeview
# update_button.grid(sticky="we")
del_button.grid(column=7, row=0)
exit_button.grid(column=8, row=0)

# Εμφάνιση αν έγινε το backup
show_backup.grid(column=0, row=9)

# Εμφάνιση των κουμίων που είναι στο frame αριστερά
buttons_frame.grid(row=2, column=0)


# search_button = Button(text='Search', command=search)
# search_button.grid(root)


conn.close()

root.mainloop()
