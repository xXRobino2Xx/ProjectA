import random
from tkinter import *
from datetime import date, datetime
from tkinter.messagebox import showinfo
import psycopg2
import time
from tkinter import ttk
from tkinter.ttk import Combobox

def clicked():
    global con
    namen = naam.get()
    berichten = bericht.get()
    print(namen, berichten)

    if len(namen) == 0:
        namen = 'Anoniem'
    if len(berichten) > 140:  # Input van gebruiker is te lang
        showinfo(title='popup', message="Uw bericht is te lang!")
    elif len(berichten) <= 0:  # Input van gebruiker is te kort
        showinfo(title='popup', message="Uw bericht is te kort!")
    else:  # input van gebruiker is goed\
        showinfo(title='popup', message="Uw bericht is verzonden en wordt beoordeeld!")

        datum = date.today()
        t = time.localtime()
        tijd= time.strftime("%H:%M:%S", t)

        stationenlijst = (
'Arnhem',
'Almere',
'Amersfoort',
'Almelo',
'Alkmaar',
'Apeldoorn',
'Assen',
'Amsterdam',
'Boxtel',
'Breda',
'Dordrecht',
'Delft',
'Deventer',
'Enschede',
'Gouda',
'Groningen',
'Den Haag',
'Hengelo',
'Haarlem',
'Helmond',
'Hoorn',
'Heerlen',
'Den Bosch',
'Hilversum',
'Leiden',
'Lelystad',
'Leeuwarden',
'Maastricht',
'Nijmegen',
'Oss',
'Roermond',
'Roosendaal',
'Sittard',
'Tilburg',
'Utrecht',
'Venlo',
'Vlissingen',
'Zaandam',
'Zwolle',
'Zutphen',
)
        stations = random.choice(stationenlijst)

        con = psycopg2.connect(
            host='localhost',  # De host waarop je database runt
            database='nszuil',  # Database naam
            user='postgres',  # Als wat voor gebruiker je connect, standaard postgres als je niets veranderd
            password='4+sgX3492ZT'  # Wachtwoord die je opgaf bij installatie
            # port=5432 runt standaard op deze port en is alleen nodig als je de port handmatig veranderd
        )

    cur = con.cursor()

    cur.execute("INSERT INTO bericht (bericht, date, naam, station_city, time) VALUES (%s, %s, %s, %s, %s)",
            (berichten, datum, namen, stations, tijd))
    con.commit()
    # Cursor en connectie sluiten (en committen)
    cur.close()
    con.close()

    naam.delete(0, END)
    bericht.delete(0, END)

hoofdscherm = Tk()
hoofdscherm.title("Ns zuil")
hoofdscherm.geometry("950x600")
hoofdscherm.config(bg='gold')
nsLogo = Label(master=hoofdscherm,
              text='Feedback scherm',
              background='#222373',
              foreground='#FEFFF7',
              font=('Helvetica', 16, 'bold italic'),
              width=74,
              height=3)
nsLogo.pack()

labelNaam = Label(master=hoofdscherm,
                    text='Voer hier uw naam in of laat leeg voor Anoniem',
                    foreground='#222373',
                    font=('Helvetica',12, 'bold italic'))
labelNaam.place(x=150, y=220)

naam = Entry(master=hoofdscherm)
naam.place(x=150, y=245, width=650, height=30)


labelBericht = Label(master=hoofdscherm,
                    text='Graag ontvagen wij uw feedback op de NS, laat hieronder een bericht achter. (Max. 140 charaters)',
                    foreground='#222373',
                    font=('Helvetica',12, 'bold italic'))
labelBericht.place(x=150, y=85)

bericht = Entry(master=hoofdscherm, width=50)
bericht.place(x=150, y=110, width=650, height=100)

button = Button(master=hoofdscherm, text='Verzend',background='#222373', foreground='#FEFFF7', command=clicked)
button.place(x=425, y=285, width=100)

hoofdscherm.mainloop()