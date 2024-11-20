import tkinter as tk
from tkinter import ttk
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class RealTimeGraph:
    def __init__(self, root):
        self.root = root
        self.root.title("Gráfica en Tiempo Real - Sonómetro IoT")
        self.root.geometry("1000x600")

        # Configuración de la base de datos
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': '',
            'database': 'sonometro_IOT',
        }

        self.setup_ui()
        self.is_running = False

    def setup_ui(self):
        # Frame principal
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Configuración del gráfico
        self.fig = Figure(figsize=(10, 6))
        self.ax = self.fig.add_subplot(111)

        # Canvas para el gráfico
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.main_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Botones de control
        self.control_frame = ttk.Frame(self.root)
        self.control_frame.pack(fill=tk.X, padx=10, pady=5)

        self.start_button = ttk.Button(self.control_frame, text="Iniciar", command=self.start_update)
        self.start_button.pack(side=tk.LEFT, padx=5)

        self.stop_button = ttk.Button(self.control_frame, text="Detener", command=self.stop_update)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        self.stop_button.state(['disabled'])  # Desactivar el botón "Detener" al inicio

    def get_data(self):
        try:
            conn = mysql.connector.connect(**self.db_config)
            query = "SELECT * FROM registro ORDER BY idRegistro DESC LIMIT 50"
            data = pd.read_sql(query, conn)
            conn.close()
            return data
        except mysql.connector.nivelSonido2 as e:
            print(f"nivelSonido2 de base de datos: {e}")
            return None

    def update_graph(self):
        if not self.is_running:
            return

        data = self.get_data()

        if data is not None and not data.empty:
            # Limpiar el gráfico anterior
            self.ax.clear()

            # Invertir el orden para mostrar los datos más recientes a la derecha
            data = data.iloc[::-1]

            # Graficar los datos
            self.ax.plot(data['idRegistro'], data['nivelSonido1'], label='Nivel de Sonido', color='blue')
            self.ax.plot(data['idRegistro'], data['nivelSonido3'], label='nivelSonido3', color='orange')
            self.ax.plot(data['idRegistro'], data['nivelSonido2'], label='nivelSonido2', color='red')

            # Configuración del gráfico
            self.ax.set_title('Comparación entre nivel de sonido 1, nivel Sonido 2 y nivel Sonido 3')
            self.ax.set_xlabel('ID Registro')
            self.ax.set_ylabel('Valores')
            self.ax.legend()
            self.ax.grid(True)

            # Rotar las etiquetas del eje x para mejor legibilidad
            plt.setp(self.ax.get_xticklabels(), rotation=45)

            # Ajustar el diseño
            self.fig.tight_layout()

            # Actualizar el canvas
            self.canvas.draw()

        # Programar la próxima actualización
        if self.is_running:
            self.root.after(1000, self.update_graph)  # Actualizar cada segundo

    def start_update(self):
        self.is_running = True
        self.update_graph()
        self.start_button.state(['disabled'])  # Desactivar el botón "Iniciar"
        self.stop_button.state(['!disabled'])  # Activar el botón "Detener"

    def stop_update(self):
        self.is_running = False
        self.start_button.state(['!disabled'])  # Activar el botón "Iniciar"
        self.stop_button.state(['disabled'])  # Desactivar el botón "Detener"

def main():
    root = tk.Tk()
    app = RealTimeGraph(root)
    root.mainloop()

if __name__ == "__main__":
    main()
