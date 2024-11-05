import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta


def crear_conexion():
    """Crea una conexión a la base de datos MySQL."""
    try:
        conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='Gimnasio',
            port='3306'
        )
        if conexion.is_connected():
            print("Conexión exitosa a la base de datos.")
            return conexion
    except Error as e:
        print(f"Error al conectarse a la base de datos: {e}")
        return None


def agregar_cliente(conexion):
    """Agrega un nuevo cliente a la base de datos y solicita el pago del mes."""
    nombre = input("Ingrese el nombre del cliente: ")
    apellidos = input("Ingrese el apellido del cliente: ")
    dni = input("Ingrese el DNI del cliente: ")
    edad = int(input("Ingrese la edad del cliente: "))
    direccion = input("Ingrese la dirección del cliente: ")
    telefono = input("Ingrese el teléfono del cliente: ")

    cursor = conexion.cursor()
    try:
        # Verificar que el DNI del cliente no esté en la base de datos
        consulta = "SELECT * FROM Clientes WHERE dni = %s"
        cursor.execute(consulta, (dni,))
        resultado = cursor.fetchone()

        if resultado:
            print("Error: El cliente ya está dado de alta.")
        else:
            consulta = "INSERT INTO Clientes (nombre, apellidos, dni, edad, direccion, telefono) VALUES (%s, %s, %s, %s, %s, %s)"
            valores = (nombre, apellidos, dni, edad, direccion, telefono)
            cursor.execute(consulta, valores)
            conexion.commit()
            print("Cliente agregado con éxito.")

            # Solicitar el pago del mes inmediatamente después de agregar al cliente
            print("\nAhora, vamos a proceder con el pago del mes.")
            agregar_pago(conexion, dni)
    except Error as e:
        print(f"Error al agregar el cliente: {e}")
    finally:
        cursor.close()


def agregar_aparato(conexion):
    """Agrega un nuevo aparato a la base de datos."""
    tipo = input("Ingrese el tipo de aparato (Cardio/Pesas): ")
    marca = input("Ingrese la marca: ")
    modelo = input("Ingrese el modelo: ")

    cursor = conexion.cursor()
    consulta = "INSERT INTO Aparatos (tipo, marca, modelo) VALUES (%s, %s, %s)"
    valores = (tipo, marca, modelo)
    cursor.execute(consulta, valores)
    conexion.commit()
    print("Aparato agregado con éxito.")


def cliente_tiene_pago(conexion, cliente_id):
    """Verifica si el cliente ha realizado algún pago."""
    cursor = conexion.cursor()
    consulta = "SELECT * FROM Pagos WHERE cliente_id = %s"
    cursor.execute(consulta, (cliente_id,))
    resultado = cursor.fetchone()
    return resultado is not None


def obtener_cliente_id(conexion, dni):
    """Obtiene el ID del cliente a partir del DNI."""
    cursor = conexion.cursor()
    consulta = "SELECT id FROM Clientes WHERE dni = %s"
    cursor.execute(consulta, (dni,))
    resultado = cursor.fetchone()
    return resultado[0] if resultado else None


def agregar_pago(conexion, dni=None):
    """Agrega un nuevo pago a la base de datos."""
    if dni is None:
        dni = input("Ingrese el DNI del cliente: ")

    cliente_id = obtener_cliente_id(conexion, dni)

    if cliente_id is None:
        print("Error: El cliente con el DNI proporcionado no existe.")
        return

    mes_actual = datetime.now().strftime("%B %Y").upper()
    mes = input(f"Ingrese el mes (ejemplo: {mes_actual}): ") or mes_actual
    fecha_pago = datetime.now().strftime("%Y-%m-%d")

    cursor = conexion.cursor()
    try:
        consulta = "INSERT INTO Pagos (cliente_id, mes_pago, fecha_pago) VALUES (%s, %s, %s)"
        valores = (cliente_id, mes, fecha_pago)
        cursor.execute(consulta, valores)
        conexion.commit()
        print("Pago agregado con éxito.")
    except Error as e:
        print(f"Error al agregar el pago: {e}")
    finally:
        cursor.close()


from datetime import datetime, timedelta

from datetime import datetime, timedelta

