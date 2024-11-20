import tkinter as tk
from tkinter import messagebox, Toplevel
import mysql.connector
import re
import string

class UserManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Usuarios - Sonómetro IoT")
        self.root.geometry("500x400")
        self.root.configure(bg="#F0F4F8")
        
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="sonometro_IOT",
            )
            self.cursor = self.conn.cursor()
        except mysql.connector.Error as err:
            messagebox.showerror("Error de Conexión", f"No se pudo conectar a la base de datos: {err}")
            root.destroy()
            return

        self.setup_ui()

    def setup_ui(self):
        label_style = {"font": ("Arial", 10, "bold"), "bg": "#F0F4F8"}
        entry_style = {"width": 30, "font": ("Arial", 10)}
        button_style = {
            "font": ("Arial", 10, "bold"),
            "bg": "#4CAF50",
            "fg": "white",
            "padx": 10,
            "pady": 5,
            "width": 10
        }

        self.form_frame = tk.Frame(self.root, bg="#F0F4F8", pady=10)
        self.form_frame.pack()

        tk.Label(self.form_frame, text="ID Usuario", **label_style).grid(row=0, column=0, sticky="w", pady=2)
        self.entry_id = tk.Entry(self.form_frame, **entry_style)
        self.entry_id.grid(row=0, column=1, padx=10, pady=2)

        tk.Label(self.form_frame, text="Nombre Usuario", **label_style).grid(row=1, column=0, sticky="w", pady=2)
        self.entry_nombre = tk.Entry(self.form_frame, **entry_style)
        self.entry_nombre.grid(row=1, column=1, padx=10, pady=2)

        tk.Label(self.form_frame, text="Contraseña", **label_style).grid(row=2, column=0, sticky="w", pady=2)
        self.entry_password = tk.Entry(self.form_frame, show="*", **entry_style)
        self.entry_password.grid(row=2, column=1, padx=10, pady=2)

        tk.Label(self.form_frame, text="tipo ID", **label_style).grid(row=3, column=0, sticky="w", pady=2)
        self.entry_tipo_id = tk.Entry(self.form_frame, **entry_style)
        self.entry_tipo_id.grid(row=3, column=1, padx=10, pady=2)

        button_frame = tk.Frame(self.root, bg="#F0F4F8")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Alta", command=self.alta_usuario, **button_style).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Baja", command=self.baja_usuario, **button_style).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Modificar", command=self.modificar_usuario, **button_style).grid(row=0, column=2, padx=5)
        tk.Button(button_frame, text="Mostrar", command=self.mostrar_usuarios_detallado, **button_style).grid(row=0, column=3, padx=5)

        self.listbox_usuarios = tk.Listbox(self.root, width=60, height=10, font=("Arial", 10))
        self.listbox_usuarios.pack(pady=10)

        self.mostrar_usuarios()

    def validar_nombre_usuario(self, nombre):
        """Valida el formato del nombre de usuario."""
        if not 3 <= len(nombre) <= 50:
            raise ValueError("El nombre debe tener entre 3 y 50 caracteres")
        if not re.match("^[a-zA-Z_]+$", nombre):  # Modificado para no aceptar números
            raise ValueError("El nombre solo puede contener letras y guiones bajos")
        return True

    def mostrar_usuarios_detallado(self):
        """Muestra una nueva ventana con los detalles de todos los usuarios."""
        try:
            # Crear nueva ventana
            detalle_window = Toplevel(self.root)
            detalle_window.title("Detalle de Usuarios")
            detalle_window.geometry("600x400")
            detalle_window.configure(bg="#F0F4F8")

            # Crear Treeview
            from tkinter import ttk
            tree = ttk.Treeview(detalle_window, columns=("ID", "Usuario", "tipo ID", "Nombre tipo"), show="headings")

            # Definir columnas
            tree.heading("ID", text="ID")
            tree.heading("Usuario", text="Usuario")
            tree.heading("tipo ID", text="tipo ID")
            tree.heading("Nombre tipo", text="Nombre tipo")

            # Configurar anchos de columna
            tree.column("ID", width=50)
            tree.column("Usuario", width=150)
            tree.column("tipo ID", width=100)
            tree.column("Nombre tipo", width=150)

            # Obtener datos detallados
            self.cursor.execute("""
                SELECT u.idUsuario, u.nombreUsuario, u.tipo_idtipo, 
                       p.nombretipo
                FROM usuario u 
                JOIN tipo p ON u.tipo_idtipo = p.idtipo
                ORDER BY u.idUsuario
            """)
            usuarios = self.cursor.fetchall()

            # Insertar datos en el Treeview
            for usuario in usuarios:
                tree.insert("", "end", values=usuario)

            # Agregar scrollbar
            scrollbar = ttk.Scrollbar(detalle_window, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)

            # Empaquetar elementos
            tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
            scrollbar.pack(side="right", fill="y", pady=10)

            # Botón para cerrar
            tk.Button(detalle_window, text="Cerrar", 
                     command=detalle_window.destroy,
                     font=("Arial", 10, "bold"),
                     bg="#4CAF50",
                     fg="white",
                     padx=10,
                     pady=5).pack(pady=10)

        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error al cargar detalles de usuarios: {e}")
    # El resto de métodos permanece igual
    def validar_password(self, password):
        """Valida el formato de la contraseña."""
        if not 3 <= len(password) <= 50:
            raise ValueError("La contraseña debe tener entre 3 y 50 caracteres")
        return True

    def validar_tipo_id(self, tipo_id):
        """Valida que el tipo existe en la base de datos."""
        try:
            tipo_id = int(tipo_id)
            self.cursor.execute("SELECT idtipo FROM tipo WHERE idtipo = %s", (tipo_id,))
            if not self.cursor.fetchone():
                raise ValueError("El tipo especificado no existe")
            return True
        except ValueError as e:
            if "invalid literal for int()" in str(e):
                raise ValueError("El ID de tipo debe ser un número")
            raise

    def limpiar_campos(self):
        """Limpia todos los campos de entrada."""
        self.entry_id.delete(0, tk.END)
        self.entry_nombre.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)
        self.entry_tipo_id.delete(0, tk.END)

    def alta_usuario(self):
        """Agrega un nuevo usuario con validaciones."""
        try:
            nombre = self.entry_nombre.get().strip()
            password = self.entry_password.get().strip()
            tipo_id = self.entry_tipo_id.get().strip()

            if not all([nombre, password, tipo_id]):
                raise ValueError("Todos los campos son obligatorios")

            self.validar_nombre_usuario(nombre)
            self.validar_password(password)
            self.validar_tipo_id(tipo_id)

            self.cursor.execute("SELECT idUsuario FROM usuario WHERE nombreUsuario = %s", (nombre,))
            if self.cursor.fetchone():
                raise ValueError("El nombre de usuario ya existe")

            self.cursor.execute(
                "INSERT INTO usuario (nombreUsuario, password, tipo_idtipo) VALUES (%s, %s, %s)",
                (nombre, password, tipo_id)
            )
            self.conn.commit()
            messagebox.showinfo("Éxito", "Usuario agregado correctamente")
            self.limpiar_campos()
            self.mostrar_usuarios()

        except ValueError as e:
            messagebox.showerror("Error de Validación", str(e))
        except mysql.connector.Error as e:
            messagebox.showerror("Error de Base de Datos", f"Error al agregar usuario: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {e}")

    def baja_usuario(self):
        """Elimina un usuario con validaciones."""
        try:
            user_id = self.entry_id.get().strip()
            if not user_id:
                raise ValueError("Debe especificar el ID del usuario")

            try:
                user_id = int(user_id)
            except ValueError:
                raise ValueError("El ID debe ser un número")

            self.cursor.execute("SELECT COUNT(*) FROM registro WHERE usuario_idUsuario = %s", (user_id,))
            if self.cursor.fetchone()[0] > 0:
                raise ValueError("No se puede eliminar el usuario porque tiene registros asociados")

            self.cursor.execute("DELETE FROM usuario WHERE idUsuario = %s", (user_id,))
            self.conn.commit()

            if self.cursor.rowcount > 0:
                messagebox.showinfo("Éxito", "Usuario eliminado correctamente")
                self.limpiar_campos()
                self.mostrar_usuarios()
            else:
                raise ValueError("No se encontró el usuario con ese ID")

        except ValueError as e:
            messagebox.showerror("Error de Validación", str(e))
        except mysql.connector.Error as e:
            messagebox.showerror("Error de Base de Datos", f"Error al eliminar usuario: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {e}")

    def modificar_usuario(self):
        """Modifica un usuario con validaciones."""
        try:
            user_id = self.entry_id.get().strip()
            nombre = self.entry_nombre.get().strip()
            password = self.entry_password.get().strip()
            tipo_id = self.entry_tipo_id.get().strip()

            if not user_id:
                raise ValueError("Debe especificar el ID del usuario")

            self.cursor.execute("SELECT * FROM usuario WHERE idUsuario = %s", (user_id,))
            if not self.cursor.fetchone():
                raise ValueError("No existe un usuario con ese ID")

            update_fields = []
            params = []
            
            if nombre:
                self.validar_nombre_usuario(nombre)
                update_fields.append("nombreUsuario = %s")
                params.append(nombre)
                
            if password:
                self.validar_password(password)
                update_fields.append("password = %s")
                params.append(password)
                
            if tipo_id:
                self.validar_tipo_id(tipo_id)
                update_fields.append("tipo_idtipo = %s")
                params.append(tipo_id)

            if not update_fields:
                raise ValueError("Debe especificar al menos un campo para modificar")

            query = f"UPDATE usuario SET {', '.join(update_fields)} WHERE idUsuario = %s"
            params.append(user_id)
            
            self.cursor.execute(query, tuple(params))
            self.conn.commit()

            messagebox.showinfo("Éxito", "Usuario modificado correctamente")
            self.limpiar_campos()
            self.mostrar_usuarios()

        except ValueError as e:
            messagebox.showerror("Error de Validación", str(e))
        except mysql.connector.Error as e:
            messagebox.showerror("Error de Base de Datos", f"Error al modificar usuario: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {e}")

    def mostrar_usuarios(self):
        """Muestra la lista básica de usuarios en el listbox principal."""
        try:
            self.cursor.execute("""
                SELECT u.idUsuario, u.nombreUsuario, p.nombretipo 
                FROM usuario u 
                JOIN tipo p ON u.tipo_idtipo = p.idtipo
            """)
            usuarios = self.cursor.fetchall()
            
            self.listbox_usuarios.delete(0, tk.END)
            for usuario in usuarios:
                self.listbox_usuarios.insert(tk.END, 
                    f"ID: {usuario[0]}, Usuario: {usuario[1]}, tipo: {usuario[2]}")

        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error al cargar usuarios: {e}")

    def __del__(self):
        """Cierra la conexión a la base de datos al cerrar la aplicación."""
        if hasattr(self, 'conn') and self.conn.is_connected():
            self.cursor.close()
            self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = UserManagementSystem(root)
    root.mainloop()
