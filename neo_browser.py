import sys, gi
gi.require_version("Gtk", "3.0")		# GUI toolkit
gi.require_version("WebKit2", "4.0")	# Web content engine
from gi.repository import Gtk, WebKit2 as wk, Gdk

class BrowserTab(Gtk.VBox):
	
	def __init__(self, *args, **kwargs):
		super(BrowserTab, self).__init__(*args, **kwargs)

		self.web_view = wk.WebView()					# initialize webview
		self.web_view.load_uri('https://google.com')	# default homepage for every tab
		self.show()

		button_go = Gtk.ToolButton(Gtk.STOCK_APPLY);				# go button widget
		self.button_back = Gtk.ToolButton(Gtk.STOCK_GO_BACK)		# back button widget
		self.button_forward = Gtk.ToolButton(Gtk.STOCK_GO_FORWARD)	# forward button widget
		self.button_refresh = Gtk.ToolButton(Gtk.STOCK_REFRESH)		# refresh button widget
		self.address_bar = Gtk.Entry()								# address bar entry widget

		button_go.connect("clicked", self.load_page)									# trigger: click
		self.address_bar.connect("activate", self.load_page)							# trigger: enter
		self.button_back.connect("clicked", lambda x : self.web_view.go_back())			# trigger: click
		self.button_forward.connect("clicked", lambda x : self.web_view.go_forward())	# trigger: click
		self.button_refresh.connect("clicked", lambda x : self.web_view.reload())		# trigger: click

		url_box = Gtk.HBox()										# create url bar
		url_box.pack_start(self.button_back, False, False, 0)
		url_box.pack_start(self.button_forward, False, False, 0)
		url_box.pack_start(self.button_refresh, False, False, 0)
		url_box.pack_start(self.address_bar, True, True, 0)
		url_box.pack_start(button_go, False, False, 0)

		scrolled_window = Gtk.ScrolledWindow()		# scrolling window widget
		scrolled_window.add(self.web_view)			# add web_view to scrolled window

		find_box = Gtk.HBox()						# find text dialog
		self.find_controller = self.web_view.get_find_controller()
		
		button_close = Gtk.ToolButton(Gtk.STOCK_CLOSE)		# close the find dialog
		button_next = Gtk.ToolButton(Gtk.STOCK_GO_DOWN)	# find next
		button_prev = Gtk.ToolButton(Gtk.STOCK_GO_UP)		# find previous
		self.find_entry = Gtk.Entry()						# text to find

		button_close.connect("clicked", lambda x : find_box.hide())
		self.find_entry.connect("activate", self.find_text)
		button_next.connect("clicked", self.find_text_next)
		button_prev.connect("clicked", self.find_text_prev)

		# attach UI elements to find dialog
		find_box.pack_start(button_close, False, False, 0)
		find_box.pack_start(self.find_entry, False, False, 0)
		find_box.pack_start(button_prev, False, False, 0)
		find_box.pack_start(button_next, False, False, 0)
		self.find_box = find_box

		# add everything to browser tab
		self.pack_start(url_box, False, False, 0)
		self.pack_start(find_box, False, False, 0)
		self.pack_start(scrolled_window, True, True, 0)

		url_box.show_all()
		scrolled_window.show_all()

	def load_page(self, widget):				# load page from URI
		url = self.address_bar.get_text()
		if url.startswith("http://") or url.startswith("https://"):
			self.web_view.load_uri(url)
		else:
			url = "https://" + url
			self.address_bar.set_text(url)
			self.web_view.load_uri(url)

	def find_text(self, widget):				
		self.find_controller.search(self.find_entry.get_text(), 0, 1)

	def find_text_next(self, widget):
		self.find_controller.search_next()

	def find_text_prev(self, widget):
		self.find_controller.search_previous()



