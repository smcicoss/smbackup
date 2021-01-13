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

import os
import time
import shutil

from lib.configdata import ConfigData
from utiles.strutil import Color, text_paragraph, clear, h2
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
        self.__HostConf = ConfigData()

        options = [{
            'item':
            "eMail:",
            'value':
            self.__HostConf.email,
            'desc':
            "Dirección email del administrador o \
                    encargado de recibir los avisos y resumenes"
        }, {
            'item': "Unidades:",
            'value': self.__HostConf.DirUnits,
            'desc': "Directorio para las configuraciones de unidades"
        }, {
            'item': "Remote Mount:",
            'value': self.__HostConf.RemoteMount,
            'desc': "Directorio en el que montar los sistemas remotos"
        }, {
            'item': "Default Mount Point:",
            'value': self.__HostConf.DefaultMountPoint,
            'desc': "Punto de Montado de unidades por defecto"
        }, {
            'item': "Nombre Unidad por defecto:",
            'value': self.__HostConf.DefaultUnitName,
            'desc': "Nombre de la unidad que se usará por defecto"
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
                self.__edit_remote_mount()
            elif editar.option == 3:
                self.__edit_default_mount_point()
            elif editar.option == 4:
                self.__edit_default_unit()

    def __del__(self):
        """
        __del__ destructor

        salva el fichero de configuración
        """
        self.__HostConf.save()

    def __str__(self):
        __str = f"\n{color.BLANCO}{'='*60}\n"
        __str += " Edicción del fichero de configuración ".center(60, "*")
        __str += f"\n{'='*60}{color.END}\n"
        __str += f"Fichero: {color.VERDE}"
        __str += f"{self.__HostConf.ConfigFile.rjust(51)}{color.END}\n"

        __lastUpdate = time.ctime(self.__HostConf.LastChange)

        __str += "Modificado por última vez: "
        __str += f"{color.VERDE}{__lastUpdate.rjust(33)}{color.END}\n"
        __str += f"{'='*60}\n\n{self.__HostConf}"
        __str += f"\n{'='*60}\n"

        return __str

    def __edit_mail(self):
        """
        __edit_mail

        edita la dirección de mail del administrador
        """
        print(h2(" Dirección de eMail "))

        print(f"Valor actual: {color.VERDE}%s{color.END}" %
              self.__HostConf.email.rjust(46, '.'))

        strhelp = '''
                  Esta dirección se usará para enviar las alertas,
                  informe de errores y resumenes de copias.
                  '''

        strhelp = text_paragraph(strhelp, 60, ' ' * 5)
        print(f"\n{color.MARRON}{strhelp}{color.END}\n\n")

        print("\n Introduce el nuevo valor")
        nuevoemail = input(f"o solo [Intro] para no modificar: {color.VERDE}")
        self.__HostConf.email = nuevoemail
        print(f"{color.END}\n{'-'*60}\n{self.__HostConf}\n{'-'*60}\n")

    def __edit_dir_unities(self):
        """
        __edit_dir_unities

        edita el directorio donde almacenar las
        configuraciones de unidades de backup
        """

        title = " Path al directorio de configuración \n"
        title += "de unidades"
        print(h2(title))

        print(f"Valor actual: {color.VERDE}%s{color.END}" %
              self.__HostConf.DirUnits.rjust(46, '.'))

        strhelp = '''
                    En este directorio se guardaren los datos de
                    configuración de unidades. Si comienza por
                    barra '/' asignará un path absoluto, si no será
                    un subdirectorio del de Configuración.
                    '''

        strhelp = text_paragraph(strhelp, 60, ' ' * 5, '')
        print(f"\n{color.MARRON}{strhelp}{color.END}\n\n")

        viejopath = self.__HostConf.DirUnits
        print("\n Introduce el nuevo valor")
        nuevopath = input(f"o solo [Intro] para no modificar: {color.VERDE}")
        print(f"{color.END}")

        if nuevopath != "":
            self.__HostConf.DirUnits = nuevopath
            if viejopath != self.__HostConf.DirUnits:
                if os.path.isdir(viejopath):
                    if os.listdir(viejopath):
                        print("El anterior direcotrio contenía ficheros")
                        print("¿Quiere moverlos a la nueva ubicación)")
                        respuesta = input("[s/n]:")
                        if respuesta[0].lower() == "s":
                            lista = os.listdir(viejopath)
                            for f in lista:
                                fullf = os.path.join(viejopath, f)
                                shutil.move(fullf,
                                            self.__HostConf.DirUnits + "/")

    def __edit_remote_mount(self):
        """
        __edit_remote_mount

        edita el directorio donde montar los sistemas de ficheros remotos
        """

        clear()
        print(h2("Punto de montado de sistemas remotos"))

        print(f"Valor actual: {color.VERDE}%s{color.END}" %
              self.__HostConf.RemoteMount.rjust(46, '.'))

        strhelp = '''
                    En este directorio se montarán los sistema
                    de archivos remotos para los casos en los
                    que no se pueda utilizar rsync directo.
                    Se creará un subdirectorio con el nombre
                    de la copia.
                    En este procedimiento suele ser mucho más lento.
                    '''

        strhelp = text_paragraph(strhelp, 60)

        print(f"\n{color.MARRON}{strhelp}{color.END}\n\n")

        print("\n Introduce el nuevo valor")
        nuevopath = input(f"o solo [Intro] para no modificar: {color.VERDE}")
        print(f"{color.END}")

        if nuevopath != "":
            try:
                self.__HostConf.RemoteMount = nuevopath
            except PermissionError:
                print(f"{color.ERROR}{'*'*60}")
                print("No se ha podido crear el directorio")
                print("No dispone de permisos. Ejecute el programa con sudo.")
                print(f"{'*'*60}{color.END}")

    def __edit_default_mount_point(self):
        """
        __edit_default_mount_point

        edita el directorio por defecto donde montar las unidades
        si no están montadas en el momento de la copia
        """

        print("-" * 60)
        print(" Punto de montado de ".center(60))
        print(" sistemas remotos".center(60))
        print("-" * 60)

        print(f"Valor actual: {color.VERDE}%s{color.END}" %
              self.__HostConf.DefaultMountPoint.rjust(46, '.'))

        strhelp = '''
                  En este directorio se montarán las unidades
                  que en el momento de utilizar no lo estuvieran.
                  '''

        strhelp = text_paragraph(strhelp, 60, ' ' * 5)

        print(f"\n{color.MARRON}{strhelp}{color.END}\n\n")

        print("\n Introduce el nuevo valor")
        nuevopath = input(f"o solo [Intro] para no modificar: {color.VERDE}")
        print(f"{color.END}")

        if nuevopath != "":
            try:
                self.__HostConf.DefaultMountPoint = nuevopath
            except PermissionError:
                print(f"{color.ERROR}{'*'*60}")
                print("No se ha podido crear el directorio")
                print("No dispone de permisos. Ejecute el programa con sudo.")
                print(f"{'*'*60}{color.END}")

    def __edit_default_unit(self):
        """
        __edit_default_unit

        edita el nombre de la unidad a usar por defecto
        """

        print("-" * 60)
        print(" Unidad por defecto ".center(60))
        print("-" * 60)

        print(f"Valor actual: {color.VERDE}%s{color.END}" %
              self.__HostConf.DefaultUnitName.rjust(46, '.'))

        strhelp = '''
                    Esta es la unidad que se utilizará en caso de que no
                    se especifique otra cosa.
                    '''

        strhelp = text_paragraph(strhelp, 60, ' ' * 5)
        print(f"\n{color.MARRON}{strhelp}{color.END}\n\n")

        lista = os.listdir(self.__HostConf.DirUnits)
        opciones = []
        for uni in lista:
            if "default" not in uni:
                opciones.append({'item': os.path.splitext(uni)[0], 'desc': ""})
        elige = Menu(opciones)

        if elige.option is not None:
            self.__HostConf.DefaultUnitName = opciones[elige.option]['item']

    @property
    def modificado(self):
        """
        modificado datos modificados

        informa si se ha modificado algún dato antes de salvar

        Returns:
            bool: True = modificado
        """

        return self.__HostConf.Modificado
