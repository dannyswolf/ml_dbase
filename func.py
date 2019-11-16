# coding=utf-8
"""
Sqlite Γραφικό περιβάλλον με Python3
******************************************************************
** Οι βάσεις πρέπει να έχουν Id ή id ή ID intiger και NOT NULL  **
******************************************************************


Version V0.9    -----------------------------------------------------------------------------------------17/11/2019
                1) Προσθήκη τελευταίας τροποποιήσης (ημερομηνία , ώρα και όνομα χρήστη που έκανε την τελευταία αλλαγή)
                2) Το σύνολο το κάνει μόνο του
                3) Ο χρήστης μπορεί να προσθέση κενό προίον
                4) Ολοι οι πίνακες εμφανίζονται στο ιδιο πλάτος

Version V0.8.4 Symbol € added to everything Db merged-----------------------------------------------------15/11/2019

Version V0.8.3 Dinamic buttons work well -------------------------------------------------------12/11/2019


Version V0.8.02 Sort added to headers-----------------------------------------------------------11/11/2019


Version v0.8 + Log File added Για το μαγαζί δουλευουν ολα ----------------------------10/11/2019
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



TO DO LIST   ********* ΠΡΕΠΕΙ ΝΑ ΤΑ ΒΑΛΩ ΟΛΛΑ ΣΕ CLASS ΓΙΑ ΝΑ ΠΕΞΟΥΝ ΣΩΣΤΑ *******************
TO DO LIST  0) Να φιάξω την επεξεργρασία επιλεγμένου απο το treeview  ΝΑ ΠΕΡΝΕΙ column αντι TONER=? κτλπ.------------Εγινε 29/10/2019
TO DO LIST  1) ΝΑ ΦΤΙΑΞΩ ΤΟ BACKUP DIRECTORY------------------------------------------------------------------------ΕΓΙΝΕ
TO DO LIST  2) ΤΟ TREE NA ΕΜΦΑΝΙΖΕΙ OTI ΒΑΣΗ ΚΑΙ ΝΑ ΕΠΙΛΕΞΩ--να εμφανίζει τους πίνακες------------------------------ΕΓΙΝΕ 30/10/2019
TO DO LIST  3) ΝΑ ΒΑΛΩ ΜΕΝΟΥ ---------------------------------------------------------------------------------------Εγινε 1/11/2019
TO DO LIST  4) ο χρήστης να επιλέγει τον πίνακα---------------------------------------------------------------------Εγινε 6/11/2019
TO DO LIST  5) ελεγχος αν ο χρήστης εισάγει αλφαριθμητικό ή αριθμό--------------------------------------------------Εγινε 17/11/2019
TO DO LIST  6) Να βάλω να έχει log αρχείο---------------------------------------------------------------------------Εγινε 10/11/2019
TO DO LIST  7) Να κάνει αυτόματα υπολογισμό το σύνολο (όταν έχουμε τιμη και τεμάχια) -------------------------------Εγινε 17/11/2019
TO DO LIST  8) Να βάλω triggers
TO DO LIST  9) Να βάλω στο μενοu RUN SQL
"""


# Πρώτα αυτό για το Combobox
from tkinter import ttk, Frame, Button, Tk, Label, RAISED, PhotoImage, Menu, StringVar, Entry, filedialog, messagebox, LEFT, FALSE, Toplevel, font
import sqlite3

# datetime για backup την βαση πριν κάθε αλλαγή
from datetime import datetime

# Import os για να κάνουμε τον φακελο backup
import os

# Για τα αρχεία log files
import logging

#Για τα directory - φακέλους
import sys

#Για την τελευταια τροποpoiήση απο ποιόν χρήστη
import getpass




table = ""  # Για να ορίσουμε πιο κάτω τον πίνακα σαν global
# Αδεία λίστα για να πάρουμε τα header απο τον πίνακα της βάσης δεδομένων
headers = []  # Για να περσνουμε της επικεφαλίδες καθε πίνκα
dbase = "ΑΠΟΘΗΚΗ.db"
tables =[]
up_data = []    # Για να πάρουμε τα δεδομένα
tree = ""
user = getpass.getuser() # Για να πάρουμε το όνομα χρήστη απο τον υπολογιστή
#-------------ΔΗΜΗΟΥΡΓΕΙΑ LOG FILE------------------
today = datetime.today().strftime("%d %m %Y")
log_dir = "logs" + "\\" + today + "\\"

