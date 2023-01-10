from datetime import date
from tkinter import *
from tkinter.messagebox import showinfo
from tkinter.ttk import Combobox
import psycopg2
import time

# code voor functies
datum = date.today()
t = time.localtime()
tijdstip = time.strftime("%H:%M:%S", t)


def accept():
    modnaam = comboExample.get()
    modopmerking = opmerking.get('1.0', END)
    if modnaam == '':
        showinfo(title='Error', message="Selecteer moderator")
    else:
        con = psycopg2.connect(
            host='localhost',  # De host waarop je database runt
            database='nszuil',  # Database naam
            user='postgres',  # Als wat voor gebruiker je connect, standaard postgres als je niets veranderd
            password='4+sgX3492ZT'  # Wachtwoord die je opgaf bij installatie
            # port=5432 runt standaard op deze port en is alleen nodig als je de port handmatig veranderd
        )
        cur = con.cursor()
        cur.execute(
            "SELECT id FROM moderator WHERE moderatornaam = (%s)", (modnaam,))
        modID = (cur.fetchone()[0])
        cur.execute(
            "INSERT INTO beoordeling (goedkeuring, datum, tijd, moderatorid, opmerking) VALUES (%s, %s, %s, %s, %s)",
            (True, datum, tijdstip, modID, modopmerking))
        con.commit()
        cur.execute(
            "SELECT beoordelingid FROM beoordeling WHERE goedkeuring = (%s) AND datum = (%s) AND tijd = (%s) AND moderatorid = (%s) AND opmerking = (%s)",
            (True, datum, tijdstip, modID, modopmerking))
        beoordelingID = (cur.fetchone()[0])
        cur.execute(
            "UPDATE bericht SET beoordelingid = (%s) WHERE bericht.id = (%s)", (beoordelingID, berichtid)
        )
        con.commit()


        showinfo(title='Melding', message="Bericht is succesvol, en wordt geaccepteerd\nVolgend bericht wordt nu getoond")
        opmerking.delete('1.0', END)
        nieuwbericht()

        cur.close()
        con.close()


def reject():
    modnaam = comboExample.get()
    modopmerking = opmerking.get('1.0', END)
    if modnaam == '':
        showinfo(title='Error', message="Selecteer een moderator")
    elif len(modopmerking) <= 1:
        showinfo(title='Error', message="Reden geven voor afkeuren bericht")
    else:
        con = psycopg2.connect(
            host='localhost',  # De host waarop je database runt
            database='nszuil',  # Database naam
            user='postgres',  # Als wat voor gebruiker je connect, standaard postgres als je niets veranderd
            password='4+sgX3492ZT'  # Wachtwoord die je opgaf bij installatie
            # port=5432 runt standaard op deze port en is alleen nodig als je de port handmatig veranderd
        )
        cur = con.cursor()
        cur.execute(
            "SELECT id FROM moderator WHERE moderatornaam = (%s)", (modnaam,))
        modID = (cur.fetchone()[0])
        cur.execute(
            "INSERT INTO beoordeling (goedkeuring, datum, tijd, moderatorid, opmerking) VALUES (%s, %s, %s, %s, %s)",
            (False, datum, tijdstip, modID, modopmerking))
        con.commit()
        cur.execute(
            "SELECT beoordelingid FROM beoordeling WHERE goedkeuring = (%s) AND datum = (%s) AND tijd = (%s) AND moderatorid = (%s) AND opmerking = (%s)",
            (False, datum, tijdstip, modID, modopmerking))
        beoordelingID = (cur.fetchone()[0])
        cur.execute(
            "UPDATE bericht SET beoordelingid = (%s) WHERE bericht.id = (%s)", (beoordelingID, berichtid)
        )
        con.commit()

        showinfo(title='Melding', message="Bericht is succesvol afgewezen\nVolgend bericht wordt nu getoond")
        opmerking.delete('1.0', END)
        nieuwbericht()

        cur.close()
        con.close()


