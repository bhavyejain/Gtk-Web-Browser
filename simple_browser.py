import gi
gi.require_version("Gtk", "3.0")		# GUI toolkit
gi.require_version("WebKit2", "4.0")	# Web content engine
from gi.repository import Gtk, WebKit2

#main class
class Window():

	def __init__(self, *args, **kwargs):
		# create window
		self.main_window = Gtk.Window(title = "My Browser")
		self.main_window.set_icon_from_file('images/icon.png')		# set icon image file
		self.main_window.connect('destroy', Gtk.main_quit)	# connect the "destroy" trigger to Gtk.main_quit procedure
		self.main_window.set_default_size(600, 600)		# set window size

		# create navigation bar
		self.navigation_bar = Gtk.HBox()		# horizontal box navigation bar

		# create UI elements for navigation bar
		self.button_back = Gtk.ToolButton(Gtk.STOCK_GO_BACK)		# back button widget
		self.button_forward = Gtk.ToolButton(Gtk.STOCK_GO_FORWARD)	# forward button widget
		self.button_refresh = Gtk.ToolButton(Gtk.STOCK_REFRESH)		# refresh button widget
		self.main_address_bar = Gtk.Entry()							# address bar entry widget

		# connect triggers for UI elements with respective procedures
		self.button_back.connect('clicked', self.go_back)			# trigger:click
		self.button_forward.connect('clicked', self.go_forward)		# trigger:click
		self.button_refresh.connect('clicked', self.refresh_page)	# trigger:click
		self.main_address_bar.connect('activate', self.load_page)	# trigger:enter

		# attach UI elements to navigation bar
		self.navigation_bar.pack_start(self.button_back, False, False, 0)
		self.navigation_bar.pack_start(self.button_forward, False, False, 0)
		self.navigation_bar.pack_start(self.button_refresh, False, False, 0)
		self.navigation_bar.pack_start(self.main_address_bar, True, True, 0)

		# Create view for webpage
		self.web_view = WebKit2.WebView()				# initialize webview
		self.web_view.load_uri('https://google.com')	# default homepage
		self.web_view.connect('notify::title', self.change_title)	# trigger: title change
		self.web_view.connect('notify::estimated-load-progress', self.change_url)	# trigger: webpage is loading
		self.scrolled_window = Gtk.ScrolledWindow()		# scrolling window widget
		self.scrolled_window.add(self.web_view)

		# Add everything and initialize
		self.vbox_container = Gtk.VBox()		# vertical box container
		self.vbox_container.pack_start(self.navigation_bar, False, False, 0)
		self.vbox_container.pack_start(self.scrolled_window, True, True, 0)
		
		self.main_window.add(self.vbox_container)
		self.main_window.show_all()
		Gtk.main()

	def load_page(self, widget):
		url = self.main_address_bar.get_text()
		if url.startswith("http://") or url.startswith("https://"):
			self.web_view.load_uri(url)
		else:
			url = "https://" + url
			self.main_address_bar.set_text(url)
			self.web_view.load_uri(url)

	def change_title(self, widget, frame):
		self.main_window.set_title("Simple Browser - " + self.web_view.get_title())

	def change_url(self, widget, frame):
		uri = self.web_view.get_uri()
		self.main_address_bar.set_text(uri)

	def go_back(self, widget):
		self.web_view.go_back()

	def go_forward(self, widget):
		self.web_view.go_forward()

	def refresh_page(self, widget):
		self.web_view.reload()

main = Window()