# -*- coding: utf-8 -*-
# ·
"""
===============================================================================
                                    Unit
===============================================================================
Autor:  Simón Martínez <simon@cicoss.net>
Fecha:  dom nov  1 18:53:33 CET 2020
===============================================================================

Clase destinada a mantener los datos de una Unidad de copia y
sus operaciones

Se entiende por unidad una partición de un disco, tanto interno
como usb, tanto abierto como cifrado destinada a albergar copias de seguridad
así como sus configuraciones.

La base de identificación de la unidad será el UUID, utilizando el Label
y un Nombre interno (generalmente coincidente con el label) para facilidad
de referencia. Este nombre ha de ser único en el sistema y se ará corresponder
con el UUID ya que el LABEL de una partición
puede estar duplicada o no existir

"""

import os
import json
from smblib.unitdata import UnitData
from utiles.strutil import clean_str
from mod.blkdevices import BlockDevices


class Unit(UnitData):
    """
     Unit: Clase de objeto que representa a una unidad
     de copia de seguridad

     Mantiene los datos y los procedimientos relativos a
     las unidades de copia de seguridad
    """
    def __init__(self, value, pathUnits):

        if pathUnits is None or not os.path.isdir(pathUnits):
            raise TypeError

        if isinstance(value, str):
            # se espera que la unidad ya exista con ese nombre
            self.__fileName = clean_str(value) + '.json'
            self.__pathFileUnit = os.path.join(pathUnits, self.__fileName)
            if self.__load_data():
                self.__exists = True

        elif isinstance(value, UnitData):
            # Nueva con UnitData
            self.__fileName = value['Name'] + '.json'
            self.__pathFileUnit = os.path.join(pathUnits, self.__fileName)
            super().__init__(value)

        elif isinstance(value, dict):
            # Nueva con dictionary
            self.__fileName = value['Name'] + '.json'
            self.__pathFileUnit = os.path.join(pathUnits, self.__fileName)
            super().__init__(value)

        elif value is None:
            super().__init__()

        else:
            raise TypeError("Error en datos pasados a Unidad")

        if os.path.exists(self.__pathFileUnit):
            self.__exists = True
        else:
            self.__exists = False

        if self.Uuid is not None:
            self.__Devices = BlockDevices()
            result = self.__Devices.full_search_uuid(self.Uuid)
            if result is None:
                self.__isConnected = False
                return

            self.__BlkDev = result[result['en']]
            self.__isConnected = True
            if not self.Crypt and self.__BlkDev.type == 'part':
                self.__mountpoint = self.__BlkDev.mountpoint
            else:
                self.__mountpoint = None

    def __str__(self):
        """
        __str__ conversión a string

        genera una representación de los datos formateada

        Returns:
            str: string formateado
        """
        string = f"Nombre: {self.Name.rjust(52, '.')}\n"
        string += f"Archivo: {self.FileName.rjust(51,'.')}\n"
        string += f"Descripción: {self.Description.rjust(47,'.')}\n"
        string += f"Label: {self.Label.rjust(53,'.')}\n"
        string += f"UUID: {self.Uuid.rjust(54,'.')}\n"
        if self.Crypt:
            string += f"UUIDP: {self.UuidP.rjust(53,'.')}\n"
        string += f"Cifrado: {str(self.Crypt).rjust(51,'.')}\n"
        string += f"Subdirectorio: {self.DirBackups.rjust(45,'.')}\n"
        string += f"Conf. copias: {self.Meta.rjust(46,'.')}\n"

        return string

    def __load_data(self):
        if not os.path.exists(self.__pathFileUnit):
            return False

        try:
            with open(self.__pathFileUnit, 'r') as funidad:
                # leo el fichero
                data_unit = json.load(funidad)

        except IOError:
            return False

        super().__init__(data_unit)
        # for field in self.fields:
        # self.__setitem(field, data_unit[field])
        self.__exists = True
        return True

    def have_copies(self):
        _copies = self.find_copies()
        if _copies is None:
            return None
        if len(_copies) == 0:
            return False
        return True

    def find_copies(self):
        if self.mountpoint is None:
            return None

        _fullMeta = os.path.join(self.__mountpoint, self.Meta)
        _copies = []
        with os.scandir(_fullMeta) as _filesMeta:
            for _fileMeta in _filesMeta:
                if not _fileMeta.name.startswith('.') and \
                   _fileMeta.is_file and \
                   _fileMeta.name.endswith('.json'):
                    _copies.append(_fileMeta)
        return _copies

    @property
    def exists(self):
        """
        exists

        Confirma si existe el fichero de configuración
        El valor se establece en el constructor

        Returns:
            Bool: True si el fichero existe
        """

        return self.__exists

    def save(self):
        """Salva los datos en fichero <nombre_unidad>.json
        """
        if self.modified and self.finised:
            data = {
                "Name": self.Name,
                "Description": self.Description,
                "Label": self.Label,
                "Uuid": self.Uuid,
                "UuidP": self.UuidP,
                "Crypt": self.Crypt,
                "DirBackups": self.DirBackups,
                "Meta": self.Meta
            }

            with open(self.__pathFileUnit, 'w') as file:
                json.dump(data, file, indent=4)

    @property
    def FileName(self):
        """Propiedad File

        Returns:
            string: Nombre del fichero de configuración
        """
        return self.__fileName

    @property
    def PathFile(self):
        return self.__pathFileUnit

    @property
    def BLkDevice(self):
        if not self.__isConnected:
            return None
        return self.__BlkDev

    @property
    def connected(self):
        return self.__isConnected

    @property
    def mountpoint(self):
        if not self.__isConnected:
            return None
        return self.__mountpoint

    @property
    def DevPath(self):
        if not self.__isConnected:
            return None
        return self.__BlkDev.path

    @property
    def myData(self):
        return super()
