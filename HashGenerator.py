import datetime
import logging
import os
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk

from licencia import generar_hash_licencia


def obtener_directorio_logs() -> Path:
    app_data = os.getenv("LOCALAPPDATA")
    if app_data:
        log_dir = Path(app_data) / "HashGenerator"
    else:
        log_dir = Path.home() / ".hash_generator"
    try:
        log_dir.mkdir(parents=True, exist_ok=True)
        return log_dir
    except OSError:
        return Path(".")


log_file = obtener_directorio_logs() / "hash_generator.log"
logging.basicConfig(
    filename=str(log_file),
    level=logging.INFO,
    encoding="utf-8",
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class HashGeneratorApp(tk.Tk):
    def __init__(self):
        logging.info("Iniciando la aplicación")
        super().__init__()
        self.title("Generador de Hash de Licencia")
        self.geometry("420x520")
        self.configure(bg="#f0f0f0")
        self.cal = None
        self.hash_var = tk.StringVar()
        self.clave_var = tk.StringVar(value=os.getenv("LICENSE_SECRET_KEY", ""))
        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="20 20 20 20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        ttk.Label(main_frame, text="Clave Secreta de Firma:").grid(column=0, row=0, sticky=tk.W, pady=2)
        clave_entry = ttk.Entry(main_frame, textvariable=self.clave_var, show="*", width=30)
        clave_entry.grid(column=0, row=1, sticky=(tk.W, tk.E), pady=4)

        ttk.Label(main_frame, text="Seleccione la fecha de caducidad:").grid(column=0, row=2, sticky=tk.W, pady=(10, 2))
        try:
            from tkcalendar import Calendar
            today = datetime.date.today()
            self.cal = Calendar(main_frame, selectmode="day", year=today.year, month=today.month, day=today.day)
            self.cal.grid(column=0, row=3, sticky=(tk.W, tk.E), pady=5)
            logging.info("Calendario creado exitosamente")
        except Exception as e:
            logging.error(f"Error al crear el calendario: {e}")
            messagebox.showerror("Error", f"No se pudo crear el calendario: {e}")

        generate_button = ttk.Button(main_frame, text="Generar Hash", command=self.generate_hash)
        generate_button.grid(column=0, row=4, sticky=tk.W, pady=15)

        ttk.Label(main_frame, text="Hash generado:").grid(column=0, row=5, sticky=tk.W, pady=2)
        hash_entry = ttk.Entry(main_frame, textvariable=self.hash_var, state="readonly", width=30)
        hash_entry.grid(column=0, row=6, sticky=(tk.W, tk.E), pady=5)

        copy_button = ttk.Button(main_frame, text="Copiar al portapapeles", command=self.copy_to_clipboard)
        copy_button.grid(column=0, row=7, sticky=tk.W, pady=10)

        for child in main_frame.winfo_children():
            child.grid_configure(padx=5)
        main_frame.columnconfigure(0, weight=1)

    def generate_hash(self):
        if not self.cal:
            messagebox.showerror("Error", "El calendario no está inicializado.")
            return

        clave = self.clave_var.get().strip()
        if not clave:
            messagebox.showwarning("Advertencia", "Debe ingresar una clave secreta para generar el hash.")
            return

        try:
            fecha_seleccionada = self.cal.selection_get()
            if isinstance(fecha_seleccionada, datetime.date):
                fecha = fecha_seleccionada
            else:
                fecha = datetime.datetime.strptime(str(fecha_seleccionada), "%m/%d/%y").date()

            hash_resultado = generar_hash_licencia(fecha, clave)
            self.hash_var.set(hash_resultado)
            logging.info("Hash generado exitosamente para la fecha seleccionada.")
        except Exception as e:
            logging.error(f"Error al generar hash: {e}")
            messagebox.showerror("Error", f"No se pudo generar el hash: {e}")

    def copy_to_clipboard(self):
        hash_value = self.hash_var.get()
        if hash_value:
            self.clipboard_clear()
            self.clipboard_append(hash_value)
            self.update()
            messagebox.showinfo("Copiado", "El hash ha sido copiado al portapapeles.")
            logging.info("Hash copiado al portapapeles")
        else:
            messagebox.showwarning("Advertencia", "No hay hash para copiar.")


if __name__ == "__main__":
    try:
        app = HashGeneratorApp()
        app.mainloop()
    except Exception as e:
        logging.critical(f"Error crítico en la aplicación: {e}")
        messagebox.showerror("Error Crítico", f"La aplicación ha encontrado un error crítico: {e}")