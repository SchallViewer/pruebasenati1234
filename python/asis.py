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

    Decir("Mi nombre es STICH22, soy el asistente del profesor Wilbert, en que le puedo ayudar ")
    
wikipedia.set_lang("es")  
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")

engine.setProperty("voice",voices[0].id)

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

def Consulta():
        r = sr.Recognizer()
        with sr.Microphone() as source:
                print("Escuchando...")
                r.pause_threshould = 1
                audio = r.listen(source)

        try:
                print("Analizando...")
                query = r.recognize_google(audio, language="es-ES")
                print(f"El usuario dijo: {query}\n")
        except Exception as ex:
                print("Repita por favor...")
                return "None"

        return query
    

def main(res,sal):
    if(res=="SI"):
        if(sal=="CONSALUDO"): 
            Saludar()
        bucle=True
        while bucle:
                query = Consulta().lower()

                if("wikipedia" in query):
                        Decir("Buscando en wikipedia...")
                        query = query.replace("buscar en wikipedia","")
                        results = wikipedia.summary(query, sentences=1)
                        Decir("De acuerdo a wikipedia")
                        print(results)
                        Decir(results)
                elif("google" in query):
                        query = query.replace("buscar en google","")

                        #webbrowser.get('chrome %s').open_new_tab('http://www.google.com')
                        #chrome_path = 'C:\Program Files (x86)\Google\Chrome\Applicationchrome.exe %s'
                        #webbrowser.get(chrome_path).open(query)

                        webbrowser.open(query)
                elif("excel" in query):
                        Decir("cargando excel")
                        #p = subprocess.Popen("C:\Program Files\Microsoft Office\Office16\excel.exe")
                        os.startfile("d:\\python\\rauxiliar.xlsx")
                elif("pausa" in query):
                        Decir("De acuerdo entramos en pausa")
                        print("Estamos en pausa")
                        bucle=False
                elif("reiniciamos" in query):
                        Decir("Ok. empecemos nuevamente")
                        print("Estamos reiniciando el asistente")
                        bucle=True

                elif("escuchar música" in query):
                        song = query.replace("reproduce musica","")
                        Decir("reproduciendo: " + song)
                        music_dir = "d:\\python\\Music"
                        songs = os.listdir(music_dir)
                        os.startfile(os.path.join(music_dir, songs[random.randint(0,2)]))
                elif("dame el tiempo" in query):
                        strTime = datetime.datetime.now().strftime("%H:%M:%S")
                        strFecha = datetime.datetime.now().strftime('%d-%m-%Y')
                        print(strFecha)
                        print(strTime)
                        Decir(f"la fecha actual es {strFecha}")
                        Decir(f"y la hora es {strTime}")
                elif("reproduce" in query):
                        song = query.replace("reproduce en youtube","")
                        Decir("reproduciendo: " + song)
                        pywhatkit.playonyt(song)
                elif("los objetivos" in query):
                        with open("d:\python\objetivos.txt","r",encoding="utf-8") as archivo:
                                for linea in archivo:
                                        print(linea)
                                        Decir(linea)
                elif("charla" in query):
                        with open("d:/python/charla.txt","r",encoding="utf-8") as archivo:
                                for linea in archivo:
                                        print(linea)
                                        Decir(linea)

                elif("bienvenido" in query):
                       Decir(f"Bien gracias profesor, estoy listo para empezar")

                elif("gracias" in query):
                       Decir(f"Ok profesor sigamos")

                elif("chiste" in query):
                        print("===================================")
                        print("Un chiste")
                        print("===================================")
                        cursor.execute("select top 1 * from tchistes order by NEWID()")
                        chistes = cursor.fetchall()
                        for chiste in chistes:
                            print(chiste[1])
                            Decir(chiste[1])

                elif("lista de alumnos" in query):
                        print("===================================")
                        print("Lista de alumnos")
                        print("===================================")
                        Decir(f"Ok, esta es la lista de alumnos")
                        cursor.execute("select codalumno,nombres from tasistencia;")
                        alumnos = cursor.fetchall()
                        for alumno in alumnos:
                            print(alumno[0] + " " + alumno[1])
                    
                elif("llamar asistencia" in query):
                        print("===================================")
                        print("LLAMANDO ASISTENCIA DEL " + str(fe))
                        print("===================================")
                        Decir("Llamando asistencia del " + str(fe))
                        Decir("Presten atencion ")

                        try:
                            cursor.execute("select codalumno,nombres from tasistencia;")
                            alumnos = cursor.fetchall()
                            for alumno in alumnos:
                                #print(alumno)
                                print(alumno[0] + " " + alumno[1])
                                Decir(alumno[1])

                                r = sr.Recognizer()
                                with sr.Microphone() as source:
                                    print("Responda...")
                                    r.pause_threshould = 1
                                    audio = r.listen(source)

                                try:
                                    print("Verificando respuesta...")
                                    query = r.recognize_google(audio, language="es-ES")
                                    query = query.replace("senté","presente")
                                    query = query.replace("presidente","presente")
                                    query = query.replace("alto","faltó")
                                    query = query.replace("Bfaltó","faltó")
                                    query = query.replace("pfaltó","faltó")
                                    print(f"El alumno Respondio: {query}\n")

                                    consulta = "update tasistencia set situacion = ? where codalumno = ?;"
                                    id_alumno = alumno[0]
                                    cursor.execute(consulta, (query, id_alumno))
                                    
                                    cursor.commit()
                                except Exception as ex:
                                    print("Ocurrio un error con el asistente...")
                                    consulta = "update tasistencia set situacion = ? where codalumno = ?;"
                                    id_alumno = alumno[0]
                                    cursor.execute(consulta, ('NO RESPONDIO', id_alumno))
                                    
                                    cursor.commit()
                                    
                            Decir("Estos son los resultados de la asistencia del día " + str(fe))
                            print("RESULTADOS DE LA ASISTENCIA")
                            print("============================")
                            cursor.execute("select situacion,count(*) as conteo from tasistencia group by situacion with rollup;")
                            rs = cursor.fetchall()
                            for resultado in rs:
                                if resultado[0] is None:
                                    resultado[0]="TOTAL ASISTENCIA:"
                                print(resultado[0].upper() + " " + str(resultado[1]))
       

                        except Exception as e:
                            print("Ocurrió un error al consultar: ", e)
                        finally:
                            print("Final asistencia")
                            #conexion.close()
		
                        
                elif("datos del curso" in query):
                        with open("d:/python/datoscurso.txt","r",encoding="utf-8") as archivo:
                                for linea in archivo:
                                        print(linea)
                                        Decir(linea)

                elif("traduce el texto" in query):
                        with open("d:/python/textoeningles.txt","r") as archivo:
                                  for linea in archivo:
                                      print(linea)
                                      Decir(linea)
							
                        eb=TextBlob(linea)
                        te = eb.translate(from_lang='en',to='es')
                        print("TEXTO TRADUCIDO")
                        print("===============")
                        print(eb.translate(from_lang='en',to='es'))
                        #print(linea)
                        f=open("d:/python/textotraducido.txt","w")
                        for linea in te:
                            f.write(linea)
                        
                        Decir(eb.translate(from_lang='en',to='es'))  


