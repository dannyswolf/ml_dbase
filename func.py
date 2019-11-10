# coding=utf-8
"""
Sqlite Γραφικό περιβάλλον με Python3
******************************************************************
** Οι βάσεις πρέπει να έχουν Id ή id ή ID intiger και NOT NULL  **
******************************************************************

Version v0.8 Για το μαγαζί δουλευουν ολα ----------------------------10/11/2019
Στην v0.7  έφτιαχνε συνεχεια frames στο root
ΕΓΙΝΕ ΚΑΘΑΡΣΙΣΜΟΣ ΚΩΔΙΚΑ
ΠΡΕΠΕΙ ΝΑ ΚΑΝΩ ΤΟ ΣΥΝΟΛΟ = TIMI * TEMAXIA


Version v0.7 Για το μαγαζί δουλευουν ολα ----------------------------9/11/2019
ΠΡΕΠΕΙ ΝΑ ΚΑΝΩ ΤΟ ΣΥΝΟΛΟ = TIMI * TEMAXIA

Version Για το μαγαζί                                               8/11/2019
Ολα δουλευουν   να κανω στο Line 103

version v 0.5 Ο χρήστης μπορεί να επιλεξει πίνακα
version v 0.4 Προσθήκη menu
version v 0.3 Η αναζήτηση δουλευει για ολες τις Βάσεις και πινακες


===============================ΓΡΑΜΜΗ 405=======================
TO DO LIST   ********* ΠΡΕΠΕΙ ΝΑ ΤΑ ΒΑΛΩ ΟΛΛΑ ΣΕ CLASS ΓΙΑ ΝΑ ΠΕΞΟΥΝ ΣΩΣΤΑ *******************
TO DO LIST  0) Να φιάξω την επεξεργρασία επιλεγμένου απο το treeview  ΝΑ ΠΕΡΝΕΙ column αντι TONER=? κτλπ.------------Εγινε 29/10/2019
TO DO LIST  1) ΝΑ ΦΤΙΑΞΩ ΤΟ BACKUP DIRECTORY------------------------------------------------------------------------ΕΓΙΝΕ
TO DO LIST  2) ΤΟ TREE NA ΕΜΦΑΝΙΖΕΙ OTI ΒΑΣΗ ΚΑΙ ΝΑ ΕΠΙΛΕΞΩ--να εμφανίζει τους πίνακες------------------------------ΕΓΙΝΕ 30/10/2019
TO DO LIST  3) ΝΑ ΒΑΛΩ ΜΕΝΟΥ ---------------------------------------------------------------------------------------Εγινε 1/11/2019
TO DO LIST  4) ο χρήστης να επιλέγει τον πίνακα---------------------------------------------------------------------Εγινε 6/11/2019
TO DO LIST  5) ελεγχος αν ο χρήστης εισάγει αλφαριθμητικό ή αριθμό
TO DO LIST  6) Να βάλω να έχει log αρχείο
TO DO LIST  7) Να κάνει αυτόματα υπολογισμό το σύνολο (όταν έχουμε τιμη και τεμάχια)
TO DO LIST  8) Να βάλω triggers
TO DO LIST  9) Να βάλω στο μενοu RUN SQL
"""


# Πρώτα αυτό για το Combobox
from tkinter import ttk, Frame, Button, Tk, Label, RAISED, PhotoImage, Menu, StringVar, Entry, filedialog, messagebox, LEFT, FALSE, Toplevel
import sqlite3
# Μετά αυτο για το Label Διαφορετικά βγαζει error για το font
#from tkinter import *

# Για να επιλεξει ο χρήστης το αρχείο (ποια βάση δεδομένων θελει να ανοιξει)
# from tkinter import filedialog

# datetime για backup την βαση πριν κάθε αλλαγή
from datetime import datetime

# Import os για να κάνουμε τον φακελο backup
import os

# Για επιβεβέωση διαγραφής
# import tkinter.messagebox




