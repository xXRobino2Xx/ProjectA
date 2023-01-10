from datetime import date
from tkinter import *
from tkinter.messagebox import showinfo
from tkinter.ttk import Combobox
import psycopg2
import time


#In elke stationshal van Nederland komt een stationshalscherm te hangen.
#Op dit scherm worden de geplaatste berichten uit heel Nederland getoond:


#De berichten worden getoond op chronologische volgorde van invoeren.
#Alleen de laatste 5 berichten worden getoond.
#Ook worden de beschikbare faciliteiten op het station getoond op het scherm.
# Het gaat hierbij om het station waar het bericht is geschreven.
# Een station heeft één of meer van de volgende faciliteiten: OV-fietsen, lift, toilet en P+R.
# De beschikbare faciliteiten staan in deze tabeltabel downloaden, deze moet je toevoegen aan je database.
# Je kunt eventueel gebruik maken van deze iconeniconen downloaden.

#Ten slotte wordt op het stationshalscherm de weersvoorspelling op de locatie van het station getoond.
# Het gaat hierbij om het station waar het stationshalscherm hangt.
# Voor het ophalen van de weersvoorspelling maak je gebruik van de OpenWeatherMap API (https://openweathermap.org/Koppelingen naar een externe site.).
#Het is belangrijk dat het stationshalscherm er goed uitziet,
#dus deze module werkt met een Graphical User Interface (GUI), in principe met behulp van Tkinter.
#Zorg dat je bij het starten van dit stationsscherm kunt kiezen voor één van de stations die jij gekozen hebt in module 1.

# -----------------------------------------------------

con = psycopg2.connect(
    host='localhost',  # De host waarop je database runt
    database='nszuil',  # Database naam
    user='postgres',  # Als wat voor gebruiker je connect, standaard postgres als je niets veranderd
    password='4+sgX3492ZT'  # Wachtwoord die je opgaf bij installatie
    # port=5432 runt standaard op deze port en is alleen nodig als je de port handmatig veranderd
)
cur = con.cursor()
cur.execute("select bericht.tekst, bericht.naam,  bericht.station_city, bericht.id from bericht INNER JOIN beoordeling ON bericht.beoordelingid = beoordeling.beoordelingid where goedkeuring is true ORDER BY id DESC limit 5")
rows = cur.fetchall()

for row in rows:
    print(row)
con.commit()
#Cursor en connectie sluiten (en committen)
cur.close()

cur = con.cursor()
cur.execute("select station_service.station_city, station_service.ov_bike, station_service.elevator, station_service.toilet, station_service.park_and_ride from station_service INNER JOIN bericht ON station_service.station_city = bericht.station_city")
rows = cur.fetchall()

for row in rows:
    station_stad = row[0]
    ov_fiets = row[1]
    lift = row[2]
    toilet = row[3]
    park_and_ride = row[4]

    if ov_fiets == True:
        ov_fiets = "Er is een ov fiets aanwezig"
    if lift == True:
        lift = "Er is een lift aanwezig"
    if toilet == True:
        toilet = "Er is een toilet aanwezig"
    if park_and_ride == True:
        park_and_ride = "Er is een P&R aanwezig"
    print(station_stad, '\n', ov_fiets, '\n', lift, '\n', toilet, '\n', park_and_ride)
    print('<br>')

con.commit()
cur.close()

con.close()

base_url = "http://api.openweathermap.org/data/2.5/weather?"
city_name = station
complete_url = base_url + "appid=" + api_key + "&q=" + city_name + '&units=metric' + '&lang=nl'
response = requests.get(complete_url)
x = response.json()
y = x["main"]
current_temperature = y["temp"]
feelslike_temperature = y["feels_like"]
min_temperature = str(y["temp_min"])
max_temperature = str(y["temp_max"])
current_pressure = str(y["pressure"])
current_humidity = str(y["humidity"])
z = x["weather"]
weather_description = z[0]["description"]