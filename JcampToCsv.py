from gi.repository import Gtk
from convert import convert
import threading

class BoxWindow(Gtk.Window):
	def __init__(self):
		Gtk.Window.__init__(self, title="Jcamp to CSV Converter")
		self.set_border_width(10)
		self.set_default_size(275,50)
		box=Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
		self.add(box)

		self.buttonOpen=Gtk.Button(label="Convert")
		self.buttonOpen.connect("clicked", self.on_convertButton_clicked)
		box.pack_start(self.buttonOpen,True,True,0)

		self.progress=Gtk.ProgressBar()
		self.progress.set_text("some text")
		box.pack_start(self.progress,True,True,0)

	def updateProgressBar(self, currentProgress, totalToProcess):
		self.progress.set_fraction(currentProgress/totalToProcess)

	def updateWinText(self, text):
		self.set_title(text)

	def getFileOpen(self):
		dialog=Gtk.FileChooserDialog("Select a file to convert", self,
	  	Gtk.FileChooserAction.OPEN,(
	  		Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
	  		Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
		response=dialog.run()
		if response == Gtk.ResponseType.OK:
			filename=dialog.get_filename()
			dialog.destroy()
			return filename
		dialog.destroy()
	
	def getFileSave(self):
		dialog=Gtk.FileChooserDialog("Select a destination file", self,
	  	Gtk.FileChooserAction.SAVE,(
	  		Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
	  		Gtk.STOCK_SAVE, Gtk.ResponseType.OK))
		response=dialog.run()
		if response == Gtk.ResponseType.OK:
			filename=dialog.get_filename()
			dialog.destroy()
			return filename
		dialog.destroy()
	
	def worker():
		print("worker")
	
	def on_convertButton_clicked(self, button):
		file_in=self.getFileOpen()
		if file_in:
			file_out=self.getFileSave()
		if file_in and file_out:	
			print("Converting:", file_in)
			print("Saving as:", file_out)
			threading.Thread(target=convert,
				args=(self, file_in, file_out)
			).start()

win=BoxWindow()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()