table = ""  # Για να ορίσουμε πιο κάτω τον πίνακα σαν global
# Αδεία λίστα για να πάρουμε τα header απο τον πίνακα της βάσης δεδομένων
headers = []  # Για να περσνουμε της επικεφαλίδες καθε πίνκα
dbase = ""
tables =[]
up_data = []    # Για να πάρουμε τα δεδομένα
dic_data = {}   # [μελανακια] = [brother , 12115, 1, 20€, κτλπ ]
tabs = []       # Για το Notebook
tree = ""


# Κουμπί να ανοιξει το αρχείο (βαση δεδομένων)
def open_file(root):

    global dbase
    # Να σβήσουμε παλιά κουμπιά και tree αν ανοιξουμε αλη βαση δεδομένων
    list = root.grid_slaves()
    print("list root.grid.slaves line 78", list)
    for i in list:
        if len(list) > 1:
            print("i line 73", i)
            if ".!frame" in str(i):
                print(i, "deleted line 83")
                i.destroy()

            elif ".!scrollbar" in str(i):
                print(i, "deleted line 87")
                i.destroy()
        else:
            print("list root.grid.slaves  after deleted line 90", list)
            continue
    dbase = filedialog.askopenfilename(initialdir=os.getcwd(), title="Επιλογή βάσης δεδομένων",
                                           filetypes=(("db files",
                                                       "*.db"), (
                                                          "all files",
                                                          "*.*")))

    print("======================opened file ===================line 98", dbase)
    get_tables()
    select_table(root)
    return dbase


#Ορισμός πινάκων
def get_tables():
    global tables
    tables = []
    # =======================Ανάγνωριση πίνκα δεδομένων=============
    conn = sqlite3.connect(dbase)
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_name = cursor.fetchall()
    cursor.close()
    conn.close()
    dont_used_tables = ["sqlite_master", "sqlite_sequence", "sqlite_temp_master"]
    for name in table_name:
        if name[0] not in dont_used_tables:
            tables.append(name[0])
            print("TABLE ", name[0], " ========added to tables line 118")

        else:
            continue

    return tables


#Δημιουργια κουμπιών συμφονα με τους πινακες της βασης
def select_table(root):
    global tables

    print(tables, "Line 130")
    buttons = []

    # Αλλαγή χρώματος κουμπιου που πατιετε
    def change_color(btn):
        print("btn_pressed Line 135", btn)
        print("buttons line 136", buttons)
        for button in buttons:
            #allazei ta xromata se ayto poy pataw
            if button == btn:
                btn.configure(background="#EFA12C")
            else:
                button.configure(background="gray20")

    search_frame = Frame(root, bg="#C2C0BD")

    # ======================Πληκτολόγιο=====================
    def search_event(event):
        search(search_data)

    # FOCUS ΣΤΗΝ ΑΝΑΖΗΤΗΣΗ
    def focus_search(event):

        search_entry.focus()

    root.bind('<Control_L>', focus_search)

    search_data = StringVar()
    search_entry = Entry(search_frame, textvariable=search_data, relief=RAISED)

    search_button = Button(search_frame, command=lambda: search(search_data), text="Αναζήτηση", bg="gray20",
                           fg="white", bd=0, compound=LEFT, relief=RAISED)

    search_entry.bind('<Return>', search_event)
    search_entry.grid(column=0, row=3, ipady=3, ipadx=200, sticky="we")
    search_entry.focus_force()

    search_button.grid(column=1, row=3, ipadx=1, ipady=1)
    buttons_frame = Frame(root, bg="#C2C0BD", relief=RAISED)
    print("buttons_frame exists line 169", buttons_frame)

    #-------------------------------------------------------------------Κουμπιά -----------------------------------

    btn1 = Button(buttons_frame, command=lambda: [update_view(root, tables[0]), change_color(btn1)], text=tables[0], bg="gray20", fg="white", bd=5, compound=LEFT, relief="raised")
    buttons.append(btn1)
    btn1.grid(row=0, column=0, ipadx=15, ipady=20)
    print("Table Line 176", tables[0])
    btn2 = Button(buttons_frame, command=lambda: [update_view(root, tables[1]), change_color(btn2)], text=tables[1], bg="gray20", fg="white", bd=5, compound=LEFT, relief="raised")
    btn2.grid(row=0, column=1, ipadx=15, ipady=20)
    buttons.append(btn2)

    btn3 = Button(buttons_frame, command=lambda: [update_view(root, tables[2]), change_color(btn3)], text=tables[2], bg="gray20", fg="white", bd=5, compound=LEFT, relief="raised")
    buttons.append(btn3)
    btn3.grid(row=0, column=2, ipadx=15, ipady=20)

    btn4 = Button(buttons_frame, command=lambda: [update_view(root, tables[3]), change_color(btn4)], text=tables[3], bg="gray20", fg="white", bd=5, compound=LEFT, relief="raised")
    buttons.append(btn4)
    btn4.grid(row=0, column=3, ipadx=15, ipady=20)

    btn5 = Button(buttons_frame, command=lambda: [update_view(root, tables[4]), change_color(btn5)], text=tables[4], bg="gray20", fg="white", bd=5, compound=LEFT, relief="raised")
    buttons.append(btn5)
    btn5.grid(row=0, column=4, ipadx=15, ipady=20)

    #----------------------------------Δυνομικη δημιουργια κουμπιών ----------------------------------
    #---------------------------------Πρεπει να αλλάξω το view δεν τα εμφανίζει καλα τα δεδομένα-------------------
    # buttons = [table for table in tables]
    # for index, name in enumerate(tables):
    #     buttons[index] = Button(buttons_frame, command=lambda: update_view(tree, tables[index]), text=name, bg="gray20", fg="white", bd=3, compound=LEFT, relief="raised")
    #     buttons[index].grid(row=0, column=index, ipadx=30, ipady=50)
    #     print("Name Line 199 ", name)
    # print("buttons Line 200", buttons)

    search_frame.grid(column=1, row=1)
    buttons_frame.grid(column=0, row=0)


