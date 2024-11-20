import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="sonometro_IOT",
    )

def cargar_datos():
    conexion = conectar()
    query = """
    SELECT r.idRegistro, r.nivelSonido1, r.nivelSonido2, r.nivelSonido3, r.fechaRegistro, r.excedeLimite,
           u.nombreUsuario as usuario, p.nombretipo as tipo, st.tipoDir
    FROM registro r
    JOIN usuario u ON r.usuario_idUsuario = u.idUsuario
    JOIN tipo p ON u.tipo_idtipo = p.idtipo
    JOIN direcion st ON r.direcion_idDir = st.idDir
    """
    df = pd.read_sql(query, conexion)
    conexion.close()
    return df

def obtener_nombres_usuarios(df):
    usuarios = df['usuario'].unique().tolist()
    return ["Todos"] + usuarios

def obtener_datos_nserie(df, usuario_seleccionado=None):
    if usuario_seleccionado and usuario_seleccionado != "Todos":
        df = df[df['usuario'] == usuario_seleccionado]
    datos_serie = df['tipoDir'].value_counts()
    tipos_serie = datos_serie.index.tolist()
    cuenta_registros_serie = datos_serie.values.tolist()
    return tipos_serie, cuenta_registros_serie

def obtener_datos_usuarios(df, usuario_seleccionado=None):
    if usuario_seleccionado and usuario_seleccionado != "Todos":
        df = df[df['usuario'] == usuario_seleccionado]
    datos_usuarios = df['usuario'].value_counts()
    nombres_usuarios = datos_usuarios.index.tolist()
    cuenta_registros_usuarios = datos_usuarios.values.tolist()
    return nombres_usuarios, cuenta_registros_usuarios

def obtener_datos_nivelSonido3_promedio_por_usuario(df, usuario_seleccionado=None):
    if usuario_seleccionado and usuario_seleccionado != "Todos":
        df = df[df['usuario'] == usuario_seleccionado]
    nivelSonido3_promedio = df.groupby('usuario')['nivelSonido3'].mean()
    nombres_usuarios = nivelSonido3_promedio.index.tolist()
    promedio_nivelSonido3 = nivelSonido3_promedio.values.tolist()
    return nombres_usuarios, promedio_nivelSonido3

def obtener_datos_nivelSonido3_vs_nivelSonido2(df, usuario_seleccionado=None):
    if usuario_seleccionado and usuario_seleccionado != 'Todos':
        df = df[df['usuario'] == usuario_seleccionado]
    nivelSonido3 = df['nivelSonido3'].tolist()
    nivelSonido2 = df['nivelSonido2'].tolist()
    return nivelSonido3, nivelSonido2

def obtener_datos_nivelSonido3_promedio_por_tipo(df, usuario_seleccionado=None):
    if usuario_seleccionado and usuario_seleccionado != "Todos":
        df = df[df['usuario'] == usuario_seleccionado]
    nivelSonido3_promedio_tipo = df.groupby('tipo')['nivelSonido3'].mean()
    tipoes = nivelSonido3_promedio_tipo.index.tolist()
    promedio_nivelSonido3 = nivelSonido3_promedio_tipo.values.tolist()
    return tipoes, promedio_nivelSonido3

def obtener_datos_fibomassi_vs_nivelSonido2(df, usuario_seleccionado=None):
    if usuario_seleccionado and usuario_seleccionado != 'Todos':
        df = df[df['usuario'] == usuario_seleccionado]
    return df['nivelSonido1'].tolist(), df['nivelSonido2'].tolist()

def obtener_datos_registros_por_tipo(df, usuario_seleccionado=None):
    if usuario_seleccionado and usuario_seleccionado != 'Todos':
        df = df[df['usuario'] == usuario_seleccionado]
    registros_por_tipo = df['tipo'].value_counts()
    tipoes = registros_por_tipo.index.tolist()
    registros = registros_por_tipo.values.tolist()
    return tipoes, registros

def crear_figura_barras(tipos, cuentas, xlabel, ylabel, title, colores=None):
    fig, ax = plt.subplots(figsize=(4, 3))
    
    # Define a list of colors
    color_palette = ['#4682B4', '#FFA07A', '#9ACD32', '#FF69B4', '#8B008B', '#00CED1', '#FF8C00', '#7B68EE', '#DB7093', '#008B8B']
    
    # Use the color palette to color the bars
    ax.bar(tipos, cuentas, color=colores if colores else color_palette)
    
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    return fig

def crear_figura_torta(tipos, cuentas, title):
    fig, ax = plt.subplots(figsize=(4, 3))
    
    # Define a list of colors
    color_palette = ['#4682B4', '#FFA07A', '#9ACD32', '#FF69B4', '#8B008B', '#00CED1', '#FF8C00', '#7B68EE', '#DB7093', '#008B8B']
    
    # Use the color palette to color the pie slices
    ax.pie(cuentas, labels=tipos, autopct='%1.1f%%', startangle=90, colors=color_palette)
    
    ax.axis('equal')
    ax.set_title(title)
    return fig

