# coding=utf-8
"""
Sqlite Γραφικό περιβάλλον με Python3
******************************************************************
** Οι βάσεις πρέπει να έχουν Id ή id ή ID intiger και NOT NULL  **
******************************************************************


Version V1.0.1   | Προσθήκη κουμπί "προσθήκη στις παραγγελίες στο παράθυρο  επεξεργρασίας | --------------24/11/2019

Version V1.0.0   | Προσθήκη πίνακα παραγγελίες και ολα  παίζουν σωστά | ---------------------------------24/11/2019

Version V0.9.6   | Προσθήκη scolledtext και ολα τα χρώματα παίζουν σωστά | ------------------------------23/11/2019

Version V0.9.5   | Προσθήκη χρωμάτων στα MAGENTA CYAN BLACK YELLOW | ------------------------------------22/11/2019

Version V0.9.4   | Fixed log file (layout), fonts και toplevel παράθυρα   | -----------------------------18/11/2019


Version V0.9.3   | ΤΑΞΙΝΟΜΗΣΗ  δουλεύει σωστά  | -----------------------18/11/2019

Version V0.9.2   | Το πρόβλημα με το , λύθηκε | ------------------------17/11/2019

Version V0.9.1   | Dynamic screen sizes |  | Cleaned code | ------------17/11/2019

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



TODO LIST   ********* ΠΡΕΠΕΙ ΝΑ ΤΑ ΒΑΛΩ ΟΛΛΑ ΣΕ CLASS ΓΙΑ ΝΑ ΠΑΙΞΟΥΝ ΣΩΣΤΑ *******************
TODO 0) Επεξεργρασία επιλεγμένου απο το treeview  ΝΑ ΠΕΡΝΕΙ column αντι TONER=? κτλπ.-----------Εγινε 29/10/2019
TODO 1) ΝΑ ΦΤΙΑΞΩ ΤΟ BACKUP DIRECTORY-----------------------------------------------------------ΕΓΙΝΕ
TODO 2) ΤΟ TREE NA ΕΜΦΑΝΙΖΕΙ OTI ΒΑΣΗ ΚΑΙ ΝΑ ΕΠΙΛΕΞΩ--να εμφανίζει τους πίνακες-----------------ΕΓΙΝΕ 30/10/2019
TODO 3) ΝΑ ΒΑΛΩ ΜΕΝΟΥ --------------------------------------------------------------------------Εγινε 1/11/2019
TODO 4) ο χρήστης να επιλέγει τον πίνακα--------------------------------------------------------Εγινε 6/11/2019
TODO 5) Ελεγχος αν ο χρήστης εισάγει αλφαριθμητικό ή αριθμό-------------------------------------Εγινε 17/11/2019
TODO 6) Να βάλω να έχει log αρχείο--------------------------------------------------------------Εγινε 10/11/2019
TODO 7) Να κάνει αυτόματα υπολογισμό το σύνολο (όταν έχουμε τιμη και τεμάχια) ------------------Εγινε 17/11/2019
TODO 8) ΠΡΕΠΕΙ ΝΑ ΦΤΙΑΞΩ ΤΟ BACKGROYND STA COLORS ΝΑ ΕΙΝΑΙ ΣΥΜΦΟΝΑ ΜΕ ΤΗΝ ΣΕΙΡΑ ΓΡΙ Ή ΑΣΠΡΟ-----Εγινε 22/11/2019
TODO 9) ΠΡΕΠΕΙ ΣΤΗΣ ΠΑΡΑΤΗΡΗΣΕΙΣ ΝΑ ΒΑΖΕΙ ΜΟΝΟ ΤΗΝ ΤΕΛΕΥΤΑΙΑ ΤΡΟΠΟΠΟΙΗΣΗ------------------------Εγινε 22/11/2019
TODO 10) Να βάλω στο μενοu RUN SQL
TODO 11) Το sort δεν παίζει καλά με τα νούμερα -------------------------------------------------Eγινε 18/11/2019
"""

__author__ = "Jordanis Ntini"
__copyright__ = "Copyright © 2019"
__credits__ = ['Athanasia Tzampazi']
__license__ = 'Gpl'
__version__ = '1.0.0'
__maintainer__ = "Jordanis Ntini"
__email__ = "ntinisiordanis@gmail.com"
__status__ = 'Development'

# Πρώτα αυτό για το Combobox
from tkinter import ttk, Frame, Button, Tk, Label, Menu, StringVar, Entry, filedialog, messagebox, LEFT, FALSE, \
    TclError, Toplevel, font, PhotoImage, RAISED, END
from tkinter.scrolledtext import ScrolledText
import sqlite3

# datetime για backup την βαση πριν κάθε αλλαγή
from datetime import datetime

# Import os για να κάνουμε τον φακελο backup
import os

# Για τα αρχεία log files
import logging

# Για τα directory - φακέλους
import sys

# Για την τελευταια τροποpoiήση απο ποιόν χρήστη
import getpass

table = ""  # Για να ορίσουμε πιο κάτω τον πίνακα σαν global
# Αδεία λίστα για να πάρουμε τα header απο τον πίνακα της βάσης δεδομένων
headers = []  # Για να περσνουμε της επικεφαλίδες καθε πίνκα
dbase = "ΑΠΟΘΗΚΗ.db"
tables = []
up_data = []  # Για να πάρουμε τα δεδομένα
tree = ""
user = getpass.getuser()  # Για να πάρουμε το όνομα χρήστη απο τον υπολογιστή
# -------------ΔΗΜΗΟΥΡΓΕΙΑ LOG FILE------------------
today = datetime.today().strftime("%d %m %Y")
log_dir = "logs" + "\\" + today + "\\"

if not os.path.exists(log_dir):
    os.makedirs(log_dir)
else:
    pass

log_file_name = "ml_database_log" + datetime.now().strftime("%d %m %Y %H %M %S") + ".log"
log_file = os.path.join(log_dir, log_file_name)

# log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)  # or whatever
handler = logging.FileHandler(log_file, 'w', 'utf-8')  # or whatever
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')  # or whatever
handler.setFormatter(formatter)  # Pass handler as a parameter, not assign
root_logger.addHandler(handler)
sys.stderr.write = root_logger.error
sys.stdout.write = root_logger.info


# Κουμπί να ανοιξει το αρχείο (βαση δεδομένων)
def open_file(root):
    """ Ανοιγμα αρχείου βάσης δεδομένων"""

    global dbase
    # Να σβήσουμε παλιά κουμπιά και tree αν ανοιξουμε αλη βαση δεδομένων
    list_of_frames = root.grid_slaves()
    # print("list_of_frames root.grid.slaves line 78", list_of_frames)
    for i in list_of_frames:

        if len(list_of_frames) > 1:
            if ".!frame" in str(i):
                i.destroy()
            elif ".!scrollbar" in str(i):
                i.destroy()
        else:
            # print("list_of_frames root.grid.slaves  after deleted line 129", list_of_frames)
            continue
    # dbase = filedialog.askopenfilename(initialdir=os.getcwd(), title="Επιλογή βάσης δεδομένων",
    # filetypes=(("db files", "*.db"), ("all files", "*.*")))
    dbase = "ΑΠΟΘΗΚΗ.db"
    # print("Γραμμή 112: Επιλεγμένη βάση δεδομένων -->>", dbase)
    get_tables()
    select_table(root)
    return dbase


