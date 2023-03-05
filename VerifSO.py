def VerifSo()
    import platform
    import psutil
    import socket
    import winreg
    import subprocess


    # Abrir archivo para escritura

    def get_windows_edition():
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion") #Busca la key en el registro
            value, _ = winreg.QueryValueEx(key, "EditionID") #Declara la key para la variable
            winreg.CloseKey(key)
            return value
        except WindowsError:
            return "Desconocido"

    windows_edition = get_windows_edition()
    with open("info.txt", "w") as f: #En dónde se guarda la info obtenida
        #De acá se obtiene la info del micro que es lo más pesado
        output = subprocess.check_output("wmic cpu get name, NumberOfCores, NumberOfLogicalProcessors, MaxClockSpeed",shell=True).decode().strip().split('\n')
        cpu_info = [x for x in output if "Intel" in x or "AMD" in x][0].split()
        cpu_name = " ".join(cpu_info[2:])

        # Obtener el nombre del equipo
        hostname = socket.gethostname()
        # Obtener la dirección IP del equipo
        ip_address = socket.gethostbyname(hostname)
        # Obtener la versión de Windows
        windows_version = platform.win32_ver()[0]
        # Imprimir la información obtenida
        edicion=windows_version[1]
        print(f"Nombre del equipo: {hostname}", file=f)
        print(f"Dirección IP: {ip_address}", file=f)
        print(f"Versión de Windows: {windows_version} {windows_edition}", file=f)
        print(f"El procesador es : {cpu_name}", file=f)

        # Obtener información sobre la memoria RAM
        mem = psutil.virtual_memory()
        print(f"RAM total: {mem.total / 2 ** 30:.2f} GB", file=f)
        # Obtener información sobre los discos
        partitions = psutil.disk_partitions()
        for partition in partitions:
            print(f"Disco: {partition.device}", file=f)
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
            except PermissionError:
                # Si no se tiene permiso para acceder al disco, se salta este disco
                continue
            print(f"Tamaño total del disco: {partition_usage.total / 2 ** 30:.2f} GB", file=f)
            print(f"Espacio libre en el disco: {partition_usage.free / 2 ** 30:.2f} GB", file=f)

    # Imprimir mensaje de confirmación
    print("Información guardada en el archivo info.txt")