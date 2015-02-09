from gi.repository import Gtk
from convert import convert
import threading

class GridWindow(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self, title="Jcamp to CSV Converter")
		self.set_border_width(10)
		self.set_default_size(400,50)

		mainGrid=Gtk.Grid()
		mainGrid.set_column_spacing(5)
		mainGrid.set_row_spacing(5)
		mainGrid.set_row_homogeneous(True)
		mainGrid.set_column_homogeneous(True)

		self.add(mainGrid)

		self.txtFileOpen=Gtk.Entry()
		self.txtFileSave=Gtk.Entry()
		self.buttonOpen=Gtk.Button(label="JCamp File")
		self.buttonSave=Gtk.Button(label="CSV File")
		self.buttonConvert=Gtk.Button(label="Convert")
		self.progress=Gtk.ProgressBar()

		mainGrid.attach(self.txtFileOpen,0,0,2,1)
		mainGrid.attach(self.buttonOpen,2,0,1,1)

		mainGrid.attach(self.txtFileSave,0,1,2,1)
		mainGrid.attach(self.buttonSave,2,1,1,1)

		mainGrid.attach(self.buttonConvert,0,2,3,1)
		mainGrid.attach(self.progress,0,3,3,1)

		self.buttonOpen.connect("clicked", self.getFileOpen)
		self.buttonSave.connect("clicked", self.getFileSave)
		self.buttonConvert.connect("clicked", self.convertButton_clicked)

	def updateProgressBar(self, currentProgress, totalToProcess):
		self.txtFileOpen.set_fraction(currentProgress/totalToProcess)

	def updateWinText(self, text):
		self.set_title(text)

	def getFileOpen(self, button):
		dialog=Gtk.FileChooserDialog("Select a file to convert", self,
	  	Gtk.FileChooserAction.OPEN,(
	  		Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
	  		Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
		response=dialog.run()
		if response == Gtk.ResponseType.OK:
			filename=dialog.get_filename()
			self.txtFileOpen.set_text(filename)
			self.txtFileOpen.do_move_cursor(self.txtFileOpen,0,100000,False)
			dialog.destroy()
		dialog.destroy()
	
	def getFileSave(self, button):
		dialog=Gtk.FileChooserDialog("Select a destination file", self,
	  	Gtk.FileChooserAction.SAVE,(
	  		Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
	  		Gtk.STOCK_SAVE, Gtk.ResponseType.OK))
		response=dialog.run()
		if response == Gtk.ResponseType.OK:
			filename=dialog.get_filename()
			self.txtFileSave.set_text(filename)
			self.txtFileSave.do_move_cursor(self.txtFileSave,0,100000,False)
			dialog.destroy()
		dialog.destroy()
	
	def worker():
		print("worker")
	
	def convertButton_clicked(self, button):
		if self.txtFileSave.get_text() and self.txtFileOpen.get_text():
			print("Converting:", self.txtFileSave.get_text())
			print("Saving as:", self.txtFileOpen.get_text())
			threading.Thread(target=convert,
				args=(self, self.txtFileOpen.get_text(), self.txtFileSave.get_text())
			).start()

win=GridWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()