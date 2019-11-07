# coding=utf-8
"""
Sqlite Γραφικό περιβάλλον με Python3
******************************************************************
** Οι βάσεις πρέπει να έχουν Id ή id ή ID intiger και NOT NULL  **
******************************************************************

Version v 0.6 Προσθήκη καρτέλων και η αναζήτηση δουλεύει παντού :-)
Να γίνει έλεγχος αν τα εισάγει τα δεδομένα δυο φορες στο tree σε καθε tree


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
from tkinter import ttk
import sqlite3
# Μετά αυτο για το Label Διαφορετικά βγαζει error για το font
from tkinter import *

# Για να επιλεξει ο χρήστης το αρχείο (ποια βάση δεδομένων θελει να ανοιξει)
from tkinter import filedialog

# datetime για backup την βαση πριν κάθε αλλαγή
from datetime import datetime

# Import os για να κάνουμε τον φακελο backup
import os

# Για επιβεβέωση διαγραφής
import tkinter.messagebox


table = ""  # Για να ορίσουμε πιο κάτω τον πίνακα σαν global
# Αδεία λίστα για να πάρουμε τα header απο τον πίνακα της βάσης δεδομένων
headers = []  # Για να περσνουμε της επικεφαλίδες καθε πίνκα
dic_headers = {}  # key , values key= πίνακας1 values= επικεφαλίδες [μελανακια] = [id, μελανακια, περιγραφή ....κτλπ]
dbase = ""
tables =[]
up_data = []    # Για να πάρουμε τα δεδομένα
dic_data = {}   # [μελανακια] = [brother , 12115, 1, 20€, κτλπ ]
tabs = []       # Για το Notebook


# Κουμπί να ανοιξει το αρχείο (βαση δεδομένων)
def open_file(root):
    # Ανοιγουμε την βάση αν δεν έχουμε ανοιξει
    global dbase, tables, table

    dbase = filedialog.askopenfilename(initialdir=os.getcwd(), title="Επιλογή βάσης δεδομένων",
                                           filetypes=(("db files",
                                                       "*.db"), (
                                                          "all files",
                                                          "*.*")))

    print("======================opened file ===================line 68", dbase)
    get_tables()
    select_table(root)

    return dbase


def get_tables():
    global tables
    # =======================Ανάγνωριση πίνκα δεδομένων=============
    conn = sqlite3.connect(dbase)
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_name = cursor.fetchall()
    cursor.close()
    conn.close()
    dont_used_tables = ["sqlite_master", "sqlite_sequence", "sqlite_temp_master"]
    tables = []
    for name in table_name:
        if name[0] not in dont_used_tables:
            tables.append(name[0])

            print("TABLE ", name[0], " ========added to tables")
        else:
            continue
    return tables


def select_table(root):
    global table, tables

    # =======================Ανάγνωριση πίνκα δεδομένων=============
    conn = sqlite3.connect(dbase)
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_name = cursor.fetchall()
    cursor.close()
    conn.close()
    dont_used_tables = ["sqlite_master", "sqlite_sequence", "sqlite_temp_master"]
    tables = []
    for name in table_name:
        if name[0] not in dont_used_tables:
            tables.append(name[0])

            print("TABLE ", name[0], " ========added to tables")
        else:
            continue

    print("=========ΟΝΟΜΑ ΠΙΝΑΚΩΝ===========LINE 82 ", tables)
    print()
    # ===============================Επιλογή πίνακα================================
    print("*" * 50 + "len(tables)" + "*" * 50 + "line 93", len(tables))

    if len(tables) > 1:
        print("*" * 50 + "len(tables)" + "*" * 50 + "Line 95",len(tables))
        print("stage 0")
        table = tables[0]

        def change_table():
            global table
            print("stage 3")
            print("====================table_var.get()=================", table_var.get())
            table = table_var.get()
            update_view(root)
            #choice_table_window.destroy()
            return table

        table_var = StringVar()
        print("stage 1  table_var", table_var.get())

        #table_var.trace("w", change_table)
        #choice_table_window = Toplevel()
        #choice_table_window.title("Επιλογή πίνακα")
        choice_table_window_title = Label(root, bg="brown", fg="white", text="Παρακαλώ επιλέξτε πίνακα",
                                 font=("Arial Bold", 15), bd=8, padx=3)
        #choice_table_window_title.grid(column=1, row=0)
        #table_label = Label(root,  text="Πίνακες")
        #table_label.grid(column=0, row=1, sticky="w", columnspan = 2)
        table_menu = OptionMenu(root, table_var, *tables)
        table_menu.grid(column=0, row=1, sticky="w")

        table_button = Button(root, bg="brown", fg="white", text="Επιλογή", command=change_table)
        table_button.grid(column=0, row=2, sticky="w")

        table_var.set(table_var.get())
        #table = change_table()
        update_view(root)
        print("=========ΟΝΟΜΑ ΠΙΝΑΚΑ===========LINE 116 ", table)

    else:

        table = tables[0]
        # table_var.trace("w", update_view(root, tree))
        print("=========ΟΝΟΜΑ ΠΙΝΑΚΑ===========LINE 109 ", table)
        print()
        update_view(root)



def update_view(root):
    global dbase, dic_data, dic_headers
    dic_data = {}
    dic_headers = {}



    def make_tabs(root):
        print("*" * 50 + "make_tabs" + 50 * "*")
        global tree, tabs, tab_control

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

        tables = get_tables()
        print("tables", tables)

        tab_control = ttk.Notebook(root)
        tabs = [table for table in tables]
        print("Tabs line 180", tabs)
        tree = [table for table in tables]
        print("Tree ================Line 185", tree)
        for i, table in enumerate(tables):
            print("I ==========={} Table==========={}=========line 184", i, table)
            tabs[i] = ttk.Frame(tab_control)
            print("tabs[i] ==========Line 186", tabs[i])
            tab_control.add(tabs[i], text=table)
            print("tabs line 192", tabs)
            tab_control.grid(column=0, row=3)
            tree[i] = ttk.Treeview(tabs[i], selectmode="browse", style="mystyle.Treeview", show="headings", height=13)
            tree[i].grid(column=0, row=4)
            tab_control.grid(column=0, row=3)
            # scrolls
            scrolly = ttk.Scrollbar(tabs[i], orient='vertical', command=tree[i].yview)
            scrolly.grid(column=0, row=3, sticky="nswe", ipadx=2)
            tree[i].configure(yscrollcommand=scrolly.set)
            scrollx = ttk.Scrollbar(tabs[i], orient='horizontal', command=tree[i].xview)
            scrollx.grid(sticky='we', column=1, row=4, ipady=2, columnspan=2)
            tree[i].configure(xscrollcommand=scrollx.set)

    # Να σβήσει πρώτα τα δεδομένω για να πάρει τα καινούρια
    # map(tree.delete, tree.get_children())
    make_tabs(root)
    for value in tree:
        print("Tree Value Line 215  ", value)
    for tre in tree:
    #    # Εμφάνηση το τι σβήνηει
        for i in tre.get_children():
            deleted_data =tre.delete(i)
            print("Deleted Line 221", deleted_data)
    #up_cursor.execute("DELETE FROM " + table + " WHERE ΚΩΔΙΚΟΙ IS 'NONE'")
    for index, table in enumerate(tables):
        up_conn = sqlite3.connect(dbase)
        up_cursor = up_conn.cursor()
        up_cursor.execute("SELECT * FROM " + table)
        print("table line 222", table)
        dic_headers[table] = list(map(lambda x: x[0], up_cursor.description))
        print("dic_headers[table]========Line 223", dic_headers[table])
        dic_data[table] = up_cursor.fetchall()
        print("Up_data[table] Line 224", dic_data[table])
        up_cursor.close()
        up_conn.close()

    for tre, headers_in_dic in zip(tree, dic_headers.values()):

        print("tre ===========  Line 230", tre)
        # tree["columns"] = sqlite3.Row
        tre["columns"] = [head for head in headers_in_dic]
        headers.insert(index, headers_in_dic)
        print("Headers line 235", headers)

        print(25 * "*", "tre[\"columns\"] Line 233", tre["columns"])
        print("headers_in_dic Line 234", headers_in_dic)
        # tree["columns"] = ["id", "TONER", "ΜΟΝΤΕΛΟ", "ΚΩΔΙΚΟΣ", "ΤΕΜΑΧΙΑ", "ΤΙΜΗ", "ΣΥΝΟΛΟ", "ΣΕΛΙΔΕΣ"]
        #tre["show"] = "headings"
        for head in headers_in_dic:

            tre.column(head, anchor="w", width=375 if head == headers_in_dic[2] else 100, stretch=False)
            tre.heading(head, text=head)
            print("tre.column Line 240", head, tre.column)
        #index = len(dic_data["ΜΕΛΑΝΑΚΙΑ"])
        #print("dic_data[melanakia] Line 241", dic_data["ΜΕΛΑΝΑΚΙΑ"])

    for tre, tab in zip(tree, dic_data): # Το tab περνει για τιμες το κλειδι απο το dic_data δλδ τους πινακες ΜΕΛΑΝΑΚΙΑ, ΤΟΝΕΡ ΚΤΛΠ
        print("tab Line 244", tab)
        print("tre Line 245", tre)
        up_index = len(dic_data[tab])
        print("Up_index = ", up_index)
        for n in range(len(dic_data[tab])):

            tre.insert("", up_index - 1, values=dic_data[tab][n])
            print("index Line 248", up_index)
            print("value Line 249", dic_data[tab][n])

    for tre in tree:
    #tab_control.grid(column=0, row=3)
        tre.grid(column=1, row=3, columnspan=2)
    print(50*"*", "Line 252")
    #up_data = up_cursor.fetchall()
    #print("up_data line 160 ", up_data)
    #up_index = len(up_data)
    #for n in range(len(up_data)):
    #    tree.insert("", up_index - 1, values=up_data[n]))
    #for tre, n in zip(tree, up_data):
    #    tre.insert("", up_index - 1, values=up_data[n]) # Για το tag μπορουμε να βάλουμε το < ,  tags=('ttk', 'simple')>
        #Αλλά δεν παίζει σε python 3.8
        #tree.tag_configure('simple', background='red')

    return table


# ====================================================================================
# ================================Συναρτήσεις για τα κουμπιά==========================
# ------------------------------------------------------------------------------------
# --------------------------------Δημηουργία νεου παραθύρου---------------------------
def add_to(root):
    global table, dbase
    print("====================Show Table + dbase ================Line 139", table, dbase)
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
    cursor.close()
    conn.close()
    for index, header in enumerate(headers):
        if header == "ID" or header == "id" or header == "Id":
            continue
        else:
            count_headers += 1
            toner_label = Label(add_window, text=header, width=10, padx=1, pady=1, font=("San Serif", 12, "bold"), bd=3)
            toner_label.grid(row=index + 1)
            var = StringVar()
            data_to_add.append(var)

            entry = Entry(add_window, textvariable=var, bd=2, width=150).grid(column=1, row=index + 1)

    # ------------------------------------Προσθήκη δεδομένων στην βάση------------------
    def add_to_db(root, dbase, headers):

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
        print("=======DATA TO ADD===== LINE 291 \n", data)
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
        # Ενημέρωση του tree με τα νέα δεδομένα

        update_view(root)

        print("Εγινε η προσθήκη")
        print(data)

    # ----------------------------------Κουμπί για να γίνει η προσθήκη-------------------
    enter_button = Button(add_window, text="Προσθήκη", bg="green", fg="White", bd=8, padx=5, pady=8, command=lambda: add_to_db(root, dbase, headers))
    enter_button.grid(column=1, row=9)


print("headers Line 372", headers)

#=====================================ΑΝΑΖΗΤΗΣΗ=========================================
def search(search_data):
    global dbase, tree, tabs
    selected_tab = tab_control.index(tab_control.select())  # Επιστρέφει το νουμερο της επιλεγμένης καρτέλας
    index = 0

    for tre, headers_in_dic in zip(tree, dic_headers.values()):
        #Φτιάχνουμε τα πεδία για την αναζήτηση id, μελάνι, μοντέλο κτλπ
        headers.insert(index, headers_in_dic)
        print("Headers line 382", headers)
        index += 1
    print("selected_tab=======Line 372", selected_tab)
    print("Ονομα του επιλεγμένου tab ", tabs[0])
    selected_table = tables[selected_tab]
    if search_data.get() != "":
        print("Headers line 388", headers[selected_tab])
        tree[selected_tab].delete(*tree[selected_tab].get_children())

        search_conn = sqlite3.connect(dbase)
        search_cursor = search_conn.cursor()
        #idea = SELECT * FROM tablename WHERE name or email or address or designation = 'nagar';

        search_headers = []
        no_needed_headers = ["id", "ID", "Id"]
        operators = []
        for header in headers[selected_tab]:
            print("Header Line 400", header)
            if header not in no_needed_headers:
                search_headers.append(header + " LIKE ?")
                operators.append('%' + str(search_data.get()) + '%')
        search_headers = " OR ".join(search_headers)
        print("search_headers Line 405", search_headers)
        print("===================Searching headers ================Line 623", search_headers)
        print("===================Operators=========================Line 627", operators)
        search_cursor.execute("SELECT * FROM " + selected_table + " WHERE " + search_headers, operators)
        fetch = search_cursor.fetchall()
        for data in fetch:
            tree[selected_tab].insert('', 'end', values=data)
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
        answer = tkinter.messagebox.showwarning("Σφάλμα.....",
                                                " Παρακαλώ πρώτα επιλέξτε απο την λίστα για να κάνετε επεξεργασία",
                                                icon='warning')
        return NONE

    selected_item = (tree.set(tree.selection(), '#1'))
    edit_conn = sqlite3.connect(dbase)
    edit_cursor = edit_conn.cursor()
    edit_cursor.execute("SELECT * FROM " + table + " WHERE ID = ?", (selected_item,))
    selected_data = edit_cursor.fetchall()
    selected_data = list(selected_data[0])
    print("selected_data line 349 ", selected_data)
    print("headers[0] γραμμή 385 = ", headers[0])
    edit_window = Toplevel()
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
            toner_label = Label(edit_window, text=header, width=10, padx=1, pady=1, font=("San Serif", 12, "bold"), bd=3)
            toner_label.grid(row=index + 1)
            var = StringVar(edit_window, value=selected_data[index])
            data_to_add.append(var)
            print("------------ΜΗ ΕΠΕΞΕΡΓΑΣΜΈΝΑ ΔΕΔΟΜΈΝΑ------------", var.get())
            entry = Entry(edit_window, textvariable=var, bd=2, width=len(var.get())).grid(column=1, row=index + 1, sticky="we")

    # --------------------   Προσθήκη δεδομένων στην βάση -------------------------------
    # ---------------------- μετά την επεξεργασία   -------------------------------------
    def update_to_db():
        global tree
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
        print("========edited data ======line 482", tuple(edited_data))
        # H ΣΥΝΤΑΞΗ ΕΙΝΑΙ ΑΥΤΉ
        # sql_insert = "INSERT INTO  " + table + "(" + culumns + ")" + "VALUES(NULL, ?, ?, ?, ?, ?, ?, ?);"
        # sqlite_update_query = """Update new_developers set salary = ?, email = ? where id = ?"""
        edit_cursor.execute("UPDATE " + table + "  SET " + culumns + " WHERE ID=? ",
            (tuple(edited_data)))

        edit_conn.commit()
        print(60 * "*")
        print(50 * "*", "Το προΐον ενημερώθηκε με επιτυχία", 50 * "*")
        print(60 * "*")
        print("==========Παλιά δεδομένα===========LINE 472 \n", selected_data)
        print()
        print("==========Νέα δεδομένα============ LINE 474 \n", edited_data)

        # Ενημέρωση του tree με τα νέα δεδομένα

        update_view(root, tree)

        print("Εγινε η Ενημέρωση του tree ")
        print(data_to_add)


    update_button = Button(edit_window, command=update_to_db, text="Ενημέρωση πρωιόντος", bg="red",
                           fg="white", bd=3)
    update_button.grid(column=1, row=9)


# ========================================================================================
# -------------------------------------BACK UP ------------------------------------------=
# ========================================================================================
# Αντιγραφα ασφαλείας βασης δεδομένων


def backup():
    global  dbase
    def progress(status, remainig, total):
        print(f"{status} Αντιγράφηκαν {total - remainig} απο {total} σελίδες...")

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
            tkinter.messagebox.showinfo('Αποτέλεσμα αντιγράφου ασφαλείας', error)
    finally:
        try:
            if back_conn:
                back_conn.close()
                print("Συνδεση με ", backup_file, " διακόπηκε")
        except UnboundLocalError as error:
            print(f"Η σύνδεση με {backup_file} δεν έγινε ποτέ {error}")
            tkinter.messagebox.showinfo(f"Η σύνδεση με {backup_file} δεν έγινε ποτέ {error}")


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
    answer = tkinter.messagebox.askquestion("Θα πραγματοποιηθεί διαγραφή!",
                                            " Είστε σήγουρος για την διαγραφή του {};".format(selected_data), icon='warning')
    if answer == 'yes':
        tkinter.messagebox.showwarning('Διαγραφή...', "Το {} διαγράφηκε!".format(selected_data))
        #Αν ο χρήστης επιλεξει το "yes" παει στην γραμμή 428
        pass
    else:
        tkinter.messagebox.showinfo('Ακύρωση διαγραφής', " Τίποτα δεν διαγράφηκε  ")
        print("=================ΑΚΥΡΟΣΗ ΔΙΑΓΡΑΦΗΣ===============line 509\n", selected_data)
        print()
        return

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