if not os.path.exists(log_dir):
    os.makedirs(log_dir)
else:
    pass


log_file_name = "ml_database_log" + datetime.now().strftime("%d %m %Y %H %M %S") + ".log"
log_file = os.path.join(log_dir, log_file_name)


#log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
root_logger= logging.getLogger()
root_logger.setLevel(logging.DEBUG) # or whatever
handler = logging.FileHandler(log_file, 'w', 'utf-8') # or whatever
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # or whatever
handler.setFormatter(formatter)  # Pass handler as a parameter, not assign
root_logger.addHandler(handler)
sys.stderr.write = root_logger.error
sys.stdout.write = root_logger.info


# Κουμπί να ανοιξει το αρχείο (βαση δεδομένων)
def open_file(root):

    global dbase
    # Να σβήσουμε παλιά κουμπιά και tree αν ανοιξουμε αλη βαση δεδομένων
    list = root.grid_slaves()
    #print("list root.grid.slaves line 78", list)
    for i in list:
        if len(list) > 1:
            #print("i line 73", i)
            if ".!frame" in str(i):
                #print(i, "deleted line 75")
                i.destroy()

            elif ".!scrollbar" in str(i):
                #print(i, "deleted line 79")
                i.destroy()
        else:
            #print("list root.grid.slaves  after deleted line 82", list)
            continue
    #dbase = filedialog.askopenfilename(initialdir=os.getcwd(), title="Επιλογή βάσης δεδομένων",
    #                                       filetypes=(("db files",
    #                                                   "*.db"), (
    #                                                      "all files",
    #                                                      "*.*")))
    dbase = "ΑΠΟΘΗΚΗ.db"
    print("Γραμμή 112: Επιλεγμένη βάση δεδομένων -->>", dbase)
    get_tables()
    select_table(root)
    return dbase


#Ορισμός πινάκων
def get_tables():
    global tables
    tables = []
    # =======================Ανάγνωριση πίνακα δεδομένων=============
    conn = sqlite3.connect(dbase)
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_name = cursor.fetchall()
    cursor.close()
    conn.close()
    dont_used_tables = ["sqlite_master", "sqlite_sequence", "sqlite_temp_master"]
    for name in table_name:
        if name[0] not in dont_used_tables:
            tables.append(name[0])
            #print("TABLE ", name[0], " ========added to tables line 118")

        else:
            continue
    print("Γραμμη 136: Πίνακες που βρέθηκαν -->>", tables)
    return tables


