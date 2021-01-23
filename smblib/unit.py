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

from pathlib import Path
import json
from smblib.unitdata import UnitData
from utiles.strutil import h2
from blkmod.blockdevices import BlockDevices
from blkmod.readdevice import is_volume_open


class Unit(UnitData):
    """
     Unit: Clase de objeto que representa a una unidad
     de copia de seguridad

     Mantiene los datos y los procedimientos relativos a
     las unidades de copia de seguridad
    """
    def __init__(self, name, pathUnits, defaultmount):

        super().__init__()

        self.__isConnected = False

        if not isinstance(pathUnits, str):
            raise ValueError
        else:
            # path a configuracion de unidades
            self.__pathUnits = Path(pathUnits)
            if not self.__pathUnits.is_dir():
                raise ValueError

        if isinstance(name, str):
            # Nombre de la unidad
            self.name = name
            self.__pathFileUnit = self.__pathUnits / (name + '.json')
            if self.__load_data():
                self.__exists = True
            else:
                return

        self.__mountpoint = Path(defaultmount) / name

        if self.wwn is not None:
            self.__Devices = BlockDevices()
            self.__disk = self.__Devices.get_disk_wwn(self.wwn)
            if self.__disk is None:
                return

            self.__isConnected = True

            if not self.crypt:
                self.__part = self.__disk.get_partition_uuid(self.uuid)
                self.__FS = self.__part
            else:
                self.__part = self.__disk.get_partition_uuid(self.uuidp)

                if not is_volume_open(self.name):
                    self.__part.open_volume(self.name)
                self.__FS = self.__part.volume

            if self.__FS.mountpoint is None:
                self.__FS.mount(self.mountpoint)
            else:
                self.__mountpoint = self.__FS.mountpoint

    def __str__(self):
        """
        __str__ conversión a string

        genera una representación de los datos formateada

        Returns:
            str: string formateado
        """
        _str = h2(f"Unidad {self.name}")
        _str += super().__str__()

        return _str

    def __load_data(self):
        if not self.__pathFileUnit.exists():
            return False

        try:
            with self.__pathFileUnit.open('r') as funidad:
                # leo el fichero
                data_unit = json.load(funidad)

        except IOError:
            return False

        for key in self.keys():
            self[key] = data_unit[key]
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

        _fullMeta = Path(self.__mountpoint) / self.Meta
        _copies = []
        with _fullMeta.glob('*.json') as _filesMeta:
            for _fileMeta in _filesMeta:
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

        return self.__pathFileUnit.exists()

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
        return self.__FS.path

    @property
    def Disk(self):
        if not self.__isConnected:
            return None
        return self.__disk

    @property
    def Part(self):
        if not self.__isConnected:
            return None
        return self.__part

    @property
    def FS(self):
        if not self.__isConnected:
            return None
        if self.__mountpoint is None:
            return None
        return self.__FS