def update_view(root, table_from_button):
    data_frame = Frame(root, bg="#C2C0BD")
    global tree, dbase, headers, table
    table = table_from_button
    tree = ttk.Treeview(data_frame, selectmode="browse", style="mystyle.Treeview", show="headings", height=20)
    # ================================ scrolls======================
    scrolly = ttk.Scrollbar(root, orient='vertical', command=tree.yview)
    scrolly.grid(column=501, row=3, sticky="ns")
    tree.configure(yscrollcommand=scrolly.set)
    scrollx = ttk.Scrollbar(root, orient='horizontal', command=tree.xview)
    scrollx.grid(sticky='we', column=0, row=4, columnspan=100)
    tree.configure(xscrollcommand=scrollx.set)

    print("table Line 219", table)
    for i in tree.get_children():
        # Εμφάνηση το τι σβήνηει
        #print("DELETED ΑΠΟ ΤΟ TREE ", i)
        tree.delete(i)
    up_conn = sqlite3.connect(dbase)
    up_cursor = up_conn.cursor()
    up_cursor.execute("SELECT * FROM " + table)
    print("table line 227", table)
    headers = list(map(lambda x: x[0], up_cursor.description))

    print("headers at line 230 ", headers)
    no_neded_headers = ["id", "ID", "Id"]
    columns = []
    for head in headers:
        columns.append(head)

    tree["columns"] = [head for head in columns]

    # tree["columns"] = ["id", "TONER", "ΜΟΝΤΕΛΟΣ", "ΚΩΔΙΚΟΣ", "ΤΕΜΑΧΙΑ", "ΤΙΜΗ", "ΣΥΝΟΛΟ", "ΣΕΛΙΔΕΣ"]
    # tree["show"] = "headings"

    for head in headers:

        tree.column(head, anchor="center", width=1000 if head == headers[2] else 100, stretch=FALSE)
        tree.heading(head, text=head)

    up_data = up_cursor.fetchall()
    print("up_data line 247 ", up_data)
    up_index = len(up_data)
    for n in range(len(up_data)):
        tree.insert("", up_index - 1, values=up_data[n])

    data_frame.grid(column=0, row=3, columnspan=100)

    def double_click(event):
        edit(root)

    tree.bind("<Double-1>", double_click)
    tree.grid(column=0, row=1, columnspan=100)

    return dbase