# Ορισμός πινάκων
def get_tables():
    """ Αποκόμιση  πινάκων απο την βάση δεδομένων """

    global tables
    tables = []
    # =======================Ανάγνωριση πίνακα δεδομένων=============
    conn = sqlite3.connect(dbase)
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
    table_name = cursor.fetchall()
    cursor.close()
    conn.close()
    dont_used_tables = ["sqlite_master", "sqlite_sequence", "sqlite_temp_master"]  # Πινακες που δεν θέλουμε
    for name in table_name:
        if name[0] not in dont_used_tables:
            tables.append(name[0])
            # print("TABLE ", name[0], " ========added to tables line 118")

        else:
            continue
    # print("Γραμμη 136: Πίνακες που βρέθηκαν -->>", tables)
    return tables





def select_table(root):
    """ Δημιουργια κουμπιών σύμφωνα με τους πίνακες της βασης """

    global tables
    buttons = []

    def change_color(table_name):

        """ Αλλαγή χρώματος κουμπιου όταν το πατάμε
            Δεχεται σαν όρισμα το ονομα του πίνακα που αντιπροσωπευει το κουμπί

            Το κάνουμε με έλνχω των θεσεων δλδ αν το κουμπί που πατάμε εχει την ίδια θέση με τον πίνακα
            που αντιπροσοπευει πατόντας το, τοτε να αλλάζει το χρώμα στο κουμπί σε πορτοκαλί
            και στα υπολειπα κουμπιά σε gray20
        """
        # print("btn_pressed Line 135", btn)
        # print("buttons line 136", buttons)
        lazaros_tables = ["ΦΩΤΟΤΥΠΙΚΑ", "ΤΟΝΕΡ"]
        for button in buttons:

            if tables.index(table_name) == buttons.index(button):

                button.configure(background="#EFA12C")
            else:
                button.configure(background="#657b83")

        # -------------------- Χρώματα για τον Λάζαρος ------------------------
        # for button in buttons:
        #     for table_name in tables:
        #         if table_name in lazaros_tables:
        #             button.configure(background="#836d65")
        #         else:
        #             continue

    search_frame = Frame(root, bg="#C2C0BD")

    # ======================Πληκτολόγιο=====================
    def search_event(event):
        """ Οταν πατάμε enter στην αναζήτηση να εκτελεστεί το search(search_data)"""
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

    # -----------------------------------------Κουμπιά -----------------------------------
    #  Δυνομική δημιουργια κουμπιών σύμφονα με του πίνακες της βάσης δεδομένων
    for index, table_name in enumerate(tables):
        btn = Button(buttons_frame, command=lambda x=table_name: [update_view(root, x), change_color(x)],
                     image="", compound=LEFT, text=table_name, font=('San Serif', '10', 'bold'),
                     bg="#657b83", fg="white", bd=5, relief=RAISED, )

        buttons.append(btn)
        if len(buttons) >= 11:
            btn.grid(row=1, column=index - 10, ipadx=len(str(table_name)) + 10, ipady=20, sticky="ew")
        else:
            btn.grid(row=0, column=index, ipady=20, sticky="ew")

    search_frame.grid(column=0, row=1)
    buttons_frame.grid(column=0, row=0)


def sort_by_culumn(tree, column, reverse):
    """ Ταξινομηση δεδομένων πατώντας στις κεφαλίδες τou tree
        tree = το tree
        column = κεφαλίδα του tree
    """

    lista = [[tree.set(k, column), k] for k in tree.get_children("")]
    """ lista = [[κατι, id],[κατι αλλο , id]]
    """
    try:
        # sorted(iterable, *, key=None, reverse=False)
        # Return a new sorted list from the items in iterable.
        if column == "ΤΙΜΗ" or column == "ΣΥΝΟΛΟ" or column == "ΚΩΔΙΚΟΣ" or column == "ΣΕΛΙΔΕΣ":
            # Αν Αληθής γίνεται  Αφαίρεση € , "" και None για να γίνει sort σαν αριθμοί
            for index, (x, y) in enumerate(lista):
                # ισως θα μπορούσε να γίνει και x = x.replace("€", "")
                # το lista[index][0] ειναι το x
                lista[index][0] = lista[index][0].replace("€", "")  # Αφαίρεση €

                lista[index][0] = lista[index][0].replace(",", ".")  # Αφαίρεση ,
                if lista[index][0] == "":  # Αφαίρεση "" αν είναι κενό δλδ
                    lista[index][0] = 0.00
                if lista[index][0] == 'None':  # Αφαίρεση  αν είναι 'None'
                    lista[index][0] = 0

        lista = sorted(lista, key=lambda x: float(x[0]), reverse=reverse)  # Ταξινόμηση για τιμές και σύνολα
    except ValueError as error:  # Αν δεν είναι αριθμοί βγάζει error για το float και το κάνει με το lista.sort()
        print("Σφάλμα ", error)
        lista = sorted(lista, reverse=reverse)

    # Εμφάνισει στο tree την ταξινομημένη lista
    for index, (val, k) in enumerate(lista):
        tree.move(k, "", index)

    tree.heading(column, command=lambda: sort_by_culumn(tree, column, not reverse))


# -----------------------------  Αδειασμα παραγγελιών  -------------------------------------------
def empty_table():
    answer = messagebox.askquestion("ΠΡΟΣΟΧΗ", "Θα πραγματοποιηθεί διαγραφή όλων των παραγγελείων,\n \
                                                Είστε σήγουρος για την διαγραφή τους", icon='warning')
    if answer == 'yes':
        empty_conn = sqlite3.connect(dbase)
        empty_cursor = empty_conn.cursor()
        empty_cursor.execute("""SELECT * FROM Ω_ΠΑΡΑΓΓΕΛΙΕΣ""")
        paraggelies = empty_cursor.fetchall()
        print("===============Παραγγελίες διαγράφικαν απο χρήστη {} ========".format(user))
        for paraggelia in paraggelies:
            print(paraggelia)
        empty_cursor.execute("""DELETE FROM Ω_ΠΑΡΑΓΓΕΛΙΕΣ;""")
        empty_conn.commit()
        empty_cursor.execute("""VACUUM;""")
        empty_cursor.close()
        empty_conn.close()
        messagebox.showwarning("ΠΡΟΣΟΧΗ ", "Ο πίνακας Ω_ΠΑΡΑΓΓΕΛΙΕΣ άδειασε")

    else:
        messagebox.showinfo('Ακύρωση διαγραφής παραγγελιών', " Τίποτα δεν διαγράφηκε  ")

        return None


