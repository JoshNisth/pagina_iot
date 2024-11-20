import tkinter as tk
from tkinter import messagebox, Toplevel, ttk
import mysql.connector
import re

class ProfileManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Perfiles - Sonómetro IoT")
        self.root.geometry("500x400")
        self.root.configure(bg="#F0F4F8")
        
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="sonometro_IOT"
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

        # Campo ID Perfil
        tk.Label(self.form_frame, text="ID Perfil", **label_style).grid(row=0, column=0, sticky="w", pady=2)
        self.entry_id = tk.Entry(self.form_frame, **entry_style)
        self.entry_id.grid(row=0, column=1, padx=10, pady=2)

        # Campo Nombre Perfil con validación en tiempo real
        tk.Label(self.form_frame, text="Nombre Perfil", **label_style).grid(row=1, column=0, sticky="w", pady=2)
        self.entry_nombre = tk.Entry(self.form_frame, **entry_style)
        self.entry_nombre.grid(row=1, column=1, padx=10, pady=2)
        self.entry_nombre.bind('<KeyRelease>', self.validar_entrada_nombre)

        # Campo Límite Máximo con validación en tiempo real
        tk.Label(self.form_frame, text="Límite Máximo", **label_style).grid(row=2, column=0, sticky="w", pady=2)
        self.entry_limite = tk.Entry(self.form_frame, **entry_style)
        self.entry_limite.grid(row=2, column=1, padx=10, pady=2)
        self.entry_limite.bind('<KeyRelease>', self.validar_entrada_limite)

        button_frame = tk.Frame(self.root, bg="#F0F4F8")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Alta", command=self.alta_perfil, **button_style).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Baja", command=self.baja_perfil, **button_style).grid(row=0, column=1, padx=5)
        tk.Button(button_frame, text="Modificar", command=self.modificar_perfil, **button_style).grid(row=0, column=2, padx=5)
        tk.Button(button_frame, text="Mostrar", command=self.mostrar_perfiles_detallado, **button_style).grid(row=0, column=3, padx=5)

        self.listbox_perfiles = tk.Listbox(self.root, width=60, height=10, font=("Arial", 10))
        self.listbox_perfiles.pack(pady=10)

        # Label para mensajes de validación
        self.label_validacion = tk.Label(self.root, text="", fg="red", bg="#F0F4F8")
        self.label_validacion.pack(pady=5)

        self.mostrar_perfiles()

    def validar_entrada_nombre(self, event=None):
        """Valida la entrada del nombre en tiempo real."""
        nombre = self.entry_nombre.get()
        if nombre:
            if not nombre.replace(' ', '').isalpha():
                self.label_validacion.config(text="El nombre solo puede contener letras y espacios")
                self.entry_nombre.config(bg="#FFE6E6")  # Fondo rojo claro
            else:
                self.label_validacion.config(text="")
                self.entry_nombre.config(bg="white")

    def validar_entrada_limite(self, event=None):
        """Valida la entrada del límite en tiempo real."""
        limite = self.entry_limite.get()
        if limite:
            # Permitir números enteros y decimales (con punto o coma)
            limite = limite.replace(',', '.')
            patron = r'^\d*\.?\d*$'
            if not re.match(patron, limite):
                self.label_validacion.config(text="El límite solo puede contener números y un punto decimal")
                self.entry_limite.config(bg="#FFE6E6")  # Fondo rojo claro
            else:
                self.label_validacion.config(text="")
                self.entry_limite.config(bg="white")

    def validar_nombre_perfil(self, nombre):
        """Valida el formato del nombre del perfil."""
        if not 3 <= len(nombre) <= 100:
            raise ValueError("El nombre debe tener entre 3 y 100 caracteres")
        if not nombre.replace(' ', '').isalpha():
            raise ValueError("El nombre solo puede contener letras y espacios")
        return True

    def validar_limite(self, limite):
        """Valida que el límite sea un número flotante válido y positivo."""
        try:
            # Reemplazar coma por punto para el procesamiento
            limite = limite.replace(',', '.')
            limite_float = float(limite)
            if limite_float <= 0:
                raise ValueError("El límite debe ser un número positivo")
            return limite_float
        except ValueError:
            raise ValueError("El límite debe ser un número válido")

    def mostrar_perfiles_detallado(self):
        """Muestra una nueva ventana con los detalles de todos los perfiles."""
        try:
            detalle_window = Toplevel(self.root)
            detalle_window.title("Detalle de Perfiles")
            detalle_window.geometry("600x400")
            detalle_window.configure(bg="#F0F4F8")

            tree = ttk.Treeview(detalle_window, columns=("ID", "Nombre", "Límite"), show="headings")

            tree.heading("ID", text="ID")
            tree.heading("Nombre", text="Nombre del Perfil")
            tree.heading("Límite", text="Límite Máximo")

            tree.column("ID", width=100)
            tree.column("Nombre", width=250)
            tree.column("Límite", width=150)

            self.cursor.execute("SELECT * FROM perfil ORDER BY idPerfil")
            perfiles = self.cursor.fetchall()

            for perfil in perfiles:
                tree.insert("", "end", values=(perfil[0], perfil[1], f"{perfil[2]:.2f}"))

            scrollbar = ttk.Scrollbar(detalle_window, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)

            tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
            scrollbar.pack(side="right", fill="y", pady=10)

            tk.Button(detalle_window, text="Cerrar", 
                     command=detalle_window.destroy,
                     font=("Arial", 10, "bold"),
                     bg="#4CAF50",
                     fg="white",
                     padx=10,
                     pady=5).pack(pady=10)

        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error al cargar detalles de perfiles: {e}")

    def limpiar_campos(self):
        """Limpia todos los campos de entrada."""
        self.entry_id.delete(0, tk.END)
        self.entry_nombre.delete(0, tk.END)
        self.entry_limite.delete(0, tk.END)
        self.label_validacion.config(text="")
        self.entry_nombre.config(bg="white")
        self.entry_limite.config(bg="white")

    def alta_perfil(self):
        """Agrega un nuevo perfil con validaciones."""
        try:
            nombre = self.entry_nombre.get().strip()
            limite = self.entry_limite.get().strip()

            if not all([nombre, limite]):
                raise ValueError("Todos los campos son obligatorios")

            self.validar_nombre_perfil(nombre)
            limite_validado = self.validar_limite(limite)

            self.cursor.execute("SELECT idPerfil FROM perfil WHERE nombrePerfil = %s", (nombre,))
            if self.cursor.fetchone():
                raise ValueError("El nombre de perfil ya existe")

            self.cursor.execute(
                "INSERT INTO perfil (nombrePerfil, limiteMax) VALUES (%s, %s)",
                (nombre, limite_validado)
            )
            self.conn.commit()
            messagebox.showinfo("Éxito", "Perfil agregado correctamente")
            self.limpiar_campos()
            self.mostrar_perfiles()

        except ValueError as e:
            messagebox.showerror("Error de Validación", str(e))
        except mysql.connector.Error as e:
            messagebox.showerror("Error de Base de Datos", f"Error al agregar perfil: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {e}")

    def baja_perfil(self):
        """Elimina un perfil con validaciones."""
        try:
            perfil_id = self.entry_id.get().strip()
            if not perfil_id:
                raise ValueError("Debe especificar el ID del perfil")

            try:
                perfil_id = int(perfil_id)
            except ValueError:
                raise ValueError("El ID debe ser un número")

            self.cursor.execute("SELECT COUNT(*) FROM usuario WHERE perfil_idPerfil = %s", (perfil_id,))
            if self.cursor.fetchone()[0] > 0:
                raise ValueError("No se puede eliminar el perfil porque tiene usuarios asociados")

            self.cursor.execute("DELETE FROM perfil WHERE idPerfil = %s", (perfil_id,))
            self.conn.commit()

            if self.cursor.rowcount > 0:
                messagebox.showinfo("Éxito", "Perfil eliminado correctamente")
                self.limpiar_campos()
                self.mostrar_perfiles()
            else:
                raise ValueError("No se encontró el perfil con ese ID")

        except ValueError as e:
            messagebox.showerror("Error de Validación", str(e))
        except mysql.connector.Error as e:
            messagebox.showerror("Error de Base de Datos", f"Error al eliminar perfil: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {e}")

    def modificar_perfil(self):
        """Modifica un perfil con validaciones."""
        try:
            perfil_id = self.entry_id.get().strip()
            nombre = self.entry_nombre.get().strip()
            limite = self.entry_limite.get().strip()

            if not perfil_id:
                raise ValueError("Debe especificar el ID del perfil")

            self.cursor.execute("SELECT * FROM perfil WHERE idPerfil = %s", (perfil_id,))
            if not self.cursor.fetchone():
                raise ValueError("No existe un perfil con ese ID")

            update_fields = []
            params = []
            
            if nombre:
                self.validar_nombre_perfil(nombre)
                update_fields.append("nombrePerfil = %s")
                params.append(nombre)
                
            if limite:
                limite_validado = self.validar_limite(limite)
                update_fields.append("limiteMax = %s")
                params.append(limite_validado)

            if not update_fields:
                raise ValueError("Debe especificar al menos un campo para modificar")

            query = f"UPDATE perfil SET {', '.join(update_fields)} WHERE idPerfil = %s"
            params.append(perfil_id)
            
            self.cursor.execute(query, tuple(params))
            self.conn.commit()

            messagebox.showinfo("Éxito", "Perfil modificado correctamente")
            self.limpiar_campos()
            self.mostrar_perfiles()

        except ValueError as e:
            messagebox.showerror("Error de Validación", str(e))
        except mysql.connector.Error as e:
            messagebox.showerror("Error de Base de Datos", f"Error al modificar perfil: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {e}")

    def mostrar_perfiles(self):
        """Muestra la lista básica de perfiles en el listbox principal."""
        try:
            self.cursor.execute("SELECT * FROM perfil")
            perfiles = self.cursor.fetchall()
            
            self.listbox_perfiles.delete(0, tk.END)
            for perfil in perfiles:
                self.listbox_perfiles.insert(tk.END, 
                    f"ID: {perfil[0]}, Perfil: {perfil[1]}, Límite: {perfil[2]:.2f}")

        except mysql.connector.Error as e:
            messagebox.showerror("Error", f"Error al cargar perfiles: {e}")

    def __del__(self):
        """Cierra la conexión a la base de datos al cerrar la aplicación."""
        if hasattr(self, 'conn') and self.conn.is_connected():
            self.cursor.close()
            self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = ProfileManagementSystem(root)
    root.mainloop()