#Δημιουργια κουμπιών συμφονα με τους πινακες της βασης
def select_table(root):
    global tables

    buttons = []

    # Αλλαγή χρώματος κουμπιου που πατιετε
    def change_color(table_name):
        # Δεχεται σαν όρισμα το ονομα του πίνακα που αντιπροσωπευει το κουμπί
        #print("btn_pressed Line 135", btn)
        #print("buttons line 136", buttons)
        for button in buttons:
            #allazei ta xromata se ayto poy pataw
            # Το κάνουμε με έλνχω των θεσεων δλδ αν το κουμπί που πατάμε εχει την ίδια θέση με τον πίνακα
            # που αντιπροσοπευει πατόντας το τοτε να αλλάζει το χρώμα στο κουμπί σε πορτοκαλί
            # και στα υπολειπα κουμπιά σε gray20
            if tables.index(table_name) == buttons.index(button):
                button.configure(background="#EFA12C")
            else:
                button.configure(background="#657b83")

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
    search_entry.grid(column=0, row=3, ipady=3, ipadx=200, sticky="w")
    search_entry.focus_force()

    search_button.grid(column=1, row=3, ipadx=1, ipady=1)
    buttons_frame = Frame(root, bg="#C2C0BD", relief=RAISED)
    #print("buttons_frame exists line 169", buttons_frame)
    #-------------------------------------------------------------------Κουμπιά -----------------------------------
    # for i in range(boardWidth):
    #     newButton = tk.Button(root, text=str(i + 1),command=lambda j=i + 1: Board.playColumn(j, Board.getCurrentPlayer()))
    #     Board.boardButtons.append(newButton)
    # ----------------------------------Δυνομικη δημιουργια κουμπιών ----------------------------------
    for index, table_name in enumerate(tables):
        btn = Button(buttons_frame, command=lambda x=table_name: [update_view(root, x), change_color(x)], text=table_name, font = ('Sans','10','bold'), bg="#657b83", fg="white", bd=5, compound=LEFT, relief="raised")
        buttons.append(btn)
        if len(buttons) >= 5:
            btn.grid(row=1, column=index-4, ipadx=len(str(table_name))+10, ipady=20, sticky="ew")
        else:
            btn.grid(row=0, column=index, ipady=20, sticky="ew")

    # btn1 = Button(buttons_frame, command=lambda: [update_view(root, tables[0]), change_color(btn1)], text=tables[0], font = ('Sans','10','bold'), bg="gray20", fg="white", bd=5, compound=LEFT, relief="raised")
    # buttons.append(btn1)
    # btn1.grid(row=0, column=0, ipadx=15, ipady=20)
    # #print("Table Line 176", tables[0])
    #
    # btn2 = Button(buttons_frame, command=lambda: [update_view(root, tables[1]), change_color(btn2)], text=tables[1], font = ('Sans','10','bold'),bg="gray20", fg="white", bd=5, compound=LEFT, relief="raised")
    # btn2.grid(row=0, column=1, ipadx=15, ipady=20)
    # buttons.append(btn2)
    #
    # btn3 = Button(buttons_frame, command=lambda: [update_view(root, tables[2]), change_color(btn3)], text=tables[2], font = ('Sans','10','bold'), bg="gray20", fg="white", bd=5, compound=LEFT, relief="raised")
    # buttons.append(btn3)
    # btn3.grid(row=0, column=2, ipadx=15, ipady=20)
    #
    # btn4 = Button(buttons_frame, command=lambda: [update_view(root, tables[3]), change_color(btn4)], text=tables[3], font = ('Sans','10','bold'), bg="gray20", fg="white", bd=5, compound=LEFT, relief="raised")
    # buttons.append(btn4)
    # btn4.grid(row=0, column=3, ipadx=15, ipady=20)
    #
    # btn5 = Button(buttons_frame, command=lambda: [update_view(root, tables[4]), change_color(btn5)], text=tables[4], font = ('Sans','10','bold'), bg="gray20", fg="white", bd=5, compound=LEFT, relief="raised")
    # buttons.append(btn5)
    # btn5.grid(row=0, column=4, ipadx=15, ipady=20)

    #----------------------------------Δυνομικη δημιουργια κουμπιών ----------------------------------
    #---------------------------------Πρεπει να αλλάξω το view δεν τα εμφανίζει καλα τα δεδομένα-------------------
    # buttons = [table for table in tables]
    # for index, name in enumerate(tables):
    #     buttons[index] = Button(buttons_frame, command=lambda: update_view(tree, tables[index]), text=name, bg="gray20", fg="white", bd=3, compound=LEFT, relief="raised")
    #     buttons[index].grid(row=0, column=index, ipadx=30, ipady=50)
    #     print("Name Line 199 ", name)
    # print("buttons Line 200", buttons)

    search_frame.grid(column=0, row=1)
    buttons_frame.grid(column=0, row=0)


#---------------------------ΤΑΞΙΝΟΜΗΣΗ-------------------------------
def sort_by_culumn(tree, column, reverse):
    l = [(tree.set(k, column), k) for k in tree.get_children("")]
    l.sort(reverse=reverse)

    for index, (val, k) in enumerate(l):
        tree.move(k, "", index)

    tree.heading(column, command=lambda: sort_by_culumn(tree, column, not reverse))



