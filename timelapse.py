#Imports
import datetime
import time
#import RPi.GPIO as IO

#Definiere Variablen
version = 1
dauer = 0  #in ms
intervall = 0 #in s
pin = 17
#Konfiguriere GPIO
#IO.setMode(IO.BCM)
#IO.setup(pin, IO.OUT)
#IO.setwarnings(False)

#Programm Starten
print "======================="
print "Timelapse-Programm v" + str(version)
print "======================="

#Aufnahmeparameter eingeben
tmpDauer = raw_input("Aufnahmedauer ([x] h, [x] m, [x] s, [x] ms): ")
tmpIntervall = raw_input("Aufnahmeintervall ([x] h.[x]m,[x] s, [x] ms):")
#Aufnahmeparameter auswerten
lstDauer = tmpDauer.split(' ')
lstIntervall = tmpIntervall.split(' ')
if len(lstDauer) == 2:
	if str(lstDauer[1]).lower() == "h":
		dauer = int(lstDauer[0]) * 3600000
	elif str(lstDauer[1]).lower() == "m":
		dauer = int(lstDauer[0]) * 60000
	elif str(lstDauer[1]).lower() == "s":
		dauer = int(lstDauer[0]) * 1000
	elif str(lstDauer[1]).lower() == "ms":
		dauer = int(lstDauer[0])

if len(lstIntervall) == 2:
	if str(lstIntervall[1]).lower() == "h":
		intervall = int(lstIntervall[0]) * 3600
	elif str(lstIntervall[1]).lower() == "m":
		intervall = int(lstIntervall[0]) * 60
	elif str(lstIntervall[1]).lower() == "s":
		intervall = int(lstIntervall[0])  
	elif str(lstIntervall[1]).lower() == "ms":
		intervall = int(lstIntervall[0]) * 0.001

if (intervall * 0.001) > dauer:
	print "Das Intervall ist goesser als die Dauer. Bitte kooregiren Sie ihre Eingabe!"
else:
	startzeit = datetime.datetime.now()
	endzeit = startzeit + datetime.timedelta(milliseconds=dauer)

	print "Startzeit:    " + str(startzeit)
	print "Endzeitpunkt: " + str(endzeit)
	count = 1
	while(datetime.datetime.now() < endzeit):
		#Fotoaufnehmen
		#IO.output(pin, IO.HIGH)
		#time.sleep(1)
		#IO.output(pin, IO.LOW)
		print "[" + str(datetime.datetime.now()) + "] " + str(count) + " Foto(s) aufgenommen"
	
		#Warten
		count = count + 1
		time.sleep(intervall - 1)

print "Programm beendet um " + str(datetime.datetime.now())
print "======================"

		

