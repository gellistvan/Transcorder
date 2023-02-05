import tkinter as tk
import json

from tkinter import filedialog
from recorder import Recorder

from tkinter import ttk

class RecorderWindow(tk.Tk):
    instance: Recorder
    _file_output: ttk.Entry
    _book_path_entry: ttk.Entry
    _book_path_browse_button: ttk.Button
    _record_button: ttk.Button
    _clipboard_button: ttk.Button
    _lang_toggle: ttk.Checkbutton
    _on_button: ttk.Button
    hun = ''
    eng = ''
    in_progress = False

    def on_file_browser_button_pressed(self, file_type: str, path: tk.StringVar, entry: ttk.Entry):
        filename = filedialog.askopenfilename(filetypes=(("Text files: ", "*.txt"), ("All files: ", "*.*")))
        path.set(filename)
        entry.xview_moveto(1)
        self.instance.output_path = filename

    def _init_source_frame(self):
        book_path_frame = ttk.Frame(self)
        book_path_frame.pack(padx=0, pady=0, fill='x', expand=True)

        book_path_label = ttk.Label(book_path_frame, text="Output file path:")
        book_path_label.pack(fill='x', expand=True)

        book_path_frame.book_path = tk.StringVar()
        self._book_path_entry = ttk.Entry(book_path_frame, textvariable=book_path_frame.book_path)
        self._book_path_entry.pack(fill=tk.X, expand=True, side=tk.LEFT, padx=2, ipady=1)

        self._book_path_browse_button = ttk.Button(book_path_frame, text="Browse",
              command=lambda: self.on_file_browser_button_pressed("text", book_path_frame.book_path, self._book_path_entry))
        self._book_path_browse_button.pack(fill=tk.BOTH, expand=True, padx=2)

    def init_button_frame(self):

        background_music_path_frame = ttk.Frame(self)
        background_music_path_frame.pack(padx=0, pady=0, fill='x', expand=True)

        record_button_style = ttk.Style()
        record_button_style.configure('Record.TButton',
                width='3',
                foreground='red',
                highlightthickness='20',
                font=('Helvetica', 20, 'bold'))

        stop_button_style = ttk.Style()
        stop_button_style.configure('Stop.TButton',
                width='3',
                foreground='gray',
                highlightthickness='20',
                font=('Helvetica', 20, 'bold'))

        clipboard_button_style = ttk.Style()
        clipboard_button_style.configure('Clipboard.TButton',
                width='3',
                highlightthickness='20',
                foreground='gray',
                font=('Helvetica', 20, 'bold'))
        clipboard_on_button_style = ttk.Style()
        clipboard_on_button_style.configure('Clipboard.On.TButton',
                width='3',
                highlightthickness='20',
                foreground='green',
                font=('Helvetica', 20, 'bold'))

        self._record_button \
            = ttk.Button(background_music_path_frame, style='Record.TButton', text="⬤", command=self.on_record)
        self._record_button.pack(fill=tk.Y, padx=2, side=tk.LEFT)

        self._clipboard_button = ttk.Button(background_music_path_frame, style='Clipboard.TButton', text="📋", command=self.on_clipboard)
        self._clipboard_button.pack(fill=tk.Y, padx=2, side=tk.LEFT)

        self.hun = tk.PhotoImage(file = "hun.png")
        self.eng = tk.PhotoImage(file = "eng.png")
        self._on_button = ttk.Button(background_music_path_frame, style='transparent.TButton',
                                     image = self.hun, command = self.switch, padding='0 10 0 10')
        self._on_button.pack(fill=tk.Y, padx=2, side=tk.RIGHT)

    def on_record(self):
        if self.in_progress:
            self._record_button.configure(text='⬤', style='Record.TButton')
            self.instance.Stop()
        else:
            self._record_button.configure(text='⏹', style='Stop.TButton')
            self.instance.Start()
        self.in_progress = not self.in_progress

    def switch(self):
        # Determine is on or off
        self.instance.dictate_hungarian = not self.instance.dictate_hungarian
        if self.instance.dictate_hungarian:
            self._on_button.config(image = self.hun)
        else:
            self._on_button.config(image = self.eng)

    def on_clipboard(self):
        self.instance.clipboard_enabled = not self.instance.clipboard_enabled
        if self.instance.clipboard_enabled:
            self._clipboard_button.configure(style='Clipboard.On.TButton')
        else:self._clipboard_button.configure(style='Clipboard.TButton')

    def __init__(self):
        super().__init__()

        self.title("Recorder")
        self.geometry("250x100")
        self.resizable(False, False)

        with open("dictaphone_config.json", "r") as file:
            data = json.load(file)
            subscription = data["subscription"]
            region = data["region"]
            self.instance = Recorder(subscription, region)

        self.init_button_frame()
        self._init_source_frame()

window = RecorderWindow()
window.iconbitmap("dictaphone.ico")

window.attributes('-topmost', True)

def handle_shortcut():
    window.on_record()

#window.bind('<Control-Shift-space>', handle_shortcut)

import keyboard
keyboard.add_hotkey('ctrl+shift+space', handle_shortcut)


window.mainloop()