def update_view(root, table_from_button):
    data_frame = Frame(root, bg="#C2C0BD")
    global tree, dbase, headers, table
    if tree:
        tree.destroy()
    else:
        pass
    table = table_from_button
    tree = ttk.Treeview(data_frame, selectmode="browse", style="mystyle.Treeview", show="headings", height=19)
    # ================================ scrolls======================
    scrolly = ttk.Scrollbar(root, orient='vertical', command=tree.yview)
    scrolly.grid(column=150, row=3, sticky="nse")
    tree.configure(yscrollcommand=scrolly.set)
    scrollx = ttk.Scrollbar(root, orient='horizontal', command=tree.xview)
    scrollx.grid(sticky='we', column=0, row=4, columnspan=100)
    tree.configure(xscrollcommand=scrollx.set)

    print("Γραμμη 236: Επιλεγμένος πίνακας -->> ", table)
    for i in tree.get_children():
        # Εμφάνηση το τι σβήνηει
        #print("DELETED ΑΠΟ ΤΟ TREE ", i)
        tree.delete(i)
    up_conn = sqlite3.connect(dbase)
    up_cursor = up_conn.cursor()
    up_cursor.execute("SELECT * FROM " + table)
    print("Γραμμη 244: Επιλογή όλων απο τον πίνακα -->>", table)
    headers = list(map(lambda x: x[0], up_cursor.description))

    print("Γραμμη 247: Κεφαλίδες -->> ", headers)
    no_neded_headers = ["id", "ID", "Id"]
    columns = []
    for head in headers:
        columns.append(head)

    tree["columns"] = [head for head in columns]

    # tree["columns"] = ["id", "TONER", "ΜΟΝΤΕΛΟΣ", "ΚΩΔΙΚΟΣ", "ΤΕΜΑΧΙΑ", "ΤΙΜΗ", "ΣΥΝΟΛΟ", "ΣΕΛΙΔΕΣ"]
    # tree["show"] = "headings"
    alignment = ""
    platos = 0
    for head in headers:
        #==================================== ΣΤΟΙΧΙΣΗ ΠΕΡΙΕΧΟΜΕΝΩΝ ===========================
        if head == "ΤΙΜΗ" or head == "ΣΥΝΟΛΟ":  # ΣΤΟΙΧΗΣΗ ΔΕΞΙΑ
            alignment = "e"
            platos = len(head) * 12
        elif head == "ΚΩΔΙΚΟΣ" or head == "ΤΕΜΑΧΙΑ":  # ΣΤΟΙΧΗΣΗ ΚΕΝΤΡΟ
            alignment = "center"
            platos = len(head) * 12
        elif head == "ΠΑΡΑΤΗΡΗΣΗΣ" or head == "ΠΕΡΙΓΡΑΦΗ": # ΣΤΟΙΧΗΣΗ ΑΡΙΣΤΕΡΑ
            if head == "ΠΑΡΑΤΗΡΗΣΗΣ" and len(headers) < 7:
                platos = 450
            elif head == "ΠΕΡΙΓΡΑΦΗ":
                platos = 1100
            alignment = "w"
        elif head == "PARTS_NR":
            platos = 150
        else:
            alignment = "center"
            platos = len(head) * 12
        tree.column(head, anchor=alignment, width=platos, stretch=FALSE)
        tree.heading(head, text=head, command=lambda _col=head: sort_by_culumn(tree, _col, False))
        #tree.heading(head, text=head, command=lambda: sort_by_culumn(tree, head, False))

    up_data = up_cursor.fetchall()
    #print("up_data line 247 ", up_data)
    up_index = len(up_data)
    tree.tag_configure('oddrow', background='#ece8de', foreground="black", font=("Calibri", 10))
    tree.tag_configure('evenrow', background='white', font=("Calibri", 10))
    for n in range(len(up_data)):
        #print("Grammh 297 Up_data[n]", up_data[n][0])
        if int(up_data[n][0]) % 2 == 0:
            #print("===========================   0    ===========")
            tree.insert("", up_index - 1, values=up_data[n], tags=('oddrow',))
        else:
            #print("=====================================     1        ====================")
            tree.insert("", up_index-1, values=up_data[n], tags=("evenrow",))

    data_frame.grid(column=0, row=3, columnspan=100)

    def double_click(event):
        edit(root)

    tree.bind("<Double-1>", double_click)
    tree.grid(column=0, row=1, columnspan=100, sticky="es")

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

            entry = Entry(add_window,  textvariable=var, bd=2, width=150).grid(column=2, row=index + 1)

    # ------------------------------------Προσθήκη δεδομένων στην βάση------------------
    def add_to_db(root, dbase, headers):
        global table
        culumns = ",".join(headers)
        # Να ορίσουμε τα VALUES ΤΗΣ SQL οσα είναι και τα culumns
        # values είναι πόσα ? να έχει ανάλογα τα culumns
        values_var = []

        for head in headers:
            if head == "ID" or head == "id" or head == "Id":
                values_var.append("null")
            else:
                values_var.append('?')
        values = ",".join(values_var)
        print("============values_var============line 371", values)
        # print("==========culumns===========", culumns)
        data = []
        for i in range(len(data_to_add)):
            data.append(data_to_add[i].get())
        # data = tuple(data_to_add)
        print("Line 406 data before €",data)
        try:
            if "ΣΥΝΟΛΟ" in headers:
                # {: 0.2f}           Για εμφάνιση 2 δεκαδικών
                # data[6]= 0 αν ο χρήστης δεν δόσει τιμή
                if data[6] == "":
                    data[6] = 0
                else:
                    pass
                data[7] = float(data[5]) * float(data[6])
                data[7] = str("{:0.2f}".format(data[7])) + "€"
                data[6] = str("{:0.2f}".format(float(data[6]))) + " €"
                data[5] = str(data[5])
        except IndexError as error:
            print("Δεν υπάρχει σύνολο για να γίνει υπολογισμός συνόλου τιμής * τεμάχια", error)
        except ValueError as error:
            print("H τιμή δεν μπορεί να είναι κενή", error)
            pass
        # ================================ Προσθήκη τελευταίας τροποποιησης ============================
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        data[-1] = now + "  " + user + "  " + data[-1]
        print("===========DATA TO ADD AFTER LOOP =========LINE 377 ", data)
        # data_to_add = (toner.get(), model.get(), kodikos.get(),
        #               temaxia.get(), str(timi.get()) + " €", str(timi.get() * temaxia.get()) + " €", selides.get())

        # ΒΑΖΟΥΜΕ ΤΟ ΠΡΩΤΟ NULL ΓΙΑ ΝΑ ΠΆΡΕΙ ΜΟΝΟ ΤΟΥ ΤΟ ID = PRIMARY KEY
        # H ΣΥΝΤΑΞΗ ΕΙΝΑΙ ΑΥΤΉ
        # INSERT        INTO         table(column1, column2,..)        VALUES(value1, value2, ...);  TA  VALUES πρεπει να είναι tuple
        # sql_insert = "INSERT INTO  " + table + "(" + culumns + ")" + "VALUES(NULL, ?, ?, ?, ?, ?, ?, ?);"
        sql_insert = "INSERT INTO  " + table + "(" + culumns + ")" + "VALUES(" + values + ");"  # values είναι πόσα ? να έχει ανάλογα τα culumns
        print("===============sql_insert==========\n", sql_insert)
        print("=======DATA TO ADD===== LINE 387 \n", data)
        add_to_db_conn = sqlite3.connect(dbase)
        print("conected ", 50 * ".")
        add_to_db_cursor = add_to_db_conn.cursor()
        print("cursor done ", 50 * ".")
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
    enter_button.grid(column=1, row=13)

    # ΕΞΩΔΟΣ
    def quit(event):

        add_window.destroy()

    add_window.bind('<Escape>', quit)





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
        tree.tag_configure('oddrow', background='#ece8de', foreground="black", font=("Calibri", 10))
        tree.tag_configure('evenrow', background='white', font=("Calibri", 10))
        odd_or_even = 0
        for data in fetch:
            odd_or_even += 1
            if odd_or_even % 2 == 0:
                tree.insert('', 'end', values=data, tags=('oddrow',))
            else:
                tree.insert("", 'end', values=data, tags=("evenrow",))
        search_cursor.close()
        search_conn.close()

