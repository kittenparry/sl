import tkinter as tk
import time
import os
import platform

class Gui(tk.Frame):

	def __init__(self, master = None):
		tk.Frame.__init__(self, master)
		self.row_top = tk.Frame(master)
		self.row_bot = tk.Frame(master)
		self.row_top.grid(row=0, column=0)
		self.row_bot.grid(row=1, column=0, sticky='ew', padx=(10,0))

		self.colour_scheme()
		master.configure(bg=self.bg)
		for frame in [self.row_top, self.row_bot]:
			frame.configure(bg=self.bg)

		self.add_elements()
		self.set_time()

	def colour_scheme(self):
		self.bg, self.fg, self.ac1, self.ac2, self.ac3 = ('#282828', '#CAD2C5', '#B3B3B3', '#576F72', '#7D9D9C')

	# draw/create gui elements
	def add_elements(self):
		# text area input and y-scrollbar
		# bind RETURN to text area input
		self.text_entry = tk.Text(self.row_bot, width=50, height=4, wrap='word', undo=True, insertbackground=self.ac1, selectbackground=self.ac2, inactiveselectbackground=self.ac3)
		self.text_entry.bind('<Return>', self.log_entry_event)
		self.text_entry.bind('<KP_Enter>', self.log_entry_event)
		self.scrolly = tk.Scrollbar(self.row_bot, orient='vertical', command=self.text_entry.yview)
		self.text_entry.configure(yscrollcommand=self.scrolly.set)

		# enter button
		self.button_enter = tk.Button(self.row_top, text='Enter', command=self.log_entry, activebackground=self.fg, activeforeground=self.bg, cursor='hand2')

		# time labels
		self.label_time = tk.Label(self.row_top, text='')

		# pack time, message, text area input and enter button
		# don't pack directory and filename label/entries
		# pack y-scrollbar separately
		for el in [self.label_time, self.text_entry, self.button_enter]:
			el.pack(side='left', pady=2, padx=1)
			el.configure(bg=self.bg, fg=self.fg, borderwidth=0)
		# self.scrolly.pack(side='left', fill='y')

		# focus text area input on launch
		self.text_entry.focus()

	# entry event bound to RETURN key press on text area input
	# return 'break' prevents the logging of a new line character born from RETURN key press
	def log_entry_event(self, event):
		self.log_entry()
		return 'break'

	# logging/appending to file function
	def log_entry(self):
		log_record(str(self.text_entry.get('1.0', 'end')))
		self.text_entry.delete('1.0', 'end')

	# reset gui date/time display every .3 seconds
	def set_time(self):
		self.label_time.config(text=get_time())
		self.after(333, self.set_time)

#### functional ####

# if on Windows spawns the window to the upper left of the screen
# else top of the middle
# note: I don't have access to OS X to see if it looks good or if it works
# FIXME: assumes 1920 screen width for other OSes
def get_geometry():
	if platform.system() == 'Windows':
		return '425x115+94+0'
	# elif os == 'Linux'
	# might as well use else to include OS X
	else:
		screen_width = 1920
		program_width = 390
		x_position = (screen_width - program_width) / 2
		return ('%dx115+%d+30' % (program_width, x_position))

def log_record(entry):
	try:
		# my own personal use relative path Other/myLogs.txt
		# could use full paths instead, e.g. "F:/git/sl"
		# for F:/git/sl/myLogs.txt
		path, file = ('Other', 'myLogs.txt')
		log_path = os.path.join(path, file)

		# format the log output
		# 2019.03.07 20:30:05| this is a test log.
		# append it to the log file
		log = get_time() + '| ' + str(entry).strip() + '\n'

		# REPLACE WITH BELOW LINE FOR UTF-8 ENCODING
		#with open(log_path, 'a', encoding='utf-8') as f:
		with open(log_path, 'a') as f:
			f.write(log)
	except IOError as e:
		print(e)

# get time in the most logical fashion ever invented by mankind
# ISO-8601 https://www.iso.org/iso-8601-date-and-time-format.html
# YYYY.MM.DD HH:MM:SS ex. 2019.03.07 20:30:05
# month, day, hour, minute and seconds are with leading zeroes
# 24 hour formatting to not lose much more space in time
def get_time():
	return time.strftime('%Y.%m.%d %H:%M:%S')


if __name__ == '__main__':
	root = tk.Tk(className='sl')
	# dpi problem fix for my own self, might not be an issue elsewhere
	if platform.system() == 'Linux':
		root.tk.call('tk', 'scaling', 1.3)
	root.title('Log Recorder')
	root.geometry(get_geometry())
	app = Gui(master=root)
	app.mainloop()
