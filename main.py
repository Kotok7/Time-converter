from decimal import Decimal, InvalidOperation, getcontext
import tkinter as tk
from tkinter import ttk, messagebox

getcontext().prec = 28

TRANSLATIONS = {
    'pl': {
        'title': 'Konwerter Czasu',
        'meta': 'Szybko zamieniaj sekundy, minuty, godziny, dni, miesiące i lata – np. sprawdź, ile sekund ma rok lub ile dni ma miesiąc.',
        'enter_value': 'Wpisz wartość',
        'value_help': 'Nieujemna liczba',
        'select_unit': 'Wybierz jednostkę',
        'convert': 'Konwertuj',
        'toggle_lang': 'EN',
        'result_intro': 'to:',
        'error_invalid': 'Wprowadź poprawną nieujemną wartość',
        'unit_second': 'Sekund',
        'unit_minute': 'Minut',
        'unit_hour': 'Godzin',
        'unit_day': 'Dni',
        'unit_month': 'Miesięcy',
        'unit_year': 'Lat',
    },
    'en': {
        'title': 'Time Converter',
        'meta': 'Quickly convert seconds, minutes, hours, days, months, and years – for example, find out how many seconds are in a year or how many days are in a month.',
        'enter_value': 'Enter value',
        'value_help': 'Non-negative number',
        'select_unit': 'Select unit',
        'convert': 'Convert',
        'toggle_lang': 'PL',
        'result_intro': 'is:',
        'error_invalid': 'Please enter a valid non-negative number',
        'unit_second': 'Seconds',
        'unit_minute': 'Minutes',
        'unit_hour': 'Hours',
        'unit_day': 'Days',
        'unit_month': 'Months',
        'unit_year': 'Years',
    },
}

FACTORS = {
    'second': Decimal(1),
    'minute': Decimal(60),
    'hour':   Decimal(3600),
    'day':    Decimal(86400),
    'month':  Decimal(2592000),
    'year':   Decimal(31536000),
}

UNITS_ORDER = ['second', 'minute', 'hour', 'day', 'month', 'year']

def fmt_decimal(d: Decimal) -> str:
    q = Decimal('0.00000001')
    dq = d.quantize(q)
    s = format(dq.normalize(), 'f')
    if s.endswith('.'):
        s = s[:-1]
    return s

class TimeConverterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.lang = 'en'
        self.title(TRANSLATIONS[self.lang]['title'])
        self.resizable(False, False)
        self._build_ui()
        self._refresh_texts()

    def _build_ui(self):
        pad = 10
        frame = ttk.Frame(self, padding=pad)
        frame.grid(row=0, column=0, sticky='nsew')

        header = ttk.Frame(frame)
        header.grid(row=0, column=0, sticky='ew')
        header.columnconfigure(0, weight=1)

        self.title_lbl = ttk.Label(header, text='', font=('Segoe UI', 14, 'bold'))
        self.title_lbl.grid(row=0, column=0, sticky='w')

        self.lang_btn = ttk.Button(header, text='', command=self._toggle_lang, width=4)
        self.lang_btn.grid(row=0, column=1, sticky='e')

        self.label_value = ttk.Label(frame, text='')
        self.label_value.grid(row=1, column=0, sticky='w', pady=(12,2))
        self.value_var = tk.StringVar()
        vcmd = (self.register(self._on_value_change), '%P')
        self.entry_value = ttk.Entry(frame, textvariable=self.value_var, validate='key', validatecommand=vcmd)
        self.entry_value.grid(row=2, column=0, sticky='ew')
        self.value_help = ttk.Label(frame, text='', foreground='#777777')
        self.value_help.grid(row=3, column=0, sticky='w')

        self.label_unit = ttk.Label(frame, text='')
        self.label_unit.grid(row=4, column=0, sticky='w', pady=(10,2))
        self.unit_var = tk.StringVar(value='second')
        self.unit_combo = ttk.Combobox(frame, textvariable=self.unit_var, state='readonly', values=UNITS_ORDER)

        self.unit_combo.grid(row=5, column=0, sticky='ew')

        self.convert_btn = ttk.Button(frame, text='', command=self._convert)
        self.convert_btn.grid(row=6, column=0, sticky='ew', pady=(12,0))
        self.convert_btn.state(['disabled'])

        self.result = tk.Text(frame, height=8, wrap='word', state='disabled', bg=self.cget('bg'), relief='flat')
        self.result.grid(row=7, column=0, sticky='ew', pady=(12,0))

        self.unit_display_map = {
            'second': None, 'minute': None, 'hour': None, 'day': None, 'month': None, 'year': None
        }

        self.entry_value.bind('<Return>', lambda e: self._maybe_convert())

    def _on_value_change(self, new_value):
        if new_value == '':
            self.convert_btn.state(['disabled'])
            return True
        try:
            if new_value in ('.', '-'):
                self.convert_btn.state(['disabled'])
                return True
            val = Decimal(new_value)
            if val.is_nan() or val < 0:
                self.convert_btn.state(['disabled'])
            else:
                self.convert_btn.state(['!disabled'])
            return True
        except InvalidOperation:
            return False

    def _toggle_lang(self):
        self.lang = 'pl' if self.lang == 'en' else 'en'
        self._refresh_texts()

    def _refresh_texts(self):
        T = TRANSLATIONS[self.lang]
        self.title(T['title'])
        self.title_lbl.config(text=T['title'])
        self.label_value.config(text=T['enter_value'])
        self.value_help.config(text=T['value_help'])
        self.label_unit.config(text=T['select_unit'])
        self.lang_btn.config(text=T['toggle_lang'])
        self.convert_btn.config(text=T['convert'])

        display_values = [T['unit_' + u] for u in UNITS_ORDER]
        self.unit_combo['values'] = display_values

        try:
            idx = UNITS_ORDER.index(self.unit_var.get())
        except ValueError:
            idx = 0
            self.unit_var.set(UNITS_ORDER[0])
        self.unit_combo.current(idx)

        for i, u in enumerate(UNITS_ORDER):
            self.unit_display_map[u] = display_values[i]

        self._refresh_result_area()

    def _maybe_convert(self):
        if 'disabled' in self.convert_btn.state():
            return
        self._convert()

    def _convert(self):
        T = TRANSLATIONS[self.lang]
        raw = self.value_var.get().strip()
        try:
            val = Decimal(raw)
            if val.is_nan() or val < 0:
                raise InvalidOperation
        except Exception:
            self._show_error(T['error_invalid'])
            return

        sel_idx = self.unit_combo.current()
        unit_key = UNITS_ORDER[sel_idx]
        total_seconds = val * FACTORS[unit_key]

        lines = []
        lines.append(f"{fmt_decimal(val)} {T['unit_' + unit_key]} {T['result_intro']}")
        for u in UNITS_ORDER:
            if u == unit_key:
                continue
            converted = total_seconds / FACTORS[u]
            lines.append(f"– {fmt_decimal(converted)} {T['unit_' + u]}")

        self._set_result('\n'.join(lines))

    def _show_error(self, msg):
        self._set_result(msg)

    def _set_result(self, text):
        self.result.config(state='normal')
        self.result.delete('1.0', tk.END)
        self.result.insert(tk.END, text)
        self.result.config(state='disabled')

    def _refresh_result_area(self):
        pass

if __name__ == '__main__':
    app = TimeConverterApp()
    app.mainloop()