def update_view(root, table_from_button):
    """ Δέχεται τον πίνακα και εμφανίζει τα δεδομένα στο tree
    """
    data_frame = Frame(root, bg="#C2C0BD")
    global tree, dbase, headers, table
    # Αν υπάρχει προηγούμενο tree το διαγράφει για να έχουμε μόνο ένα tree
    if tree:
        tree.destroy()
    else:
        pass
    rows = int(root.winfo_screenheight() / 60)
    table = table_from_button
    tree = ttk.Treeview(data_frame, selectmode="browse", style="mystyle.Treeview", show="headings", height=rows)
    # ================================ scrolls======================
    scrolly = ttk.Scrollbar(root, orient='vertical', command=tree.yview)
    scrolly.grid(column=100, row=3, sticky="nse")
    tree.configure(yscrollcommand=scrolly.set)
    scrollx = ttk.Scrollbar(root, orient='horizontal', command=tree.xview)
    scrollx.grid(sticky='we', column=0, row=4, columnspan=100)
    tree.configure(xscrollcommand=scrollx.set)

    # print("Γραμμη 236: Επιλεγμένος πίνακας -->> ", table)
    for i in tree.get_children():
        # Εμφάνηση το τι σβήνηει
        # print("DELETED ΑΠΟ ΤΟ TREE ", i)
        tree.delete(i)
    up_conn = sqlite3.connect(dbase)
    up_cursor = up_conn.cursor()
    up_cursor.execute("SELECT * FROM " + table)
    # print("Γραμμη 266: Επιλογή όλων απο τον πίνακα -->>", table)
    headers = list(map(lambda x: x[0], up_cursor.description))

    # print("Γραμμη 269: Κεφαλίδες -->> ", headers)
    columns = []
    for head in headers:
        columns.append(head)

    tree["columns"] = [head for head in columns]

    # tree["columns"] = ["id", "TONER", "ΜΟΝΤΕΛΟΣ", "ΚΩΔΙΚΟΣ", "ΤΕΜΑΧΙΑ", "ΤΙΜΗ", "ΣΥΝΟΛΟ", "ΣΕΛΙΔΕΣ"]
    # tree["show"] = "headings"

    width = root.winfo_screenwidth()
    alignment = ""
    for head in headers:
        # ==================================== ΣΤΟΙΧΙΣΗ ΠΕΡΙΕΧΟΜΕΝΩΝ ===========================
        if head == "ΤΙΜΗ" or head == "ΣΥΝΟΛΟ":  # ΣΤΟΙΧΗΣΗ ΔΕΞΙΑ
            alignment = "e"
            if head == "ΤΙΜΗ":
                platos = int(width / 25)
            else:
                platos = int(width / 23)
        elif head == "ΚΩΔΙΚΟΣ" or head == "ΤΕΜΑΧΙΑ":  # ΣΤΟΙΧΗΣΗ ΚΕΝΤΡΟ
            alignment = "center"
            if head == "ΚΩΔΙΚΟΣ":
                platos = int(width / 23)
            else:
                platos = int(width / 20)
        elif head == "ΠΑΡΑΤΗΡΗΣΗΣ" or head == "ΠΕΡΙΓΡΑΦΗ":  # ΣΤΟΙΧΗΣΗ ΑΡΙΣΤΕΡΑ
            if head == "ΠΑΡΑΤΗΡΗΣΗΣ" and len(headers) < 7:
                platos = int(width / 3)
            elif head == "ΠΕΡΙΓΡΑΦΗ":
                platos = int(width / 2.37)
            else:
                platos = int(width / 12)
            alignment = "w"

        elif head == "PARTS_NR":
            platos = int(width / 12)
        else:
            alignment = "center"
            platos = int(width / 17)
        tree.column(head, anchor=alignment, width=platos, stretch="false")
        tree.heading(head, text=head, command=lambda _col=head: sort_by_culumn(tree, _col, False))

    up_data = up_cursor.fetchall()
    # print("up_data line 247 ", up_data)
    up_index = len(up_data)
    colors = ["MAGENTA", "YELLOW", "CYAN", "BLACK", "C/M/Y"]
    tree.tag_configure('oddrow', background='#ece8de', foreground="black", font=("San Serif", 10))
    tree.tag_configure('evenrow', background='white', font=("San Serif", 10))
    tree.tag_configure('oddrowYELLOW', background='#ece8de', foreground="orange", font=("San Serif", 10, "bold"))
    tree.tag_configure('evenrowYELLOW', background='white', foreground="orange", font=("San Serif", 10, "bold"))
    tree.tag_configure('oddrowCYAN', background='#ece8de', foreground="cyan", font=("San Serif", 10, "bold"))
    tree.tag_configure('evenrowCYAN', background='white', foreground="cyan", font=("San Serif", 10, "bold"))
    tree.tag_configure('oddrowMAGENTA', background='#ece8de', foreground="magenta", font=("San Serif", 10, "bold"))
    tree.tag_configure('evenrowMAGENTA', background='white', foreground="magenta", font=("San Serif", 10, "bold"))
    tree.tag_configure('oddrowBLACK', background="#ece8de", foreground="BLACK", font=("San Serif", 10, "bold"))
    tree.tag_configure('evenrowBLACK', background="white", foreground="BLACK", font=("San Serif", 10, "bold"))
    tree.tag_configure("oddrowC/M/Y", background="#ece8de", foreground="green", font=("San Serif", 10, "bold"))
    tree.tag_configure("evenrowC/M/Y", background="white", foreground="green", font=("San Serif", 10, "bold"))

    for n in range(len(up_data)):
        # Κατασκευή tree το up_index -1 == το τελος ("end")
        try:
            # up_data[n][columns.index("ΠΕΡΙΓΡΑΦΗ")] == Ψάχνει όπου είναι η ΚΕΦΑΛΙΔΑ "περιγραφή"
            color = [color for color in colors if color in up_data[n][headers.index("ΠΕΡΙΓΡΑΦΗ")]]

        except TypeError as error:
            # Αν δεν έχει πειργραφή μαλλον συνεχίζει
            continue
            # Οταν στον πίνακα το up_data[n][4] δεν είναι η περιγραφή
        if int(up_data[n][0]) % 2 == 0 and color:
            # Αν το id διαιρείται με το δυο αλλάζουμε το background

            tree.insert("", up_index - 1, values=up_data[n],
                        tags=("oddrow" + str(color[0]) if len(color) < 2 else "oddrow" + str(color[-1]),))

        elif int(up_data[n][0]) % 2 == 0 and not color:
            tree.insert("", up_index - 1, values=up_data[n], tags=("oddrow",))

        elif int(up_data[n][0]) % 2 != 0 and color:
            tree.insert("", up_index - 1, values=up_data[n],
                        tags=("evenrow" + str(color[0]) if len(color) < 2 else "evenrow" + str(color[-1]),))

        else:
            tree.insert("", up_index - 1, values=up_data[n], tags=("evenrow",))

    data_frame.grid(column=0, row=3, columnspan=100)

    def double_click(event):
        """ Με δυπλό click εμφανίζεται η επεξεργασία δεδομένων"""
        edit(root)

    tree.bind("<Double-1>", double_click)

    if table_from_button == "Ω_ΠΑΡΑΓΓΕΛΙΕΣ":
        empty_button = Button(data_frame, text="Αδειασμα παραγγελιών", command=empty_table, bg="red", fg="white",
                              bd=3, padx=3, pady=10)
        tree.grid(column=0, row=0, columnspan=100)
        empty_button.grid(column=103, row=0, sticky="we")

    else:
        tree.grid(column=0, row=1, columnspan=100)

    return dbase


