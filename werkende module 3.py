from tkinter.ttk import Combobox
import psycopg2
from tkinter import *
import row as row
import requests

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
    bericht = row[1]

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
    else:
        ov_fiets = "Er is GEEN ov fiets aanwezig"
    if lift == True:
        lift = "Er is een lift aanwezig"
    else:
        lift= 'Er is GEEN lift aanwezig'
    if toilet == True:
        toilet = "Er is een toilet aanwezig"
    else:
        toilet = "Er is GEEN toilet aanwezig"
    if park_and_ride == True:
        park_and_ride = "Er is een P&R aanwezig"
    else:
        park_and_ride = "Er is GEEN P&R aanwezig"
    print(station_stad, '\n', ov_fiets, '\n', lift, '\n', toilet, '\n', park_and_ride)
    print('<br>')

con.commit()
cur.close()

#weather api en opvragen
base_url = "http://api.openweathermap.org/data/2.5/weather?"
city_name = station_stad
api_key = 'a2f6b3a51ff89a649eb0f7a600b9e84a'
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

def show_weather():
    print("Weersvoorspelling voor", station_stad, '\n',
          "Huidige temperatuur is", current_temperature, "graden Celsius", '\n',
          "Gevoelstemperatuur is", feelslike_temperature, "graden Celsius", '\n',
          "Minimum temperatuur is", min_temperature, "graden Celsius", '\n',
          "Maximum temperatuur is", max_temperature, "graden Celsius", '\n',
          "Huidige druk is", current_pressure, "hPa", '\n',
          "Huidige luchtvochtigheid is", current_humidity, "%", '\n',
          "Weersbeschrijving is:", weather_description, '\n')

def show_last_messages():
    print("Laatste 5 berichten:")
    for row in rows:
        print(row[0], "-", row[1], "-", row[2], "-", row[3])
        print('<br>')


# Hier begint de GUI

root = Tk()
root.title("NS Zuil")
root.geometry("450x550+200+200")
root.configure(background="gold")

# Berichten
message_label = Label(root, text="Naam + Bericht:", background='#222373', foreground='#FEFFF7',font=('Helvetica',12, 'bold italic'))
message_label.grid(row=1, column=0, padx=10, pady=10)

message_listbox = Listbox(root, width=35, height=5, borderwidth=3, relief="sunken")
message_listbox.grid(row=1, column=1, padx=10, pady=10, columnspan=2)

# Weer
weather_label = Label(root, text="Weersvoorspelling:", background='#222373', foreground='#FEFFF7',font=('Helvetica',12, 'bold italic'))
weather_label.grid(row=4, column=0, padx=10, pady=10)

weather_listbox = Listbox(root, width=30, height=11, borderwidth=3, relief="sunken")
weather_listbox.grid(row=4, column=1, padx=10, pady=10, columnspan=2)

# Faciliteiten
facilities_label = Label(root, text="Faciliteiten:", background='#222373', foreground='#FEFFF7',font=('Helvetica',12, 'bold italic'))
facilities_label.grid(row=3, column=0, padx=10, pady=10)

facilities_listbox = Listbox(root, width=25, height=5, borderwidth=3, relief="sunken")
facilities_listbox.grid(row=3, column=1, padx=10, pady=10, columnspan=2)

# Station
station_label = Label(root, text="Stations:", background='#222373', foreground='#FEFFF7', font=('Helvetica',12, 'bold italic'))
station_label.grid(row=2, column=0, padx=10, pady=10)

station_listbox = Listbox(root, width=20, height=5, borderwidth=3, relief="sunken")
station_listbox.grid(row=2, column=1, padx=10, pady=10, columnspan=2)
cur = con.cursor()
cur.execute("select bericht.tekst, bericht.naam,  bericht.station_city, bericht.id from bericht INNER JOIN beoordeling ON bericht.beoordelingid = beoordeling.beoordelingid where goedkeuring is true ORDER BY id DESC limit 5")
rows = cur.fetchall()

for row in rows:
    bericht = row[0]
    bericht_titel = row[1]
    bericht_stad = row[2]
    #print(row[0], row[1], row[2])
    #print(row)
    message_listbox.insert(0, row[1] + "-" + row[0]) #voeg bericht toe aan message_listbox

for station_stad in rows:

    station_listbox.insert(0, station_stad[2])  # voeg station toe aan station_combobox

con.commit()
#Cursor en connectie sluiten (en committen)
cur.close()
con.close()
#message_listbox.insert(0, row[0], row[1]) #voeg bericht toe aan message_listbox
weather_listbox.insert(0, "Dit gaat over " + city_name, "Huidige temperatuur is", current_temperature, "Gevoelstemperatuur is", feelslike_temperature, "Minimum temperatuur is", min_temperature, "Maximum temperatuur is", max_temperature, "Weersbeschrijving is: " + weather_description) #voeg weersbeschrijving toe aan weather_listbox
facilities_listbox.insert(0,"Dit gaat over " + city_name, ov_fiets, lift, toilet, park_and_ride) #voeg ov fiets toe aan facilities_listbox
#station_combobox.insert(0, station_stad) #voeg station toe aan station_combobox
# Buttons
quit_button = Button(root, text="Sluiten", command=root.quit, background='#222373', foreground='#FEFFF7', font=('Helvetica',12, 'bold italic'))
quit_button.grid(row=5, column=2, padx=10, pady=10)



root.mainloop()