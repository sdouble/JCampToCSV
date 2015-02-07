#! /usr/bin/env python

from gi.repository import Gtk
from gi.repository import Gdk
from convert import convert
import threading

class BoxWindow(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self, title="Jcamp to CSV Converter")
		self.set_border_width(10)
		self.set_default_size(400,50)
		mainBox=Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		self.add(mainBox)

		# openBox
		openBox=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=3)
		mainBox.pack_start(openBox,False,False,0)

		self.txtFileOpen=Gtk.Entry()
		openBox.pack_start(self.txtFileOpen,True,True,0)

		self.buttonOpen=Gtk.Button(label="Convert")
		self.buttonOpen.connect("clicked", self.getFileOpen)
		openBox.pack_end(self.buttonOpen,False,False,0)

		# saveBox
		saveBox=Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=3)
		mainBox.pack_start(saveBox,False,False,0)

		self.txtFileSave=Gtk.Entry()
		saveBox.pack_start(self.txtFileSave,True,True,0)
		
		self.buttonSave=Gtk.Button(label="Save  As")
		self.buttonSave.connect("clicked", self.getFileSave)
		saveBox.pack_start(self.buttonSave,False,False,0)

		self.buttonConvert=Gtk.Button(label="Convert")
		self.buttonConvert.connect("clicked", self.convertButton_clicked)
		mainBox.pack_start(self.buttonConvert,False,False,0)

		self.progress=Gtk.ProgressBar()
		self.progress.set_text("some text")
		mainBox.pack_start(self.progress,False,True,0)

	def updateProgressBar(self, currentProgress, totalToProcess):
		self.progress.set_fraction(currentProgress/totalToProcess)

	def updateWinText(self, text):
		self.set_title(text)

	def getFileOpen(self, button):
		dialog=Gtk.FileChooserDialog("Select a file to convert", self,
	  	Gtk.FileChooserAction.OPEN,(
	  		"_Cancel", Gtk.ResponseType.CANCEL,
	  		"_Open", Gtk.ResponseType.OK))
		response=dialog.run()
		if response == Gtk.ResponseType.OK:
			filename=dialog.get_filename()
			self.txtFileOpen.set_text(filename)
			dialog.destroy()
		dialog.destroy()
	
	def getFileSave(self, button):
		dialog=Gtk.FileChooserDialog("Select a destination file", self,
	  	Gtk.FileChooserAction.SAVE,(
	  		"_Cancel", Gtk.ResponseType.CANCEL,
	  		"_Save", Gtk.ResponseType.OK))
		response=dialog.run()
		if response == Gtk.ResponseType.OK:
			filename=dialog.get_filename()
			self.txtFileSave.set_text(filename)
			dialog.destroy()
		dialog.destroy()
	
	def worker():
		print("worker")
	
	def convertButton_clicked(self, button):
		if self.txtFileSave.get_text() and self.txtFileOpen.get_text():
			print("Converting:", self.txtFileOpen.get_text())
			print("Saving as:", self.txtFileSave.get_text())
			threading.Thread(target=convert,
				args=(self, self.txtFileOpen.get_text(), self.txtFileSave.get_text())
			).start()

win=BoxWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()
win.set_resizable(False)