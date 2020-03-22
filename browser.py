import gi
# import webkit
gi.require_version("Gtk", "3.0")
gi.require_version("WebKit", "3.0")
from gi.repository import Gtk, WebKit

#main class
class Window():

	def __init__(self, *args, **kwargs):
		# create window
		self.much_window = Gtk.Window(title = "My Browser")
		self.much_window.set_icon_from_file('images/icon.png')		# here goes to image file
		self.much_window.connect('destroy', Gtk.main_quit)
		self.much_window.set_default_size(600, 600)		# window size

		# create navigation bar
		self.navigation_bar = Gtk.HBox()		# lib name hbox

		self.many_back = Gtk.ToolButton(Gtk.STOCK_GO_BACK)
		self.such_forward = Gtk.ToolButton(Gtk.STOCK_GO_FORWARD)
		self.very_refresh = Gtk.ToolButton(Gtk.STOCK_REFRESH)
		self.main_address_bar = Gtk.Entry()

		self.many_back.connect('clicked', self.go_back)
		self.such_forward.connect('clicked', self.go_forward)
		self.very_refresh.connect('clicked', self.refresh_page)
		self.main_address_bar.connect('activate', self.load_page)

		self.navigation_bar.pack_start(self.many_back, False, False, 0)
		self.navigation_bar.pack_start(self.such_forward, False, False, 0)
		self.navigation_bar.pack_start(self.very_refresh, False, False, 0)
		self.navigation_bar.pack_start(self.main_address_bar, True, True, 0)

		# Create view for webpage

		self.very_view = Gtk.ScrolledWindow()
		self.such_webview = WebKit.WebView()
		self.such_webview.open('https://google.com')
		self.such_webview.connect('title-changed', self.change_title)
		self.such_webview.connect('load-committed', self.change_url)
		self.very_view.add(self.such_webview)

		# Add everything and initialize
		self.vbox_container = Gtk.VBox()
		self.vbox_container.pack_start(self.navigation_bar, False, False, 0)
		self.vbox_container.pack_start(self.very_view, True, True, 0)
		
		self.much_window.add(self.vbox_container)
		self.much_window.show_all()
		Gtk.main()

	def load_page(self, widget):
		so_add = self.main_address_bar.get_text()
		if so_add.startswith("http://") or so_add.startswith("https://"):
			self.such_webview.open(so_add)
		else:
			so_add = "https://" + so_add
			self.main_address_bar.set_text(so_add)
			self.such_webview.open(so_add)

	def change_title(self, widget, frame, title):
		self.much_window.set_title("MyBrowser - " + title)

	def change_url(self, widget, frame):
		uri = frame.get_uri()
		self.main_address_bar.set_text(uri)

	def go_back(self, widget):
		self.such_webview.go_back()

	def go_forward(self, widget):
		self.such_webview.go_forward()

	def refresh_page(self, widget):
		self.such_webview.reload()

main = Window()