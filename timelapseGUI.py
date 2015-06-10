#Imports
import datetime
import time
import sys
try:
	import pygtk
	#pygtk.require(2.0)
except:
	print("PYGTK not availible")
	pass
try:
	import gtk, gobject
	import gtk.glade
except:
	print("GTK not availible")
	sys.exit(1)
try:
	import RPi.GPIO as IO
except:
	print("RPi not availible")
	pass

#Definiere Variablen
version = 1
dauer = 0  #in ms
intervall = 0 #in s
pin = 17
new_val = 0.0

def getFaktor(zeit):
	faktor = 0
	if str(zeit).lower() == "stunden":
		faktor = 3600000
	elif str(zeit).lower() == "minuten":
		faktor =  60000
	elif str(zeit).lower() == "sekunden":
		faktor =  1000
	elif str(zeit).lower() == "millisekunden":
		faktor = 1
	else: 
		print("Es konnte kein Faktor ermittelt werden")
	return faktor

def calcDauerIntervall(tbxDauer, cboDauer, tbxIntervall, cboIntervall):
	faktorDauer = 0
	faktorIntervall = 0
	
	txtDauerEinheit = cboDauer.get_active_text()
	if txtDauerEinheit != None:
		print("Einheit der Dauer: %s" % (txtDauerEinheit))
		faktorDauer = getFaktor(txtDauerEinheit)
		print("Faktor der Dauer: %s" % (faktorDauer))
	
	txtIntervallEinheit = cboIntervall.get_active_text()
	if txtIntervallEinheit != None:
		print("Einheit des Intervalls: %s" % (txtIntervallEinheit))
		faktorIntervall = getFaktor(txtIntervallEinheit)
		print("Faktor der Dauer: %s" % (faktorIntervall))
	
	intDauer = 0
	intIntervall = 0

	try:
		intDauer = int(tbxDauer.get_text())
	except:
		intDauer = 0
	try:
		intIntervall = int(tbxIntervall.get_text())
	except:
		intIntervall = 0

	print("Dauer: %s" % (intDauer))
	print("Intervall: %s" % (intIntervall))

	if intDauer >0 and intIntervall > 0 and faktorDauer > 0 and faktorIntervall > 0:
		dauer = intDauer * faktorDauer
		intervall = intIntervall * faktorIntervall
	else:
		#print("Ueberpruefen Sie ihre Eingaben")	
		return {}

	dicSet = { "intervall": intervall, "dauer": dauer }
	return dicSet

# Update the value of the progress bar so that we get
# some movement
def takeShot(pbobj, maxVal):	
	# Calculate the value of the progress bar using the
	# value range set in the adjustment object
	global new_val	
	#print("maxVal " + str(maxVal))
	new_val = (1.0 / maxVal) * pbobj.count
	#print("new_val " + str(new_val))
	if new_val > 1.0:	
		#Set the new value
		new_val = 0
		pbobj.wTree.get_widget("statusbar1").push(1,"Timelapse wurde beendet")
		pbobj.timer = 0
		return False
		
	pbobj.progressbar.set_fraction(new_val)
	pbobj.progressbar.set_text("[" + str(datetime.datetime.now()) + "] " + str(pbobj.count) + " Foto(s) aufgenommen")
	pbobj.count = pbobj.count + 1
	
	#Take the Shot
	#IO.output(pin, IO.HIGH)
	time.sleep(1)
	#IO.output(pin, IO.LOW)
	
	print "[" + str(datetime.datetime.now()) + "] " + str(pbobj.count) + " Foto(s) aufgenommen"
		
	return True
    
