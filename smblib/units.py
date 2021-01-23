# -*- coding: utf-8 -*-
# ·
"""
===========================================================
                          Unidades
===========================================================
Autor: Simón Martínez <simon@cicoss.net>
Fecha: dom nov  1 18:53:33 CET 2020
-----------------------------------------------------------

Clase Unidades para el mantenimiento de la colección
de unidades configuradas

"""

from pathlib import Path

from smblib.settings import Settings
from smblib.unit import Unit


class Units(object):
    """
     Unidades de backup

    Representa la colección de unidades

    """
    def __init__(self):
        """
        __init__ Constructor

        Obtiene la colección de Unidades

        """
        super().__init__()

        # Obtiene los datos de configuración
        self.__Config = Settings()

        # el punto de montaje por defecto
        self._DefaultMountPoint = self.__Config.units_mount

        self.__Lista = []  # Lista de unidades

        # lee el directorio de ficheros de configuración de unidades
        self.__dirconfunits = Path(self.__Config.units_conf)
        _filesunit = self.__dirconfunits.glob("*.json")
        for fichero in _filesunit:
            self.__Lista.append(
                Unit(fichero.stem, self.__dirconfunits,
                     self.__Config.units_mount))

    def __del__(self):
        """
        __del__ Destructor

        Slava las unidades que se hubieran modificado
        """
        for unit in self.Lista:
            unit.save()

    def get_list_names(self):
        """Obtiene los nombres de la colección de unidades

        Returns:
            list: nombres
        """
        names = []
        for uni in self._Lista:
            names.append(uni.Name)
        return names

    def get_default(self):
        """Devuelve la unidad por defecto

        Returns:
            Unidad: objeto Unidad
        """
        return self._DefaultUnit

    def unit_exists(self, name):  # OK
        """Comprueba si existe una unidad con nombre argumento

        Args:
            name (string): nombre de la unidad

        Returns:
            bool: True si existe, False si no
        """
        for uni in self._Lista:
            if uni.Name == name:
                return True
        return False

    def get_unit(self, name):  # OK
        """Obtiene el objeto de clase Unidad con nombre argumento

        Args:
            name (string): nombre de unidad

        Returns:
            Unidad: Objeto Unidad si existe, si no None
        """
        for uni in self._Lista:
            if uni.Name == name:
                return uni
        return None

    def add_unit(self, data):  # TODO
        """Añade una nueva unidad

        Args:
            data (object UnitData): Datos de la clase unidad

        Raises:
            NameError: Temporalmente sin implementar
        """
        if data.finised:
            _newUnit = Unit(data, self.__Config.DirUnits)
            _newUnit.save()
            return True
        return False

    def del_unit(self, name):  # OK
        """Borra la configuración de una unidad

        Args:
            name (string): nombre de la unidad

        Returns:
            bool: True sin errores, False si no
        """
        if not self.unit_exists(name):
            return False

        unitToDel = self.get_unit(name)
        fileConfUnit = unitToDel.PathFile
        if os.path.exists(fileConfUnit):
            os.remove(fileConfUnit)
        else:
            return False
        for indice in range(0, len(self._Lista)):
            if self._Lista[indice].Name == name:
                del (self._Lista[indice])
                return True
        return False

    @property
    def Lista(self):  # OK
        """Devuelve la colección de objetos Unidad

        Returns:
            list: [unidad,unidad,...]
        """
        return self._Lista
