# coding=utf-8
"""
Sqlite Γραφικό περιβάλλον με Python3
******************************************************************
************** ΔΕΝ ΔΗΜΗΟΥΡΓΕΙ ΒΑΣΗ ΟΥΤΕ ΠΙΝΑΚΕΣ*******************
** Οι βάσεις πρέπει να έχουν Id ή id ή ID intiger και NOT NULL  **
******************************************************************

Version V1.0.3   | Δημιουργία πίνακα απο τον χρήστη και δυνατότητα ανοίγματος άλλης βάσης δεδομένων  | -----28/11/2019


Version V0.9.1   | Dynamic screen sizes |  | Cleaned code | ------------17/11/2019

Version v0.8 + Log File added Για το μαγαζί δουλευουν ολα ----------------------------10/11/2019
Στην v0.7  έφτιαχνε συνεχεια frames στο root
ΕΓΙΝΕ ΚΑΘΑΡΣΙΣΜΟΣ ΚΩΔΙΚΑ
ΠΡΕΠΕΙ ΝΑ ΚΑΝΩ ΤΟ ΣΥΝΟΛΟ = TIMI * TEMAXIA


Version v0.7 Για το μαγαζί δουλευουν ολα ----------------------------9/11/2019
ΠΡΕΠΕΙ ΝΑ ΚΑΝΩ ΤΟ ΣΥΝΟΛΟ = TIMI * TEMAXIA

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

TODO LIST  8) Να βάλω triggers
TODO LIST  9) Να βάλω στο μενοu RUN SQL
"""

from func import *

root = Tk()
root.geometry('800x600+100+100')
root.title('ML ΑΠΟΘΗΚΗ V 1.0.4')
root.config(bg="#C2C0BD")
# root.withdraw()  # hide root
root.resizable(True, True)
# width = 1200
# height = 600
# screen_width = root.winfo_screenwidth()
# screen_height = root.winfo_screenheight()
# x = (screen_width / 2) - (width / 2)
# y = (screen_height / 2) - (height / 2)
# root.geometry("%dx%d+%d+%d" % (width, height, x, y))


# ------------------------Style------------------------------------
def fixed_map(option):
    # Fix for setting text colour for Tkinter 8.6.9
    # From: https://core.tcl.tk/tk/info/509cafafae
    #
    # Returns the style map for 'option' with any styles starting with
    # ('!disabled', '!selected', ...) filtered out.

    # style.map() returns an empty list for missing options, so this
    # should be future-safe.
    return [elm for elm in style.map('Treeview', query_opt=option) if elm[:2] != ('!disabled', '!selected')]


width_of_tree = root.winfo_screenwidth()
style = ttk.Style()
# style.theme_names()-->> ('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative')
style.theme_use('vista')
# # # Modify the font of the body
style.theme_create("mystyle.Treeview", parent="vista")
# style.configure("mystyle.Treeview.Heading", background="gray", foreground="white", relief="flat")
style.map('mystyle.Treeview', foreground=fixed_map('foreground'), background=fixed_map('background'))

# ==================================== Εμφάνηση δεδομένων ==============================================
style.configure("mystyle.Treeview", highlightthickness=0, width=width_of_tree-100, font=('San Serif', 11))
# style.configure('W.TButton', font=('calibri', 10, 'bold', 'underline'), foreground='red')

# "map": {"background": [("selected", myred)],"expand": [("selected", [1, 1, 1, 0])]}
# fieldbackground="black"
style.configure("mystyle.Treeview.Heading", font=('San Serif', 12, 'bold'),  background="#657b83", foreground="black",
                relief=[('active', 'groove'), ('pressed', 'sunken')])  # Modify the font of the headings
# style.layout("mystyle.Treeview", [('mystyle.Treeview.treearea', {'sticky': 'nswe'})])  # Remove the borders
style.configure("mystyle.Treeview", background="white", rowheight=round(width_of_tree / 40))
# style.configure("mystyle.Treeview", background="#850664", foreground="#000000", fieldbackground="#FFFFFF")
# style.theme_use("mystyle.Treeview")
#         # -------------------------New Style--------------------------------
# style1 = ttk.Style()
# mygreen = "gray"
# myred = "green"
# Styles - normal, bold, roman, italic, underline, and overstrike.
# style.theme_create("mystyle.Treeview", parent="alt", settings={
#         "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0]}},
#         "Treeview": {"configure": {"font": ['San Serif', 13, "normal"]}, "rowhight": 50, "highlightthickness": 10,
#         "background": [("selected", myred)]},
#         "Treeview.treearea": {"configure": {'sticky': 'nswe'}},
#         "Treeview.Heading": {"configure": {"font": ['San Serif', 11, 'bold']}, "background": "red",
#                             "foreground": "white", "relief": "flat"},
#         "TNotebook.Tab": {
#             "configure": {"padding": [50, 1], "background": mygreen, "foreground": "white"},
#             "map": {"background": [("selected", myred)],
#                     "expand": [("selected", [1, 1, 1, 0])]}}})
#
# style.theme_use("mystyle.Treeview")


# Τίτλος προγράμματος
app_title = Label(root, bg="brown", fg="white", text="ML ΑΠΟΘΗΚΗ v1.0.4 ", font=("San Serif", 15), bd=8)
# app_title.grid(column=0, row=0, sticky="we")

# ---------------------binds------------------------------
# #ΑΝΑΝΕΩΣΗ
# def reset_event(event):
#
#     update_view(root)
#
# #Δεν χρειάζεται γιατι πρέπει να στέλνω και πινακα στο update_view
# root.bind('<F5>', reset_event)


# ΕΞΩΔΟΣ
def exit_event(event):
    if messagebox.askokcancel("Εξωδος", "Θέλετε πραγματικά να εγκαταλείψετε;"):
        root.destroy()


root.bind('<Escape>', exit_event)


# ΠΡΟΣΘΗΚΗ
def add_event(event):

    add_to(root)


root.bind('<F1>', add_event)


# ΕΠΕΞΕΡΓΑΣΙΑ
def edit_event(event):

    edit(root)


root.bind('<F3>', edit_event)

# --------------------------------------   MENU   -----------------------------------------
menubar = Menu(root)

filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Ανοιγμα αρχείου", command=lambda: open_file(root))

filemenu.add_command(label="Προσθήκη --> F1", command=lambda: add_to(root))
filemenu.add_command(label="Επεξεργασία --> F3", command=lambda: edit(root))
filemenu.add_separator()
filemenu.add_command(label="Διαγραφή", command=del_from_tree)
filemenu.add_command(label="Εξωδος --> Esc", command=root.quit)
menubar.add_cascade(label="Αρχείο", menu=filemenu)

backup_menu = Menu(menubar, tearoff=0)
backup_menu.add_command(label="===Αντίγραφο ασφαλείας!===", command=backup)
menubar.add_cascade(label="Αντίγραφο ασφαλείας", menu=backup_menu)

table_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Πίνακες", menu=table_menu)
table_menu.add_command(label="Δημιουργία νέου πίνακα", command=lambda: make_new_table(root))

info_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Info", menu=info_menu)
info_menu.add_command(label="Πληροφορίες", command=get_info)


root.config(menu=menubar)

get_tables()
select_table(root)
if __name__ == "__main__":
    root.mainloop()