def crear_figura_scatter(x, y, xlabel, ylabel, title):
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.scatter(x, y, color='#4682B4')
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    plt.tight_layout()
    return fig

def crear_figura_linea(x, y1, y2, title):
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.plot(x, y1, label="Fibomassi", color="#4682B4")
    ax.plot(x, y2, label="nivelSonido2", color="#FFA07A")
    ax.set_xlabel("Nreg")
    ax.set_ylabel("Valores")
    ax.set_title(title)
    ax.legend()
    plt.tight_layout()
    return fig

def actualizar_graficos(event, combobox, frame_graficos, df):
    usuario_seleccionado = combobox.get()

    for widget in frame_graficos.winfo_children():
        widget.destroy()

    tipos_serie, cuenta_registros_serie = obtener_datos_nserie(df, usuario_seleccionado)
    fig1 = crear_figura_barras(tipos_serie, cuenta_registros_serie, "Tipo de Serie", "Número de Registros", "Registros por Tipo de Serie")

    fig2 = crear_figura_torta(tipos_serie, cuenta_registros_serie, "Porcentaje por Tipo de Serie")

    nombres_usuarios, cuenta_registros_usuarios = obtener_datos_usuarios(df, usuario_seleccionado)
    fig3 = crear_figura_barras(nombres_usuarios, cuenta_registros_usuarios, "Usuario", "Registros", "Registros por Usuario")

    fig4 = crear_figura_torta(nombres_usuarios, cuenta_registros_usuarios, "Porcentaje de Registros por Usuario")

    nombres_usuarios, promedio_nivelSonido3 = obtener_datos_nivelSonido3_promedio_por_usuario(df, usuario_seleccionado)
    fig5 = crear_figura_barras(nombres_usuarios, promedio_nivelSonido3, "Usuario", "nivelSonido3 Promedio", "nivelSonido3 Promedio por Usuario")

    nivelSonido3, nivelSonido2 = obtener_datos_nivelSonido3_vs_nivelSonido2(df, usuario_seleccionado)
    fig6 = crear_figura_scatter(nivelSonido3, nivelSonido2, "nivelSonido3", "nivelSonido2", "nivelSonido3 vs nivelSonido2")

    tipoes, promedio_nivelSonido3_tipo = obtener_datos_nivelSonido3_promedio_por_tipo(df, usuario_seleccionado)
    fig7 = crear_figura_barras(tipoes, promedio_nivelSonido3_tipo, "tipo", "nivelSonido3 Promedio", "nivelSonido3 Promedio por tipo")

    fibomassi, nivelSonido2 = obtener_datos_fibomassi_vs_nivelSonido2(df, usuario_seleccionado)
    fig8 = crear_figura_linea(range(len(fibomassi)), fibomassi, nivelSonido2, "Fibomassi y nivelSonido2 en el Tiempo")

    tipoes, registros = obtener_datos_registros_por_tipo(df, usuario_seleccionado)
    fig9 = crear_figura_barras(tipoes, registros, "tipo", "Registros", "Registros por tipo")

    figuras = [fig3, fig4, fig5, fig7, fig8, fig9]
    for i, fig in enumerate(figuras):
        row = i // 3
        col = i % 3
        canvas_fig = FigureCanvasTkAgg(fig, master=frame_graficos)
        canvas_fig.draw()
        widget = canvas_fig.get_tk_widget()
        widget.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')

def crear_interfaz():
    df = cargar_datos()

    root = tk.Tk()
    root.title("DASHBOARD SONÓMETRO")
    root.resizable(True, True)

    usuarios = obtener_nombres_usuarios(df)

    frame_opciones = ttk.Frame(root)
    frame_opciones.pack(fill=tk.X, padx=10, pady=5)
    label_usuario = ttk.Label(frame_opciones, text="Seleccione Usuario:")
    label_usuario.pack(side=tk.LEFT, padx=5)
    combobox = ttk.Combobox(frame_opciones, values=usuarios)
    combobox.set("Todos")
    combobox.pack(side=tk.LEFT)

    frame_graficos = ttk.Frame(root)
    frame_graficos.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
    frame_graficos.grid_columnconfigure(0, weight=1)
    frame_graficos.grid_columnconfigure(1, weight=1)
    frame_graficos.grid_columnconfigure(2, weight=1)

    combobox.bind("<<ComboboxSelected>>", lambda event: actualizar_graficos(event, combobox, frame_graficos, df))

    actualizar_graficos(None, combobox, frame_graficos, df)

    root.mainloop()

if __name__ == "__main__":
    crear_interfaz()