def nieuwbericht():
    global berichtid
    global bericht
    con = psycopg2.connect(
        host='localhost',  # De host waarop je database runt
        database='nszuil',  # Database naam
        user='postgres',  # Als wat voor gebruiker je connect, standaard postgres als je niets veranderd
        password='4+sgX3492ZT'  # Wachtwoord die je opgaf bij installatie
        # port=5432 runt standaard op deze port en is alleen nodig als je de port handmatig veranderd
    )

    cur = con.cursor()
    cur.execute(
        "SELECT bericht.id, bericht.tekst, bericht.naam, bericht.beoordelingid FROM bericht WHERE bericht.beoordelingid IS NULL ORDER BY datum")

    result = cur.fetchone()
    if result:
        naam = result[2]
        bericht = result[1].rstrip()
        berichtid = result[0]
        naamlabel2.config(text=naam)
        berichtlabel2.config(text=bericht)
    else:
        showinfo(title='Melding', message="Alle berichten zijn beoordeeld.\nApp wordt gesloten")

    cur.close()
    con.close()

hoofdscherm = Tk()
hoofdscherm.title("NS Moderator Scherm")
hoofdscherm.geometry("400x400")
hoofdscherm.config(bg='#0000FF')

welkom = Label(hoofdscherm, text="Welkom", font=("NS Sans", 20), bg='#0000FF', fg='#FFFF14')
welkom.grid(column=0, row=0, columnspan=2, sticky=W)

tekst = Label(hoofdscherm, text="Begin met beoordelen", font=("NS Sans", 12), bg='#0000FF', fg='#FFFF14')
tekst.grid(column=0, row=1)

onzichtbaar = Label(hoofdscherm, bg='#0000FF')
onzichtbaar.grid(column=0, row=2)

tekst = Label(hoofdscherm, text="Moderator", font=("NS Sans", 10), bg='#0000FF', fg='#FFFF14')
tekst.grid(column=0, row=3, sticky=W)

comboExample = Combobox(hoofdscherm,
                        values=[
                            "robin",
                            "donald", ], font=("NS Sans", 10), state="readonly")
comboExample.grid(column=1, row=3, sticky=W)

onzichtbaar = Label(hoofdscherm, bg='#0000FF')
onzichtbaar.grid(column=0, row=4)

naamlabel = Label(hoofdscherm, text="Naam reiziger:", font=("NS Sans", 10), bg='#0000FF', fg='#FFFF14')
naamlabel.grid(column=0, row=5, sticky=W)

berichtlabel = Label(hoofdscherm, text="Bericht:", font=("NS Sans", 10), bg='#0000FF', fg='#FFFF14')
berichtlabel.grid(column=0, row=6, sticky=W + N)

opmerkinglabel = Label(hoofdscherm, text="feedback:", font=("NS Sans", 10), bg='#0000FF', fg='#FFFF14')
opmerkinglabel.grid(column=0, row=8, sticky=W + N)

# Hier komt de echte naam te staan
naamlabel2 = Label(hoofdscherm, text='', font=("NS Sans", 10), bg='white', fg='black')
naamlabel2.grid(column=1, row=5, sticky=W, columnspan=2)

# Hier komt het echte bericht te staan
berichtlabel2 = Label(hoofdscherm, text='', font=("NS Sans", 10), bg='white', fg='black',
                      wraplength=180)
berichtlabel2.grid(column=1, row=6, sticky=W)

onzichtbaar = Label(hoofdscherm, bg='#0000FF')
onzichtbaar.grid(column=0, row=7)

# Hier wordt opmerking van de mod opgenomen
opmerking = Text(hoofdscherm, width=20, height=5)
opmerking.grid(column=1, row=8, sticky=W)

onzichtbaar = Label(hoofdscherm, bg='#0000FF')
onzichtbaar.grid(column=0, row=9)

rejectbutton = Button(hoofdscherm, text="Reject", bg='Royalblue2', fg='white', width=8, command=lambda: reject())
rejectbutton.grid(column=1, row=10, sticky=W)

acceptbutton = Button(hoofdscherm, text="Accept", bg='Royalblue2', fg='white', width=8, command=lambda: accept())
acceptbutton.grid(column=1, row=10, sticky=E)


nieuwbericht()
hoofdscherm.mainloop()