class timelapse:
	wTree = None
	faktorDauer = 0
	faktorIntervall = 0
	count = 1
	#print("init")
	def __init__(self):
		self.wTree = gtk.glade.XML("timelapse1.glade")

		dic = { 
			"on_btnStop_clicked" : self.quit,
			"on_btnStart_clicked" : self.add,
			"on_windowMain_destroy" : self.destroy_progress,
			"on_objekt_changed": self.checkchange,
		}
		self.wTree.signal_autoconnect(dic)
		
		#self.window.connect("destroy", self.destroy_progress)
		
		#Defaultwerte
		self.wTree.get_widget("tbxDauer").set_text('12')
		self.wTree.get_widget("tbxIntervall").set_text('3')
		self.wTree.get_widget("cboIntervall").set_active(1)
		self.wTree.get_widget("cboDauer").set_active(0)
		self.wTree.get_widget("rdbDSLR").set_active(1)
		
		#Get the progressbar
		self.progressbar = self.wTree.get_widget("pbar")
		
		#gtk.main()

	def quit(self, widget):
		sys.exit(0)
		
	# Clean up allocated memory and remove the timer
	def destroy_progress(self, widget, data=None):
		gobject.source_remove(self.timer)
		self.timer = 0
		gtk.main_quit()
	
	def checkchange(self, combo):		
		#txtDauerEinheit = self.wTree.get_widget("cboDauer").get_active_text()
		#if txtDauerEinheit != None:
	    #	print("Einheit der Dauer: %s" % (txtDauerEinheit))
		#	faktorDauer = getFaktor(txtDauerEinheit)
		#	print("Faktor der Dauer: %s" % (faktorDauer))
		
		#txtIntervallEinheit = self.wTree.get_widget("cboIntervall").get_active_text()
		#if txtIntervallEinheit != None:
		#	print("Einheit des Intervalls: %s" % (txtIntervallEinheit))
		#	faktorIntervall = getFaktor(txtIntervallEinheit)
		#	print("Faktor der Dauer: %s" % (faktorIntervall))
		
		#intDauer = 0
		#intIntervall = 0

		#try:
		#	intDauer = int(self.wTree.get_widget("tbxDauer").get_text())
		#except:
		#	intDauer = 0
		#try:
		#	intIntervall = int(self.wTree.get_widget("tbxIntervall").get_text())
		#except:
		#	intIntervall = 0

		#print("Dauer: %s" % (intDauer))
		#print("Intervall: %s" % (intIntervall))

		#if intDauer >0 and intIntervall > 0 and faktorDauer > 0 and faktorIntervall > 0:
		#	dauer = intDauer * faktorDauer
		#	intervall = intIntervall * faktorIntervall

		dicset = calcDauerIntervall(self.wTree.get_widget("tbxDauer"),self.wTree.get_widget("cboDauer"),self.wTree.get_widget("tbxIntervall"),self.wTree.get_widget("cboIntervall"))
		if len(dicset) > 0:
			print(dicset["intervall"])
			print(dicset["dauer"])
			intervall = int(dicset["intervall"])
			dauer = int(dicset["dauer"])
			if intervall > dauer:
				print "Das Intervall ist goesser als die Dauer. Bitte kooregiren Sie ihre Eingabe!"
			else:
				startzeit = datetime.datetime.now()
				endzeit = startzeit + datetime.timedelta(milliseconds=dauer)
				AnzBilder = dauer/intervall
				self.wTree.get_widget("lblEndzeit").set_text("Endzeit: ca. " + str(endzeit.strftime("%d.%m.%Y %H:%M:%S")))	
				self.wTree.get_widget("lblBilder").set_text("Anzahl Bilder: " + str(AnzBilder))
		#else:
		#	print("Ueberpruefen Sie ihre Eingaben")	
		
	def setFortschritt(self,data):
		self.wTree.get_widget("statusbar1").push(1,data)
		return True
					
	def add(self, widget):
		self.wTree.get_widget("statusbar1").push(1,"Timelapse wird gestartet")
		dicset = calcDauerIntervall(self.wTree.get_widget("tbxDauer"),self.wTree.get_widget("cboDauer"),self.wTree.get_widget("tbxIntervall"),self.wTree.get_widget("cboIntervall"))
		intervall = int(dicset["intervall"])
		dauer = int(dicset["dauer"])
		if intervall > dauer:
			print "Das Intervall ist goesser als die Dauer. Bitte kooregiren Sie ihre Eingabe!"
			self.wTree.get_widget("statusbar1").push(1,"Das Intervall ist goesser als die Dauer. Bitte kooregiren Sie ihre Eingabe!")
		else:
			startzeit = datetime.datetime.now()
			endzeit = startzeit + datetime.timedelta(milliseconds=dauer)
			AnzBilder = dauer/intervall
			self.wTree.get_widget("lblEndzeit").set_text("Endzeit: ca. " + str(endzeit.strftime("%d.%m.%Y %H:%M:%S")))	
			self.wTree.get_widget("lblBilder").set_text("Anzahl Bilder: " + str(AnzBilder))
					
			#intervall = intervall*0.001
			print(dauer)
			print(intervall)
			#count = 1			

			self.progressbar.set_fraction(0.0)
			self.wTree.get_widget("statusbar1").push(1,"Timelapse laeuft ...")
			# Add a timer callback to update the value of the progress bar
			self.timer = gobject.timeout_add (intervall, takeShot, self, AnzBilder)


def main():
	gtk.main()
	return 0
	
if __name__ == "__main__":
	timelapse()
	main()
#start = timelapse()
