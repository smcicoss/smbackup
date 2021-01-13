# -*- coding: utf-8 -*-
# ·
"""
=====================================================================
                            settings.py
=====================================================================
    Autor: Simón Martínez <simon@cicoss.net>
    Fecha: domingo, 10 de enero de 2021
---------------------------------------------------------------------

    definición de la clase Settings

"""

from pathlib import Path
from smblib.configdata import ConfigData


class Settings(ConfigData):

    __version = "4.0"
    ConfigDir = Path(f"/etc/smbackup-{__version}")
    ConfigFile = ConfigDir / "smbconfig.json"

    def __init__(self):
        self.__DirThisFile = Path(__file__).parent
        self.__CurrentDir = Path.cwd()

        super().__init__(self.ConfigFile)

    def __del__(self):
        super().save(self.file_conf)

    @property
    def DefaultMountPoint(self):
        return self.units_mount

    @DefaultMountPoint.setter
    def DefaultMountPoint(self, value):
        path = Path(value).resolve()
        if path.parents[0] != "/":
            path = Path("/mnt") / path

        path.mkdir(parents=True, exist_ok=True)
        self.units_mount = path
