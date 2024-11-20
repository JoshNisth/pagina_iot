import mysql.connector
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from abm_servidor import abrir_interfaz_principal

def conectar():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="sonometro_IOT",
        )
        return conexion
    except mysql.connector.Error as err:
        messagebox.showerror("Error de conexión", f"No se pudo conectar a la base de datos: {err}")
        return None

def verificar_login():
    usuario = entry_usuario.get()
    contrasena = entry_contrasena.get()
    
    # Verificar credenciales en la base de datos
    conexion = conectar()
    if conexion:
        try:
            cursor = conexion.cursor()
            query = "SELECT idUsuario, nombreUsuario FROM usuario WHERE nombreUsuario = %s AND password = %s"
            cursor.execute(query, (usuario, contrasena))
            resultado = cursor.fetchone()
            
            if resultado:
                id_usuario = resultado[0]
                messagebox.showinfo("Login exitoso", f"Bienvenido {resultado[1]}")
                root.destroy()
                abrir_interfaz_principal(id_usuario)
            else:
                messagebox.showerror("Error", "Usuario o contraseña incorrectos.")
            
            cursor.close()
            conexion.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error en la base de datos: {err}")

def on_enter(e):
    e.widget['background'] = '#148F77'

def on_leave(e):
    e.widget['background'] = '#1ABC9C'

# Configuración de la ventana principal
root = Tk()
root.title("Sistema de Monitoreo - Login")
root.geometry("500x400")
root.configure(bg="#2C3E50")

# Centrar la ventana
window_width = 500
window_height = 400
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
center_x = int(screen_width/2 - window_width/2)
center_y = int(screen_height/2 - window_height/2)
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

# Frame principal
frame_login = Frame(root, bg="#34495E", bd=5)
frame_login.place(relx=0.5, rely=0.5, anchor=CENTER, width=400, height=300)

# Título con mejor diseño
title_frame = Frame(frame_login, bg="#34495E")
title_frame.pack(pady=20)
title_label = Label(title_frame, 
                   text="SISTEMA DE MONITOREO", 
                   font=("Helvetica", 20, "bold"), 
                   fg="#ECF0F1", 
                   bg="#34495E")
title_label.pack()
subtitle_label = Label(title_frame, 
                      text="Inicio de Sesión", 
                      font=("Helvetica", 12), 
                      fg="#BDC3C7", 
                      bg="#34495E")
subtitle_label.pack()

# Frame para los campos de entrada
entry_frame = Frame(frame_login, bg="#34495E")
entry_frame.pack(pady=20, padx=40, fill=X)

# Usuario
Label(entry_frame, text="Usuario", 
      font=("Helvetica", 12), 
      fg="#ECF0F1", 
      bg="#34495E").pack(anchor=W)
entry_usuario = Entry(entry_frame, 
                     font=("Helvetica", 12), 
                     bg="#ECF0F1", 
                     fg="#2C3E50", 
                     bd=0, 
                     relief=FLAT)
entry_usuario.pack(fill=X, pady=(0, 15))

# Contraseña
Label(entry_frame, text="Contraseña", 
      font=("Helvetica", 12), 
      fg="#ECF0F1", 
      bg="#34495E").pack(anchor=W)
entry_contrasena = Entry(entry_frame, 
                        font=("Helvetica", 12), 
                        bg="#ECF0F1", 
                        fg="#2C3E50", 
                        bd=0, 
                        relief=FLAT, 
                        show="•")
entry_contrasena.pack(fill=X)

# Botón de login con efectos hover
btn_login = Button(frame_login, 
                  text="INICIAR SESIÓN", 
                  font=("Helvetica", 12, "bold"), 
                  bg="#1ABC9C", 
                  fg="white", 
                  relief=FLAT, 
                  activebackground="#148F77", 
                  activeforeground="white", 
                  cursor="hand2", 
                  command=verificar_login)
btn_login.pack(pady=0, padx=0, fill=X)

# Agregar efectos hover al botón
btn_login.bind("<Enter>", on_enter)
btn_login.bind("<Leave>", on_leave)

# Vincular la tecla Enter para iniciar sesión
root.bind('<Return>', lambda e: verificar_login())

root.mainloop()