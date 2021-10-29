import functools
from flask import Flask, render_template, blueprints, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from markupsafe import escape
import sqlite3
from db import get_db

main = blueprints.Blueprint('main', __name__)

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'usuario' not in session:
            return redirect(url_for('main.login'))
        return view(**kwargs)
    return wrapped_view


@main.route('/')
def index():

    return render_template("index.html")


@main.route('/misDatos')
@login_required
def misDatos():

    return render_template("misDatos.html")




@main.route('/terminosYcondiciones')
def terminos():

    return render_template("politicasdeprivacidad.html")


@main.route('/recuperar')
def recuperarContraseña():

    return render_template("recuperarcontraseña.html")


@main.route('/reserva')
@login_required
def reserva():

    return render_template("reservas.html")



#Inicio de sesión 
@main.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        usuario = escape(request.form['usuario'])
        contraseña = escape(request.form['password'])

        db = get_db()
        user = db.execute('select * from usuario where usuario = ? ', (usuario,)).fetchone()
        administrador = db.execute('select * from administrador where usuario = ? ', (usuario,)).fetchone()
        superadmin = db.execute('select * from superadministrador where usuario = ? ', (usuario,)).fetchone()
        db.commit()
        db.close()

        #Validaciones de usuario
        if user is not None:
            contraseña = contraseña + usuario
            sw = check_password_hash(user[5], contraseña)

            if(sw):
                session['id'] = user[0]
                session['nombre'] = user[1]
                session['apellido'] = user[2]
                session['usuario'] = user[3]
                session['correo'] = user[4]
                session['password'] = user[5]
                session['telefono'] = user[6]
                session['direccion'] = user[7]
                session['rol'] = user[8]

                return redirect(url_for('main.index'))

            flash('Usuario o clave incorrecta')
        
        #Validaciones administrador
        if administrador is not None:
            contraseña = contraseña + usuario
            sw = check_password_hash(administrador[8], contraseña)

            if(sw):
                session['id'] = administrador[0]
                session['cedula'] = administrador[1]
                session['nombre'] = administrador[2]
                session['apellido'] = administrador[3]
                session['telefono'] = administrador[4]
                session['direccion'] = administrador[5]
                session['usuario'] = administrador[6]
                session['correo'] = administrador[7]
                session['password'] = administrador[8]
                session['rol'] = administrador[9]

                return redirect(url_for('main.index'))

            flash('Usuario o clave incorrecta')

        #validaciones superadministrador
        if superadmin is not None:
            contraseña = contraseña + usuario
            sw = check_password_hash(superadmin[5], contraseña)

            if(sw):

                session['nombre'] = superadmin[1]
                session['apellido'] = superadmin[2]
                session['usuario'] = superadmin[3]
                session['correo'] = superadmin[4]
                session['password'] = superadmin[5]
                session['telefono'] = superadmin[6]
                session['direccion'] = superadmin[7]
                session['rol'] = superadmin[8]

                return redirect(url_for('main.index'))

            flash('Usuario o clave incorrecta')

    return render_template("login.html")

#Registro de usuarios
@main.route('/registro', methods=['GET', 'POST'])
def registro():

    if request.method == 'POST':

        nombre = escape(request.form['nombre'])
        apellido = escape(request.form['apellido'])
        usuario = escape(request.form['usuario'])
        correo = escape(request.form['correo'])
        contraseña = escape(request.form['password'])
        telefono = escape(request.form['telefono'])

        db = get_db()
        # agregarle SLAT
        contraseña = contraseña + usuario
        contraseña = generate_password_hash(contraseña)
        db.execute("insert into usuario ( nombre, apellido, usuario, correo, contraseña, telefono, rol) values ( ?, ?, ?, ?, ?, ?, ?)",(nombre, apellido, usuario, correo, contraseña, telefono, 'user'))
        db.commit()
        db.close()
        return redirect(url_for('main.login'))
    return render_template("registro.html")

#Cerar cesión
@main.route('/logout')
def logout():
    session.clear()
    return render_template("index.html")

