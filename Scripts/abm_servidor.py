import tkinter as tk 
from tkinter import ttk, messagebox
import sys
from PIL import Image, ImageTk
from dashboard import crear_interfaz
from ABM_tipo import ProfileManagementSystem
from ABM_usuarios import UserManagementSystem
# Importar la clase de la gráfica en tiempo real
from Grafica_Tiempo_Real import RealTimeGraph

class MainInterface:
    def __init__(self, root, id_usuario):
        self.root = root
        self.id_usuario = id_usuario
        self.root.title("Sistema de Monitoreo - Menú Principal")
        self.root.geometry("800x600")
        self.root.configure(bg="#2C3E50")
        
        # Centrar la ventana
        window_width = 800
        window_height = 600
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        self.setup_ui()

    def setup_ui(self):
        # Frame principal
        main_frame = tk.Frame(self.root, bg="#34495E", bd=5)
        main_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER, relwidth=0.8, relheight=0.8)

        # Título
        title_frame = tk.Frame(main_frame, bg="#34495E")
        title_frame.pack(pady=20)
        
        title_label = tk.Label(title_frame,
                             text="SISTEMA DE MONITOREO",
                             font=("Helvetica", 24, "bold"),
                             fg="#ECF0F1",
                             bg="#34495E")
        title_label.pack()
        
        subtitle_label = tk.Label(title_frame,
                                text="Menú Principal",
                                font=("Helvetica", 14),
                                fg="#BDC3C7",
                                bg="#34495E")
        subtitle_label.pack()

        # Frame para los botones
        button_frame = tk.Frame(main_frame, bg="#34495E")
        button_frame.pack(pady=30, expand=True)

        # Estilo común para los botones
        button_style = {
            "font": ("Helvetica", 12, "bold"),
            "bg": "#1ABC9C",
            "fg": "white",
            "relief": tk.FLAT,
            "activebackground": "#148F77",
            "activeforeground": "white",
            "cursor": "hand2",
            "width": 20,
            "height": 2
        }

        # Botones principales
        buttons = [
            ("ABM Usuarios", self.abrir_abm_usuarios),
            ("ABM tipo", self.abrir_abm_tipo),
            ("Dashboard", self.abrir_dashboard),
            ("Gráfica Tiempo Real", self.abrir_grafica)  # Botón de gráfica en tiempo real
        ]

        for text, command in buttons:
            btn = tk.Button(button_frame, text=text, command=command, **button_style)
            btn.pack(pady=10)
            btn.bind("<Enter>", self.on_enter)
            btn.bind("<Leave>", self.on_leave)

        # Botón de cerrar sesión en la parte inferior
        logout_frame = tk.Frame(main_frame, bg="#34495E")
        logout_frame.pack(side=tk.BOTTOM, pady=20)
        
        logout_btn = tk.Button(logout_frame,
                             text="Cerrar Sesión",
                             command=self.cerrar_sesion,
                             font=("Helvetica", 11, "bold"),
                             bg="#E74C3C",
                             fg="white",
                             relief=tk.FLAT,
                             activebackground="#C0392B",
                             activeforeground="white",
                             cursor="hand2",
                             width=15,
                             height=1)
        logout_btn.pack()
        logout_btn.bind("<Enter>", self.on_enter_logout)
        logout_btn.bind("<Leave>", self.on_leave_logout)

    def on_enter(self, e):
        e.widget['background'] = '#148F77'

    def on_leave(self, e):
        e.widget['background'] = '#1ABC9C'

    def on_enter_logout(self, e):
        e.widget['background'] = '#C0392B'

    def on_leave_logout(self, e):
        e.widget['background'] = '#E74C3C'

    def abrir_abm_usuarios(self):
        # Crear una nueva ventana para el ABM Usuario
        usuario_window = tk.Toplevel(self.root)
        # Inicializar el sistema de gestión de Usuarios
        UserManagementSystem(usuario_window)

    def abrir_abm_tipo(self):
        # Crear una nueva ventana para el ABM tipo
        tipo_window = tk.Toplevel(self.root)
        # Inicializar el sistema de gestión de tipoes
        ProfileManagementSystem(tipo_window)

    def abrir_dashboard(self):
        crear_interfaz()

    def abrir_grafica(self):
        # Abrir la ventana con la gráfica en tiempo real
        grafica_window = tk.Toplevel(self.root)
        RealTimeGraph(grafica_window)

    def cerrar_sesion(self):
        if messagebox.askokcancel("Cerrar Sesión", "¿Está seguro que desea cerrar sesión?"):
            self.root.destroy()
            self.abrir_login()

    def abrir_login(self):
        import subprocess
        subprocess.Popen([sys.executable, 'login.py'])

def abrir_interfaz_principal(id_usuario):
    root = tk.Tk()
    app = MainInterface(root, id_usuario)
    root.mainloop()

if __name__ == "__main__":
    # Para pruebas
    root = tk.Tk()
    app = MainInterface(root, 1)  # 1 es un ID de usuario de prueba
    root.mainloop()