# ====================================================================================
# ================================Συναρτήσεις για τα κουμπιά==========================
# ------------------------------------------------------------------------------------
# --------------------------------Δημηουργία νεου παραθύρου---------------------------
def add_to(root):
    """ Προσθήκη προίοντος """
    global table, dbase, headers
    height = int(root.winfo_screenheight() / 18 * len(headers))
    width = int(root.winfo_screenwidth() / 1.5)
    add_window = Toplevel()
    add_window_geometry = str(width) + "x" + str(height) + "+100+100"
    add_window.geometry(add_window_geometry)
    add_window.focus()
    add_window.title("Προσθήκη δεδομένων")
    # Τίτλος παραθύρου
    add_window_title = Label(add_window, bg="brown", fg="white", text="Προσθήκη προϊόντος", font=("San Serif Bold", 15),
                             bd=8, padx=3, )
    add_window_title.grid(column=1, row=0)

    # ------------------------------Να πάρουμε τις κεφαλίδες---------------------------
    try:
        conn = sqlite3.connect(dbase)
        cursor = conn.execute("SELECT * FROM " + table)
        headers = list(map(lambda x: x[0], cursor.description))

    except sqlite3.OperationalError as error:
        messagebox.showwarning("Σφάλμα.....", "{} \nΠαρακαλώ πρώτα επιλέξτε πίνακα για να κάνετε προσθήκη δεδομένων"
                               .format(error),
                               icon='warning')
        add_window.destroy()
        return None

    # ===========================Εμφάνιση κεφαλίδων======================================
    # ΟΙ ΚΕΦΑΛΊΔΕΣ ΕΊΝΑΙ ΤΑ COLUMNS ΤΟΥ ΠΊΝΑΚΑ
    # Nα μετρίσουμε πόσες κεφαλίδες έχει ο πίνακας χωρίς τα " ID " , μας χρειάζεται για τα entry που θα κάνει ο χρήστης
    count_headers = 0
    data_to_add = []

    for index, header in enumerate(headers):
        if header == "ID" or header == "id" or header == "Id":
            continue
        else:
            count_headers += 1
            toner_label = Label(add_window, text=header, width=15, padx=1, pady=1, font=("San Serif", 12, "bold"), bd=3)
            toner_label.grid(column=1, row=index + 1)
            var = StringVar()
            # Εμφάνισει περιγραφής σαν Scrolledtext και όχι σαν απλο Entry
            if header == "ΠΕΡΙΓΡΑΦΗ":
                perigrafi = ScrolledText(add_window, bd=2, width=58, height=3)
                data_to_add.append(perigrafi)

                perigrafi.grid(column=2, row=index + 1)
            else:
                Entry(add_window, textvariable=var, bd=2, width=80).grid(column=2, row=index + 1)
                data_to_add.append(var)

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
        # print("============values_var============line 371", values)
        # print("==========culumns===========", culumns)
        data = []
        for i in range(len(data_to_add)):
            # Ελενχος αν είναι απο το scrolledtext
            # Το scrolledtext θελει get('1.0', 'end-1c') και οχι απλό get
            # Ο Ελεγχος γίνεται με το αν το data_to_add[i] == με class scrolledtext
            # Αν δεν ειναι scrolledtext τότε πέρνουμε τα δεδομένα με το var.get()
            type_of_data_to_add = str(type(data_to_add[i]))
            if "scrolledtext" in type_of_data_to_add:
                # print("Line 513 Data do add need .get", data_to_add[i].get('1.0', 'end-1c'))
                data.append(data_to_add[i].get('1.0', 'end-1c'))

            else:
                data.append(data_to_add[i].get())
        # data = tuple(data_to_add)
        # print("Line 406 data before €", data)

        try:
            if "ΣΥΝΟΛΟ" in headers:
                # {: 0.2f}           Για εμφάνιση 2 δεκαδικών
                # data[6]= 0 αν ο χρήστης δεν δόσει τιμή να δώσουμε 0 ------data[6] == ΤΙΜΗ
                if data[6] == "":
                    data[6] = 0
                else:
                    data[6] = data[6].replace(",", ".")  # Μετατροπή , σε . για πολλαπλασιασμό (να βρούμε το σύνολο)
                data[7] = float(data[5]) * float(data[6])
                data[7] = str("{:0.2f}".format(data[7])) + "€"
                data[6] = str("{:0.2f}".format(float(data[6]))) + " €"
                data[5] = str(data[5])
        except IndexError as error:
            print("Δεν υπάρχει σύνολο στον πίνκα {} για υπολογισμό συνόλου τιμής * τεμάχια".format(table), error)
        except ValueError as error:
            print("H τιμή δεν μπορεί να είναι κενή", error)
            pass
        # ================================ Προσθήκη τελευταίας τροποποιησης ============================
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # Ελεγχος αν ο πίνακας είναι παραγγελίες
        if table == "Ω_ΠΑΡΑΓΓΕΛΙΕΣ":
            # Αν ο χρήστης είναι στον πίνακα παραγγελίες τότε προσθέτει την ημερωμηνία αυτόματα
            # now[:10] == ημερωμηνία χωρείς την ώρα
            data[headers.index("ΗΜΕΡΩΜΗΝΙΑ")-1] = now[:10]
            data[-1] = data[-1]
        else:
            data[-1] = now + " " + user + " ==>> " + data[-1]
        # print("===========DATA TO ADD AFTER LOOP =========LINE 377 ", data)
        # data_to_add = (toner.get(), model.get(), kodikos.get(),
        #               temaxia.get(), str(timi.get()) + " €", str(timi.get() * temaxia.get()) + " €", selides.get())

        # ΒΑΖΟΥΜΕ ΤΟ ΠΡΩΤΟ NULL ΓΙΑ ΝΑ ΠΆΡΕΙ ΜΟΝΟ ΤΟΥ ΤΟ ID = PRIMARY KEY
        # H ΣΥΝΤΑΞΗ ΕΙΝΑΙ ΑΥΤΉ
        # INSERT INTO table(column1, column2,..)VALUES(value1, value2, ...);  TA  VALUES πρεπει να είναι tuple
        # sql_insert = "INSERT INTO  " + table + "(" + culumns + ")" + "VALUES(NULL, ?, ?, ?, ?, ?, ?, ?);"
        # values είναι πόσα ? να έχει ανάλογα τα culumns
        sql_insert = "INSERT INTO  " + table + "(" + culumns + ")" + "VALUES(" + values + ");"
        # print("===============sql_insert==========\n", sql_insert)
        print("===========Προθήκη δεδομένων στο Πίνακα {} Line 483 =========".format(table), "\n", headers)
        print(data)
        add_to_db_conn = sqlite3.connect(dbase)
        # print("conected ", 50 * ".")
        add_to_db_cursor = add_to_db_conn.cursor()
        # print("cursor done ", 50 * ".")
        add_to_db_cursor.execute(sql_insert, tuple(data))
        # print("sql executed  ", 50 * ".")

        add_to_db_conn.commit()
        # print("ΣΤΗΝ ΒΑΣΗ ΠΡΟΣΤΕΘΗΚΑΝ ", data)
        add_to_db_cursor.close()
        add_to_db_conn.close()
        messagebox.showinfo('Εγινε προσθήκη δεδομένων', "Στην κατηγορία {} Προστέθηκε το {} ".format(table, str(data)))
        # Ενημέρωση του tree με τα νέα δεδομένα

        update_view(root, table)
        add_window.destroy()
        # print("Εγινε η προσθήκη")
        # print(data)

    # ----------------------------------Κουμπί για να γίνει η προσθήκη-------------------
    enter_button = Button(add_window, text="Προσθήκη", bg="green", fg="White", bd=8, padx=5, pady=8,
                          command=lambda: add_to_db(root, dbase, headers))
    enter_button.grid(column=1, row=13)

    # ΕΞΩΔΟΣ
    def quit_app(event):

        add_window.destroy()

    add_window.bind('<Escape>', quit_app)


