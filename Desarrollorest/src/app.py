from flask import Flask, render_template, jsonify, request
from flask import Flask, redirect, url_for
from config import config
from flask_mysqldb import MySQL
from flask_cors import CORS
import os
import database as db

app=Flask(__name__)
conexion = MySQL(app)
app.debug = True

template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))

# Aquí está la corrección: se elimina el espacio adicional antes de "templates"
template_dir = os.path.join(template_dir, 'templates')

app = Flask(__name__, template_folder='templates', static_url_path='/static')



# Rutas de la aplicación
@app.route('/')
def index():
    return render_template('index.html')

#Ruta para insertar nominas

@app.route('/nomina', methods=['POST'])
def addNomina():
    horas_trabajadas = request.form['horas_trabajadas']
    horas_extras = request.form['horas_extras']
    horas_nocturnas = request.form['horas_nocturnas']
    horas_dominicales = request.form['horas_dominicales']
    comisiones = request.form['comisiones']
    deducciones = request.form['deducciones']
    fecha_emision = request.form['fecha_emision']
    salarioinicial = request.form['salarioinicial']

    if horas_trabajadas and horas_extras and horas_nocturnas and horas_dominicales and comisiones and deducciones and fecha_emision and salarioinicial :
        cursor = db.database.cursor()
        sql = "INSERT INTO nomina(horas_trabajadas, horas_extras, horas_nocturnas, horas_dominicales, comisiones, deducciones, fecha_emision, salarioinicial) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

        data = (horas_trabajadas, horas_extras, horas_nocturnas, horas_dominicales, comisiones, deducciones, fecha_emision, salarioinicial)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('index'))

CORS(app)

@app.route('/nominas', methods=['GET'])
def listar_nominas():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM nominas"
        cursor.execute(sql)
        datos = cursor.fetchall()
        nominas = []
        for fila in datos:
            nomina = {
                'id': fila[0],
                'id_empleado': fila[1],
                'nombre': fila[2],
                'salario_base': fila[3],
                'horas_trabajadas': fila[4],
                'horas_extras': fila[5],
                'horas_nocturnas': fila[6],
                'horas_dominicales': fila[7],
                'comisiones': fila[8],
                'deducciones': fila[9],
                'salario_bruto': fila[10],
                'salario_neto': fila[11],
                'fecha_emision': fila[12],
                }
            nominas.append(nomina)
        return jsonify({'nominas': nominas, 'mensaje': "Nominas"})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': "Error"})


@app.route('/empleados', methods=['GET'])
def listar_empleados():
    try:
        cursor = conexion.connection.cursor()
        sql = "SELECT * FROM empleados"
        cursor.execute(sql)
        datos = cursor.fetchall()
        empleados = []
        for fila in datos:
            empleado = {
                'id': fila[0],
                'documento': fila[1],
                'nombre': fila[2],
                'sexo': fila[3],
                'telefono': fila[4],
                'fechaingreso': fila[5],
                'fechanacimiento': fila[6],
                'cargo': fila[7],
                'salarioinicial': fila[8],
                }
            empleados.append(empleado)
        return jsonify({'empleados': empleados, 'mensaje': "Empleados"})
    except Exception as ex:
        print(ex)
        return jsonify({'mensaje': "Error"})

@app.route('/empleados/<id>', methods=['GET'])
def leer_empleados(id):
    try:
        cursor=conexion.connection.cursor()
        sql="SELECT * FROM empleados WHERE id = '{0}'".format(id)
        cursor.execute(sql)
        datos = cursor.fetchone()
        if datos != None:
            cursor={'id':datos[0], 'documento':datos[1], 'nombre':datos[2],
            'sexo':datos[3], 'telefono':datos[4],'fechaingreso':datos[5],'fechanacimiento':datos[6],'cargo':datos[7],'salarioinicial':datos[8]}
            return jsonify({'mensaje':"Empleado Encontrado."})
        else:
            return jsonify({'Mensaje': "Empleado no encontrado."})
    except Exception as ex:
        return jsonify({'Mensaje': "Error."})

@app.route('/empleados',methods=['POST'])
def registrar_empleados():
#print(request.json)
    try:
        cursor=conexion.connection.cursor()
        sql = """INSERT INTO empleados (id, documento, nombre, sexo, telefono, fechaingreso, fechanacimiento, cargo, salarioinicial)
        VALUES ('{0}', '{1}', '{2}', '{3}', '{4}','{5}','{6}','{7}','{8}'
        )""".format(request.json['id'],request.json['documento'],request.json['nombre'],
        request.json['sexo'], request.json['telefono'], request.json['fechaingreso'], request.json['fechanacimiento'],
        request.json['cargo'], request.json['salarioinicial'])
        cursor.execute(sql)
        conexion.connection.commit()
        print("Registro exitoso")
        return jsonify({'Mensaje': "Empleadoo registrado."})
    except Exception as ex:
        print(ex)
        return jsonify({'Mensaje': "Error."})

@app.route('/empleados/<id>',methods=['DELETE'])
def eliminar_empleados(id):
    try:
        cursor=conexion.connection.cursor()
        sql = "DELETE FROM empleados WHERE id = '{0}'".format(id)
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify({'Mensaje': "Empleado Eliminado."})
    except Exception as ex:
        return jsonify({'Mensaje': "Error."})
    
