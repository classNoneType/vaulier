import tkinter as tk
import pandas as pd
import socket, os, datetime, shutil, subprocess
from time import strftime
from tkinter.constants import FALSE, TRUE
from tkinter.font import BOLD
from tkinter import Button, filedialog, ttk, messagebox
from service import BaseDatos
from PIL import Image, ImageTk

# Usuario
class Operador:
    def __init__(self):
        self.HOST = socket.gethostname()
        self.IP = socket.gethostbyname(self.HOST)
        self.USUARIO = f' {self.HOST}@{self.IP} '

# Propiedades del programa
class Propiedades:
    def __init__(self):

        self.ENTORNO = os.getcwd()
        self.RUTA_ENTORNO = self.ENTORNO.replace('\\', '/')
        print(self.RUTA_ENTORNO)

        self.MANAGE = 'manage.py'

        # Rutas
        self.RUTA_MANAGE = f'{self.RUTA_ENTORNO}/{self.MANAGE}'
        self.RUTA_DIR = f'{self.RUTA_ENTORNO}/'
        self.RUTA_DIR_APP = f'{self.RUTA_ENTORNO}/app/'
        self.RUTA_DIR_ICONO = f'{self.RUTA_ENTORNO}/app/icon/'
        self.RUTA_BASE = []
        self.RUTA_STATIC_IMG = []

        self.RUTA_ICONO = None
        self.__VerificarEntorno()
        self.RUTA_ICONO_INICIO = r'./app/icon/inicio.png'
        self.RUTA_ICONO_VINILOS = r'./app/icon/vinilos.png'
        self.RUTA_ICONO_SALIR = r'./app/icon/salir.png'
        self.RUTA_ICONO_EXPLORADOR = r'./app/icon/explorador_w.png'
        self.RUTA_ICONO_PROPIEDADES = r'./app/icon/propiedades.png'
        self.RUTA_ICONO_BUSCADOR = r'./app/icon/buscador.png'
        self.RUTA_ICONO_CARGAR = r'./app/icon/buscador.png'


        self.TABLA_VAULIER_VINILOS = 'vaulier_producto'



        self.SERVICIOS = BaseDatos()

        self.COMANDO_RUNSERVER = f'python {self.MANAGE} runserver'
        self.COMANDO_CD = f'cd {self.RUTA_DIR}'
        self.COMANDO_INICIAR_WEB = f'{self.COMANDO_CD} && {self.COMANDO_RUNSERVER}'
        self.COMANDO_INICIAR_BRAVE = 'start brave --incognito http://127.0.0.1:8000/'

        self.ESTADO_WEB = False
    
    def __VerificarEntorno(self):
        ENTORNO = [e for e in os.listdir()]
        if 'app' in ENTORNO:
            self.RUTA_ICONO = f'{self.RUTA_DIR_ICONO}icono.ico'

# Producto vinilo
class Vinilo(object):
    def __init__(self):
        self.Propiedades = Propiedades()

        self.PORTADA = []
        self.ID = [i for i in range(0,1000)]
        self.__HabilitarID()
        self.STOCK = [s for s in range(0,100)]
        self.ID_AUTOR = 2

    def __HabilitarID(self):
        self.Propiedades.SERVICIOS.CURSOR.execute(f'SELECT id FROM {self.Propiedades.TABLA_VAULIER_VINILOS}')
        y = [i[0] for i in self.Propiedades.SERVICIOS.CURSOR.fetchall()]
        for item in y:
            if item in self.ID:
                self.ID.remove(item)

