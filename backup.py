#  -*- coding: utf-8 -*-
from datetime import datetime
import os
from tkinter import Tk, ttk, messagebox
from tkinter.ttk import Progressbar
import time
import sqlite3


def backup(dbase):

    root = Tk()
    root.geometry("350x150+50+50")
    root.title("Backup")
    backup_label = ttk.Label(root, text="Αντίγραφο ασφαλείας")
    backup_label.pack()
    # Progress bar widget

    progress = Progressbar(root, orient='horizontal', length=100, mode='determinate')
    progress["maximum"] = 100
    progress.pack(pady=10)
    # Function responsible for the updation
    # of the progress bar value
    progress.start()
    progress['value'] = 25
    progress.update()

    def progress_to_file(status, remainig, total):
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
        progress['value'] = 50
        progress.update()
        print("===========Υπάρχουσα βάση===========Line 744\n ", dbase, "\n")

        # Δημιουργία νέας βάσης και αντίγραφο ασφαλείας
        back_conn = sqlite3.connect(backup_file)
        progress['value'] = 75
        progress.update()
        with back_conn:
            conn.backup(back_conn, pages=10, progress=progress_to_file)
            back_conn.close()
            text = "Η βάση αντιγράφηκε :  "
            result = text + os.path.realpath(backup_file)
            progress['value'] = 100
            progress.update()
            progress.stop()
            # print("=====Αποτέλεσμα ====Line 558\n", result)
            # Ειναι ενοχλητικο να εμφανιζει καθε φορα μηνυμα οτι εγινε backup
            messagebox.showinfo('Αποτέλεσμα αντιγράφου ασφαλείας', result)
            root.destroy()
    except FileNotFoundError as file_error:
        messagebox.showwarning("Σφάλμα...", "{}".format(file_error))
        print("File Error Line 641", file_error)

    except sqlite3.Error as error:
        if not os.path.exists(backup_file):
            result = "Σφάλμα κατα την αντιγραφή : ", error
            messagebox.showwarning("Σφάλμα...", "{}".format(result))
    finally:
        try:
            if back_conn:
                back_conn.close()
                print("Δημιουργία αντιγράφου ασφαλείας στο αρχείο  ", backup_file, " ολοκληρώθηκε")
        except UnboundLocalError as error:
            print(f"Η σύνδεση με {backup_file} δεν έγινε ποτέ Line 1074 {error}")
            messagebox.showinfo(f"Η σύνδεση με {backup_file} δεν έγινε ποτέ Line 1075 {error}")
            





