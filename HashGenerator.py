import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
import hashlib
import datetime
import sys
import os
import logging

# Código de diagnóstico
import babel
print("Babel version:", babel.__version__)
print("Babel path:", babel.__file__)
try:
    import babel.numbers
    print("babel.numbers importado correctamente")
except ImportError as e:
    print("Error importando babel.numbers:", str(e))

# Configurar logging
logging.basicConfig(filename='hash_generator.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class HashGeneratorApp(tk.Tk):
    def __init__(self):
        logging.info("Iniciando la aplicación")
        super().__init__()
        self.title("Generador de Hash de Licencia")
        self.geometry("400x450")
        self.configure(bg='#f0f0f0')
        self.create_widgets()

    def create_widgets(self):
        logging.info("Creando widgets")
        main_frame = ttk.Frame(self, padding="20 20 20 20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        ttk.Label(main_frame, text="Seleccione la fecha de caducidad:").grid(column=0, row=0, sticky=tk.W, pady=5)
        try:
            self.cal = Calendar(main_frame, selectmode='day', year=datetime.date.today().year, 
                                month=datetime.date.today().month, day=datetime.date.today().day)
            self.cal.grid(column=0, row=1, sticky=(tk.W, tk.E), pady=5)
            logging.info("Calendario creado exitosamente")
        except Exception as e:
            logging.error(f"Error al crear el calendario: {str(e)}")
            messagebox.showerror("Error", f"No se pudo crear el calendario: {str(e)}")

        generate_button = ttk.Button(main_frame, text="Generar Hash", command=self.generate_hash)
        generate_button.grid(column=0, row=2, sticky=tk.W, pady=20)

        ttk.Label(main_frame, text="Hash generado:").grid(column=0, row=3, sticky=tk.W, pady=5)
        self.hash_var = tk.StringVar()
        hash_entry = ttk.Entry(main_frame, textvariable=self.hash_var, state='readonly', width=30)
        hash_entry.grid(column=0, row=4, sticky=(tk.W, tk.E), pady=5)

        copy_button = ttk.Button(main_frame, text="Copiar al portapapeles", command=self.copy_to_clipboard)
        copy_button.grid(column=0, row=5, sticky=tk.W, pady=10)

        for child in main_frame.winfo_children(): 
            child.grid_configure(padx=5)
        main_frame.columnconfigure(0, weight=1)
        logging.info("Widgets creados exitosamente")

    def generate_hash(self):
        logging.info("Generando hash")
        try:
            fecha_str = self.cal.get_date()
            fecha = datetime.datetime.strptime(fecha_str, "%m/%d/%y")
            clave = "291292"
            combinacion = f"{fecha.strftime('%d/%m/%Y')}:{clave}"
            hash_completo = hashlib.sha1(combinacion.encode()).hexdigest()
            hash_resultado = hash_completo[:12]
            self.hash_var.set(hash_resultado)
            logging.info(f"Hash generado: {hash_resultado}")
        except Exception as e:
            logging.error(f"Error al generar hash: {str(e)}")
            messagebox.showerror("Error", f"No se pudo generar el hash: {str(e)}")

    def copy_to_clipboard(self):
        logging.info("Copiando al portapapeles")
        hash_value = self.hash_var.get()
        if hash_value:
            self.clipboard_clear()
            self.clipboard_append(hash_value)
            self.update()
            messagebox.showinfo("Copiado", "El hash ha sido copiado al portapapeles.")
            logging.info("Hash copiado al portapapeles")
        else:
            messagebox.showwarning("Advertencia", "No hay hash para copiar.")
            logging.warning("Intento de copiar hash vacío")

if __name__ == "__main__":
    try:
        app = HashGeneratorApp()
        app.mainloop()
    except Exception as e:
        logging.critical(f"Error crítico en la aplicación: {str(e)}")
        messagebox.showerror("Error Crítico", f"La aplicación ha encontrado un error crítico: {str(e)}")