# Interfaz grafica del programa
class Interfaz(tk.Frame):
    def __init__(self, w, ERROR):
        # Errores del programa
        self.ERROR = ERROR
        super().__init__(w)
        # Establecimiento de propiedades
        self.Operador = Operador()
        self.Propiedades = Propiedades()

        

        self.Vinilo = Vinilo()

        # Propiedades de la ventana principal
        self.w = w
        self.w.geometry('1300x700')
        self.w.title('VAULIER ')
        self.w.iconbitmap(self.Propiedades.RUTA_ICONO)
        self.pack(fill = tk.BOTH, expand = True)
        self.configure(background = '#FFFFFF')
        self.w.bind('<F11>', lambda event: self.w.attributes('-fullscreen',
                                            not self.w.attributes('-fullscreen')))
        self.w.bind(
            '<Escape>', self.__Salir
        )



        # Establecimiento de iconos
        self.IconoInicio = tk.PhotoImage(file = self.Propiedades.RUTA_ICONO_INICIO)
        self.IconoVinilo = tk.PhotoImage(file = self.Propiedades.RUTA_ICONO_VINILOS)
        self.IconoExplorador = tk.PhotoImage(file = self.Propiedades.RUTA_ICONO_EXPLORADOR)
        self.IconoSalir = tk.PhotoImage(file = self.Propiedades.RUTA_ICONO_SALIR)
        self.IconoPropiedades = tk.PhotoImage(file = self.Propiedades.RUTA_ICONO_PROPIEDADES)
        self.IconoBuscador = tk.PhotoImage(file = self.Propiedades.RUTA_ICONO_BUSCADOR)
        self.IconoCargar = tk.PhotoImage(file = self.Propiedades.RUTA_ICONO_CARGAR)

        # Establecimiento de panel izquierdo
        self.FramePanel = tk.Frame(self, background = '#D5A27C')
        self.FramePanel.pack(fill = tk.Y, expand = True, side = tk.LEFT, ipadx = 5, ipady = 10)

        # Establecimiento de panel de operacion
        self.FrameOperacion = tk.Frame(self)
        self.FrameOperacion.pack(fill = tk.BOTH, expand = True, side = tk.RIGHT, ipadx = 1000)
        self.__LimpiarFrame()
        self.__Inicio()

        # Establecimiento de botones
        self.ButtonInicio = tk.Button(
            self.FramePanel, text = 'Inicio', compound = tk.TOP,
            font = ('Ubuntu', 9, BOLD),
            background = '#D5A27C', foreground = '#FFFFFF',
            relief = tk.FLAT, image = self.IconoInicio,
            justify = tk.CENTER, command = self.__Inicio
        )
        self.ButtonInicio.configure(activebackground = '#D5A27C')
        self.ButtonInicio.pack(fill = tk.BOTH, expand = True, pady = 2, padx = 2)

        self.ButtonVinilos = tk.Button(
            self.FramePanel, text = 'Gestion de Vinilos', compound = tk.TOP,
            font = ('Ubuntu', 9, BOLD),
            background = '#D5A27C', foreground = '#FFFFFF',
            relief = tk.FLAT, image = self.IconoVinilo,
            justify = tk.CENTER, command = self.__GestionVinilos
        )
        self.ButtonVinilos.configure(activebackground = '#D5A27C')
        self.ButtonVinilos.pack(fill = tk.BOTH, expand = True, pady = 2, padx = 2)

        self.ButtonExplorador = tk.Button(
            self.FramePanel, text = 'Explorador de archivos', compound = tk.TOP,
            font = ('Ubuntu', 9, BOLD),
            background = '#D5A27C', foreground = '#FFFFFF',
            relief = tk.FLAT, image = self.IconoExplorador,
            justify = tk.CENTER, command = self.__Explorador
        )
        self.ButtonExplorador.configure(activebackground = '#D5A27C')
        self.ButtonExplorador.pack(fill = tk.BOTH, expand = True, pady = 2, padx = 2)

        '''self.ButtonPropiedades = tk.Button(
            self.FramePanel, text = 'Propiedades', compound = tk.TOP,
            font = ('Ubuntu', 9, BOLD),
            background = '#D5A27C', foreground = '#FFFFFF',
            relief = tk.FLAT, image = self.IconoPropiedades,
            justify = tk.CENTER, command = self.__Propiedades
        )
        self.ButtonPropiedades.configure(activebackground = '#D5A27C')
        self.ButtonPropiedades.pack(fill = tk.BOTH, expand = True, pady = 2, padx = 2)'''

        self.ButtonBuscador = tk.Button(
            self.FramePanel, text = 'Buscador', compound = tk.TOP,
            font = ('Ubuntu', 9, BOLD),
            background = '#D5A27C', foreground = '#FFFFFF',
            relief = tk.FLAT, image = self.IconoBuscador,
            justify = tk.CENTER
        )
        self.ButtonBuscador.configure(activebackground = '#D5A27C')
        self.ButtonBuscador.pack(fill = tk.BOTH, expand = True, pady = 2, padx = 2)

        self.ButtonSalir = tk.Button(
            self.FramePanel, text = 'Salir', compound = tk.TOP,
            font = ('Ubuntu', 9, BOLD),
            background = '#D5A27C', foreground = '#FFFFFF',
            relief = tk.FLAT, image = self.IconoSalir,
            justify = tk.CENTER, command = lambda: self.__Salir(event = None)
        )
        self.ButtonSalir.configure(activebackground = '#D5A27C')
        self.ButtonSalir.pack(fill = tk.BOTH, expand = True, pady = 2, padx = 2)