# =====================================ΑΝΑΖΗΤΗΣΗ=========================================
def search(search_data):
    global tree, table
    if search_data.get() != "":
        tree.delete(*tree.get_children())
        search_conn = sqlite3.connect(dbase)
        search_cursor = search_conn.cursor()
        # idea = SELECT * FROM tablename WHERE name or email or address or designation = 'nagar';
        search_headers = []
        no_neded_headers = ["id", "ID", "Id"]
        operators = []
        for header in headers:
            if header not in no_neded_headers:
                search_headers.append(header + " LIKE ?")
                operators.append('%' + str(search_data.get()) + '%')
        search_headers = " OR ".join(search_headers)
        # print("===================search_data=======================Line 385", search_data)
        # print("===================Searching headers ================Line 386", search_headers)
        # print("===================Operators=========================Line 387", operators)
        # print("=====================table===========================Line 388", table)

        # search_cursor.execute("SELECT * FROM " + table + " WHERE \
        # ΤΟΝΕΡ LIKE ? OR ΜΟΝΤΕΛΟ LIKE ? OR ΚΩΔΙΚΟΣ LIKE ? OR TEMAXIA LIKE ? OR ΤΙΜΗ LIKE ? etc...
        # ('%' + str(search_data.get()) + '%', '%' + str(search_data.get()) + '%', '%' + str(search_data.get()) +
        # '%', '%' + str(search_data.get()) + '%', '%' + str(search_data.get()) + '%', '%' + str(search_data.get()) +
        # '%', '%' + str(search_data.get()) + '%'))
        search_cursor.execute("SELECT * FROM " + table + " WHERE " + search_headers, operators)
        # ('%' + str(search_data.get()) + '%', '%' + str(search_data.get()) + '%', '%' + str(search_data.get()) + '%',
        #  '%' + str(search_data.get()) + '%', '%' + str(search_data.get()) + '%', '%' + str(search_data.get()) + '%',
        #  '%' + str(search_data.get()) + '%'))

        fetch = search_cursor.fetchall()
        colors = ["MAGENTA", "YELLOW", "CYAN", "BLACK", "C/M/Y"]
        tree.tag_configure('oddrow', background='#ece8de', foreground="black", font=("San Serif", 10))
        tree.tag_configure('evenrow', background='white', font=("San Serif", 10))
        tree.tag_configure('oddrowYELLOW', background='#ece8de', foreground="orange", font=("San Serif", 10, "bold"))
        tree.tag_configure('evenrowYELLOW', background='white', foreground="orange", font=("San Serif", 10, "bold"))
        tree.tag_configure('oddrowCYAN', background='#ece8de', foreground="cyan", font=("San Serif", 10, "bold"))
        tree.tag_configure('evenrowCYAN', background='white', foreground="cyan", font=("San Serif", 10, "bold"))
        tree.tag_configure('oddrowMAGENTA', background='#ece8de', foreground="magenta", font=("San Serif", 10, "bold"))
        tree.tag_configure('evenrowMAGENTA', background='white', foreground="magenta", font=("San Serif", 10, "bold"))
        tree.tag_configure('oddrowBLACK', background="#ece8de", foreground="BLACK", font=("San Serif", 10, "bold"))
        tree.tag_configure('evenrowBLACK', background="white", foreground="BLACK", font=("San Serif", 10, "bold"))
        tree.tag_configure("oddrowC/M/Y", background="#ece8de", foreground="green", font=("San Serif", 10, "bold"))
        tree.tag_configure("evenrowC/M/Y", background="white", foreground="green", font=("San Serif", 10, "bold"))
        odd_or_even = 0
        for data in fetch:
            # Κάνει αναζήτηση του color μόνο στην κεφαλίδα "ΠΕΙΓΡΑΦΉ"
            color = [color for color in colors if color in data[headers.index("ΠΕΡΙΓΡΑΦΗ")]]
            # color = [color for color in colors if color in data[4]]  # up_data[n][4] == ΠΕΡΙΓΡΑΦΗ
            odd_or_even += 1
            if odd_or_even % 2 == 0 and color:
                tree.insert("", "end", values=data,
                            tags=("oddrow" + color[0] if len(color) < 2 else "oddrow" + color[-1],))

            elif odd_or_even % 2 == 0 and not color:
                tree.insert("", "end", values=data, tags=("oddrow",))

            elif odd_or_even % 2 != 0 and color:
                tree.insert("", "end", values=data,
                            tags=("evenrow" + color[0] if len(color) < 2 else "evenrow" + color[-1],))
            else:
                tree.insert("", 'end', values=data, tags=("evenrow",))

        search_cursor.close()
        search_conn.close()


