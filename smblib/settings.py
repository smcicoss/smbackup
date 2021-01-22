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
    def units_conf(self):
        return super().units_conf

    @units_conf.setter
    def units_conf(self, value):
        if value is None:
            self.set_units_conf(value)
            return
        elif isinstance(value, str):
            path = Path(value).expanduser()
        elif isinstance(value, Path):
            path = value.expanduser()
        else:
            raise ValueError

        if path.root != "/":
            path = self.ConfigDir / path

        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)

        self.set_units_conf(path)

    @property
    def units_mount(self):
        return Path(super().units_mount)

    @units_mount.setter
    def units_mount(self, value):
        if value is None:
            self.set_units_mount(value)
            return
        elif isinstance(value, str):
            path = Path(value).expanduser()
        elif isinstance(value, Path):
            path = value.expanduser()
        else:
            raise ValueError

        if path.root != "/":
            path = Path("/mnt") / path

        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)

        self.set_units_mount(path)