# Seccion
    def __Inicio(self):
        self.__LimpiarFrame()
        # D9A99C
        self.FrameOperacion.configure(background = '#D3D3D3')

        self.FrameReloj = tk.Frame(self.FrameOperacion, background = '#786271')
        self.FrameReloj.pack(fill = tk.BOTH, expand = True, side = tk.TOP)
        self.FrameWeb = tk.Frame(self.FrameOperacion, background = '#786271')
        self.FrameWeb.pack(fill = tk.BOTH, expand = True)
        self.FrameInicio = tk.Frame(self.FrameOperacion, background = '#F0F0F0')
        self.FrameInicio.pack(fill = tk.BOTH, expand = True, ipady = 200)

        self.ButtonDetenerWeb = tk.Button(
            self.FrameWeb, text = ' Detener servicios WEB  ', font = ('Ubuntu', 13),
            background = '#D5A27C', foreground = '#FFFFFF',
            relief = tk.FLAT, width = 25, command = self.__DetenerWeb)
        self.ButtonDetenerWeb.pack(expand = True, side = tk.RIGHT, pady = 12)
        
        self.ButtonIniciarWeb = tk.Button(
            self.FrameWeb, text = ' Iniciar servicios WEB  ', font = ('Ubuntu', 13),
            background = '#D5A27C', foreground = '#FFFFFF',
            relief = tk.FLAT, width = 25, command = self.__IniciarWeb)
        self.ButtonIniciarWeb.pack(expand = True, side = tk.RIGHT, pady = 12)



        self.LabelUsuario = tk.Label(
            self.FrameOperacion, text = f'{self.Operador.USUARIO}', font = ('Ubuntu light', 14),
            background = '#D9A99C', foreground = '#FFFFFF')
        self.LabelUsuario.pack(fill = tk.BOTH, expand = True, anchor = 'w', side = tk.BOTTOM)


        self.LabelEstadoWeb = tk.Label(
            self.FrameOperacion, text = f'[ {self.Propiedades.ESTADO_WEB} ]', font = ('Ubuntu light', 16),
            background = '#D9A99C', foreground = '#D83A3A'
        )
        self.LabelEstadoWeb.pack(fill = tk.BOTH, expand = True, anchor = 'w', side = tk.LEFT)

        # Conexion
        self.FrameConexion = tk.Frame(self.FrameInicio, background = '#F0F0F0')
        self.FrameConexion.pack(fill = tk.BOTH, expand = True, side = tk.RIGHT)

        # Frame entry de Conexion
        self.FrameEntriesConexion = tk.Frame(self.FrameConexion, background = '#F0F0F0')
        self.FrameEntriesConexion.pack(fill = tk.X, side = tk.LEFT)

        # Entry
        self.__EntryRutaBaseDatos = tk.Entry(
            self.FrameEntriesConexion, relief = tk.SOLID, font = ('Ubuntu', 13),
            width = 80, justify = tk.CENTER
        )
        self.__EntryRutaBaseDatos.pack(expand = True, pady = 5, padx = 10)
        self.__EntryRutaBaseDatos.insert(0, f'{self.Propiedades.SERVICIOS.RUTA_BASE}')
        self.__EntryRutaBaseDatos.configure(state = 'readonly')

        
        STRING_RUTA_BASE = f'{self.__EntryRutaBaseDatos.get()}'
        RUTA_BASE = STRING_RUTA_BASE[:-10]
        
        self.Propiedades.RUTA_BASE.append(RUTA_BASE)

        self.__EntryArchivoBaseDatos = tk.Entry(
            self.FrameEntriesConexion, relief = tk.SOLID, font = ('Ubuntu', 13),
            width = 80, justify = tk.CENTER
        )
        self.__EntryArchivoBaseDatos.pack(expand = True, pady = 5, padx = 10)
        self.__EntryArchivoBaseDatos.insert(0, f'{self.Propiedades.SERVICIOS.BASE_DATOS}')

        self.__EntryArchivoBaseDatos.configure(state = 'readonly')


        self.__EntryConexionBaseDatos = tk.Entry(
            self.FrameEntriesConexion, relief = tk.SOLID, font = ('Ubuntu', 13),
            width = 80, justify = tk.CENTER
        )
        self.__EntryConexionBaseDatos.pack(expand = True, pady = 5, padx = 10)
        self.__EntryConexionBaseDatos.insert(0, f'{self.Propiedades.SERVICIOS.CONEXION}')
        self.__EntryConexionBaseDatos.configure(state = 'readonly')

        self.__EntryCursorBaseDatos = tk.Entry(
            self.FrameEntriesConexion, relief = tk.SOLID, font = ('Ubuntu', 13),
            width = 80, justify = tk.CENTER
        )
        self.__EntryCursorBaseDatos.pack(expand = True, pady = 5, padx = 10)
        self.__EntryCursorBaseDatos.insert(0, f'{self.Propiedades.SERVICIOS.CURSOR}')
        self.__EntryCursorBaseDatos.configure(state = 'readonly')

        # Frame detalle de Conexion
        self.FrameDetalleConexion = tk.Frame(self.FrameInicio, background = '#F0F0F0')
        self.FrameDetalleConexion.pack(fill = tk.X, expand = True, side = tk.LEFT, padx = 15)

        self.LabelRutaConexion = tk.Label(
            self.FrameDetalleConexion, text = 'Ruta de Conexion', font = ('Ubuntu light', 14),
            background = '#F0F0F0', foreground = '#786271'
        )
        self.LabelRutaConexion.pack(expand = True, anchor = 'w')

        self.LabelBaseDatosConexion = tk.Label(
            self.FrameDetalleConexion, text = 'Base de datos', font = ('Ubuntu light', 14),
            background = '#F0F0F0', foreground = '#786271'
        )
        self.LabelBaseDatosConexion.pack(expand = True, anchor = 'w')

        self.LabelConexion = tk.Label(
            self.FrameDetalleConexion, text = 'Clase Conexion', font = ('Ubuntu light', 14),
            background = '#F0F0F0', foreground = '#786271'
        )
        self.LabelConexion.pack(expand = True, anchor = 'w')

        self.LabelCursor = tk.Label(
            self.FrameDetalleConexion, text = 'Clase Cursor', font = ('Ubuntu light', 14),
            background = '#F0F0F0', foreground = '#786271'
        )
        self.LabelCursor.pack(expand = True, anchor = 'w')


        # Reloj
        self.LabelReloj = tk.Label(
            self.FrameReloj, font = ('Ubuntu light', 15, BOLD),
            background = '#786271', foreground = '#FFFFFF'
        )
        self.LabelReloj.pack(expand = tk.YES, pady = 10)
        self.RelojSistema()

    def __Explorador(self):
        self.__LimpiarFrame()

        self.FrameExplorador = tk.Frame(
            self.FrameOperacion, background = '#F0F0F0'
        )
        self.FrameExplorador.pack(expand = True)

        self.EntryRuta = tk.Entry(
            self.FrameExplorador, relief = tk.SOLID, font = ('Ubuntu', 14),
            width = 35, justify = tk.CENTER
        )
        self.EntryRuta.pack(fill = tk.X, expand = 1, side = tk.LEFT, padx = 5)

        self.ButtonExplorador = tk.Button(
            self.FrameExplorador, text = '  Buscar ruta  ', font = ('Ubuntu', 12),
            background = '#D5A27C', foreground = '#FFFFFF',
            relief = tk.FLAT, command = lambda:self.__IniciarExplorador(event=None), width = 25
        )
        self.ButtonExplorador.pack(expand = True, side = tk.RIGHT)
        self.w.bind(
            '<Return>', self.__IniciarExplorador
        )

        self.Frame = tk.Frame(
            self.FrameOperacion, background = '#FFFFFF'
        )
        self.Frame.pack(
            fill = tk.BOTH, expand = True
        )
        self.FrameNotebook = tk.Frame(
            self.Frame, background = '#FFFFFF'
        )
        self.FrameNotebook.pack(
            fill = tk.BOTH, expand = True, side = tk.LEFT
        )
        self.Notebook = ttk.Notebook(self.FrameNotebook)
        self.Notebook.pack(fill = tk.BOTH, expand = True, padx=10, pady=10)

        self.__IniciarRutaConexion(event = None)

    def __IniciarRutaConexion(self, event):
        CONTADOR = 0
        Directorio = self.Propiedades.RUTA_BASE[0]
        dirs = os.listdir(Directorio)

        if CONTADOR <= 1:
            self.FrameTreeView = tk.Frame(
                self.Frame, background = '#FFFFFF'
            )
            self.FrameTreeView.pack(
                fill = tk.BOTH, expand = True, side = tk.LEFT
            )

            self.TreeView = ttk.Treeview(
                self.FrameTreeView, height = 50,
                column = ('#1', '#2', '#3'),
                show = 'headings'
            )

            self.TreeView.pack(fill = 'both', expand = True, side = tk.LEFT)
            self.TreeView.heading('#1', text = 'Nombre del Archivo', anchor = tk.CENTER)
            self.TreeView.heading('#2', text = 'Tamano', anchor = tk.CENTER)
            self.TreeView.heading('#3',text = 'Fecha de Creacion', anchor = tk.CENTER)
            self.TreeView.column('#1', width = 138, anchor = tk.W)
            self.TreeView.column('#2', width = 138, anchor = tk.W)
            self.TreeView.column('#3', width = 138, anchor = tk.W)
            self.ScrollBarTreeView_y = ttk.Scrollbar(
                self.TreeView, orient = 'vertical',
                command = self.TreeView.yview
            )
            self.ScrollBarTreeView_y.pack(fill = 'y', side = tk.RIGHT)



            self.Notebook.add(self.FrameTreeView, text=f'{Directorio}', padding=20)

            for filename in dirs:
                filepath = str(f'{Directorio}/{filename}')
                filesize = os.path.getsize(filepath)
                date = os.path.getmtime(filepath)
                filedate = datetime.datetime.fromtimestamp(date)
                self.TreeView.insert(
                    '', tk.END,
                    values = (filename,str(f'{filesize}  MB'), filedate)
                )


            self.TreeView.configure(
                yscrollcommand = self.ScrollBarTreeView_y.set
                #style = 'mystyle.Treeview'
            )
            CONTADOR+=1
        else:
            pass

    def __IniciarExplorador(self, event):
        if self.EntryRuta.get() == '':
            Directorio = filedialog.askdirectory(
                parent = self.w,
                initialdir = '/',
                title='Elige una carpeta'
            )
            dirs = os.listdir(Directorio)
            self.EntryRuta.insert(0, str(Directorio))
        elif len(self.EntryRuta.get()) != 0:
            Directorio = self.EntryRuta.get()
            dirs = os.listdir(self.EntryRuta.get())
        

        self.FrameTreeView = tk.Frame(
            self.Frame, background = '#FFFFFF'
        )
        self.FrameTreeView.pack(
            fill = tk.BOTH, expand = True, side = tk.LEFT
        )

        self.TreeView = ttk.Treeview(
            self.FrameTreeView, height = 50,
            column = ('#1', '#2', '#3'),
            show = 'headings'
        )

        self.TreeView.pack(fill = 'both', expand = True, side = tk.LEFT)
        self.TreeView.heading('#1', text = 'Nombre del Archivo', anchor = tk.CENTER)
        self.TreeView.heading('#2', text = 'Tamano', anchor = tk.CENTER)
        self.TreeView.heading('#3',text = 'Fecha de Creacion', anchor = tk.CENTER)
        self.TreeView.column('#1', width = 138, anchor = tk.W)
        self.TreeView.column('#2', width = 138, anchor = tk.W)
        self.TreeView.column('#3', width = 138, anchor = tk.W)
        self.ScrollBarTreeView_y = ttk.Scrollbar(
            self.TreeView, orient = 'vertical',
            command = self.TreeView.yview
        )
        self.ScrollBarTreeView_y.pack(fill = 'y', side = tk.RIGHT)



        self.Notebook.add(self.FrameTreeView, text=f'{Directorio}', padding=20)

        for filename in dirs:
            filepath = str(f'{Directorio}/{filename}')
            filesize = os.path.getsize(filepath)
            date = os.path.getmtime(filepath)
            filedate = datetime.datetime.fromtimestamp(date)
            self.TreeView.insert(
                '', tk.END,
                values = (filename,str(f'{filesize}  MB'), filedate)
            )


        self.TreeView.configure(
            yscrollcommand = self.ScrollBarTreeView_y.set
            #style = 'mystyle.Treeview'
        )

    def __Propiedades(self):
        self.__LimpiarFrame()
        self.LabelFramePropiedades = tk.LabelFrame(
            self.FrameOperacion, text = ' Propiedades ', font = ('Ubuntu', 13, BOLD),
            background = '#FFFFFF', foreground = '#D5A27C'
        )
        self.LabelFramePropiedades.pack(fill = tk.BOTH, expand = True, padx = 25, pady = 10)

        self.LabelFrameOperador = tk.LabelFrame(
            self.LabelFramePropiedades, text = ' Usuario del sistema ', font = ('Ubuntu light', 12, BOLD),
            background = '#FFFFFF', foreground = '#D5A27C'
        )
        self.LabelFrameOperador.pack(fill = tk.X, expand = True, padx = 25, pady = 10)

        self.__EntryHost = tk.Entry(
            self.LabelFrameOperador, relief = tk.SOLID, font = ('Ubuntu', 13),
            width = 35, justify = tk.CENTER
        )
        self.__EntryHost.pack(expand = 1, padx = 15, pady = 5)
        self.__EntryHost.insert(0, f'{self.Operador.HOST}')
        self.__EntryHost.configure(state = 'readonly')

        self.__EntryIP = tk.Entry(
            self.LabelFrameOperador, relief = tk.SOLID, font = ('Ubuntu', 13),
            width = 35, justify = tk.CENTER
        )
        self.__EntryIP.pack(expand = 1, padx = 15, pady = 5)
        self.__EntryIP.insert(0, f'{self.Operador.IP}')
        self.__EntryIP.configure(state = 'readonly')

        if self.__EntryHost.get() == 'DESKTOP-77GL42T':
            self.__EntryRol = tk.Entry(
                self.LabelFrameOperador, relief = tk.SOLID, font = ('Ubuntu', 13),
                width = 35, justify = tk.CENTER
            )
            self.__EntryRol.pack(expand = 1, padx = 15, pady = 5)
            self.__EntryRol.insert(0, 'ADMINISTRADOR')
            self.__EntryRol.configure(state = 'readonly')
        else:
            self.__EntryRol = tk.Entry(
                self.LabelFrameOperador, relief = tk.SOLID, font = ('Ubuntu', 13),
                width = 35, justify = tk.CENTER
            )
            self.__EntryRol.pack(expand = 1, padx = 15, pady = 5)
            self.__EntryRol.insert(0, 'OPERADOR')
            self.__EntryRol.configure(state = 'readonly')
        
    def __GestionVinilos(self):
        self.__LimpiarFrame()
        df = pd.read_sql_query(
            f'SELECT * from {self.Propiedades.TABLA_VAULIER_VINILOS}', self.Propiedades.SERVICIOS.CONEXION
        )
        self.FrameOperacion.configure(background = '#F0F0F0')
        self.FrameTreeView = tk.Frame(self.FrameOperacion, background = '#F0F0F0')
        self.FrameTreeView.pack(fill = tk.BOTH, expand = True, padx = 10, pady = 5)

        # Buscador
        self.FramePanelBuscador = tk.Frame(self.FrameOperacion, background = '#786271')
        self.FramePanelBuscador.pack(fill = tk.BOTH, expand = True)

        self.FrameBuscador = tk.Frame(self.FramePanelBuscador, background = '#786271')
        self.FrameBuscador.pack(expand = True)

        self.EntryBuscador = tk.Entry(
            self.FrameBuscador, relief = tk.SOLID, font = ('Ubuntu', 14),
            justify = tk.CENTER, width = 38
        )
        self.EntryBuscador.pack(fill = tk.X, expand = True, pady = 8, padx = 5, side = tk.LEFT)

        self.ButtonBuscador = tk.Button(
            self.FrameBuscador, text = '  Buscar vinilo ', font = ('Ubuntu', 12),
            background = '#D5A27C', foreground = '#FFFFFF',
            relief = tk.FLAT, width = 29, command = lambda: self.__BusquedaVinilo(event = None)
        )
        self.ButtonBuscador.pack(expand = True, pady = 8, side = tk.RIGHT)


        self.TreeView = ttk.Treeview(self.FrameTreeView)
        
        self.ScrollY = tk.Scrollbar(
            self.FrameTreeView, orient='vertical', command = self.TreeView.yview
        )
        self.ScrollX = tk.Scrollbar(
            self.FrameTreeView, orient='horizontal', command = self.TreeView.xview
        )
        self.TreeView.configure(xscrollcommand = self.ScrollX.set, yscrollcommand = self.ScrollY.set)
        self.ScrollX.pack(side = tk.BOTTOM, fill = tk.X)
        self.ScrollY.pack(side = tk.RIGHT, fill = tk.Y) 
        self.TreeView.pack(fill = tk.BOTH, expand = True, side = tk.TOP, pady = 10)
        self.__LimpiarDatos()
        self.TreeView['column'] = list(df.columns)
        self.TreeView['show'] = 'headings'
        for column in self.TreeView['columns']:
            self.TreeView.heading(column, text=column)

        df_rows = df.to_numpy().tolist()
        for row in df_rows:
            self.TreeView.insert('', tk.END, values = row)
        
        self.w.bind(
            '<Return>', self.__BusquedaVinilo
        )
        self.TreeView.bind(
            '<Double-Button-1>',
            lambda event:self.__PerfilVinilo(event)
        )
        return None

    def __BusquedaVinilo(self, event):
        DATO = str(self.EntryBuscador.get())
        SELECCION_VINILO = []
        REGISTROS_VINILO = self.TreeView.get_children()

        if len(self.EntryBuscador.get()) != 0:
            for Vinilo in REGISTROS_VINILO:
                if (DATO.lower() or DATO.upper()) in self.TreeView.item(Vinilo)['values']:
                    print(self.TreeView.item(Vinilo)['values'])
                    SELECCION_VINILO.append(Vinilo)
            for Vinilos in REGISTROS_VINILO:
                self.TreeView.delete(Vinilos)
            self.EntryBuscador.delete(0, tk.END)

            df = pd.read_sql_query(
                f'''
                SELECT *
                FROM {self.Propiedades.TABLA_VAULIER_VINILOS} 
                WHERE id LIKE '{DATO.upper()}%' OR ArtistaProducto LIKE '{DATO.upper()}%' OR AlbumProducto LIKE '{DATO.upper()}%';
                ''', self.Propiedades.SERVICIOS.CONEXION
            )
            self.TreeView['column'] = list(df.columns)
            self.TreeView['show'] = 'headings'
            for column in self.TreeView['columns']:
                self.TreeView.heading(column, text=column)

            df_rows = df.to_numpy().tolist()
            for row in df_rows:
                self.TreeView.selection_set(self.TreeView.insert('', tk.END, values = row))
                
        else:
            for Vinilo in REGISTROS_VINILO:
                if (DATO.lower() or DATO.upper()) in self.TreeView.item(Vinilo)['values']:
                    print(self.TreeView.item(Vinilo)['values'])
                    SELECCION_VINILO.append(Vinilo)
            for Vinilos in REGISTROS_VINILO:
                self.TreeView.delete(Vinilos)
            self.EntryBuscador.delete(0, tk.END)

            df = pd.read_sql_query(
                f'SELECT * from {self.Propiedades.TABLA_VAULIER_VINILOS} ORDER BY id ASC;', self.Propiedades.SERVICIOS.CONEXION
            )
            self.TreeView['column'] = list(df.columns)
            self.TreeView['show'] = 'headings'
            for column in self.TreeView['columns']:
                self.TreeView.heading(column, text=column)

            df_rows = df.to_numpy().tolist()
            for row in df_rows:
                self.TreeView.selection_set(self.TreeView.insert('', tk.END, values = row))