# ========================================================================================
# ------------------------------------- ΠΡΟΣΘΗΚΗ ΠΑΡΑΓΓΕΛΙΑΣ ----------------------------=
# ========================================================================================
# Δεχεται σαν όρισμα το edit_windows για να μππορέσουμε να το κλείσουμε όταν κάνουμε την προσθήκη παραγγελίας
def add_to_orders(edit_window, data_to_add):
    # Προσθήκη κωδικού και περιγραφής στις παραγγελίες
    code_for_order = data_to_add[headers.index("ΚΩΔΙΚΟΣ")]
    perigrafi_for_order = data_to_add[headers.index("ΠΕΡΙΓΡΑΦΗ")]
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    data_to_orders = [code_for_order, now[:10], perigrafi_for_order, "", user]

    # print("Line 701 ", tuple(data_to_orders))

    order_conn = sqlite3.connect(dbase)
    order_cursos = order_conn.cursor()
    order_cursos.execute("""SELECT * FROM Ω_ΠΑΡΑΓΓΕΛΙΕΣ;""")

    headers_of_orders = list(map(lambda x: x[0], order_cursos.description))
    culumns = ",".join(headers_of_orders)

    values_var = []
    for head in headers_of_orders:
        if head == "ID" or head == "id" or head == "Id":
            values_var.append("null")
        else:
            values_var.append('?')
    values = ",".join(values_var)

    data_from_paraggelies = order_cursos.fetchall()
    print("line 722 code to find", code_for_order)
    print("Line 723 data_from_paraggelies", data_from_paraggelies)
    found = False
    for data in data_from_paraggelies:
        print("Line 719 data", data)
        if code_for_order in data:
            found = True    # Δηλαδή βρεθηκε ο κωδικός στις παραγγελίες
            answer = messagebox.askquestion("ΠΡΟΣΟΧΗ",
                                            " Ο κωδικός {} υπαρχει ήδη στης παραγγελίες, "
                                            "θέλετε να το ξανα προσθέσετε;".format(code_for_order),
                                            icon='warning')
            # Αν ο χρήστης θέλει να το ξαναπροσθέσει
            if answer == "yes":
                sql_insert = "INSERT INTO Ω_ΠΑΡΑΓΓΕΛΙΕΣ " + "(" + culumns + ")" + "VALUES(" + values + ");"
                order_cursos.execute(sql_insert, tuple(data_to_orders))
                order_conn.commit()
                order_cursos.close()
                order_conn.close()
                messagebox.showwarning("ΠΡΟΣΘΗΚΗ", "Ο κωδικός {} προστέθηκε στις παραγγελίες".format(code_for_order))
                edit_window.destroy()
            else:
                messagebox.showwarning("ΑΚΥΡΩΣΗ", "Ο κωδικός {} δεν προστέθηκε στις παραγγελίες".format(code_for_order))
                edit_window.destroy()
                return None

    # Αν δεν βρέθηκε στις παραγγελίες
    if not found:
        sql_insert = "INSERT INTO Ω_ΠΑΡΑΓΓΕΛΙΕΣ " + "(" + culumns + ")" + "VALUES(" + values + ");"
        order_cursos.execute(sql_insert, tuple(data_to_orders))
        order_conn.commit()
        order_cursos.close()
        order_conn.close()
        messagebox.showwarning("ΠΡΟΣΘΗΚΗ", "Ο κωδικός {} προστέθηκε στις παραγγελίες".format(code_for_order))
        edit_window.destroy()

    # Αν Ο πίνακας παραγγελίες είναι άδειος
    if not data_from_paraggelies:
        sql_insert = "INSERT INTO Ω_ΠΑΡΑΓΓΕΛΙΕΣ " + "(" + culumns + ")" + "VALUES(" + values + ");"
        order_cursos.execute(sql_insert, tuple(data_to_orders))
        order_conn.commit()
        order_cursos.close()
        order_conn.close()
        messagebox.showwarning("ΠΡΟΣΘΗΚΗ", "Ο κωδικός {} προστέθηκε στις παραγγελίες".format(code_for_order))
        edit_window.destroy()
        return None


