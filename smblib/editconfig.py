# -*- coding: utf-8 -*-
# ·
"""
===============================================================================
                              editconfig.py
===============================================================================
    Autor: Simón Martínez <simon@cicoss.net>
    Fecha: mié nov 18 13:01:00 CET 2020
-------------------------------------------------------------------------------

    Clase para la edición del fichero de configuración general

"""

from smblib.settings import Settings
from utiles.color import Color
from utiles.strutil import h1, h2, data_line, clear
from utiles.editdata import edit_data
from utiles.menu import Menu

color = Color()


class EditConfig():
    """
    EditConfig

    Edita el fichero de configuración de forma interactiva
    """
    def __init__(self):
        """
        __init__ Constructor

        Realiza la presentación y controla el menú
        """
        self.__LocalConf = Settings()

        options = [{
            'item':
            "email:",
            'value':
            self.__LocalConf.email,
            'desc':
            """
                        Dirección email del administrador o
                        encargado de recibir los avisos y resumenes
                        """
        }, {
            'item':
            "units_conf:",
            'value':
            self.__LocalConf.units_conf,
            'desc':
            """
                        Directorio para las configuraciones
                        de unidades
                        """
        }, {
            'item':
            "units_mount:",
            'value':
            self.__LocalConf.DefaultMountPoint,
            'desc':
            """
                        Punto de Montado de unidades
                        por defecto
                        """
        }]

        while True:
            clear()
            print(self)

            editar = Menu(options)

            if editar.option is None:
                break
            if editar.option == 0:
                self.__edit_mail()
            elif editar.option == 1:
                self.__edit_dir_unities()
            elif editar.option == 2:
                self.__edit_default_mount_point()

    def __del__(self):
        """
        __del__ destructor

        salva el fichero de configuración
        """
        self.__LocalConf.save(self.__LocalConf.file_conf)

    def __str__(self):
        __str = h1("Edicción del fichero de configuración")
        __str += data_line({
            'key': "Fichero",
            'value': f"{self.__LocalConf.ConfigFile}"
        })
        h2('')

        # __lastUpdate = time.ctime(self.__LocalConf.m_time)

        __str += data_line({
            'key': "Modificado por última vez",
            'value': f"{self.__LocalConf.m_time}"
        })
        __str += str(self.__LocalConf)

        return __str

    def __edit_mail(self):
        """
        __edit_mail

        edita la dirección de mail del administrador
        """
        _data = {}
        _data['title'] = "Dirección de eMail"
        _data['key'] = "Valor actual"
        _data['value'] = self.__LocalConf.email
        _data['help'] = '''
                  Esta dirección se usará para enviar las alertas,
                  informe de errores y resumenes de copias.
                  '''
        _data['prompt'] = "Introduce el nuevo valor"

        self.__LocalConf.email = edit_data(_data)

    def __edit_dir_unities(self):
        """
        __edit_dir_unities

        edita el directorio donde almacenar las
        configuraciones de unidades de backup
        """

        _data = {}
        _data['title'] = " Path al directorio de configuración \nde unidades"
        _data['key'] = "Valor actual"
        _data['value'] = str(self.__LocalConf.units_conf)
        _data['help'] = '''
                    En este directorio se guardaren los datos de
                    configuración de unidades. Si comienza por
                    barra '/' asignará un path absoluto, si no será
                    un subdirectorio del de Configuración.
                    '''

        _data['prompt'] = "Introduce el nuevo valor"

        self.__LocalConf.units_conf = edit_data(_data)

        return

    def __edit_default_mount_point(self):
        """
        __edit_default_mount_point

        edita el directorio por defecto donde montar las unidades
        si no están montadas en el momento de la copia
        """

        _data = {}
        _data[
            'title'] = "Punto de montado por defecto de \n" + \
                        " sistemas remotos"
        _data['key'] = "Valor actual"
        _data['value'] = str(self.__LocalConf.units_mount)
        _data['help'] = '''
                  En este directorio se montarán las unidades
                  que en el momento de utilizar no lo estuvieran.
                  '''
        _data['prompt'] = "Introduce el nuevo valor"

        self.__LocalConf.units_mount = edit_data(_data)

        if self.__LocalConf.changed:
            if not self.__LocalConf.units_mount.exists():
                try:
                    self.__LocalConf.units_mount.mkdir(parents=True)
                except PermissionError:
                    input("No está autorizado para esta operación")
                    self.__LocalConf = Settings()

        return

    @property
    def modificado(self):
        """
        modificado datos modificados

        informa si se ha modificado algún dato antes de salvar

        Returns:
            bool: True = modificado
        """

        return self.__LocalConf.Modificado