ventana = Tk()
ventana.geometry("600x270")
ventana.title("Asistente virtual del Senati / Proyecto de Innovación 2022")
ventana['bg'] = '#0059b3'
lbl = Label(ventana,fg="#ffffff", bg="#0059b3", text="Soy Stich22", font=("Arial Bold", 30))
lbl.place(x=10,y=10)

logo = PhotoImage(file='logo1.png')


tit = Label(ventana,fg="#ffffff", bg="#0059b3", text="Asistente virtual", font=("Arial Bold", 22))
tit.place(x=300,y=70)

tit1 = Label(ventana,fg="#ffffff", bg="#0059b3", text="del SENATI", font=("Arial Bold", 22))
tit1.place(x=325,y=120)

butini = Button(ventana,fg="#ffffff", bg="#0059b3", text="  Iniciar ", font=("Arial Bold", 16),command= lambda: main("SI","CONSALUDO"))
butini.place(x=250,y=210)

butre = Button(ventana,fg="#ffffff", bg="#0059b3", text=" Reiniciar ", font=("Arial Bold", 16),command= lambda: main("SI","SINSALUDO"))
butre.place(x=350,y=210)


butdet = Button(ventana,fg="#ffffff", bg="#0059b3", text="   Salir    ", font=("Arial Bold", 16),command=Detener)
butdet.place(x=480,y=210)



asis = Label(ventana, image=logo,borderwidth=0).place(x=40,y=60)

ventana.mainloop()
