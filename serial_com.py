import serial.tools.list_ports
import serial # comunicare seriala
import pywhatkit # trimitere mesaje pe whatsapp
import pyautogui # controlul mouse-ului
from tkinter import * # interfata grafica
from datetime import datetime # timpul curent
# inserarea librariilor

#selectarea portului serial
def selectare_port_serial():
    porturi = list(serial.tools.list_ports.comports()) # lista cu porturile COM disponibile

    if not porturi: # daca nu exista niciun port COM disponibil 
        print("Niciun port COM disponibil. Asigurati-va ca dispozitivul este conectat.") 
        return None

    print("Porturi COM disponibile:") 
    for i, port in enumerate(porturi, start=1): # enumerarea porturilor COM disponibile
        print(f"{i}. {port}")

    while True: # selectarea portului COM
        try:
            selectie = int(input("Selecteaza portul COM (1, 2, etc.): ")) # selectarea portului COM
            if 1 <= selectie <= len(porturi): # daca selectia este valida
                port_selectat = porturi[selectie - 1].device 
                return port_selectat
            else:
                print("Selectie invalida. Va rugam introduceti un numar valid.") # daca selectia nu este valida
        except ValueError:
            print("Selectie invalida. Va rugam introduceti un numar valid.") # daca selectia nu este valida

def deschidere_comunicare_seriala(port): # deschiderea comunicarii seriale
    try:
        ser = serial.Serial(port, baudrate=9600, timeout=0) 
        print(f"Comunicare seriala deschisa pe {port}")
        return ser
    except serial.SerialException as e:
        print(f"Eroare la deschiderea comunicarii seriale: {e}")
        return None

#programul principal
def main():
    trimite_mesaj = True # variabila ce va fi folosita pentru a selecta daca se trimit mesaje pe whatsapp sau nu
    mesaj = None # mesajul ce va fi trimis pe whatsapp

    ecran = Tk() # crearea ferestrei principale
    ecran_latime = ecran.winfo_screenwidth() # dimensiunile ecranului
    ecran_lungime = ecran.winfo_screenheight() # dimensiunile ecranului

    utilizatori = { 
        "A119F0E3": {"nume": "Persoana 1", "apropieri_card": 0, "sosire": {"ora": 0, "minut": 0, "secunda": 0, "timp": None}, "plecare": {"ora": 0, "minut": 0, "secunda": 0, "timp": None}},
        "315AF7E3": {"nume": "Persoana 2", "apropieri_card": 0, "sosire": {"ora": 0, "minut": 0, "secunda": 0, "timp": None}, "plecare": {"ora": 0, "minut": 0, "secunda": 0, "timp": None}},
        "D1CA08E4": {"nume": "Persoana 3", "apropieri_card": 0, "sosire": {"ora": 0, "minut": 0, "secunda": 0, "timp": None}, "plecare": {"ora": 0, "minut": 0, "secunda": 0, "timp": None}},
        "A1E6F5E3": {"nume": "Persoana 4", "apropieri_card": 0, "sosire": {"ora": 0, "minut": 0, "secunda": 0, "timp": None}, "plecare": {"ora": 0, "minut": 0, "secunda": 0, "timp": None}},
    }
    # dictionarul cu ID-urile cardurilor si datele utilizatorilor

    port_selectat = selectare_port_serial() # selectarea portului serial
    if port_selectat: # daca portul serial a fost selectat cu succes
        ser = deschidere_comunicare_seriala(port_selectat) # deschiderea comunicarii seriale
        if ser: # daca comunicarea seriala a fost deschisa cu succes
            try: # citirea ID-ului cardului
                while True:
                    ID = ser.readline().decode().strip() # citirea ID-ului cardului

                    if ID:
                        utilizatori[ID]["apropieri_card"] += 1 # utilizatorul a apropiat cardul de cititor
                        timp_curent = datetime.now()

                        if utilizatori[ID]["apropieri_card"] == 1: # utilizatorul a apropiat cardul de cititor pentru prima data
                            utilizatori[ID]["sosire"]["ora"] = timp_curent.strftime("%H") # %H - ora in format 24h
                            utilizatori[ID]["sosire"]["minut"] = timp_curent.strftime("%M") # %M - minutul
                            utilizatori[ID]["sosire"]["secunda"] = timp_curent.strftime("%S") # %S - secunda 
                            utilizatori[ID]["sosire"]["timp"] = timp_curent.strftime("%H:%M:%S")  # %H:%M:%S - timpul in format 24h
                            mesaj = f'{utilizatori[ID]["nume"]} a sosit la {utilizatori[ID]["sosire"]["ora"]}:{utilizatori[ID]["sosire"]["minut"]}:{utilizatori[ID]["sosire"]["secunda"]}' # mesajul ce va fi trimis pe whatsapp
                            #f-format string

                        if utilizatori[ID]["apropieri_card"] == 2: # utilizatorul a apropiat cardul de cititor pentru a doua oara
                            utilizatori[ID]["plecare"]["ora"] = timp_curent.strftime("%H") # %H - ora in format 24h
                            utilizatori[ID]["plecare"]["minut"] = timp_curent.strftime("%M") # %M - minutul 
                            utilizatori[ID]["plecare"]["secunda"] = timp_curent.strftime("%S") # %S - secunda 
                            utilizatori[ID]["plecare"]["timp"] = timp_curent.strftime("%H:%M:%S") # %H:%M:%S - timpul in format 24h

                            delta = datetime.strptime(utilizatori[ID]["plecare"]["timp"], "%H:%M:%S") - datetime.strptime(utilizatori[ID]["sosire"]["timp"], "%H:%M:%S") # calcularea timpului petrecut in cladire
                            ora = int(delta.seconds // 3600)  # // - impartire intreaga si calcularea timpului petrecut in cladire
                            minut = int((delta.seconds // 60) % 60) 
                            secunda = int(delta.seconds % 60) # % - restul impartirii si calcularea timpului petrecut in cladire

                            mesaj = f'{utilizatori[ID]["nume"]} a plecat la {utilizatori[ID]["plecare"]["ora"]}:{utilizatori[ID]["plecare"]["minut"]}:{utilizatori[ID]["plecare"]["secunda"]}. Timp petrecut: {ora} ore {minut} minute {secunda} secunde'
                            # mesajul ce va fi trimis pe whatsapp
                            utilizatori[ID]["apropieri_card"] = 0 # resetarea numarului de apropiere a cardului de cititor

                        if trimite_mesaj: # daca utilizatorul a selectat optiunea de a trimite mesaje pe whatsapp
                            pywhatkit.sendwhatmsg_instantly("+40758243330", mesaj, tab_close=True, wait_time=10, close_time=3)
                            pyautogui.moveTo(ecran_latime * 0.694, ecran_lungime * 0.964) # mutarea mouse-ului pe butonul de inchidere a ferestrei de conversatie
                            pyautogui.click() # apasarea butonului de inchidere a ferestrei de conversatie
                            pyautogui.press('enter') # apasarea tastei Enter pentru a inchide fereastra de conversatie

            except KeyboardInterrupt: # apasarea tastei Ctrl+C pentru a opri programul
                print("\nComunicarea seriala s-a terminat.")
                ser.close() # inchiderea comunicarii seriale


if __name__ == "__main__": # daca fisierul este rulat direct
    main()
