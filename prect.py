from operator import index
from sqlite3 import dbapi2
from pathlib import Path
import sqlite3
from prettytable import PrettyTable, from_db_cursor
import datetime
from numpy import datetime_data
from reportlab.pdfgen.canvas import Canvas


DB_FILE = Path(__file__).parent/"Proiect.db"

class Bloc:
    def __init__(self):
        self.meniu()
    def introduceti_bloc(self):
        self.adresa = input("adresa:")
        self.nume_presedinte = input("nume presedinte:")
        with sqlite3.connect(DB_FILE) as connection:
            cursor = connection.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS blocuri
                            (Adresa text,
                            Nume_presedinte text)''')

            cursor.execute("""INSERT INTO blocuri (Adresa, Nume_presedinte) VALUES (?, ?)""",
            (self.adresa, self.nume_presedinte))
            connection.commit()
        self.meniu()
            
                #ADAUGA APARTAMENT
    def introduceti_apartament(self):
        self.nr_apartament = input("nr apartament :")
        self.nume_proprietar = input("nume proprietar :")
        self.nr_locatari = input("nr locatari :")
        self.nr_camere = input("nr camere :")
        self.id_bloc = input("id bloc :")
        with sqlite3.connect(DB_FILE) as connection:
            cursor = connection.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS apartamente
                            (nr_ap integer primary key,
                            nume_proprietar text,
                            nr_locatari integer,
                            nr_camere integer,
                            id_bloc integer)''')

            cursor.execute("""INSERT INTO apartamente (nr_ap, nume_proprietar, nr_locatari, nr_camere, id_bloc)
            VALUES (?, ?, ?, ?, ?)""",
            (self.nr_apartament, self.nume_proprietar, self.nr_locatari, self.nr_camere, self.id_bloc))
            connection.commit()
        self.meniu()

            #EDITEAZA APARTAMENT
    def editeaza_apartament(self):
        self.nume_proprietar = input("nume proprietar: ")
        self.nr_locatari = input("nr locatari: ")
        self.id = input("id: ")
        with sqlite3.connect(DB_FILE) as connection:
            cursor = connection.cursor()
            cursor.execute("""UPDATE apartamente SET nume_proprietar = ?, nr_locatari = ? WHERE Id = ? """,
            (self.nume_proprietar, self.nr_locatari,self.id))
            connection.commit()

        self.meniu()

            #ADAUGA CONTRACT
    def adauga_contract(self):
        self.firma_utilitati = input("firma_utilitati: ")
        self.valoare_luna = int(input("valoare luna: "))
        self.id_bloc = input("id bloc: ")
        with sqlite3.connect(DB_FILE) as connection:
            cursor = connection.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS utilitati/contract
                                        (firma text,
                                        valoare_luna integer,
                                        id_bloc integer)''')

            cursor.execute("""INSERT INTO utilitati/contract (firma, valoare_luna, id_bloc) VALUES (?, ?, ?)""",
            (self.firma_utilitati, self.valoare_luna, self.id_bloc))
            connection.commit()
        self.meniu()

            #ADAUGA INDEX APA RECE
    def adauga_index_apa_rece(self):
        self.ind = input("index: ")
        self.data_citire = str(datetime_data)
        self.alege_blocul = input("alege_blocul: ")
        self.alege_apartament = input("alege_apartament: ")
        with sqlite3.connect(DB_FILE) as connection:
            cursor = connection.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS index_apa_rece
                                        (ind integer,
                                        data_citire text,
                                        alege_blocul integer,
                                        alege_apartament integer)''')

            cursor.execute("""INSERT INTO index_apa_rece 
            (ind, data_citire, alege_blocul, alege_apartament) VALUES (?, ?, ?, ?)""",
            (self.ind,self.data_citire, self.alege_blocul, self.alege_apartament))
            connection.commit()

        self.meniu()

    #MODIFICARE APARTAMENT

    def meniu(self):
        meniu = input("""
        1 Adaugare bloc :
        2 Adaugare apartament :
        3 Editeaza apartament :
        4 Adaugare contract :
        5 Editeaza contract :
        6 Adauga index apa rece :
        7 Print report :
        8 Exit:
        """)
        if meniu == "1":
            self.introduceti_bloc()     
        elif meniu == "2":
            self.introduceti_apartament()
        elif meniu == "3":
            self.editeaza_apartament()
        elif meniu == "4":
            self.adauga_contract() 
        elif meniu == "5":
            self.editeaza contract
        elif meniu == "6":
            self.adauga_index_apa_rece()
        elif meniu == "7":
            self.print_report()
        elif meniu == "8":
            exit()

    def print_report(self):
        with sqlite3.connect(DB_FILE) as connection:
            cursor = connection.cursor()
            cursor.execute('''SELECT 
                                apartamente.nr_ap, 
                                apartamente.nr_locatari,
                                apartamente.nr_camere,
                                index_apa_rece.ind
                            FROM
                                apartamente, index_apa_rece
                            WHERE
                                apartamente.nr_ap = index_apa_rece.alege_apartament''')
            # prt = from_db_cursor(cursor)
            rows = cursor.fetchall()

        # print(prt)
        # print(rows)
        nr_pers, nr_camere, index_total = 0, 0, 0
        nr_apt = len(rows)
        x = PrettyTable()
        x.border = True
        x.field_names = ['apartament', 'Numar persoane', 'Numar camere', 'Index Apa']
        for row in rows:
            nr_pers += row[1]
            nr_camere += row[2]
            index_total += row[-1]
            x.add_row(row)
        blank_row = ('----', '----', '----', '----')
        total_row = ('Total', '', '', '')
        total_data = [nr_apt, nr_pers, nr_camere, index_total]
        x.add_rows([blank_row, total_row, total_data])

        canvas = Canvas('report.pdf', pagesize=(623.0, 792.0))
        t = canvas.beginText(10, 750)
        t.setFont('Helvetica-Oblique', 14)
        lines = str(x).split('\n')
        for line in lines:
            t.textLine(line)
        canvas.drawText(t)
        canvas.showPage()
        canvas.save()
        print(x)

        self.meniu()


b = Bloc()           

class Apartment:
    def __init__(self, id, nr_ap, nume_proprietar, nr_locatari, nr_camere,id_bloc ):
        self.id = id
        self.nr_ap = nr_ap
        self.nume_proprietar = nume_proprietar
        self.nr_locatari = nr_locatari
        self.nr_camere = nr_camere 
        self.id_bloc = id_bloc
        