def edit(root):
    global dbase, tree, headers

    # ===============ΠΡΩΤΑ BACKUP =========

    # print("Γραμμη 425: ΕΠΕΞΕΡΓΑΣΙΑ ΣΤΟ Επιλεγμένο id -->", (tree.set(tree.selection(), '#1')))
    if not tree.set(tree.selection(), "#1"):
        messagebox.showwarning("Σφάλμα.....", " Παρακαλώ πρώτα επιλέξτε απο την λίστα για να κάνετε επεξεργασία",
                               icon='warning')

        return None

    selected_item = (tree.set(tree.selection(), '#1'))
    edit_conn = sqlite3.connect(dbase)
    edit_cursor = edit_conn.cursor()
    edit_cursor.execute("SELECT * FROM " + table + " WHERE ID = ?", (selected_item,))
    selected_data = edit_cursor.fetchall()
    selected_data = list(selected_data[0])
    # print("selected_data line 424 ", selected_data)
    # print("headers[0] γραμμή 425 = ", headers[0])
    edit_window = Toplevel()
    height = int(root.winfo_screenheight() / 20 * len(headers))
    width = int(root.winfo_screenwidth() / 1.5)
    x = "+200"
    y = "+200"
    edit_window_geometry = str(width) + "x" + str(height) + x + y
    edit_window.geometry(edit_window_geometry)
    edit_window.focus()
    edit_window.title("Επεξεργασία δεδομέμων")
    edit_window_title = Label(edit_window, bg="brown", fg="white", text="Επεξεργασία δεδομέμων",
                              font=("San Serif Bold", 15),
                              bd=8, padx=3, )
    edit_window_title.grid(column=0, row=0)
    # Label(edit_window, text=tree.selection()).grid(column=0, row=0)
    # ===========================Εμφάνιση κεφαλίδων======================================
    count_headers = 0
    data_to_add = []
    colors = ["MAGENTA", "YELLOW", "CYAN", "BLACK", "C/M/Y"]

    for index, header in enumerate(headers):
        if header == "ID" or header == "id" or header == "Id":
            continue
        else:

            count_headers += 1
            ton_label = Label(edit_window, text=header, width=15, padx=1, pady=1, font=("San Serif", 12, "bold"), bd=3)
            ton_label.grid(row=index + 1)
            var = StringVar(edit_window, value=selected_data[index])
            # Αν υπάρχει "περιγραφη" στις κεφαλίδες η εμφάνιση των δεδομένων της κεφαλίδας περιγραφή ειναι με scrolltext
            if header == "ΠΕΡΙΓΡΑΦΗ":
                color = [color for color in colors if color in selected_data[index]]

                perigrafi = ScrolledText(edit_window, height=3, width=80, bd=2)
                # Αν υπάρχει χρώμα να ελέγχει ποιο χρώμα και ανάλογα να τροποποιεί  το κείμενο
                if color:
                    if color[0] == "YELLOW":
                        perigrafi.insert('1.0', selected_data[index], "YELLOW")
                        perigrafi.tag_config(color, foreground="orange", font=("San Serif", 10, "bold"))

                    elif len(color) > 1 or "C/M/Y" in color:
                        perigrafi.insert('1.0', selected_data[index], "green")
                        perigrafi.tag_config("green", foreground="green", font=("San Serif", 10, "bold"))
                    else:

                        perigrafi.insert('1.0', selected_data[index], color)
                        perigrafi.tag_config(color, foreground=color, font=("San Serif", 10, "bold"))
                else:
                    perigrafi.insert('1.0', selected_data[index])

                perigrafi.grid(column=1, row=index + 1)

                data_to_add.append(perigrafi)
            else:

                # print("------------ΜΗ ΕΠΕΞΕΡΓΑΣΜΈΝΑ ΔΕΔΟΜΈΝΑ------------", header, var.get())
                Entry(edit_window, textvariable=var, bd=2, width=len(var.get()) + 5) \
                    .grid(column=1, row=index + 1, ipady=3, sticky="we")
                data_to_add.append(var)

    # --------------------   Προσθήκη δεδομένων στην βάση -------------------------------
    # ---------------------- μετά την επεξεργασία   -------------------------------------
    def update_to_db():
        backup()
        print("Γραμμή 733: ---------------ΛΟΓΟΣ BACKUP --->>> ΕΠΕΞΕΡΓΑΣΙΑ ΔΕΔΟΜΕΝΩΝ ------------------------- ")
        global tree, table
        # culumns = ",".join(headers)
        # Τα culumns ειναι της μορφής ID, ΤΟΝΕΡ, ΜΟΝΤΕΛΟ, ΚΩΔΙΚΟΣ κτλπ.
        # Πρεπει να γίνουν ΤΟΝΕΡ=?, ΜΟΝΤΕΛΟ=?, ΚΩΔΙΚΟΣ=? κτλπ για την σύνταξη της sql
        # Ευκολο άν μπουν σε νεα λίστα παρά να τροποποιησω την υπάρχουσα λίστα
        edited_culumns = []
        for culumn in headers:
            if culumn == "id" or culumn == "ID":
                continue
            else:
                edited_culumns.append(culumn + "=?")
        culumns = ",".join(edited_culumns)
        # print("-------------edited_culumns--------------Line 554", edited_culumns)

        # ====================ΕΠΙΛΕΓΜΈΝΟ ID =================
        selected_item = tree.selection()
        selected_id = tree.set(selected_item, "#1")
        # print("==========selected_id==========LINE 469 \n", selected_id)

        # Θα βάζει το data_to_add απο πάνω γραμμη 371
        # βαζουμε και το id που χρειάζεται για το WHERE ID=?
        edited_data = []

        for data in data_to_add:
            type_of_data = str(type(data))
            # Ελεγχος εάν είναι scrolledtext τοτε η προσθήκη θελει (data.get('1.0', 'end-1c') και οχι σκετο data.get()
            # το '1.0' το 1 είναι η πρώτη γραμμή  το 0 είναι ο πρώτος χαρακτήρας
            if "scrolledtext" in type_of_data:
                edited_data.append(data.get('1.0', 'end-1c'))
            else:
                edited_data.append(data.get())

        # ================================ Προσθήκη τελευταίας τροποποιησης ============================
        # edited_data[-1] ==>> Ειναι η ΠΑΡΑΤΗΡΗΣΗΣ
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        # Aν ο πίνακας εχει περισσοτερα απο 7 κεφαλίδες τότε στο "ΠΑΡΑΤΗΡΗΣΕΙΣ" να βάλει μόνο ημερωμηνία και χρήστη
        if table == "Ω_ΠΑΡΑΓΓΕΛΙΕΣ":
            edited_data[-1] = data_to_add[-1].get()
        elif len(edited_culumns) > 7:
            edited_data[-1] = now + " " + user
        # Διαφορετικά να βάλει και ότι γράφει ο χρήστης
        else:
            edited_data[-1] = now + " " + user + " ==>> " + data_to_add[-1].get()
        # print("Line 772", edited_data[-1][0:-1])
        # ================================= Προσθήκη id =================================================
        edited_data.append(selected_id)
        # print("Line 573 Edited data ", edited_data)
        # ====================================== ΑΥΤΟΜΑΤΗ ΕΝΗΜΕΡΩΣΗ ΣΥΝΟΛΟΥ =============================
        # ======================================= ΚΑΙ ΠΡΟΣΘΗΚΗ ΣΥΜΒΟΛΟΥ €    =============================
        if "ΣΥΝΟΛΟ=?" in edited_culumns:
            try:
                # edited_data[6] == τιμή
                edited_data[edited_culumns.index("ΤΙΜΗ=?")] = \
                    edited_data[edited_culumns.index("ΤΙΜΗ=?")].replace(",", ".")  # Μετατροπή , σε . για πολλαπλασιασμό

                # Αν ο χρήστης δεν βάλει τεμάχειο να γίνει αυτόματα 0
                if edited_data[edited_culumns.index("ΤΕΜΑΧΙΑ=?")] == "":
                    edited_data[edited_culumns.index("ΤΕΜΑΧΙΑ=?")] = "0"
                    # print("Line 604 edited_data[5] ", edited_data[5])

                else:
                    pass
                # Αν ο χρήστης δεν ορίσει τιμή να γίνει αυτόματα 0
                if edited_data[edited_culumns.index("ΤΙΜΗ=?")] == "":
                    edited_data[edited_culumns.index("ΤΙΜΗ=?")] = "0"  # 0 σε string γιατί ψάχνουμε αν έχει το € μέσα
                    # print("Line 610 edited_data[6] ", edited_data[6])

                else:
                    pass
                # {:0.2f} Για να εμφανίνζει την τιμή με 2 δεκαδικά πίσω απο την τιμή 10.00 € και οχι 10 €

                if "€" in edited_data[edited_culumns.index("ΤΙΜΗ=?")]:
                    edited_data[edited_culumns.index("ΣΥΝΟΛΟ=?")] = \
                        str("{:0.2f}".format(float(edited_data[edited_culumns.index("ΤΙΜΗ=?")][:-1]) *
                                             float(edited_data[edited_culumns.index("ΤΕΜΑΧΙΑ=?")]))) + " €"
                    edited_data[edited_culumns.index("ΤΕΜΑΧΙΑ=?")] = str(edited_data[edited_culumns.index("ΤΕΜΑΧΙΑ=?")])

                else:
                    edited_data[edited_culumns.index("ΣΥΝΟΛΟ=?")] = \
                        str("{:0.2f}".format(float(edited_data[edited_culumns.index("ΤΙΜΗ=?")]) *
                                             float(edited_data[edited_culumns.index("ΤΕΜΑΧΙΑ=?")]))) + " €"
                    edited_data[edited_culumns.index("ΤΕΜΑΧΙΑ=?")] = str(edited_data[edited_culumns.index("ΤΕΜΑΧΙΑ=?")])

                if "€" not in str(edited_data[edited_culumns.index("ΤΙΜΗ=?")]):
                    edited_data[edited_culumns.index("ΤΙΜΗ=?")] = \
                        str("{:0.2f}".format(float(edited_data[edited_culumns.index("ΤΙΜΗ=?")]))) + " €"

                else:
                    edited_data[edited_culumns.index("ΤΙΜΗ=?")] = \
                        str("{:0.2f}".format(float(edited_data[edited_culumns.index("ΤΙΜΗ=?")][:-1]))) + " €"

            except ValueError as error:
                messagebox.showwarning('ΠΡΟΣΟΧΉ ...',
                                       "Σφάλμα {} \n1)Ο Πίνακας δεν είναι σωστός".format(error))
                print("Line 827 Σφάλμα {} \n1)Ο Πίνακας δεν είναι σωστός".format(error))

                edit_window.destroy()
                return None
        else:
            pass
        # print("Γραμμη 491:  ----------- ΕΠΕΞΕΡΓΑΣΜΈΝΑ ΔΕΔΟΜΈΝΑ------------", tuple(edited_data))
        # H ΣΥΝΤΑΞΗ ΕΙΝΑΙ ΑΥΤΉ
        # sql_insert = "INSERT INTO  " + table + "(" + culumns + ")" + "VALUES(NULL, ?, ?, ?, ?, ?, ?, ?);"
        # sqlite_update_query = """Update new_developers set salary = ?, email = ? where id = ?"""
        edit_cursor.execute("UPDATE " + table + "  SET " + culumns + " WHERE ID=? ", (tuple(edited_data)))

        edit_conn.commit()
        print(60 * "*")
        print(50 * "*", "Το προΐον ενημερώθηκε με επιτυχία", 50 * "*")
        print(60 * "*")
        print("Γραμμη 701 Παλιά δεδομένα στον πίνακα ==> {}".format(table), "\n", headers, "\n", selected_data)
        print("Γραμμη 702 Νέα δεδομένα στον πίνακα ==>{}".format(table), "\n", headers[1:], "\n", edited_data[:-1])

        # Ενημέρωση του tree με τα νέα δεδομένα

        update_view(root, table)
        edit_window.destroy()
        # print("Γραμμη 510: Εγινε η Ενημέρωση του tree ")
        # print(data_to_add)

        # ΕΞΩΔΟΣ

    def quit_app(event):

        edit_window.destroy()

    edit_window.bind('<Escape>', quit_app)
    update_button = Button(edit_window, command=update_to_db, text="Ενημέρωση προϊόντος", bg="red",
                           fg="white", bd=3)
    update_button.grid(column=0, row=len(headers) + 1)

    # print("Line 909 data to orders", selected_data)
    if table != tables[-1]:
        order_button = Button(edit_window, command=lambda: add_to_orders(edit_window, selected_data),
                              text="Προσθήκη στις παραγγελίες", bg="blue", fg="white", bd=3)
        order_button.grid(column=3, row=len(headers) + 1)


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
        # print("============BACKUP FILE===========Line 542=\n", backup_file, "\n")
        if not os.path.exists(back_dir):
            os.makedirs(back_dir)
        else:
            pass
        # Υπάρχουσα βάση
        conn = sqlite3.connect(dbase)
        print("===========Υπάρχουσα βάση===========Line 744\n ", dbase, "\n")

        # Δημιουργία νέας βάσης και αντίγραφο ασφαλείας
        back_conn = sqlite3.connect(backup_file)
        with back_conn:
            conn.backup(back_conn, pages=10, progress=progress)
            back_conn.close()
            text = "Η βάση αντιγράφηκε :  "
            result = text + os.path.realpath(backup_file)
            # print("=====Αποτέλεσμα ====Line 558\n", result)
            # Ειναι ενοχλητικο να εμφανιζει καθε φορα μηνυμα οτι εγινε backup
            # tkinter.messagebox.showinfo('Αποτέλεσμα αντιγράφου ασφαλείας', result)
    except FileNotFoundError as file_error:
        messagebox.showwarning("Σφάλμα...", "{}".format(file_error))
        print("File Error Line 710", file_error)
        backup()
    except sqlite3.Error as error:
        if not os.path.exists(backup_file):
            result = "Σφάλμα κατα την αντιγραφή : ", error
            messagebox.showwarning("Σφάλμα...", "{}".format(result))
    finally:
        try:
            if back_conn:
                back_conn.close()
                print("Δημηουργεία αντιγράφου ασφαλείας στο αρχείο  ", backup_file, " ολοκληρώθηκε")
        except UnboundLocalError as error:
            print(f"Η σύνδεση με {backup_file} δεν έγινε ποτέ Line 562 {error}")
            messagebox.showinfo(f"Η σύνδεση με {backup_file} δεν έγινε ποτέ Line 771 {error}")


