# -*- coding: utf-8 -*-
# ·
"""
===============================================================================
                              editunits.py
===============================================================================
    Autor: Simón Martínez <simon@cicoss.net>
    Fecha: jue nov 19 14:59:09 CET 2020
-------------------------------------------------------------------------------

Crea, edita o borra unidades de copia

"""

from lib.editcopies import EditCopies
import os
import shutil
import textwrap

from mod.blkdevices import BlockDevices
from lib.units import Units
from lib.unitdata import UnitData
from utiles.strutil import Color, text_paragraph
from utiles.strutil import clean_str, clear, h1, h2
from utiles.menu import Menu

color = Color()


class EditUnits():
    """
    EditUnits Edita unidades

    Crea, modifica o borra unidades
    """
    def __init__(self, HostConfig):
        """Bucle de menú para la realización del Mantenimiento

        Raises:
            NameError: Si el menú devuelve una opción inesperada
        """

        clear()

        self.__hConfig = HostConfig
        self.__myUnits = Units()
        self.__myDevs = BlockDevices()

        opciones = [  # opciones menú
            {
                'item': "Nueva",
                'desc': "Añadir un nueva unidad"
            }, {
                'item': "Editar",
                'desc': "Editar los datos de una unidad existente"
            }, {
                'item': "Borrar",
                'desc': "Eliminar una unidad existente"
            }, {
                'item': "Listar",
                'desc': "Listar las unidades configuradas"
            }, {
                'item': "Copias",
                'desc': "Configura copias en unidad"
            }
        ]

        while True:
            clear()
            self.__update()
            print(h1("Configuración de unidades"))

            _names = self.__myUnits.get_list_names()
            listaHorizontal = ', '.join(_names)
            if listaHorizontal != '':
                listaHorizontal = text_paragraph(listaHorizontal, 60, '',
                                                 ' ' * 21)

                listaUnidades = "Unidades existentes: "
                listaUnidades += f"{color.MARRON}" + \
                                 f"{listaHorizontal}" + \
                                 f"{color.END}\n\n"
            else:
                listaUnidades = f"{color.MARRON}" + \
                                "Sin unidades configuradas." + \
                                f"{color.END}"

            print(h2(listaUnidades))

            elige = Menu(opciones)

            if elige.option is None:
                return

            _item = elige.option
            if _item == 0:
                # Crea
                self.__new_unit()

            elif _item == 1:
                # Edita
                self.__edit_unit()

            elif _item == 2:
                # Borra
                self.__del_unit()

            elif _item == 3:
                self.__lista()

            elif _item == 4:
                unit = self.__choose_unit()
                if unit is None:
                    continue
                EditCopies(unit)

            else:
                raise NameError("Error interno: Opción de menú desconocida")

    def __new_unit(self):
        """función interna para crear una nueva unidad
        """
        clear()
        print(h2('Añadir Nueva Unidad'))

        # Mostramos ayuda
        _strhelp = """
            Al crear una nueva unidad es necesario
            conectar la unidad antes de comenzar el proceso a fin
            de poder identificarla adecuadamente. Lo mas conveniente,
            aunque no necesario es que la unidad este vacía y lista
            para su funcionamiento.
            No es necesario montar la unidad.
        """

        _strhelp = text_paragraph(_strhelp, 60, ' ' * 10)

        print(f"{color.MARRON}{_strhelp}{color.END}\n")

        _resp = input("¿Desea analizar solo unidades USB? (S/n): ")
        if _resp == '':
            _unitsUSB = True
        elif _resp.lower() == "s":
            # lista unidades USB
            _unitsUSB = True
        else:
            # lista todas las unidades
            _unitsUSB = False

        print(f"\n{color.DESTACA}", end='')
        print("¿Está ya conectada la unidad?", end='')
        print(f"{color.END}\n")
        print(
            text_paragraph(
                "Tenga en cuenta que el sistema puede" +
                " tardar un tiempo en detectarla", 60))
        input("Pulse [Intro] cuando esté lista.")

        # actualizamos la lectura de dispositivos
        self.__update()

        _devSelected = self.__selectDev(_unitsUSB)

        if _devSelected is None:
            # se ligió salir
            return

        if _devSelected.count_partitions() == 0:
            # Disco sin particionar
            print("La unidad seleccionada no está aún preparada" +
                  "No contiene particiones.")
            input("Pulse intro para salir")
            return

        # elegir partición
        _partSelected = self.__selectPart(_devSelected)

        if _partSelected is None:
            return

        if _partSelected.mountpoint is not None:
            # La partición está montada
            # Presentamos datos
            print(_partSelected)

        elif _partSelected.fstype is None:
            # partición no formateada o cifrada
            _str_result = '''
                La partición no tiene asignado un sistema de archivos.
                Por favor, termine el programa y formatee adecuadamente
                la unidad.
            '''
            _str_result = text_paragraph(_str_result, 60, ' ' * 5)
            print(_str_result)
            input("Pulse intro para cancelar")
            return

        elif _partSelected.fstype == 'crypto_LUKS':
            # TODO: partición cifrada
            input(f"\n\t{color.MARRON}En construcción: " +
                  f"Unidades cifradas{color.END}\n\n")
            clear()
            return

        else:
            # Partición lista pero sin montar
            print("La partición no está montada, procedo a montar")
            # Se monta en el directorio Configurado + label
            _mountpoint = os.path.join(self.__hConfig.DefaultMountPoint,
                                       _partSelected.label)

            if _partSelected.mount(_mountpoint):
                # actualizamos
                self.__update()
                _devSelected = self.__myDevs.find_disk_kname(
                    _devSelected.kname)
                _partSelected = _devSelected.find_part_with_uuid(
                    _partSelected.uuid)

                # presento datos
                print(_partSelected)

        # Confirmar
        _resp = input("¿Quiere utilizar este dispositivo" +
                      " para la nueva unidad?\n(Sí/No): ")
        if _resp != 'Sí':
            print("Cancelo...")
            return

        print(f"{color.ALERTA}El nombre por defecto para la unidad es " +
              f" {_partSelected.label}{color.END}")
        _resp = input("Introduzca un nuevo nombre\no intro para mantener:\n")
        if _resp == "":
            _nameUnit = _partSelected.label
        else:
            # limpio el nombre
            _nameUnit = clean_str(_resp)

        # compruebo si ya existe
        if self.__myUnits.unit_exists(_nameUnit):
            print("Ya existe una unidad con ese nombre")
            input("Pulse intro para cancelar")
            clear()
            return

        # Asigno datos
        data = UnitData()
        data.Name = _nameUnit
        data.Description = input("Introduzca una " +
                                 "descripción para la unidad:\n")
        if _partSelected.label is None:
            data.Label = ''
        else:
            data.Label = _partSelected.label
        data.Uuid = _partSelected.uuid
        if _partSelected.fstype == 'crypto_LUKS':
            # pendiente de uso al implementar unidades cifradas
            data.Crypt = True
        else:
            data.Crypt = False

        data.UuidP = _devSelected.ptuuid

        _str_help = '''
            A continuación se le solicita el directorios bajo el que
            almacenar las copias de seguridad. Este directorio es
            relativo al punto de montado de la unidad. Es un path
            relativo, no lo inicie con barra. P. ej.: 'backups' o
            backups/mis_copias. No incluya espacios ni caracteres
            especiales
        '''
        print(f"{color.MARRON}{text_paragraph(_str_help,60)}{color.END}")

        # limpio el nombre del directorio
        _resp = clean_str(input("Path: "))

        while _resp[0] == '/':
            _resp = _resp[1:]

        data.DirBackups = _resp

        # Creamos el directorio
        _fullpath = os.path.join(_partSelected.mountpoint, data.DirBackups)
        os.makedirs(_fullpath, exist_ok=True)
        if not os.path.exists(_fullpath):
            print(f"{color.ERROR}Error al crear el" +
                  f" directorio de backups{color.END}")
            input("pulse intro para cancelar")
            clear()
            return

        _str_help = '''
            A continuación se le solicita el directorios bajo el que
            almacenar las configuraciones de copias de seguridad.
            Este directorio es relativo al punto de montado de la
            unidad. Es un path relativo, no lo inicie con barra.
            P. ej.: 'backups' o backups/mis_copias.
            No incluya espacios ni caracteres especiales
        '''
        print(f"{color.MARRON}{text_paragraph(_str_help,60)}{color.END}")

        # limpio el nombre del directorio
        _resp = clean_str(input("Path: "))

        while _resp[0] == '/':
            _resp = _resp[1:]

        data.Meta = _resp

        _fullpath = os.path.join(_partSelected.mountpoint, data.Meta)
        os.makedirs(_fullpath, exist_ok=True)
        if not os.path.exists(_fullpath):
            print(f"{color.ERROR}Error al crear el" +
                  f" directorio de configs backups{color.END}")
            input("pulse intro para cancelar")
            clear()
            return

        print(data)

        self.__myUnits.add_unit(data)

    def __edit_name(self, unit):
        print(f"{'-'*60}")
        print("Editar el nombre de la unidad".center(60))
        print(unit.Name.center(60))
        print(f"{'-'*60}")
        strhelp = """El nombre de la unidad determina el nombre del fichero
        de confiuración de la unidad por lo que, al cambiar el nombre, los
        datos se guardarán en el nuevo fichero y el antiguo de borrará. Por
        motivos de seguridad los caracteres especiales serán sustituidos por
        guión bajo '_'"""

        # Elimino dobles espacios
        strhelp = " ".join(strhelp.split())

        strhelp = textwrap.dedent(strhelp).strip()
        strhelp = textwrap.fill(
            strhelp,
            initial_indent=' ' * 10,
            subsequent_indent='',
            width=60,
        )
        print(f"{color.MARRON}{strhelp}{color.END}")
        print(f"{color.DESTACA}", end='')
        print("No necesita tener la unidad montada para esta operación.",
              end='')
        print(f"{color.END}\n")
        old_name = unit.Name
        print("Solo [Intro] no cambia")
        new_name = input("Introduzca el nuevo nombre: ")
        if new_name == "":
            return
        new_name = os.path.basename(clean_str(new_name))
        print(f"\n{color.DESTACA}{old_name} -> {new_name}{color.END}")
        confirma = input("¿Es esto correcto? (s/n): ")
        if confirma.lower() == 's':
            unit.Name = new_name

        print("")
        print(unit)

    def __edit_description(self, unit):
        print(f"{'-'*60}")
        print("Editar la Descripción de la unidad".center(60))
        print(unit.Name.center(60))
        print(f"{'-'*60}")
        strhelp = """Breve descripción de la unidad"""
        print(f"{color.MARRON}{strhelp}{color.END}")
        print(f"{color.DESTACA}", end='')
        print("No necesita tener la unidad montada para esta operación.",
              end='')
        print(f"{color.END}\n")
        print(
            f"Descripción actual: {color.VERDE}{unit.Description}{color.END}")
        print("Solo [Intro] no cambia")
        new_desc = input("Introdzca la nueva descripción:\n\t")
        if new_desc == "":
            return
        unit.Description = new_desc

        print("")
        print(unit)

    def __edit_subdir(self, unit):
        print(f"{'-'*60}")
        print("Editar el path de copias de la unidad".center(60))
        print(unit.Name.center(60))
        print(f"{'-'*60}")
        strhelp = """Aquí ha de especificar la carpeta relativa
        al punto de montado de la unidad sin incluir este punto de montado.
        La barra inicial, si la pone será eliminada.
        """

        # Elimino dobles espacios
        strhelp = " ".join(strhelp.split())

        strhelp = textwrap.dedent(strhelp).strip()
        strhelp = textwrap.fill(
            strhelp,
            initial_indent=' ' * 10,
            subsequent_indent='',
            width=60,
        )
        print(f"{color.MARRON}{strhelp}{color.END}")
        print(f"{color.DESTACA}", end='')
        print("Necesita tener la unidad montada para esta operación.", end='')
        print(f"{color.END}\n")
        while True:
            if unit.is_mounted():
                break
            else:
                print("La unidad no está montada")
                print("Por favor, salte a otra consola y monte la unidad")
                print("Luego desde aquí pulse [Intro] para continuar")
                print("o 'q'+[Intro] para terminar: ", end='')
                r = input()
                if r == 'q':
                    return
        print(f"Carpeta actual:{unit.DirBackups.rjust(45,'.')}")
        new_carpeta = input("Introduzca la nueva carpeta:\n")
        if new_carpeta[0] == '/':
            new_carpeta = new_carpeta[1:]
        new_carpeta = os.path.normpath(new_carpeta)
        check_carpeta = os.path.abspath(
            os.path.join(unit.mount_point(), new_carpeta))
        if os.path.exists(check_carpeta):
            if os.listdir(check_carpeta):
                print("La carpeta indicada existe y no está vacía")
                r = input("¿está seguro de continuar (s/n)?: ")
                if r.lower() != 's':
                    return
        else:
            os.makedirs(check_carpeta, 0o750, True)
        old_carpeta = unit.path_to_copy()
        unit.DirBackups = new_carpeta
        if os.listdir(old_carpeta):
            print(f"La carpeta anterior {old_carpeta} tiene contenido")
            r = input("¿Quiere moverlo a la nueva carpeta?(s/n): ")
            if r.lower() == 's':
                print("\ncopiando ...", end='')
                for entrada in os.listdir(old_carpeta):
                    shutil.move(os.path.join(old_carpeta, entrada),
                                unit.path_to_copy())
                os.rmdir(old_carpeta)
                print("hecho\n\n")

    def __edit_meta(self, unit):

        # Cabecera
        print(f"{'-'*60}")
        print("Editar el path de configuración de copias de la unidad".center(
            60))
        print(unit.Name.center(60))
        print(f"{'-'*60}")
        strhelp = """Aquí ha de especificar la carpeta relativa
        al punto de montado de la unidad sin incluir este punto de montado.
        La barra inicial, si la pone será eliminada.
        """

        # Formatea la ayuda multilínea
        strhelp = " ".join(strhelp.split())
        strhelp = textwrap.dedent(strhelp).strip()
        strhelp = textwrap.fill(
            strhelp,
            initial_indent=' ' * 5,
            subsequent_indent='',
            width=60,
        )
        print(f"{color.MARRON}{strhelp}{color.END}")

        print(f"{color.DESTACA}", end='')
        print("Necesita tener la unidad montada para esta operación.", end='')
        print(f"{color.END}\n")

        # Espera esté montada la unidad
        while True:
            if unit.mountpoint is not None:
                break
            else:
                print("La unidad no está montada")
                print("Por favor, salte a otra consola y monte la unidad")
                print("Luego desde aquí pulse [Intro] para continuar")
                print("o 'q'+[Intro] para terminar: ", end='')
                r = input()
                if r == 'q':
                    return

        print(f"Carpeta actual:{unit.Meta.rjust(45,'.')}")
        new_carpeta = input("Introduzca la nueva carpeta:\n")

        # elimina la escalada a directorios padre
        if new_carpeta[0:1] == "..":
            new_carpeta = new_carpeta[2:]

        # elimina la barra inicial
        if new_carpeta[0] == '/':
            new_carpeta = new_carpeta[1:]

        # normaliza el path
        new_carpeta = os.path.normpath(new_carpeta)

        # Compone la ruta absoluta
        check_carpeta = os.path.abspath(
            os.path.join(unit.path_to_copy(), new_carpeta))

        # comprueba si existe
        if os.path.exists(check_carpeta):
            if os.listdir(check_carpeta):
                print("La carpeta indicada existe y no está vacía")
                r = input("¿está seguro de continuar (s/n)?: ")
                if r.lower() != 's':
                    # Si no contesta s sale sin cambios
                    return
        else:
            # Crea la carpeta
            os.makedirs(check_carpeta, 0o750, True)

        # Salva valor anterior
        old_carpeta = os.path.join(unit.path_to_copy(), unit.Meta)

        # Establece el nuevo valor
        unit.Meta = new_carpeta

        # Comprueba si carpeta anterior tiene contenido
        if os.listdir(old_carpeta):
            print(f"La carpeta anterior {old_carpeta} tiene contenido")
            r = input("¿Quiere moverlo a la nueva carpeta?(s/n): ")
            if r.lower() == 's':
                print("\ncopiando ...", end='')
                # Movemos el contenido a la nueva carpeta
                for entrada in os.listdir(old_carpeta):
                    shutil.move(os.path.join(old_carpeta, entrada),
                                check_carpeta)
                print("hecho\n\n")

        os.rmdir(old_carpeta)

    def __edit_unit(self):
        """función interna para editar una unidad
        """
        clear()
        print(h1('Editar Unidad'))

        unitToEdit = self.__choose_unit()
        if unitToEdit is None:
            return

        print(
            h2(f"Unidad: {color.MARRON}{unitToEdit.Name.rjust(52)}{color.END}")
        )
        print(unitToEdit)

        opciones = [  #
            {
                'item': 'Nombre',
                'value': unitToEdit.Name,
                'desc':
                'El nombre de la unidad (determina el nombre del fichero)'
            }, {
                'item': 'Descripción',
                'value': unitToEdit.Description,
                'desc': "Breve descripción de la unidad"
            }, {
                'item':
                'Subdirectorio',
                'value':
                unitToEdit.DirBackups,
                'desc':
                "Directorio dentro de la unidad donde se alojarán las copias"
            }, {
                'item':
                'Conf. copias',
                'value':
                unitToEdit.Meta,
                'desc':
                "Directorio dentro de la unidad donde se guardarán los datos "
                + "de configuración de las copias"
            }
        ]

        while True:
            editaDato = Menu(opciones)
            if editaDato.option is None:
                break

            if editaDato.option == 0:
                self.__edit_name(unitToEdit)
                # salvo para no perder el fichero
                unitToEdit.save()

            elif editaDato.option == 1:
                self.__edit_description(unitToEdit)

            elif editaDato.option == 2:
                self.__edit_subdir(unitToEdit)
                unitToEdit.save()

            elif editaDato.option == 3:
                self.__edit_meta(unitToEdit)
                unitToEdit.save()

            else:
                raise NameError(
                    "Error Interno: Opción invalida al elegir dato en unidades"
                )
        unitToEdit.save()

    def __del_unit(self):
        """función interna para borrar una unidad
        """
        opciones = []
        for uni in self.__myUnits.Lista:
            opciones.append({'item': uni.Name, 'desc': uni.Description})
        elige = Menu(opciones)
        if elige.option is None:
            return

        nameUnitSelected = self.__myUnits.Lista[elige.option].Name

        print(f"{color.ALERTA}", end='')
        print(f"Ha seleccionado borrar la unidad '{nameUnitSelected}'")
        print("Esto no tiene vuelta atrás")
        print("¿Seguro que quieres continuar?")
        respuesta = input(
            "Teclee Sí para aceptar, cualquier otra cosa para cancelar: ")
        if respuesta == "Sí":
            print(f"\nProcedo al borrado de {nameUnitSelected}{color.END}\n\n")
            self.__myUnits.del_unit(nameUnitSelected)
            self.__update()
            return

        print(f"\nCancelado{color.END}\n\n")

    def __lista(self):
        """Lista los nombres de unidades configuradas y
        las etiquetas de partición
        """
        clear()
        print(h2('Lista de unidades'))
        lista = self.__myUnits.get_list_names()
        labels = []
        for nameUnit in lista:
            labels.append(self.__myUnits.get_unit(nameUnit).Label)
        print("%s %s" % ('Nombre', 'LABEL'.rjust(60 - len('Nombre '))))
        print(f"{'-'*60}{color.MARRON}")
        if len(lista) == 0:
            print("No se han definido Unidades")
        else:
            for indice in range(0, len(lista)):
                print(f"{lista[indice]} ", end='')
                print(f"{labels[indice].rjust(60-(len(lista[indice])+1),'.')}")

        print(f"{color.END}{'-'*60}\n\n")
        input("Pulse [Intro] para continuar")

    def __choose_unit(self):
        """
        __choose_unit Elije Unidad

        Muestra la lista de Uniodades y presenta un menu de selección

        Returns:
            Unit: La unidad seleccionada
        """

        opciones = []
        for unit in self.__myUnits.Lista:
            opciones.append({
                'item': unit.Name,
                'value': unit.Label,
                'desc': unit.Uuid
            })
        elige = Menu(opciones, 'Elija la unidad a editar', True)
        if elige.option is None:
            return None
        else:
            return self.__myUnits.get_unit(opciones[elige.option]['item'])

    def __selectDev(self, USBOnly=True):
        if USBOnly:
            _lista = self.__myDevs.find_usb_disks()
        else:
            _lista = self.__myDevs.ListDisks

        _optMenu = []
        for _dev in _lista:
            _optMenu.append({
                'item':
                f"{_dev.type} {_dev.tran} {_dev.size}",
                'value':
                f"{_dev.model}",
                'desc':
                f"{_dev.path} con {len(_dev.sons)} particiones"
            })

        elige = Menu(_optMenu, f"{len(_lista)} dispositivos conectados", True)

        if elige.option is None:
            return None
        else:
            return _lista[elige.option]

    def __selectPart(self, dev):
        _optMenu = []
        for part in dev.partitions:
            if part.label is None:
                _optMenu.append({
                    'item': f"{part.fstype} de {part.size}",
                    'value': f"{part.path}",
                    "desc": f"UUID: {part.uuid}"
                })
            else:
                _optMenu.append({
                    'item': f"{part.fstype} de {part.size} [{part.label}]",
                    'value': f"{part.path}",
                    'desc': f"UUID: {part.uuid}"
                })

        elige = Menu(_optMenu, f"Particiones en {dev.path}", True)

        if elige.option is None:
            return None
        return dev.partitions[elige.option]

    def __update(self):
        self.__myDevs.update()
        self.__myUnits = Units()
