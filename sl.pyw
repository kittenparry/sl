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

	def add_elements(self):
		self.text_entry = tk.Text(self.row_bot, width=50, height=4, wrap='word', undo=True, insertbackground=self.ac1, selectbackground=self.ac2, inactiveselectbackground=self.ac3)
		self.text_entry.bind('<Return>', self.log_entry_event)
		self.text_entry.bind('<KP_Enter>', self.log_entry_event)
		self.scrolly = tk.Scrollbar(self.row_bot, orient='vertical', command=self.text_entry.yview)
		self.text_entry.configure(yscrollcommand=self.scrolly.set)

		self.button_enter = tk.Button(self.row_top, text='Enter', command=self.log_entry, activebackground=self.fg, activeforeground=self.bg, cursor='hand2')

		self.label_time = tk.Label(self.row_top, text='')

		for el in [self.label_time, self.text_entry, self.button_enter]:
			el.pack(side='left', pady=2, padx=1)
			el.configure(bg=self.bg, fg=self.fg, borderwidth=0)

		self.text_entry.focus()

	def log_entry_event(self, event):
		self.log_entry()
		return 'break'

	def log_entry(self):
		log_record(str(self.text_entry.get('1.0', 'end')))
		self.text_entry.delete('1.0', 'end')

	def set_time(self):
		self.label_time.config(text=get_time())
		self.after(333, self.set_time)


def get_geometry():
	if platform.system() == 'Windows':
		return '425x115+94+0'
	else:
		screen_width, program_width = (1920, 390)
		x_position = (screen_width - program_width) / 2
		return ('%dx115+%d+30' % (program_width, x_position))

def log_record(entry):
	try:
		path, file = ('Other', 'myLogs.txt')
		log_path = os.path.join(path, file)

		log = get_time() + '| ' + str(entry).strip() + '\n'
		with open(log_path, 'a', encoding='utf-8') as f:
			f.write(log)
	except IOError as e:
		print(e)

def get_time():
	return time.strftime('%Y.%m.%d %H:%M:%S')


if __name__ == '__main__':
	root = tk.Tk(className='sl')
	if platform.system() == 'Linux':
		root.tk.call('tk', 'scaling', 1.3)
	root.title('Log Recorder')
	root.geometry(get_geometry())
	app = Gui(master=root)
	app.mainloop()