# ================================Συνάρτηση για διαγραφή  =================

def del_from_tree():
    global dbase, tree
    print("Γραμμή 778: ---------------ΛΟΓΟΣ BACKUP --->>> ΔΙΑΓΡΑΦΗ ΔΕΔΟΜΕΝΩΝ ------------------------- ")
    backup()
    selected_item = (tree.set(tree.selection(), '#1'))

    del_conn = sqlite3.connect(dbase)
    del_cursor = del_conn.cursor()
    del_cursor.execute("SELECT * FROM " + table + " WHERE ID = ?", (selected_item,))
    selected_data = del_cursor.fetchall()
    selected_data = list(selected_data[0])
    print("Γραμμη 787: Επιλεγμένα για διαγραφή δεδομένα -->>", headers, selected_data)

    # ======================ΕΠΙΒΕΒΑΙΩΣΗ ΔΙΑΓΡΑΦΗΣ============
    answer = messagebox.askquestion("Θα πραγματοποιηθεί διαγραφή!",
                                    " Είστε σήγουρος για την διαγραφή του {};".format(selected_data), icon='warning')
    # print('Γραμμή 792: =============ΔΙΑΓΡΑΦΗ===============', "Το {} επιλέχθηκε για διαγαφή !".format(selected_data))
    if answer == 'yes':
        messagebox.showwarning('Διαγραφή...', "Το {} διαγράφηκε!".format(selected_data))
        # Αν ο χρήστης επιλεξει το "yes" παει στην γραμμή 804 ==>> del_cursor.execute("DEL............

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
    print("Γραμμη 789:===============ΠΡΑΓΜΑΤΟΠΟΙΗΘΗΚΕ ΔΙΑΓΡΑΦΉ ΤΟΥ===============\n", headers, selected_data)
    print()

    try:
        tree.delete(tree.selection())
        # print("=============================ΕΓΙΝΕ ΔΙΑΓΡΑΦΗ ΑΠΟ ΤΟ TREE====================================line 600 ")
        return selected_item
    except TclError as error:
        print("ΣΦΑΛΜΑ Line 816", error)