# ====================================================================================
# ================================Συναρτήσεις για τα κουμπιά==========================
# ------------------------------------------------------------------------------------
# --------------------------------Δημηουργία νεου παραθύρου---------------------------
def add_to(root):
    global table, dbase
    print("====================Show Table + dbase ================Line 269", table, dbase)
    add_window = Toplevel()
    add_window.focus()
    add_window.title("Προσθήκη δεδομένων")
    # Τίτλος παραθύρου
    add_window_title = Label(add_window, bg="brown", fg="white", text="Προσθήκη αναλώσιμου", font=("Arial Bold", 15),
                             bd=8, padx=3, )
    add_window_title.grid(column=1, row=0)

    # ------------------------------Να πάρουμε τις κεφαλίδες---------------------------

    conn = sqlite3.connect(dbase)
    cursor = conn.execute("SELECT * FROM " + table)

    headers = list(map(lambda x: x[0], cursor.description))
    print("HEADERS ============= Line 284 ", headers)

    # ===========================Εμφάνιση κεφαλίδων======================================
    # ΟΙ ΚΕΦΑΛΊΔΕΣ ΕΊΝΑΙ ΤΑ COLUMNS ΤΟΥ ΠΊΝΑΚΑ
    count_headers = 0  # Για να μετρίσουμε πόσες κεφαλίδες έχει ο πίνακας  χωρίς τα " ID " γιατι μας χρειάζεται για τα entry που θα κάνει ο χρήστης
    data_to_add = []
    cursor.close()
    conn.close()
    for index, header in enumerate(headers):
        if header == "ID" or header == "id" or header == "Id":
            continue
        else:
            count_headers += 1
            toner_label = Label(add_window, text=header, width=15, padx=1, pady=1, font=("San Serif", 12, "bold"), bd=3)
            toner_label.grid(column=1, row=index + 1)
            var = StringVar()
            data_to_add.append(var)

            entry = Entry(add_window, textvariable=var, bd=2, width=150).grid(column=2, row=index + 1)

    # ------------------------------------Προσθήκη δεδομένων στην βάση------------------
    def add_to_db(root, dbase, headers):
        global table
        culumns = ",".join(headers)
        # Να ορίσουμε τα VALUES ΤΗΣ SQL οσα είναι και τα culumns
        # values είναι πόσα ? να έχει ανάλογα τα culumns
        values_var = []

        for header in headers:
            if header == "ID" or header == "id" or header == "Id":
                values_var.append("null")
            else:
                values_var.append('?')
        values = ",".join(values_var)
        print("============values_var============line 318", values)
        # print("==========culumns===========", culumns)
        data = []
        for i in range(len(data_to_add)):
            data.append(data_to_add[i].get())
        # data = tuple(data_to_add)
        print("===========DATA TO ADD AFTER LOOP =========LINE 324 ", data)
        # data_to_add = (toner.get(), model.get(), kodikos.get(),
        #               temaxia.get(), str(timi.get()) + " €", str(timi.get() * temaxia.get()) + " €", selides.get())

        # ΒΑΖΟΥΜΕ ΤΟ ΠΡΩΤΟ NULL ΓΙΑ ΝΑ ΠΆΡΕΙ ΜΟΝΟ ΤΟΥ ΤΟ ID = PRIMARY KEY
        # H ΣΥΝΤΑΞΗ ΕΙΝΑΙ ΑΥΤΉ
        # INSERT        INTO         table(column1, column2,..)        VALUES(value1, value2, ...);  TA  VALUES πρεπει να είναι tuple
        # sql_insert = "INSERT INTO  " + table + "(" + culumns + ")" + "VALUES(NULL, ?, ?, ?, ?, ?, ?, ?);"
        sql_insert = "INSERT INTO  " + table + "(" + culumns + ")" + "VALUES(" + values + ");"  # values είναι πόσα ? να έχει ανάλογα τα culumns
        print("===============sql_insert==========\n", sql_insert)
        print("=======DATA TO ADD===== LINE 334 \n", data)
        add_to_db_conn = sqlite3.connect(dbase)
        print("conected ", 50 * ".")
        add_to_db_cursor = add_to_db_conn.cursor()
        print("cursor maked ", 50 * ".")
        add_to_db_cursor.execute(sql_insert, tuple(data))
        print("sql executed  ", 50 * ".")

        add_to_db_conn.commit()
        print("ΣΤΗΝ ΒΑΣΗ ΠΡΟΣΤΕΘΗΚΑΝ ", data)
        add_to_db_cursor.close()
        add_to_db_conn.close()
        messagebox.showinfo('Εγινε προσθήκη δεδομένων', "Στην κατηγορία {} Προστέθηκε το {} ".format(table, str(data)))
        # Ενημέρωση του tree με τα νέα δεδομένα

        update_view(root, table)
        add_window.destroy()
        print("Εγινε η προσθήκη")
        print(data)

    # ----------------------------------Κουμπί για να γίνει η προσθήκη-------------------
    enter_button = Button(add_window, text="Προσθήκη", bg="green", fg="White", bd=8, padx=5, pady=8, command=lambda: add_to_db(root, dbase, headers))
    enter_button.grid(column=1, row=10)

    # ΕΞΩΔΟΣ
    def quit(event):

        add_window.destroy()

    add_window.bind('<Escape>', quit)


