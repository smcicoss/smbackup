# -*- coding: utf-8 -*-
# ·
"""
===============================================================================
                               configdata.py
===============================================================================
    Autor: Simón Martínez <simon@cicoss.net>
    Fecha: domingo, 10 de enero de 2021
-------------------------------------------------------------------------------

    definición de la clase ConfigData

"""

import json
import os
from pathlib import Path
from pathlib import PurePosixPath as PPP
from utiles.strutil import color, is_valid_email
from utiles.pathutil import disjoin


class ConfigData():
    """
    ConfigData

    Clase para el mantenimiento y acceso al
    fichero de configuración de smbackup
    """

    # variables de clase

    ConfigDir = PPP("/etc/smbackup-4.0")
    ConfigFile = ConfigDir.joinpath(ConfigDir, "config.json")

    def __init__(self):
        """
        __init__ Constuctor

        declara variables y lee los ficheros
        config y defaults
        """
        self._modificado = False
        self._version = "4.0"
        self._DirThisFile = PPP(__file__).parent
        self._CurrentDir = Path.cwd()

        self._LastChange = Path(self.ConfigFile).stat().st_mtime
        with open(self.ConfigFile, 'r') as file:
            data_conf = json.load(file)

        self._Presenta = data_conf['presenta']
        self._email = data_conf['email']
        self._DirUnits = self.ConfigDir.joinpath(
            data_conf['DIRS']['CONF_UNITS'])
        self._DirInstall = PPP(data_conf['DIRS']['INSTALL'])
        self._DirLibraries = self._DirInstall.joinpath(
            data_conf['DIRS']['LIBRARIES'])

        file_default_unit = self._DirUnits.joinpath("default.json")

        with open(file_default_unit, 'r') as file:
            data_default_unit = json.load(file)

        self._DefaultUnitName = data_default_unit['nombre']
        self._DefaultMountPoint = data_default_unit['mount_point']

    def __str__(self):
        """
        __str__

        formatea los dato de salida en un print()

        Returns:
            string: cadena formateada
        """
        string = f"eMail:{color.VERDE}{self.email.rjust(54,'.')}{color.END}\n"
        string += "Directorios:\n"
        string += f"\tConfiguración:{color.VERDE}"
        string += f"{str(self.ConfigDir).rjust(38,'.')}"
        string += f"{color.END}\n"
        string += f"\tUnidades:{color.VERDE}"
        string += f"{str(self.DirUnits).rjust(43,'.')}{color.END}\n"
        string += f"{color.END}\n"
        string += "Defaults:\n"
        string += f"\tDirectorio unidades:{color.VERDE}"
        string += f"{self.DefaultMountPoint.rjust(32,'.')}{color.END}\n"
        string += f"\tUnidad:{color.VERDE}{self.DefaultUnitName.rjust(45,'.')}"
        string += f"{color.END}"
        return string

    def __del__(self):
        """
        __del__ Destructor

        Genera un error si se cierra sin salvar

        Raises:
            NameError: "Quedan modificaciones sin salvar"
        """
        if self._modificado:
            raise NameError(color.ERROR + "Quedan modificaciones sin salvar" +
                            color.END)

    def save(self):
        """
        save salva los datos

        Necesita ser expresamente llamada ya que
        la funcion interna open no es llamable desde
        el destructor
        """

        data_conf = {}
        data_conf['nombre'] = 'config'
        data_conf['presenta'] = self.Presenta
        data_conf['email'] = self.email
        data_conf['DIRS'] = {}
        data_conf['DIRS']['CONF_UNITS'] = disjoin(self.ConfigDir,
                                                  self._DirUnits)
        data_conf['DIRS']['INSTALL'] = self.DirInstall
        data_conf['DIRS']['LIBRARIES'] = disjoin(self.DirInstall,
                                                 self.DirLibraries)
        data_conf['DIRS']['MOUNT_REMOTOS'] = self.RemoteMount
        data_default_unit = {}
        data_default_unit['nombre'] = self.DefaultUnitName
        data_default_unit['mount_point'] = self.DefaultMountPoint
        with open(self.ConfigFile, 'w') as file:
            json.dump(data_conf, file)

        file_default_unit = self.DirUnits + "/default.json"

        with open(file_default_unit, 'w') as file:
            json.dump(data_default_unit, file)

        self._modificado = False

    @property
    def version(self):
        return self._version

    @property
    def DirThisFile(self):
        return self._DirThisFile

    @property
    def Presenta(self):
        return self._Presenta

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if is_valid_email(value):
            self._email = value
            self._modificado = True

    @property
    def DirUnits(self):
        return self._DirUnits

    @DirUnits.setter
    def DirUnits(self, value):
        if not value:
            return
        if value[0] == "/":
            path = PPP(value)
        else:
            path = self.ConfigDir.joinpath(value)

        os.makedirs(path, exist_ok=True)
        self._DirUnits = path
        self._modificado = True

    @property
    def DirInstall(self):
        return self._DirInstall

    @property
    def CurrentDir(self):
        return self._CurrentDir

    @property
    def DirLibraries(self):
        return self._DirLibraries

    @property
    def DefaultMountPoint(self):
        return self._DefaultMountPoint

    @DefaultMountPoint.setter
    def DefaultMountPoint(self, value):
        path = os.path.normpath(os.path.expanduser(value))
        if path[0] != "/":
            path = os.path.join("/mnt", path)

        os.makedirs(path, exist_ok=True)
        self._DefaultMountPoint = path
        self._modificado = True

    @property
    def DefaultUnitName(self):
        return self._DefaultUnitName

    @DefaultUnitName.setter
    def DefaultUnitName(self, value):
        self._DefaultUnitName = value
        self._modificado = True

    @property
    def LastChange(self):
        return self._LastChange

    @property
    def Modificado(self):
        return self._modificado