#VISTAS HABITACIONES

#Lista de habitaciones
@main.route('/ListaDeHabitaciones')
@login_required
def ListaDeHabitaciones():
    db = get_db()
    habitacion = db.execute ('Select * from habitacion').fetchall ()
    print (habitacion)
    return render_template(("ListaDeHabitaciones.html"), habs = habitacion)

#Nueva habitación
@main.route('/NuevaHabitacion', methods=['GET', 'POST'])
@login_required
def NuevaHabitacion():
    if request.method == 'POST':

        CodHab = escape(request.form['codigoHabitacion'])
        Numpiso = escape(request.form['numPiso'])
        Precio = escape(request.form['precio'])

        db = get_db()

        db.execute("insert into habitacion ( CodHab, Numpiso, Precio ) values ( ?, ?, ?)", (CodHab, Precio, Numpiso))
        db.commit()
        db.close()
        return redirect(url_for('main.ListaDeHabitaciones'))

    return render_template("NuevaHabitacion.html")

# Editar información de las habitaciones
@main.route('/editHab/<string:id>')
def edit_room(id):
    db = get_db()
    dataHab = db.execute ('SELECT * FROM habitacion WHERE id = {0}'.format(id)).fetchall()
    print (dataHab)
    return render_template ('EditHab.html', dhabs = dataHab[0])

@main.route('/updateHab/<id>', methods = ['POST'])
def update_room(id):
    if request.method == 'POST':
        CodHab = request.form ['codigoHabitacion']
        Numpiso = request.form ['numPiso']
        Precio = request.form ['Precio']
        db = get_db()
        db.execute ("""
            UPDATE habitacion
            SET CodHab = ?,
                Numpiso = ?,
                Precio = ?
            WHERE id = ?
         """ , (CodHab, Numpiso, Precio, id))
        db.commit()
        return redirect(url_for('main.ListaDeHabitaciones'))

#Eliminar habitación
@main.route('/deleteHab/<string:id>')
def delete_room(id):
    db = get_db()
    db.execute ('DELETE FROM habitacion WHERE id = {0}'.format(id))
    db.commit ()
    return redirect(url_for('main.ListaDeHabitaciones'))


#VISTAS ADMINISTRADOR

#Listas de administradores
@main.route('/ListaDeAdministradores')
@login_required
def ListaDeAdministradores():
    db = get_db()
    adminitrador = db.execute ('Select * from administrador').fetchall ()
    print (adminitrador)
    return render_template(("ListaDeAdministradores.html"), admins = adminitrador)