def agregar_reserva(conexion):
    """Agrega una nueva reserva a la base de datos usando el DNI del cliente."""
    cursor = None
    try:
        dni = input("Ingrese el DNI del cliente: ")
        aparato_id = int(input("Ingrese el ID del aparato: "))
        hora_inicio = input("Ingrese la hora de inicio (YYYY-MM-DD HH:MM:SS): ")
        hora_inicio_dt = datetime.strptime(hora_inicio, "%Y-%m-%d %H:%M:%S")
        hora_fin_dt = hora_inicio_dt + timedelta(minutes=30)
        hora_fin = hora_fin_dt.strftime("%Y-%m-%d %H:%M:%S")

        print(f"Hora de fin: {hora_fin}")

        cursor = conexion.cursor()
        consulta = """
            SELECT * FROM Reservas 
            WHERE aparato_id = %s AND 
            ((hora_inicio <= %s AND hora_fin > %s) OR 
            (hora_inicio < %s AND hora_fin >= %s))
        """
        cursor.execute(consulta, (aparato_id, hora_fin, hora_inicio, hora_inicio, hora_fin))
        reservas_existentes = cursor.fetchall()

        if reservas_existentes:
            print("Esta máquina está reservada en esta hora, prueba otra hora.")
            ver_reservas_aparato(conexion)
            return

        consulta = "INSERT INTO Reservas (cliente_dni, aparato_id, hora_inicio, hora_fin) VALUES (%s, %s, %s, %s)"
        valores = (dni, aparato_id, hora_inicio, hora_fin)
        cursor.execute(consulta, valores)

        conexion.commit()

        print("Reserva agregada con éxito.")
        print(f"Hora de inicio: {hora_inicio}, Hora de fin: {hora_fin}")

    except mysql.connector.Error as err:
        print(f"Error de base de datos: {err}")
        if conexion.is_connected():
            conexion.rollback()  # Deshacer cambios en caso de error
    except ValueError as ve:
        print(f"Error de valor: {ve}")
    except Exception as e:
        print(f"Error inesperado: {e}")
    finally:
        # Paso 9: Cerrar el cursor
        if cursor:
            cursor.close()


def ver_pagos_cliente(conexion):
    """Muestra los meses que ha pagado un cliente a partir de su DNI."""
    dni = input("Ingrese el DNI del cliente: ")
    cliente_id = obtener_cliente_id(conexion, dni)

    if cliente_id is None:
        print("Error: El cliente con el DNI proporcionado no existe.")
        return

    cursor = conexion.cursor()
    consulta = "SELECT mes_pago, fecha_pago FROM Pagos WHERE cliente_id = %s"
    cursor.execute(consulta, (cliente_id,))
    resultados = cursor.fetchall()

    if resultados:
        print(f"Meses pagados por el cliente con DNI {dni}:")
        for mes_pago, fecha_pago in resultados:
            print(f"Mes: {mes_pago}, Fecha de Pago: {fecha_pago}")
    else:
        print("El cliente no tiene pagos registrados.")


def ver_clientes(conexion):
    """Muestra todos los clientes en la base de datos."""
    cursor = conexion.cursor()
    consulta = "SELECT * FROM Clientes"
    cursor.execute(consulta)
    resultados = cursor.fetchall()

    if resultados:
        print("Clientes en la base de datos:")
        for cliente in resultados:
            print(
                f"ID: {cliente[0]}, Nombre: {cliente[1]}, Apellidos: {cliente[2]}, DNI: {cliente[3]}, Edad: {cliente[4]}, Dirección: {cliente[5]}, Teléfono: {cliente[6]}")
    else:
        print("No hay clientes registrados.")


def ver_aparatos(conexion):
    """Muestra todos los aparatos en la base de datos."""
    cursor = conexion.cursor()
    consulta = "SELECT * FROM Aparatos"
    cursor.execute(consulta)
    resultados = cursor.fetchall()

    if resultados:
        print("Aparatos en la base de datos:")
        for aparato in resultados:
            print(f"ID: {aparato[0]}, Tipo: {aparato[1]}, Marca: {aparato[2]}, Modelo: {aparato[3]}")
    else:
        print("No hay aparatos registrados.")


def ver_reservas_aparato(conexion):
    """Muestra las reservas de un aparato a partir de su ID."""
    aparato_id = int(input("Ingrese el ID del aparato: "))
    cursor = conexion.cursor()
    consulta = """
    SELECT r.hora_inicio, r.hora_fin, c.nombre, c.apellidos 
    FROM Reservas r 
    JOIN Clientes c ON r.cliente_dni = c.dni 
    WHERE r.aparato_id = %s
    """
    cursor.execute(consulta, (aparato_id,))
    resultados = cursor.fetchall()

    if resultados:
        print(f"Reservas para el aparato ID {aparato_id}:")
        for hora_inicio, hora_fin, nombre, apellidos in resultados:
            print(f"Cliente: {nombre} {apellidos}, Hora Inicio: {hora_inicio}, Hora Fin: {hora_fin}")
    else:
        print("No hay reservas para el aparato especificado.")


def main():
    conexion = crear_conexion()
    if conexion:
        while True:
            print("\nSeleccione una opción:")
            print("1. Agregar cliente")
            print("2. Agregar aparato")
            print("3. Agregar reserva")
            print("4. Agregar pago")
            print("5. Ver pagos del cliente")
            print("6. Ver clientes")
            print("7. Ver aparatos")
            print("8. Ver reservas de un aparato")
            print("9. Salir")
            opcion = input("Ingrese su opción: ")

            if opcion == '1':
                agregar_cliente(conexion)
            elif opcion == '2':
                agregar_aparato(conexion)
            elif opcion == '3':
                agregar_reserva(conexion)
            elif opcion == '4':
                agregar_pago(conexion)
            elif opcion == '5':
                ver_pagos_cliente(conexion)
            elif opcion == '6':
                ver_clientes(conexion)
            elif opcion == '7':
                ver_aparatos(conexion)
            elif opcion == '8':
                ver_reservas_aparato(conexion)
            elif opcion == '9':
                break
            else:
                print("Opción no válida. Intente de nuevo.")

        conexion.close()


if __name__ == "__main__":
    main()