# Sistema
    def RelojSistema(self):
        # Hora sistema
        HoraSistema = strftime('%H:%M:%S %p')
        self.LabelReloj.config(text = HoraSistema)
        self.LabelReloj.after(200, self.RelojSistema)

    def __Salir(self, event):
        self.w.destroy()

    def __LimpiarFrame(self):
        try:
            self.FrameOperacion.destroy()

            self.FrameOperacion = tk.Frame(
                self, background = '#F0F0F0'
            )
            self.FrameOperacion.pack(fill = tk.BOTH, expand = True, side = tk.RIGHT, ipadx = 1000)

        except Exception as e:
            self.ERROR.append(e)

    def __LimpiarDatos(self):
        self.TreeView.delete(*self.TreeView.get_children())
        return None


# Perfil
    def __PerfilVinilo(self, event):
        
        VINILO_SELECCIONADO = self.TreeView.item(self.TreeView.focus())

        for v in VINILO_SELECCIONADO:
            print(VINILO_SELECCIONADO[v])

        if VINILO_SELECCIONADO != '':
            try:
                STRING_RUTA_BASE = f'{self.Propiedades.SERVICIOS.RUTA_BASE}'
                RUTA_BASE = STRING_RUTA_BASE[:-10]
                RUTA_STATIC_IMG = str(f'{RUTA_BASE}vaulier/static/images/vinilos/')
                for PORTADA_ALBUM in os.listdir(RUTA_STATIC_IMG):
                    self.Vinilo.PORTADA.append(PORTADA_ALBUM)
                
                self.VentanaPerfil = tk.Toplevel()
                self.VentanaPerfil.focus_set()
                self.VentanaPerfil.grab_set()
                self.VentanaPerfil.iconbitmap(self.Propiedades.RUTA_ICONO)
                self.VentanaPerfil.geometry('1200x625')
                self.VentanaPerfil.resizable(False, False)
                self.VentanaPerfil.title(f"{VINILO_SELECCIONADO['values'][3]}")
                self.VentanaPerfil.configure(background = '#786271')
                self.LabelFramePerfil = tk.LabelFrame(
                    self.VentanaPerfil, text = '',
                    font = ('Ubuntu light', 14), relief = tk.FLAT, border = 1,
                    background = '#F0F0F0', foreground = '#D5A27C'
                )
                self.LabelFramePerfil.pack(fill = tk.BOTH, expand = tk.YES, padx = 40, pady = 20)

                self.FramePortadaAlbum = tk.Frame(
                    self.LabelFramePerfil, background = '#D5A27C',
                    width = 400, height = 400, relief = tk.GROOVE, border = 1,
                    highlightbackground = '#222222' 
                )
                self.FramePortadaAlbum.pack(
                    expand = tk.YES, padx = 15, pady = 15,
                    side = tk.LEFT
                )
                self.LabelFrameInformacion = tk.LabelFrame(
                    self.LabelFramePerfil, text = '',
                    font = ('Ubuntu light', 14), relief = tk.GROOVE, border = 1,
                    background = '#FFFFFF', foreground = '#D5A27C'
                )
                self.LabelFrameInformacion.pack(
                    fill = tk.BOTH, expand = tk.YES, padx = 40, pady = 90,
                    side = tk.RIGHT
                )
                for IMG_PORTADA_ALBUM in self.Vinilo.PORTADA:
                    IMG_PORTADA_ALBUM = str(VINILO_SELECCIONADO['values'][4])
                    
                    self.PORTADA_ALBUM = ImageTk.PhotoImage(
                        Image.open(
                            f'{RUTA_STATIC_IMG}{IMG_PORTADA_ALBUM}'
                        )
                    )
                print(f'[ img ] {RUTA_STATIC_IMG}{IMG_PORTADA_ALBUM}')
                self.Propiedades.RUTA_STATIC_IMG.append(f'{RUTA_STATIC_IMG}{IMG_PORTADA_ALBUM}')

                self.Portada = tk.Button(
                    self.FramePortadaAlbum, image = self.PORTADA_ALBUM,
                    relief = tk.GROOVE, border = 0, command = self.__IniciarPerfilVinilo
                )
                self.Portada.pack(fill = tk.BOTH, expand = tk.YES)

                self.FrameInformacionAlbum = tk.Frame(
                    self.LabelFrameInformacion, background = '#D5A27C',
                    width = 700, height = 400, relief = tk.FLAT, border = 0
                )
                self.FrameInformacionAlbum.pack(fill = tk.BOTH, expand = tk.YES, side = tk.TOP)

                self.NombreAlbum = tk.Label(
                    self.FrameInformacionAlbum, text = VINILO_SELECCIONADO['values'][3],
                    font = ('Ubuntu light', 22, 'bold'), background = '#D5A27C',
                    foreground = '#FFFFFF'
                )
                self.NombreAlbum.pack(expand = tk.YES)
                self.ArtistaAlbum = tk.Label(
                    self.FrameInformacionAlbum,
                    text = str(f"{VINILO_SELECCIONADO['values'][2]} \n\n\n\n"),
                    font = ('Ubuntu light', 18), background = '#D5A27C',
                    foreground = '#FFFFFF'
                )
                self.ArtistaAlbum.pack(expand = tk.YES)

                self.FramePanelInformacion = tk.Frame(
                    self.FrameInformacionAlbum, background = '#786271',
                    relief = 'flat', border = 0
                )
                self.FramePanelInformacion.pack(
                    fill = tk.BOTH, expand = tk.YES, side = tk.BOTTOM
                )
                self.FrameInformacionPublicacion = tk.Frame(
                    self.FramePanelInformacion, background = '#786271',
                    relief = 'flat', border = 0
                )
                self.FrameInformacionPublicacion.pack(
                    fill = tk.BOTH, expand = tk.YES, side = tk.LEFT
                )
                self.FrameInformacionVinilo = tk.Frame(
                    self.FramePanelInformacion, background = '#786271',
                    relief = 'flat', border = 0
                )
                self.FrameInformacionVinilo.pack(
                    fill = tk.BOTH, expand = tk.YES, side = tk.RIGHT
                )
                self.CodigoAlbum = tk.Label(
                    self.FrameInformacionPublicacion, text = 'Codigo Spotify',
                    font = ('Ubuntu light', 14, 'bold'), background = '#786271',
                    foreground = '#FFFFFF'
                )
                self.CodigoAlbum.pack(expand = tk.YES, anchor = tk.W, padx = 10)
                self.FechaCreacion = tk.Label(
                    self.FrameInformacionPublicacion, text = 'Fecha creación',
                    font = ('Ubuntu light', 14, 'bold'), background = '#786271',
                    foreground = '#FFFFFF'
                )
                self.FechaCreacion.pack(expand = tk.YES, anchor = tk.W, padx = 10)
                self.FechaPublicacion = tk.Label(
                    self.FrameInformacionPublicacion, text = 'Fecha publicación',
                    font = ('Ubuntu light', 14, 'bold'), background = '#786271',
                    foreground = '#FFFFFF'
                )
                self.FechaPublicacion.pack(expand = tk.YES, anchor = tk.W, padx = 10)

                self.StockPublicacion = tk.Label(
                    self.FrameInformacionPublicacion, text = 'Stock disponible',
                    font = ('Ubuntu light', 14, 'bold'), background = '#786271',
                    foreground = '#FFFFFF'
                )
                self.StockPublicacion.pack(expand = tk.YES, anchor = tk.W, padx = 10)

                self.PrecioPublicacion = tk.Label(
                    self.FrameInformacionPublicacion, text = 'Precio',
                    font = ('Ubuntu light', 14, 'bold'), background = '#786271',
                    foreground = '#FFFFFF'
                )
                self.PrecioPublicacion.pack(expand = tk.YES, anchor = tk.W, padx = 10)


                self.CodigoAlbumValor = tk.Label(
                    self.FrameInformacionVinilo, text = VINILO_SELECCIONADO['values'][6],
                    font = ('Ubuntu light', 15), background = '#786271',
                    foreground = '#FFFFFF'
                )
                self.CodigoAlbumValor.pack(expand = tk.YES, anchor = tk.W, padx = 10)
                self.FechaCreacionValor = tk.Label(
                    self.FrameInformacionVinilo, text = VINILO_SELECCIONADO['values'][8],
                    font = ('Ubuntu light', 15), background = '#786271',
                    foreground = '#FFFFFF'
                )
                self.FechaCreacionValor.pack(expand = tk.YES, anchor = tk.W, padx = 10)

                self.FechaPublicacionValor = tk.Label(
                    self.FrameInformacionVinilo, text = VINILO_SELECCIONADO['values'][9],
                    font = ('Ubuntu light', 15), background = '#786271',
                    foreground = '#FFFFFF'
                )
                self.FechaPublicacionValor.pack(expand = tk.YES, anchor = tk.W, padx = 10)

                self.StockPublicacionValor = tk.Label(
                    self.FrameInformacionVinilo, text = VINILO_SELECCIONADO['values'][7],
                    font = ('Ubuntu light', 15), background = '#786271',
                    foreground = '#FFFFFF'
                )
                self.StockPublicacionValor.pack(expand = tk.YES, anchor = tk.W, padx = 10)

                self.PrecioPublicacionValor = tk.Label(
                    self.FrameInformacionVinilo, text = f"$ {VINILO_SELECCIONADO['values'][5]}",
                    font = ('Ubuntu light', 15), background = '#786271',
                    foreground = '#FFFFFF'
                )
                self.PrecioPublicacionValor.pack(expand = tk.YES, anchor = tk.W, padx = 10)


                self.VentanaPerfil.mainloop()
            except Exception as e:
                self.ERROR.append(e)


