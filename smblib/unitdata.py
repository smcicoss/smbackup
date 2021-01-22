# -*- coding: utf-8 -*-
# ·
#

import re
import pathlib as Path
from utiles.strutil import clean_str


class UnitData(object):
    def __init__(self, data=None):
        super().__init__()
        if data is None or (not isinstance(data, dict)
                            and not isinstance(data, UnitData)):
            for field in self.keys():
                self[field] = None

            self.__modified = False
        else:
            for field in self.keys():
                self[field] = data[field]

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
        # TODO
        return "En construción UnidData.__str__"

    @property
    def keys(self):
        return [
            'Name', 'Description', 'Label', 'Uuid', 'UuidP', 'Crypt',
            'DirBackups', 'Meta'
        ]

    @property
    def Name(self):
        """
        Name

        Nombre de la unidad

        Returns:
            str: Nombre
        """
        return self.__name

    @Name.setter
    def Name(self, value):
        self.__name = clean_str(value)
        self.__modified = True

    @property
    def Description(self):
        return self.__description

    @Description.setter
    def Description(self, value):
        self.__description = value
        self.__modified = True

    @property
    def Label(self):
        return self.__label

    @Label.setter
    def Label(self, value):
        if len(value) > 16:
            value = value[0:15]
        label_regexp = re.compile(r"^([A-Z])\w+$", re.VERBOSE)
        if label_regexp.match(value) is not None:
            self.__label = value
            self.__modified = True

    @property
    def Uuid(self):
        try:
            return self.__uuid
        except AttributeError:
            return None

    @Uuid.setter
    def Uuid(self, value):
        value = value.lower()
        uuid_regexp = re.compile(r"^[a-f0-9]{8}-[a-f0-9]{4}-4[a-f0-9]{3}-" +
                                 r"[89aAbB][a-f0-9]{3}-[a-f0-9]{12}$")
        if uuid_regexp.match(value) is not None:
            self.__uuid = value
            self.__modified = True

    @property
    def UuidP(self):
        return self.__uuidp

    @UuidP.setter
    def UuidP(self, value):
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
    def Crypt(self):
        """
        Crypt

        Determina si el sistema de ficheros está cifrado o no

        Returns:
            bool: True si cifrado
        """
        return self.__crypt

    @Crypt.setter
    def Crypt(self, value):
        if not isinstance(value, bool):
            return
        self.__crypt = value
        self.__modified = True

    @property
    def DirBackups(self):
        return self.__dir_backups

    @DirBackups.setter
    def DirBackups(self, value):
        """
        DirBackups Directorio de backups

        Directorio relativo al punto de montado de la unidad
        donde se almacenarán las copias

        Args:
            value (str): path relativo
        """
        value = clean_str(value)
        if path.isabs(value):
            value = value[1:]
        self.__dir_backups = path.normpath(path.normcase(value))
        self.__modified = True

    @property
    def Meta(self):
        return self.__meta

    @Meta.setter
    def Meta(self, value):
        """
        Meta Directorio

        Directorio relativo al punto de montado de la unidad
        donde se guardaran las configuraciones de las copias

        Args:
            value (str): path relativo
        """
        value = clean_str(value)
        if path.isabs(value):
            value = value[1:]
        self.__meta = path.normpath(path.normcase(value))
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
