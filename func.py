"""
Sqlite Γραφικό περιβάλλον με Python3
******************************************************************
** Οι βάσεις πρέπει να έχουν Id ή id ή ID intiger και NOT NULL  **
******************************************************************
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
headers = []
dbase = ""


# Κουμπί να ανοιξει το αρχείο (βαση δεδομένων)
def open_file(tree):
    # Ανοιγουμε την βάση αν δεν έχουμε ανοιξει
    global dbase

    dbase = filedialog.askopenfilename(initialdir=os.getcwd(), title="Επιλογή βάσης δεδομένων",
                                           filetypes=(("db files",
                                                       "*.db"), (
                                                          "all files",
                                                          "*.*")))
    print("======================opened file ===================line 45", dbase)
    update_view(tree)

    return dbase


def update_view(tree):
    global dbase
    # global dbase
    # # Αν τρέξει απο το κουμπί προσθήκη του παραθύρου προσθήκη να μήν ανοιξει άλλο αρχείο
    # # διαφορετικα να ανοιξει αρχείο
    # if open_new_file == "yes":
    #
    #     dbase = open_file()

    # Να σβήσει πρώτα τα δεδομένω για να πάρει τα καινούρια
    # map(tree.delete, tree.get_children())
    for i in tree.get_children():
        # Εμφάνηση το τι σβήνηει
        #print("DELETED ΑΠΟ ΤΟ TREE ", i)
        tree.delete(i)

    up_conn = sqlite3.connect(dbase)
    print("=============Σύνδεση με Βαση Δεδομένων τώρα=============Line 116 ", dbase)
    print()
    up_cursor = up_conn.cursor()
    print("=====================up_cursor============================Line 119", up_cursor)

    # =======================Ανάγνωριση πίνκα δεδομένων=============
    up_cursor = up_conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_name = up_cursor.fetchall()
    dont_used_tables = ["sqlite_master", "sqlite_sequence", "sqlite_temp_master"]
    for name in table_name:
        if name[0] not in dont_used_tables:
            global table
            table = name[0]
            print("TABLE ", name[0])

    print("=========ΟΝΟΜΑ ΠΙΝΑΚΑ===========LINE 153 ", table)
    print()
    #up_cursor.execute("DELETE FROM " + table + " WHERE ΚΩΔΙΚΟΙ IS 'NONE'")
    up_cursor.execute("SELECT * FROM " + table)
    global headers
    headers = list(map(lambda x: x[0], up_cursor.description))
    print("headers at line 158 ", headers)
    print("**********************head, for head in headers************* Line 175", headers)
    # tree["columns"] = sqlite3.Row
    tree["columns"] = [head for head in headers]
    # tree["columns"] = ["id", "TONER", "ΜΟΝΤΕΛΟ", "ΚΩΔΙΚΟΣ", "ΤΕΜΑΧΙΑ", "ΤΙΜΗ", "ΣΥΝΟΛΟ", "ΣΕΛΙΔΕΣ"]
    # tree["show"] = "headings"
    up_data = up_cursor.fetchall()

    def sort():
        l = [(tree.item(k)[head], k) for k in tree.get_children()]  # Display column #0 cannot be set
        l.sort(key=lambda t: t[0], reverse=reverse)

        for index, (val, k) in enumerate(l):
            tree.move(k, '', index)

    for head in headers:
        tree.column(head, anchor="w", width=350 if head == headers[2] else 100, stretch=False)
        tree.heading(head, text=head)

    up_cursor.close()
    up_conn.close()
    print("up_data line 147 ", up_data)
    up_index = len(up_data)
    for n in range(len(up_data)):
        tree.insert("", up_index - 1, values=up_data[n],  tags=('ttk', 'simple'))
        tree.tag_configure('simple', background='red')

    return dbase


# ====================================================================================
# ================================Συναρτήσεις για τα κουμπιά==========================
# ------------------------------------------------------------------------------------
# --------------------------------Δημηουργία νεου παραθύρου---------------------------
def add_to(tree):
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
    def add_to_db(tree, dbase, headers):


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
        open_new_file = "no"
        update_view(tree)

        print("Εγινε η προσθήκη")
        print(data)

    # ----------------------------------Κουμπί για να γίνει η προσθήκη-------------------
    enter_button = Button(add_window, text="Προσθήκη", bg="green", fg="White", bd=8, padx=5, pady=8, command=lambda: add_to_db(tree, dbase, headers))
    enter_button.grid(column=1, row=9)


#=====================================ΑΝΑΖΗΤΗΣΗ=========================================
def search(tree, search_data):
    global dbase
    if search_data.get() != "":
        tree.delete(*tree.get_children())
        search_conn = sqlite3.connect(dbase)
        search_cursor = search_conn.cursor()
        #idea = SELECT * FROM tablename WHERE name or email or address or designation = 'nagar';
        search_headers = []
        no_needed_headers = ["id", "ID", "Id"]
        operators = []
        for header in headers:
            if header not in no_needed_headers:
                search_headers.append(header + " LIKE ?")
                operators.append('%' + str(search_data.get()) + '%')
        search_headers = " OR ".join(search_headers)
        print("===================Searching headers ================Line 623", search_headers)
        print("===================Operators=========================Line 627", operators)
        search_cursor.execute("SELECT * FROM " + table + " WHERE " + search_headers, operators)
        fetch = search_cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=data)
        search_cursor.close()
        search_conn.close()


# ========================================================================================
# ------------------------------------- ΕΠΕΞΕΡΓΑΣΙΑ -------------------------------------=
# ========================================================================================
def edit(tree):
    global dbase
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

        update_view(tree)

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
            tkinter.messagebox.showinfo('Αποτέλεσμα αντιγράφου ασφαλείας', result)
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

def del_from_tree(tree):
    global dbase
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