# -*- coding: utf-8 -*-
# ·
#

import re
from utiles.strutil import clean_str, data_line


class UnitData(object):
    def __init__(self, data=None):
        super().__init__()
        if data is None:
            for key in self.keys():
                self[key] = None
            self.__modified = False
        elif isinstance(data, dict) or isinstance(data, UnitData):
            for key in self.keys():
                self[key] = data[key]
            self.__modified = True
        else:
            raise ValueError

    def __getitem__(self, key):
        return self.__getattribute__(key)

    def __setitem__(self, key, value):
        if key in self.keys():
            self.__setattr__(key, value)
        else:
            raise NameError

    def __len__(self):
        lenOfData = 0
        for key in self.keys():
            if self[key] is not None:
                lenOfData += 1

        return lenOfData

    def __str__(self):
        _str = ""
        for key in self.keys():
            _str += data_line({'key': key, 'value': str(self[key])})

        return _str

    def keys(self):
        return [
            "name", "description", "wwn", "uuid", "uuidp", "label", "crypt",
            "dirbackups", "meta"
        ]

    @property
    def name(self):
        """
        Name

        Nombre de la unidad

        Returns:
            str: Nombre
        """
        return self.__name

    @name.setter
    def name(self, value):
        if value is None:
            self.__name = None
        else:
            self.__name = clean_str(value)
        self.__modified = True

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, value):
        self.__description = value
        self.__modified = True

    @property
    def wwn(self):
        return self.__wwn

    @wwn.setter
    def wwn(self, value):
        if value is None:
            self.__wwn = None
            return
        value = value.lower()
        wwn_regexp = re.compile(r"^0x[a-f0-9]{16}$")
        if wwn_regexp.match(value) is not None:
            self.__wwn = value
            self.__modified = True

    @property
    def uuid(self):
        return self.__uuid

    @uuid.setter
    def uuid(self, value):
        if value is None:
            self.__uuid = None
            return
        value = value.lower()
        uuid_regexp = re.compile(r"^[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-" +
                                 r"[89aAbB][a-f0-9]{3}-[a-f0-9]{12}$")
        if uuid_regexp.match(value) is not None:
            self.__uuid = value
            self.__modified = True

    @property
    def uuidp(self):
        return self.__uuidp

    @uuidp.setter
    def uuidp(self, value):
        """
        Uuidp UUID Padre

        UUID de la unidad padre del sistema de ficheros
        mismas caracteristicvas que el Uuid.
        corresponde al UUID accesible antes del montado
        del sistema de ficheros

        Args:
            value (str): UUID
        """
        if value is None or value == '':
            self.__uuidp = ''
            return

        value = value.lower()
        uuidp_regexp = re.compile(r"^[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-" +
                                  r"[89aAbB][a-f0-9]{3}-[a-f0-9]{12}$")
        if uuidp_regexp.match(value) is not None:
            self.__uuidp = value
            self.__modified = True

    @property
    def label(self):
        return self.__label

    @label.setter
    def label(self, value):
        if value is None:
            self.__label = None
            return

        if len(value) > 16:
            value = value[0:15]
        label_regexp = re.compile(r"^([A-Za-z])\w+$", re.VERBOSE)
        if label_regexp.match(value) is not None:
            self.__label = value
            self.__modified = True

    @property
    def crypt(self):
        """
        Crypt

        Determina si el sistema de ficheros está cifrado o no

        Returns:
            bool: True si cifrado
        """
        return self.__crypt

    @crypt.setter
    def crypt(self, value):
        if value is None:
            self.__crypt = None
            return
        if not isinstance(value, bool):
            raise ValueError
        self.__crypt = value
        self.__modified = True

    @property
    def dirbackups(self):
        return self.__dir_backups

    @dirbackups.setter
    def dirbackups(self, value):
        """
        DirBackups Directorio de backups

        Directorio relativo al punto de montado de la unidad
        donde se almacenarán las copias

        Args:
            value (str): path relativo
        """
        if value is None:
            self.__dir_backups = None
            return

        if value[0] == '/':
            value = value[1:]
        value = clean_str(value)

        self.__dir_backups = value
        self.__modified = True

    @property
    def meta(self):
        return self.__meta

    @meta.setter
    def meta(self, value):
        """
        Meta Directorio

        Directorio relativo al punto de montado de la unidad
        donde se guardaran las configuraciones de las copias

        Args:
            value (str): path relativo
        """
        if value is None:
            self.__meta = None
            return
        self.__meta = clean_str(value)
        if value[0] == '/':
            value = value[1:]
        self.__modified = True

    @property
    def modified(self):
        """
        modified

        Informa si ya ha sido establecido algún dato

        Returns:
            bool: True si modificado
            None: Si aún no se ha modificado ningún dato
        """
        return self.__modified

    @property
    def finised(self):
        """
        finised Terminado

        Informa si ya han sido establecidos todos los datos

        Returns:
            bool: True si terminado
        """
        if len(self) == len(self.keys()):
            return True
        return False