@app.route('/empleados/<int:id>', methods=['PUT'])
def actualizar_empleados(id):
    try:
        cursor = conexion.connection.cursor()
        sql = """
        UPDATE empleados
        SET documento = %s, nombre = %s, sexo = %s, telefono = %s, fechaingreso = %s,
        fechanacimiento = %s, cargo = %s, salarioinicial = %s
        WHERE id = %s
        """
        cursor.execute(
            sql,
            (
                request.json['documento'],
                request.json['nombre'],
                request.json['sexo'],
                request.json['telefono'],
                request.json['fechaingreso'],
                request.json['fechanacimiento'],
                request.json['cargo'],
                request.json['salarioinicial'],
                id
            )
        )
        conexion.connection.commit()
        return jsonify({'Mensaje': "Empleado Actualizado."})
    except Exception as ex:
        return jsonify({'Mensaje': "Error."})
#Seleccionar nomina si funciona
@app.route('/nominas/<id>', methods=['GET'])
def leer_nominas(id):
    try:
        cursor=conexion.connection.cursor()
        sql="SELECT * FROM nominas WHERE id = '{0}'".format(id)
        cursor.execute(sql)
        datos = cursor.fetchone()
        if datos != None:
            cursor={'id':datos[0], 'id_empleado':datos[1], 'nombre':datos[2],
            'salario_base':datos[3], 'horas_trabajadas':datos[4], 'horas_extras':datos[5],'horas_nocturnas':datos[6],'horas_dominicales':datos[7],
            'comisiones':datos[8],'deducciones':datos[9],
            'salario_bruto':datos[10], 'salario_neto':datos[11], 'fecha_emision':datos[12]}
            return jsonify({'mensaje':"Nomina Encontrada."})
        else:
            return jsonify({'Mensaje': "Nomina no encontrada."})
    except Exception as ex:
        return jsonify({'Mensaje': "Error."})

#Lo unico que se agrego, si funciona
@app.route('/nominas', methods=['POST'])
def registrar_nominas():
    try:
        cursor = conexion.connection.cursor()

        # Obtén los datos proporcionados por el usuario
        id_empleado = request.json['id_empleado']
        nombre = request.json['nombre']
        salario_base = request.json['salario_base']
        horas_trabajadas = request.json['horas_trabajadas']
        horas_extras = request.json['horas_extras']
        horas_nocturnas = request.json['horas_nocturnas']
        horas_dominicales = request.json['horas_dominicales']
        comisiones = request.json['comisiones']
        deducciones = request.json['deducciones']
        fecha_emision = request.json['fecha_emision']

        # Calcula el bono por horas nocturnas y dominicales
        bono_nocturno = int(horas_nocturnas) * 10
        bono_dominical = int(horas_dominicales) * 10

        # Realiza los cálculos para la generación de la nómina
        salario_bruto = (
            float(salario_base) +
            float(comisiones) +
            float(horas_extras) * 5 +  # Ejemplo: $5 por cada hora extra
            bono_nocturno +
            bono_dominical
        )

        salario_neto = salario_bruto - float(deducciones)

        # Inserta la nómina en la base de datos
        sql_nominas = """
            INSERT INTO nominas (
                id_empleado, nombre, salario_base, horas_trabajadas, horas_extras, horas_nocturnas,
                horas_dominicales, comisiones, deducciones, salario_bruto, salario_neto, fecha_emision
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql_nominas, (
            id_empleado, nombre, salario_base, horas_trabajadas, horas_extras, horas_nocturnas,
            horas_dominicales, comisiones, deducciones, salario_bruto, salario_neto, fecha_emision
        ))
        conexion.connection.commit()

        return jsonify({
            'Mensaje': f'Nómina generada para {nombre}.',
            'Nomina': {
                'id_empleado': id_empleado,
                'nombre': nombre,
                'salario_base': salario_base,
                'horas_trabajadas': horas_trabajadas,
                'horas_extras': horas_extras,
                'horas_nocturnas': horas_nocturnas,
                'horas_dominicales': horas_dominicales,
                'comisiones': comisiones,
                'deducciones': deducciones,
                'salario_bruto': salario_bruto,
                'salario_neto': salario_neto,
                'fecha_emision': fecha_emision,
            },
        })

    except Exception as ex:
        print(ex)
        return jsonify({'Mensaje': 'Error al generar la nómina.'})


#Eliminar nomina si funciona
@app.route('/empleados/<id>',methods=['DELETE'])
def eliminar_nominas(id):
    try:
        cursor=conexion.connection.cursor()
        sql = "DELETE FROM nominas WHERE id = '{0}'".format(id)
        cursor.execute(sql)
        conexion.connection.commit()
        return jsonify({'Mensaje': "Nómina Eliminada."})
    except Exception as ex:
        return jsonify({'Mensaje': "Error."})
#/Actualizar nomina no se ha probado, no se ha cambiado   
@app.route('/nominas/<int:id>', methods=['PUT'])
def actualizar_nominas(id):
    try:
        cursor = conexion.connection.cursor()
        sql = """
        UPDATE nominas
        SET nombre = %s, salario_base = %s, horas_trabajadas = %s, horas_extras = %s, horas_nocturnas = %s,
        horas_dominicales = %s, comisiones = %s, deducciones = %s, salario_bruto = %s, salario_neto = %s, fecha_emision = %s
        WHERE id = %s
        """
        cursor.execute(
            sql,
            (
                request.json['nombre'],
                request.json['salario_base'],
                request.json['horas_trabajadas'],
                request.json['horas_extras'],
                request.json['horas_nocturnas'],
                request.json['horas_dominicales'],
                request.json['comisiones'],
                request.json['deducciones'],
                request.json['salario_neto'],
                request.json['salario_bruto'],
                request.json['fecha_emision'],
                id
            )
        )
        conexion.connection.commit()
        return jsonify({'Mensaje': "Nómina Actualizada."})
    except Exception as ex:
        return jsonify({'Mensaje': "Error."})


def pagina_no_encontrada(error):
    return "<h1>Página no encontrada </h1>", 404

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run()