class Browser(Gtk.Window):
	
	def __init__(self, *args, **kwargs):
		super(Browser, self).__init__(*args, **kwargs)

		self.set_title("My Browser")			# set title of window
		self.set_icon_from_file('images/icon.png')		# set icon image file
		self.set_default_size(600, 600)

		self.tool_bar = Gtk.HBox()		# create horizontal box for tool bar
		self.button_new_tab = Gtk.ToolButton(Gtk.STOCK_ADD)			# create new tab
		self.button_close_tab = Gtk.ToolButton(Gtk.STOCK_CLOSE)		# close current tab
		self.button_find = Gtk.ToolButton(Gtk.STOCK_FIND)			# show find dialog
		self.button_home = Gtk.ToolButton(Gtk.STOCK_HOME)

		self.button_new_tab.connect("clicked", self.open_new_tab)
		self.button_close_tab.connect("clicked", self.close_current_tab)
		self.button_find.connect("clicked", self.raise_find_dialog)
		self.button_home.connect("clicked", self.goto_home)

		self.tool_bar.pack_start(self.button_new_tab, False, False, 0)
		self.tool_bar.pack_start(self.button_close_tab, False, False, 0)
		self.tool_bar.pack_start(self.button_find, False, False, 0)
		self.tool_bar.pack_start(self.button_home, False, False, 0)

		# create notebook and tabs
		self.notebook = Gtk.Notebook()
		self.notebook.set_scrollable(True)

		self.tabs = []						# list of tuples : each tuple represents a tab (tab, label)
		self.set_size_request(600, 600)

		# create a first empty browser tab
		self.tabs.append((self.create_tab(), Gtk.Label("New Tab")))
		self.notebook.insert_page(self.tabs[0][0], self.tabs[0][1], 0)

		# connect signals
		self.connect("destroy", Gtk.main_quit)
		self.notebook.connect("switch-page", self.tab_changed)

		self.vbox_container = Gtk.VBox()		# pack tool bar and notebook in a vertical box
		self.vbox_container.pack_start(self.tool_bar, False, False, 0)
		self.vbox_container.pack_start(self.notebook, True, True, 0)

		# add vertical box to the Window
		self.add(self.vbox_container)

		# show widgets
		self.tool_bar.show_all()
		self.notebook.show()
		self.vbox_container.show()
		self.show()

	def tab_changed(self, notebook, current_page, index):
		if not index:
			return
		title = self.tabs[index][0].web_view.get_title()
		if title:
			self.set_title("Neo Browser - " + title)

	def title_changed(self, web_view, frame):
		current_page = self.notebook.get_current_page()

		counter = 0
		for tab, label in self.tabs:
			if tab.web_view is web_view:
				label.set_text(tab.web_view.get_title())
				if counter == current_page:
					self.tab_changed(None, None, counter)
				break
			counter += 1

	def create_tab(self):
		tab = BrowserTab()
		tab.web_view.connect("notify::title", self.title_changed)
		return tab

	def close_current_tab(self, widget):
		if self.notebook.get_n_pages() == 1:
			return
		page = self.notebook.get_current_page()
		current_tab = self.tabs.pop(page)
		self.notebook.remove(current_tab[0])

	def open_new_tab(self, widget):
		current_page = self.notebook.get_current_page()
		page_tuple = (self.create_tab(), Gtk.Label("New Tab"))
		self.tabs.insert(current_page + 1, page_tuple)
		self.notebook.insert_page(page_tuple[0], page_tuple[1], current_page + 1)
		self.notebook.set_current_page(current_page + 1)

	def raise_find_dialog(self, widget):
		current_page = self.notebook.get_current_page()
		self.tabs[current_page][0].find_box.show_all()
		self.tabs[current_page][0].find_entry.grab_focus()

	def goto_home(self, widget):
		current_page = self.notebook.get_current_page()
		self.tabs[current_page][0].web_view.load_uri("https://www.google.com/")



if __name__ == "__main__":
	Gtk.init(sys.argv)
	browser = Browser()
	Gtk.main()