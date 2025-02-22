from tkinter import *
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import random
import pywhatkit
import pyodbc
import subprocess
from tkinter import messagebox
from textblob import TextBlob 

fe = datetime.datetime.now().strftime('%d-%m-%Y')
def Detener():
    messagebox.showinfo(message="Saliendo del asistente / Proyecto de Innovación", title="Asistente STICH22")
    ventana.destroy()

def Decir(audio):
    engine.say(audio)
    engine.runAndWait()
    
def Saludar():
    
    hour = int(datetime.datetime.now().hour)
    if(hour>=0 and hour<12):
        Decir("Buenos dias!")
    elif(hour>=12 and hour<18):
        Decir("Buenas tardes!")
    else:
        Decir("Buenas noches!")

    Decir("Mi nombre es ALS, en que le puedo ayudar ")
# Initialize speech engine
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[0].id)

# Initialize Wikipedia language
wikipedia.set_lang("es")

# Initialize database connection
server = 'basesitaxd123.database.windows.net'
bd = 'DatabaseSenati'
user = 'carmenwita123'
passw = 'Holaxd123456'
try:
   conexion = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' +
   server+';DATABASE='+bd+';UID='+user+';PWD=' + passw)
   cursor = conexion.cursor()
except Exception as e:
   print("Ocurrió un error al conectar a SQL Server: ", e)

# Initialize Tkinter window
ventana = Tk()
ventana.geometry("600x270")
ventana.title("Asistente virtual del Senati / Proyecto de Innovación 2022")
ventana['bg'] = '#0059b3'

# Labels and Buttons
lbl = Label(ventana, fg="#ffffff", bg="#0059b3", text="Soy Stich22", font=("Arial Bold", 30))
lbl.place(x=10, y=10)

tit = Label(ventana, fg="#ffffff", bg="#0059b3", text="Asistente virtual", font=("Arial Bold", 22))
tit.place(x=300, y=70)

tit1 = Label(ventana, fg="#ffffff", bg="#0059b3", text="del SENATI", font=("Arial Bold", 22))
tit1.place(x=325, y=120)

butini = Button(ventana, fg="#ffffff", bg="#0059b3", text="  Iniciar ", font=("Arial Bold", 16), command=lambda: main("SI", "CONSALUDO"))
butini.place(x=250, y=210)

butdet = Button(ventana, fg="#ffffff", bg="#0059b3", text="   Salir    ", font=("Arial Bold", 16), command=Detener)
butdet.place(x=480, y=210)

# Entry for text input
entry1 = Entry(ventana, width=50)
entry1.pack()

# Function to get the text from Entry widget
def send_text():
    return entry1.get()

# Function to handle text input and process the command
import tkinter as tk
from tkinter import messagebox
import threading
import time

# This function will handle the pop-up dialog and the timer for presence
def preguntar_asistencia(alumno):
    respuesta = None  # To store the user's answer
    
    # Function to run the timer in the background
    def timer():
        nonlocal respuesta
        time.sleep(5)  # Wait for 5 seconds
        if respuesta is None:  # If no answer was given within 5 seconds
            print(f"Tiempo agotado para el alumno {alumno[1]}")
            respuesta = "presente"  # Automatically set to "presente"
            print(f"{alumno[1]} está marcado como presente (por defecto)")

            # Update the database with "presente"
            consulta = "UPDATE tasistencia SET situacion = ? WHERE codalumno = ?"
            id_alumno = alumno[0]
            cursor.execute(consulta, (respuesta, id_alumno))
            cursor.commit()

    # Create a pop-up asking if the student is present
    def mostrar_dialogo():
        nonlocal respuesta
        respuesta = messagebox.askquestion(
            "Asistencia",
            f"¿Está presente {alumno[1]}?",
            icon='question'
        )
        if respuesta == 'yes':
            respuesta = "presente"
        else:
            respuesta = "faltó"

        # Update the database with the answer
        consulta = "UPDATE tasistencia SET situacion = ? WHERE codalumno = ?"
        id_alumno = alumno[0]
        cursor.execute(consulta, (respuesta, id_alumno))
        cursor.commit()

    # Run the timer in a separate thread
    threading.Thread(target=timer, daemon=True).start()

    # Show the dialog to the user
    mostrar_dialogo()

