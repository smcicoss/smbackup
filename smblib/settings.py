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

import os
from datetime import datetime
import json
from pathlib import Path
from utiles.strutil import color, is_valid_email
from utiles.pathutil import disjoin
from utiles.systools import SysInfo


class Settings(ConfigData):

    __version = "4.0"
    ConfigDir = Path(f"/etc/smbackup-{__version}")
    ConfigFile = ConfigDir.joinpath(ConfigDir, "config.json")

    def __init__(self):
        self.__sysinfo = SysInfo()

        self.__modificado = False
        self.__DirThisFile = Path(__file__).parent
        self.__CurrentDir = Path.cwd()

        self.__LastChange = datetime.fromtimestamp(
            self.ConfigFile.stat().st_mtime)
        with open(self.ConfigFile, 'r') as file:
            data_conf = json.load(file)

        self.__Presenta = data_conf['presenta']
        self.__email = data_conf['email']
        self.__DirUnits = self.ConfigDir.joinpath(
            data_conf['DIRS']['CONF_UNITS'])
        self.__DirInstall = Path(data_conf['DIRS']['INSTALL'])
        self.__DirLibraries = self.__DirInstall.joinpath(
            data_conf['DIRS']['LIBRARIES'])

        file_default_unit = self.__DirUnits.joinpath("default.json")

        with open(file_default_unit, 'r') as file:
            data_default_unit = json.load(file)

        self.__DefaultUnitName = data_default_unit['nombre']
        self.__DefaultMountPoint = data_default_unit['mount_point']

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
        return string

    def __del__(self):
        """
        __del__ Destructor

        Genera un error si se cierra sin salvar

        Raises:
            NameError: "Quedan modificaciones sin salvar"
        """
        if self.__modificado:
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
                                                  self.__DirUnits)
        data_conf['DIRS']['INSTALL'] = self.DirInstall
        data_conf['DIRS']['LIBRARIES'] = disjoin(self.DirInstall,
                                                 self.DirLibraries)
        data_default_unit = {}
        data_default_unit['nombre'] = self.DefaultUnitName
        data_default_unit['mount_point'] = self.DefaultMountPoint
        with open(self.ConfigFile, 'w') as file:
            json.dump(data_conf, file)

        file_default_unit = self.DirUnits + "/default.json"

        with open(file_default_unit, 'w') as file:
            json.dump(data_default_unit, file)

        self.__modificado = False

    def __getitem__(self, item):
        if item == "nombre":
            return self.nombre
        if item == 'version':
            return self.version
        if item == 'Presenta':
            return self.Presenta
        if item == 'email':
            return self.email
        if item == "DirUnits":
            return self.DirUnits
        if item == "DirInstall":
            return self.DirInstall
        if item == "DirLibraries":
            return self.DirLibraries
        if item == "CurrentDir":
            return self.CurrentDir
        if item == 'uuid':
            return self.uuid

    @property
    def version(self):
        return self.__version

    @property
    def DirThisFile(self):
        return self.__DirThisFile

    @property
    def Presenta(self):
        return self.__Presenta

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        if is_valid_email(value):
            self.__email = value
            self.__modificado = True

    @property
    def DirUnits(self):
        return self.__DirUnits

    @DirUnits.setter
    def DirUnits(self, value):
        if not value:
            return
        if value[0] == "/":
            path = Path(value)
        else:
            path = self.ConfigDir.joinpath(value)

        os.makedirs(path, exist_ok=True)
        self.__DirUnits = path
        self.__modificado = True

    @property
    def DirInstall(self):
        return self.__DirInstall

    @property
    def CurrentDir(self):
        return self.__CurrentDir

    @property
    def DirLibraries(self):
        return self.__DirLibraries

    @property
    def DefaultMountPoint(self):
        return self.__DefaultMountPoint

    @DefaultMountPoint.setter
    def DefaultMountPoint(self, value):
        path = Path(value).resolve()
        if path[0] != "/":
            path = os.path.join("/mnt", path)

        os.makedirs(path, exist_ok=True)
        self.__DefaultMountPoint = path
        self.__modificado = True

    @property
    def DefaultUnitName(self):
        return self.__DefaultUnitName

    @DefaultUnitName.setter
    def DefaultUnitName(self, value):
        self.__DefaultUnitName = value
        self.__modificado = True

    @property
    def uuid(self):
        return self.__uuid

    @property
    def LastChange(self):
        return self.__LastChange

    @property
    def Modificado(self):
        return self.__modificado