print("headers Line 366", headers)


#=====================================ΑΝΑΖΗΤΗΣΗ=========================================
def search(search_data):
    global tree, table
    if search_data.get() != "":
        tree.delete(*tree.get_children())
        search_conn = sqlite3.connect(dbase)
        search_cursor = search_conn.cursor()
        #idea = SELECT * FROM tablename WHERE name or email or address or designation = 'nagar';
        search_headers = []
        no_neded_headers = ["id", "ID", "Id"]
        operators = []
        for header in headers:
            if header not in no_neded_headers:
                search_headers.append(header + " LIKE ?")
                operators.append('%' + str(search_data.get()) + '%')
        search_headers = " OR ".join(search_headers)
        print("===================search_data=======================Line 385", search_data)
        print("===================Searching headers ================Line 386", search_headers)
        print("===================Operators=========================Line 387", operators)
        print("=====================table===========================Line 388", table)

        #search_cursor.execute("SELECT * FROM " + table + " WHERE \
        #               ΤΟΝΕΡ LIKE ? OR ΜΟΝΤΕΛΟ LIKE ? OR ΚΩΔΙΚΟΣ LIKE ? OR TEMAXIA LIKE ? OR ΤΙΜΗ LIKE ? OR  ΣΥΝΟΛΟ LIKE ? OR ΣΕΛΙΔΕΣ LIKE ?",
        #               ('%' + str(search_data.get()) + '%', '%' + str(search_data.get()) + '%', '%' + str(search_data.get()) + '%', '%' + str(search_data.get()) + '%', '%' + str(search_data.get()) + '%', '%' + str(search_data.get()) + '%', '%' + str(search_data.get()) + '%'))
        search_cursor.execute("SELECT * FROM " + table + " WHERE " + search_headers, operators)
            # ('%' + str(search_data.get()) + '%', '%' + str(search_data.get()) + '%', '%' + str(search_data.get()) + '%',
            #  '%' + str(search_data.get()) + '%', '%' + str(search_data.get()) + '%', '%' + str(search_data.get()) + '%',
            #  '%' + str(search_data.get()) + '%'))

        fetch = search_cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=data)
        search_cursor.close()
        search_conn.close()