#Nuevo administrador
@main.route('/NuevoAdministrador', methods=['GET', 'POST'])
@login_required
def NuevoAdministrador():

    if request.method == 'POST':
        cedula = escape(request.form['cedula'])
        nombre = escape(request.form['nombreAdministrador'])
        apellido = escape(request.form['apellidoAdminsitrador'])
        telefono = escape(request.form['telefonoAdministrador'])
        direccion = escape(request.form['direccionAdministrador'])
        usuario = escape(request.form['nombreAdministrador'])
        correo = escape(request.form['emailAdministrador'])
        contraseña = escape(request.form['passwordAdmministrador'])
        rol = escape(request.form['ROL'])
        
        db = get_db()
        # agregarle SLAT
        contraseña = contraseña + usuario
        contraseña = generate_password_hash(contraseña)
        db.execute("insert into administrador ( cedula, nombre, apellido, telefono, direccion, usuario, correo, contraseña, rol) values ( ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (cedula, nombre, apellido, telefono, direccion, usuario, correo, contraseña, rol))
        db.commit()
        db.close()
        return redirect(url_for('main.ListaDeAdministradores'))

    return render_template("NuevoAdministrador.html")

#Editar informacion administrador
@main.route('/editAdm/<string:id>')
def edit_Adm(id):
    db = get_db()
    dataAdm = db.execute ('SELECT * FROM administrador WHERE id = {0}'.format(id)).fetchall()
    print (dataAdm)
    return render_template ('EditAdm.html', dadm = dataAdm[0])

@main.route('/updateAdm/<id>', methods = ['POST'])
def update_Adm(id):
    if request.method == 'POST':
        cedula = request.form['cedula']
        nombre = request.form['nombreAdministrador']
        apellido = request.form['apellidoAdminsitrador']
        telefono = request.form['telefonoAdministrador']
        direccion = request.form['direccionAdministrador']
        usuario = request.form['nombreAdministrador']
        correo = request.form['emailAdministrador']
        contraseña = request.form['passwordAdmministrador']
        rol = request.form['ROL']
        db = get_db()
        db.execute ("""
            UPDATE administrador
            SET cedula = ?,
                nombre = ?,
                apellido = ?,
                telefono = ?,
                direccion = ?,
                usuario = ?,
                correo = ?,
                contraseña = ?,
                rol = ?
            WHERE id = ?
         """ , (cedula, nombre, apellido, telefono, direccion, usuario, correo, contraseña, rol, id))
        db.commit()
        return redirect(url_for('main.ListaDeAdministradores'))

#Eliminar administrador
@main.route('/deleteAdm/<string:id>')
def delete_contact(id):
    db = get_db ()
    db.execute ('DELETE FROM administrador WHERE id = {0}'.format(id))
    db.commit ()
    db.close
    return redirect(url_for('main.ListaDeAdministradores'))

#VISTA CLIENTES

#Lista clientes
@main.route('/listaDeClientes')
@login_required
def listaDeClientes():
    db = get_db()
    cliente = db.execute ('Select * from usuario').fetchall ()
    print (cliente)
    return render_template(("listaDeClientes.html"), cxs = cliente)  
 
#actualizar informacion
@main.route('/editUser/<string:id>')
def edit_User(id):
    db = get_db()
    dataUser = db.execute ('SELECT * FROM usuario WHERE id = {0}'.format(id)).fetchall()
    print (dataUser)
    return render_template ('EditUser.html', duser = dataUser[0])

@main.route('/updateUser/<id>', methods = ['POST'])
def update_User(id):
    if request.method == 'POST':
        nombre = request.form['nombreAdministrador']
        apellido = request.form['apellidoAdminsitrador']
        telefono = request.form['telefonoAdministrador']
        usuario = request.form['nombreAdministrador']
        correo = request.form['emailAdministrador']
        contraseña = request.form['passwordAdmministrador']
        rol = request.form['ROL']
        db = get_db()
        db.execute ("""
            UPDATE usuario
            SET nombre = ?,
                apellido = ?,
                usuario = ?,
                correo = ?,
                contraseña = ?,
                telefono = ?,
                rol = ?
            WHERE id = ?
         """ , (nombre, apellido, usuario, correo, contraseña, telefono, rol, id))
        db.commit()
        return redirect(url_for('main.listaDeClientes'))

#Eliminar cliente
@main.route('/deleteCx/<string:id>')
def delete_Cliente(id):
    db = get_db()
    db.execute ('DELETE FROM usuario WHERE id = {0}'.format(id))
    db.commit ()
    return redirect(url_for('main.listaDeClientes'))










@main.route('/edituser/<string:id>')
def edit_user(id):
    db = get_db()
    datauser = db.execute ('SELECT * FROM usuario WHERE id = {0}'.format(id)).fetchall()
    print (datauser)
    return render_template ('actualiarDatos.html', dadm = datauser[0])

@main.route('/updateDatos/<id>', methods = ['POST'])
def update_Datos(id):
    if request.method == 'POST':
        nombre = request.form['nombre-up']
        apellido = request.form['apellido-up']
        telefono = request.form['telefono-up']
        direccion = request.form['direccion-up']
        db = get_db()
        db.execute ("""
            UPDATE usuario
            SET nombre = ?,
                apellido = ?,
                telefono = ?,
                direccion = ?,
            WHERE id = ?
         """ , (nombre, apellido, telefono, direccion, id))
        db.commit()
        return render_template ('misDatos.html')