# Web
    def __IniciarWeb(self):
        print(self.Propiedades.RUTA_MANAGE)
        ESTADO = False
        try:
            if self.Propiedades.ESTADO_WEB == False:
                os.popen(f'start cmd /k {self.Propiedades.COMANDO_INICIAR_WEB} && exit')
                os.system(f'{self.Propiedades.COMANDO_INICIAR_BRAVE} && exit')
                ESTADO = True
                self.Propiedades.ESTADO_WEB = True
                self.LabelEstadoWeb['text'] = f'[ {self.Propiedades.ESTADO_WEB} ]'
                self.LabelEstadoWeb['foreground'] = '#A6F2A1'


        except Exception as e:
            self.ERROR.append(e)
            messagebox.showerror(
                '[ ! ] Servicio no iniciado',
                'WEB Django no se pudo iniciar correctamente'
            )
            ESTADO = False
            self.Propiedades.ESTADO_WEB = False
            self.LabelEstadoWeb['text'] = f'[ {self.Propiedades.ESTADO_WEB} ]'
            self.LabelEstadoWeb['foreground'] = '#D83A3A'
        finally:
            print(
                f'└ [ {ESTADO} ]   exec >> start cmd /k {self.Propiedades.COMANDO_INICIAR_WEB}\n└ [ {ESTADO} ]   exec >> {self.Propiedades.COMANDO_INICIAR_BRAVE}'
            )

    def __DetenerWeb(self):
        if self.Propiedades.ESTADO_WEB == True:
            os.system('taskkill /f /im cmd.exe"')
            self.Propiedades.ESTADO_WEB = False
            self.LabelEstadoWeb['text'] = f'[ {self.Propiedades.ESTADO_WEB} ]'
            self.LabelEstadoWeb['foreground'] = '#D83A3A'
        else:
            pass

    def __IniciarPerfilVinilo(self):
        VINILO_SELECCIONADO = self.TreeView.item(self.TreeView.focus())
        SECCION = 'vinilo/'
        ID_VINILO_SELECCIONADO = self.TreeView.item(self.TreeView.selection())['values'][0]
        
        COMANDO_INICIAR_PERFIL_VINILO = f'start brave --incognito http://127.0.0.1:8000/{SECCION}{ID_VINILO_SELECCIONADO}'

        ESTADO = False
        try:
            if self.Propiedades.ESTADO_WEB == False:
                os.popen(f'start cmd /k {self.Propiedades.COMANDO_INICIAR_WEB}')
                os.system(f'{COMANDO_INICIAR_PERFIL_VINILO}')
                ESTADO = True
                self.Propiedades.ESTADO_WEB = True
                self.LabelEstadoWeb['text'] = f'[ {self.Propiedades.ESTADO_WEB} ]'
                self.LabelEstadoWeb['foreground'] = '#A6F2A1'

        except Exception as e:
            self.ERROR.append(e)
            messagebox.showerror(
                '[ ! ] Servicio no iniciado',
                'WEB Django no se pudo iniciar correctamente'
            )
            ESTADO = False
            self.Propiedades.ESTADO_WEB = False
            self.LabelEstadoWeb['text'] = f'[ {self.Propiedades.ESTADO_WEB} ]'
            self.LabelEstadoWeb['foreground'] = '#D83A3A'
        finally:

            print(
                f'''
Sistema
└ [ {ESTADO} ]   exec >> start cmd /k {self.Propiedades.COMANDO_INICIAR_WEB}
└ [ {ESTADO} ]   exec >> {COMANDO_INICIAR_PERFIL_VINILO}

Vinilo
└ ID                    {self.TreeView.item(self.TreeView.selection())['values'][0]}
└ ID AUTOR              {self.TreeView.item(self.TreeView.selection())['values'][1]}
└ ARTISTA               {self.TreeView.item(self.TreeView.selection())['values'][2]}
└ ALBUM                 {self.TreeView.item(self.TreeView.selection())['values'][3]}
└ IMG                   {self.TreeView.item(self.TreeView.selection())['values'][4]}
└ PRECIO                {self.TreeView.item(self.TreeView.selection())['values'][5]}
└ ID SPOTIFY            {self.TreeView.item(self.TreeView.selection())['values'][6]}
└ STOCK                 {self.TreeView.item(self.TreeView.selection())['values'][7]}
└ FECHA CREACION        {self.TreeView.item(self.TreeView.selection())['values'][8]}
└ FECHA PUBLICACION     {self.TreeView.item(self.TreeView.selection())['values'][9]}

            ''')
if __name__ == '__main__':
    # Inicializacion Tk
    w = tk.Tk()

    # Manejo de errores
    ERROR = []

    # Inicio de app
    Interfaz(w, ERROR).mainloop()