# ========================================================================================
# ------------------------------------- ΕΠΕΞΕΡΓΑΣΙΑ -------------------------------------=
# ========================================================================================
def edit(root):
    global dbase, tree
    # ===============ΠΡΩΤΑ BACKUP =========
    backup()
    print("tree.selection()", (tree.set(tree.selection(), '#1')))
    if not tree.set(tree.selection(), "#1"):
        answer = messagebox.showwarning("Σφάλμα.....",
                                                " Παρακαλώ πρώτα επιλέξτε απο την λίστα για να κάνετε επεξεργασία",
                                                icon='warning')
        return NONE

    selected_item = (tree.set(tree.selection(), '#1'))
    edit_conn = sqlite3.connect(dbase)
    edit_cursor = edit_conn.cursor()
    edit_cursor.execute("SELECT * FROM " + table + " WHERE ID = ?", (selected_item,))
    selected_data = edit_cursor.fetchall()
    selected_data = list(selected_data[0])
    print("selected_data line 424 ", selected_data)
    print("headers[0] γραμμή 425 = ", headers[0])
    edit_window = Toplevel()
    edit_window.focus()
    edit_window.title("Επεξεργασία δεδομέμων")
    edit_window_title = Label(edit_window, bg="brown", fg="white", text="Επεξεργασία δεδομέμων",
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
            toner_label = Label(edit_window, text=header, width=15, padx=1, pady=1, font=("San Serif", 12, "bold"), bd=3)
            toner_label.grid(row=index + 1)
            var = StringVar(edit_window, value=selected_data[index])
            data_to_add.append(var)
            print("------------ΜΗ ΕΠΕΞΕΡΓΑΣΜΈΝΑ ΔΕΔΟΜΈΝΑ------------", var.get())
            entry = Entry(edit_window, textvariable=var, bd=2, width=len(var.get())).grid(column=1, row=index + 1, sticky="we")

    # --------------------   Προσθήκη δεδομένων στην βάση -------------------------------
    # ---------------------- μετά την επεξεργασία   -------------------------------------
    def update_to_db():
        global tree, table
        #culumns = ",".join(headers)
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
        print("-------------edited_culumns--------------Line 464", edited_culumns)

        # ====================ΕΠΙΛΕΓΜΈΝΟ ID =================
        selected_item = tree.selection()
        selected_id = tree.set(selected_item, "#1")
        print("==========selected_id==========LINE 469 \n", selected_id)

        # Θα βάζει το data_to_add απο πάνω γραμμη 371
        #βαζουμε και το id που χρειάζεται για το WHERE ID=?
        edited_data = []
        for data in data_to_add:
            edited_data.append(data.get())
        edited_data.append(selected_id)
        print("========edited data ======line 477", tuple(edited_data))
        # H ΣΥΝΤΑΞΗ ΕΙΝΑΙ ΑΥΤΉ
        # sql_insert = "INSERT INTO  " + table + "(" + culumns + ")" + "VALUES(NULL, ?, ?, ?, ?, ?, ?, ?);"
        # sqlite_update_query = """Update new_developers set salary = ?, email = ? where id = ?"""
        edit_cursor.execute("UPDATE " + table + "  SET " + culumns + " WHERE ID=? ",
            (tuple(edited_data)))

        edit_conn.commit()
        print(60 * "*")
        print(50 * "*", "Το προΐον ενημερώθηκε με επιτυχία", 50 * "*")
        print(60 * "*")
        print("==========Παλιά δεδομένα===========LINE 488 \n", selected_data)
        print()
        print("==========Νέα δεδομένα============ LINE 490 \n", edited_data)

        # Ενημέρωση του tree με τα νέα δεδομένα

        update_view(root, table)
        edit_window.destroy()
        print("Εγινε η Ενημέρωση του tree Line 496 ")
        print(data_to_add)

        # ΕΞΩΔΟΣ

    def quit(event):

        edit_window.destroy()

    edit_window.bind('<Escape>', quit)
    update_button = Button(edit_window, command=update_to_db, text="Ενημέρωση πρωιόντος", bg="red",
                           fg="white", bd=3)
    update_button.grid(column=1, row=10)


# ========================================================================================
# -------------------------------------BACK UP ------------------------------------------=
# ========================================================================================
# Αντιγραφα ασφαλείας βασης δεδομένων

def backup():
    global dbase

    def progress(status, remainig, total):
        print(f"{status} Αντιγράφηκαν {total - remainig} απο {total} σελίδες...")

    try:
        now = datetime.now().strftime("%d %m %Y %H %M %S")
        today = datetime.today().strftime("%d %m %Y")
        back_dir = "backups" + "\\" + today + "\\"

        backup_file = os.path.join(back_dir, os.path.basename(dbase[:-3]) + " " + now + ".db")
        print("============BACKUP FILE===========Line 528=\n", backup_file, "\n")
        if not os.path.exists(back_dir):
            os.makedirs(back_dir)
        else:
            pass
        # Υπάρχουσα βάση
        conn = sqlite3.connect(dbase)
        print("===========Υπάρχουσα βάση===========Line 535=\n ", dbase, "\n")

        # Δημιουργία νέας βάσης και αντίγραφο ασφαλείας
        back_conn = sqlite3.connect(backup_file)
        with back_conn:
            conn.backup(back_conn, pages=10, progress=progress)
            back_conn.close()
            text = "Η βάση αντιγράφηκε :  "
            result = text + os.path.realpath(backup_file)
            print("=====Αποτέλεσμα ====Line 544\n", result)
            # Ειναι ενοχλητικο να εμφανιζει καθε φορα μηνυμα οτι εγινε backup
            #tkinter.messagebox.showinfo('Αποτέλεσμα αντιγράφου ασφαλείας', result)
    except FileNotFoundError as file_error:
        print("File Error", file_error)
        backup()
    except sqlite3.Error as error:
        if os.path.exists(backup_file):
            result = os.path.abspath(backup_file)
        else:
            result = "Σφάλμα κατα την αντιγραφή : ", error
            messagebox.showinfo('Αποτέλεσμα αντιγράφου ασφαλείας', error)
    finally:
        try:
            if back_conn:
                back_conn.close()
                print("Συνδεση με ", backup_file, " διακόπηκε")
        except UnboundLocalError as error:
            print(f"Η σύνδεση με {backup_file} δεν έγινε ποτέ Line 562 {error}")
            messagebox.showinfo(f"Η σύνδεση με {backup_file} δεν έγινε ποτέ Line 563 {error}")


# ================================Συνάρτηση για διαγραφή  =================

def del_from_tree():
    global dbase, tree
    backup()
    selected_item = (tree.set(tree.selection(), '#1'))

    del_conn = sqlite3.connect(dbase)
    del_cursor = del_conn.cursor()
    del_cursor.execute("SELECT * FROM " + table + " WHERE ID = ?", (selected_item,))
    selected_data = del_cursor.fetchall()
    selected_data = list(selected_data[0])

    # ======================ΕΠΙΒΕΒΑΙΩΣΗ ΔΙΑΓΡΑΦΗΣ============
    answer = messagebox.askquestion("Θα πραγματοποιηθεί διαγραφή!",
                                            " Είστε σήγουρος για την διαγραφή του {};".format(selected_data), icon='warning')
    if answer == 'yes':
        messagebox.showwarning('Διαγραφή...', "Το {} διαγράφηκε!".format(selected_data))
        #Αν ο χρήστης επιλεξει το "yes" παει στην γραμμή 592 ==>> del_cursor.execute("DEL............
        pass
    else:
        messagebox.showinfo('Ακύρωση διαγραφής', " Τίποτα δεν διαγράφηκε  ")
        print("=================ΑΚΥΡΟΣΗ ΔΙΑΓΡΑΦΗΣ===============line 588\n", selected_data)
        print()
        return

    del_cursor.execute("DELETE FROM " + table + " WHERE ID=?", (selected_item,))
    del_conn.commit()
    del_conn.close()
    print("===============ΠΡΑΓΜΑΤΟΠΟΙΗΘΗΚΕ ΔΙΑΓΡΑΦΉ ΤΟΥ===============Line 595\n", selected_data)
    print()

    try:
        tree.delete(tree.selection())
        print("=============================ΕΓΙΝΕ ΔΙΑΓΡΑΦΗ ΑΠΟ ΤΟ TREE====================================line 600 ")
        return selected_item
    except TclError as error:
        print("ΣΦΑΛΜΑ Line 603", error)