# ========================================================================================
# ------------------------------------- ΕΠΕΞΕΡΓΑΣΙΑ -------------------------------------=
# ========================================================================================
def edit(root):
    global dbase, tree, headers
    print("Γραμμή 423: ---------------ΛΟΓΟΣ BACKUP --->>> ΕΠΕΞΕΡΓΑΣΙΑ ΔΕΔΟΜΕΝΩΝ ------------------------- ")
    # ===============ΠΡΩΤΑ BACKUP =========
    backup()
    print("Γραμμη 425: ΕΠΕΞΕΡΓΑΣΙΑ ΣΤΟ Επιλεγμένο id -->", (tree.set(tree.selection(), '#1')))
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
    #print("selected_data line 424 ", selected_data)
    #print("headers[0] γραμμή 425 = ", headers[0])
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
            #print("------------ΜΗ ΕΠΕΞΕΡΓΑΣΜΈΝΑ ΔΕΔΟΜΈΝΑ------------", header, var.get())
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
        print("-------------edited_culumns--------------Line 554", edited_culumns)

        # ====================ΕΠΙΛΕΓΜΈΝΟ ID =================
        selected_item = tree.selection()
        selected_id = tree.set(selected_item, "#1")
        #print("==========selected_id==========LINE 469 \n", selected_id)

        # Θα βάζει το data_to_add απο πάνω γραμμη 371
        #βαζουμε και το id που χρειάζεται για το WHERE ID=?
        edited_data = []

        for data in data_to_add:
            edited_data.append(data.get())

        # ================================ Προσθήκη τελευταίας τροποποιησης ============================
        # edited_data[-1] ==>> Ειναι η ΠΑΡΑΤΗΡΗΣΗΣ
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        edited_data[-1] = now + "  " + user + "  " + edited_data[-1]
        #================================= Προσθήκη id =================================================
        edited_data.append(selected_id)
        print("Line 573 Edited data ", edited_data)
        # ====================================== ΑΥΤΟΜΑΤΗ ΕΝΗΜΕΡΩΣΗ ΣΥΝΟΛΟΥ =============================
        #======================================= ΚΑΙ ΠΡΟΣΘΗΚΗ ΣΥΜΒΟΛΟΥ €    =============================
        if "ΣΥΝΟΛΟ=?" in edited_culumns:
            print("Συνολο == ", "ΣΥΝΟΛΟ=?" in edited_culumns)
            try:
                #Αν ο χρήστης δεν βάλει τεμάχειο να γίνει αυτόματα 0
                if edited_data[5] == "":
                    edited_data[5] = 0
                    print("Line 604 edited_data[5] ", edited_data[5])
                else:
                    pass
                # Αν ο χρήστης δεν ορίσει τιμή να γίνει αυτόματα 0
                if edited_data[6] == "":
                    edited_data[6] = "0"   # 0 σε string γιατί ψάχνουμε αν έχει το € μέσα
                    print("Line 610 edited_data[6] ", edited_data[6])
                else:
                    pass
                # {:0.2f} Για να εμφανίνζει την τιμή με 2 δεκαδικά πίσω απο την τιμή 10.00 € και οχι 10 €
                if "€" in edited_data[6]:
                    edited_data[7] = str("{:0.2f}".format(float(edited_data[6][:-1]) * float(edited_data[5]))) + " €"
                    edited_data[5] = str(edited_data[5])

                else:
                    edited_data[7] = str("{:0.2f}".format(float(edited_data[6]) * float(edited_data[5]))) + " €"
                    edited_data[5] = str(edited_data[5])

                if "€" not in str(edited_data[6]):
                    edited_data[6] = str("{:0.2f}".format(float(edited_data[6]))) + " €"

                else:
                    edited_data[6] = str("{:0.2f}".format(float(edited_data[6][:-1]))) + " €"


            except ValueError as error:
                messagebox.showwarning('ΠΡΟΣΟΧΉ ...', "Σφάλμα {} \n1)Η Τιμή πρέπει να είναι αριθμός και με .(τελεία) όχι ,(κομμα) "\
                                   .format(error))

                edit_window.destroy()
                return None
        else:
            pass
        #print("Γραμμη 491:  ----------- ΕΠΕΞΕΡΓΑΣΜΈΝΑ ΔΕΔΟΜΈΝΑ------------", tuple(edited_data))
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
        print("Γραμμη 510: Εγινε η Ενημέρωση του tree ")
        #print(data_to_add)

        # ΕΞΩΔΟΣ

    def quit(event):

        edit_window.destroy()

    edit_window.bind('<Escape>', quit)
    update_button = Button(edit_window, command=update_to_db, text="Ενημέρωση πρωιόντος", bg="red",
                           fg="white", bd=3)
    update_button.grid(column=1, row=len(headers)+1)


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
        print("============BACKUP FILE===========Line 542=\n", backup_file, "\n")
        if not os.path.exists(back_dir):
            os.makedirs(back_dir)
        else:
            pass
        # Υπάρχουσα βάση
        conn = sqlite3.connect(dbase)
        print("===========Υπάρχουσα βάση===========Line 549=\n ", dbase, "\n")

        # Δημιουργία νέας βάσης και αντίγραφο ασφαλείας
        back_conn = sqlite3.connect(backup_file)
        with back_conn:
            conn.backup(back_conn, pages=10, progress=progress)
            back_conn.close()
            text = "Η βάση αντιγράφηκε :  "
            result = text + os.path.realpath(backup_file)
            print("=====Αποτέλεσμα ====Line 558\n", result)
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
    print("Γραμμή 423: ---------------ΛΟΓΟΣ BACKUP --->>> ΔΙΑΓΡΑΦΗ ΔΕΔΟΜΕΝΩΝ ------------------------- ")
    backup()
    selected_item = (tree.set(tree.selection(), '#1'))

    del_conn = sqlite3.connect(dbase)
    del_cursor = del_conn.cursor()
    del_cursor.execute("SELECT * FROM " + table + " WHERE ID = ?", (selected_item,))
    selected_data = del_cursor.fetchall()
    selected_data = list(selected_data[0])
    print("Γραμμη 592: Επιλεγμένα για διαγραφή δεδομένα -->>", selected_data)

    # ======================ΕΠΙΒΕΒΑΙΩΣΗ ΔΙΑΓΡΑΦΗΣ============
    answer = messagebox.askquestion("Θα πραγματοποιηθεί διαγραφή!",
                                            " Είστε σήγουρος για την διαγραφή του {};".format(selected_data), icon='warning')
    print('Γραμμή 597: =================ΔΙΑΓΡΑΦΗ===============', "Το {} επιλέχθηκε για διαγαφή !".format(selected_data))
    if answer == 'yes':
        messagebox.showwarning('Διαγραφή...', "Το {} διαγράφηκε!".format(selected_data))
        #Αν ο χρήστης επιλεξει το "yes" παει στην γραμμή 607 ==>> del_cursor.execute("DEL............

        pass
    else:
        messagebox.showinfo('Ακύρωση διαγραφής', " Τίποτα δεν διαγράφηκε  ")
        print("Γραμμή 604: =================ΑΚΥΡΟΣΗ ΔΙΑΓΡΑΦΗΣ===============\n", selected_data)
        print()
        return

    del_cursor.execute("DELETE FROM " + table + " WHERE ID=?", (selected_item,))
    del_conn.commit()
    del_conn.close()
    print()
    print("Γραμμη 612:===============ΠΡΑΓΜΑΤΟΠΟΙΗΘΗΚΕ ΔΙΑΓΡΑΦΉ ΤΟΥ===============\n", selected_data)
    print()

    try:
        tree.delete(tree.selection())
        #print("=============================ΕΓΙΝΕ ΔΙΑΓΡΑΦΗ ΑΠΟ ΤΟ TREE====================================line 600 ")
        return selected_item
    except TclError as error:
        print("ΣΦΑΛΜΑ Line 603", error)


