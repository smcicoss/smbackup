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

from pathlib import Path
from shutil import copy2
import json
from datetime import datetime
from utiles.strutil import color, h1, h2, data_line


class ConfigData():
    """
    ConfigData

    Clase para el mantenimiento  de los datos
    y acceso al fichero de configuración de 'smbackup'
    """
    def __init__(self, data=None):

        self.__fileexists = False
        self.__fileconf = None
        self.__modtime = None

        if isinstance(data, dict) or isinstance(data, ConfigData):
            for item in data.keys():
                self[item] = data[item]
        elif isinstance(data, Path):
            self.load(data)
        elif data is None:
            for item in self.keys():
                self[item] = None
        else:
            raise ValueError("parametro inválido en ConfigData")

        self.__changed = False

    def __str__(self):
        _str = h1(self.display)
        _str += h2(f"Versión: {self.version} - {self.m_time}")
        for item in self.keys():
            _line = {'key': item, 'value': self[item]}
            _str += data_line(_line)
        return _str

    def __del__(self):
        if self.__changed:
            raise NameError("Quedan modificaciones sin salvar")

    def keys(self):
        return [
            "version", "uuid", "vendor", "model", "distro", "display", "email",
            "units_conf", "installation", "libraries", "units_mount"
        ]

    def __getitem__(self, item):
        if item == 'version':
            return self.version
        if item == 'uuid':
            return self.uuid
        if item == 'vendor':
            return self.vendor
        if item == 'model':
            return self.model
        if item == 'distro':
            return self.distro
        if item == 'display':
            return self.display
        if item == 'email':
            return self.email
        if item == 'units_conf':
            return self.units_conf
        if item == 'installation':
            return self.installation
        if item == 'libraries':
            return self.libraries
        if item == 'units_mount':
            return self.units_mount
        raise ValueError(f"{item} no existe")

    def __setitem__(self, item, value):
        if item == 'version':
            self.version = value
            return
        if item == 'uuid':
            self.uuid = value
            return
        if item == 'vendor':
            self.vendor = value
            return
        if item == 'model':
            self.model = value
            return
        if item == 'distro':
            self.distro = value
            return
        if item == 'display':
            self.display = value
            return
        if item == 'email':
            self.email = value
            return
        if item == 'units_conf':
            self.units_conf = value
            return
        if item == 'installation':
            self.installation = value
            return
        if item == 'libraries':
            self.libraries = value
            return
        if item == 'units_mount':
            self.units_mount = value
            return
        raise ValueError(f"{item} no existe")

    def load(self, pathfile):
        if pathfile.exists():
            self.__fileexists = True
            self.__fileconf = pathfile
            self.__modtime = pathfile.stat().st_mtime
        else:
            raise RuntimeError("El fichero de configuración no existe")

        with pathfile.open('r') as file:
            _data = json.load(file)
            for item in _data.keys():
                self[item] = _data[item]

    def save(self, pathfile):
        """ save salva los datos
        """

        if self.file_exists:
            _backfile = str(self.file_conf) + '~'
            copy2(str(self.file_conf), str(_backfile))

        _data = {}
        for item in self.keys():
            _data[item] = self[item]
        with open(self.file_conf, 'w') as file:
            json.dump(_data, file, indent=4, ensure_ascii=False)

        self.__fileconf = pathfile
        self.__modtime = pathfile.stat().st_mtime

        self.__changed = False

    @property
    def file_conf(self):
        return self.__fileconf

    @property
    def file_exists(self):
        return self.__fileexists

    @property
    def m_time(self):
        if self.__fileexists:
            return datetime.fromtimestamp(self.__modtime)
        return None

    @property
    def changed(self):
        return self.__changed

    @property
    def version(self):
        return self.__version

    @property
    def uuid(self):
        return self.__uuid

    @property
    def vendor(self):
        return self.__vendor

    @property
    def model(self):
        return self.__model

    @property
    def distro(self):
        return self.__distro

    @property
    def display(self):
        return self.__display

    @property
    def email(self):
        return self.__email

    @property
    def units_conf(self):
        return self.__units_conf

    @property
    def installation(self):
        return self.__installation

    @property
    def libraries(self):
        return self.__libraries

    @property
    def units_mount(self):
        return self.__units_mount

    @version.setter
    def version(self, value):
        self.__version = value
        self.__changed = True

    @uuid.setter
    def uuid(self, value):
        self.__uuid = value
        self.__changed = True

    @vendor.setter
    def vendor(self, value):
        self.__vendor = value
        self.__changed = True

    @model.setter
    def model(self, value):
        self.__model = value
        self.__changed = True

    @distro.setter
    def distro(self, value):
        self.__distro = value
        self.__changed = True

    @display.setter
    def display(self, value):
        self.__display = value
        self.__changed = True

    @email.setter
    def email(self, value):
        self.__email = value
        self.__changed = True

    @units_conf.setter
    def units_conf(self, value):
        self.__units_conf = value
        self.__changed = True

    @installation.setter
    def installation(self, value):
        self.__installation = value
        self.__changed = True

    @libraries.setter
    def libraries(self, value):
        self.__libraries = value
        self.__changed = True

    @units_mount.setter
    def units_mount(self, value):
        self.__units_mount = value
        self.__changed = True