def llamar_asistencia():
    print("===================================")
    print("LLAMANDO ASISTENCIA DEL " + str(fe))
    print("===================================")
    Decir("Llamando asistencia del " + str(fe))
    Decir("Presten atención")

    try:
        cursor.execute("SELECT codalumno, nombres FROM tasistencia;")
        alumnos = cursor.fetchall()
        for alumno in alumnos:
            print(f"{alumno[0]} {alumno[1]}")
            Decir(alumno[1])

            # Ask for the presence using the pop-up dialog and timer
            preguntar_asistencia(alumno)

    except Exception as e:
        print("Ocurrió un error al consultar: ", e)

    finally:
        Decir("Estos son los resultados de la asistencia del día " + str(fe))
        print("RESULTADOS DE LA ASISTENCIA")
        print("============================")
        cursor.execute("SELECT situacion, COUNT(*) as conteo FROM tasistencia GROUP BY situacion WITH ROLLUP;")
        rs = cursor.fetchall()
        for resultado in rs:
            if resultado[0] is None:
                resultado[0] = "TOTAL ASISTENCIA:"
            print(resultado[0].upper() + " " + str(resultado[1]))


def handle_input():
    query = send_text().lower()  # Get the text from the Entry widget
    print(f"Query received: {query}")
    
    if "wikipedia" in query:
        Decir("Buscando en wikipedia...")
        query = query.replace("buscar en wikipedia", "")
        results = wikipedia.summary(query, sentences=1)
        Decir("De acuerdo a wikipedia")
        print(results)
        Decir(results)
    elif "google" in query:
        query = query.replace("buscar en google", "")
        webbrowser.open(query)
    elif "excel" in query:
        Decir("Cargando Excel")
        os.startfile("d:\\python\\rauxiliar.xlsx")
    elif "pausa" in query:
        Decir("De acuerdo, entramos en pausa")
    elif "reiniciamos" in query:
        Decir("Ok. Empecemos nuevamente")
    elif "escuchar música" in query:
        song = query.replace("reproduce musica", "")
        Decir("Reproduciendo: " + song)
        music_dir = "d:\\python\\Music"
        songs = os.listdir(music_dir)
        os.startfile(os.path.join(music_dir, songs[random.randint(0, 2)]))
    elif "dame el tiempo" in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        strFecha = datetime.datetime.now().strftime('%d-%m-%Y')
        print(strFecha)
        print(strTime)
        Decir(f"la fecha actual es {strFecha}")
        Decir(f"y la hora es {strTime}")
    elif "reproduce" in query:
        song = query.replace("reproduce en youtube", "")
        Decir("Reproduciendo: " + song)
        pywhatkit.playonyt(song)

    elif("lista de alumnos" in query):
        print("===================================")
        print("Lista de alumnos")
        print("===================================")
        Decir(f"Ok, esta es la lista de alumnos")
        cursor.execute("select codalumno,nombres from tasistencia;")
        alumnos = cursor.fetchall()
        for alumno in alumnos:
            print(str(alumno[0])     + " " + alumno[1])

    elif("llamar asistencia" in query):
        llamar_asistencia()
    # Add more conditions as needed for other functionalities

# Button to trigger text handling
but = Button(ventana, text="Enviar", width=5, height=3, command=handle_input)
but.pack()

# Function to stop the program
def Detener():
    messagebox.showinfo(message="Saliendo del asistente / Proyecto de Innovación", title="Asistente STICH22")
    ventana.destroy()

# Main function that starts the program
def main(res, sal):
    if res == "SI":
        if sal == "CONSALUDO":
            Saludar()

# Run Tkinter main loop
ventana.mainloop()