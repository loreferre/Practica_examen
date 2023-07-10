from flask import session, render_template, redirect, request
from flask_bcrypt import Bcrypt
from app_practica import app
from flask import flash
from app_practica.modeladores.modelo_user import Usuario 

bcrypt=Bcrypt(app) #al instalar bcrypt arriba tb se hace aquí

@app.route('/', methods=['GET']) #1 ruta
def desplegar_login_registro():
    return render_template('login.html') #seguirnlo como login_registro

@app.route('/crear/usuario', methods=['POST']) #2 ruta, con el query para que lo datos lleguen a la bd
def nuevo_usuario():
    data={
        **request.form
        } #modo de encriptacion de password # agregar los datos en sesion
    usuario_existe=Usuario.obtener_uno_con_email(data) #Validacion de que este correo ya existe
    if Usuario.validar_registro(data, usuario_existe) == False:
        return redirect('/')
    else: 
        password_encriptado =bcrypt.generate_password_hash(data['password']) #desde el diccionario de Usuario
        data['password'] = password_encriptado
        id_usuario= Usuario.crear_uno(data)
        session['nombre']=data['nombre']
        session['apellido']=data['apellido']
        session['id_usuario']=id_usuario

        return redirect ('/recetas') #este es el sitio que llega cuando se registra
    
@app.route('/mi_dashboard', methods = ['GET']) #Que no se te vuelvan a repetir las rutas
def desplegar_dashboard ():
    if'nombre' not in session:
        return redirect('/')
    else:
        return render_template ('recetas.html') # 3 ruta, aquí se creo la pagina dashboard y ahora se hace el html
        

@app.route('/login', methods=['POST']) #validacion de usuario registrado
def procesa_login():
    data= {
        "email":request.form['email_login']
    }
    usuario=Usuario.obtener_uno_con_email (data)

    if usuario == None:
        flash("Email o contraseña incorrectos", "error_email_login")
        return redirect ('/')
    else:
        if not bcrypt.check_password_hash(usuario.password, request.form['login_password']):
            flash ("Contraseña Incorrecta","error_passwod_login" )
            return redirect ('/')
        else:
            session['nombre']=usuario.nombre
            session['apellido']=usuario.apellido
            session['id_usuario']=usuario.id
            return redirect ('/recetas')
    

@app.route ('/logout', methods=['POST'])
def procesa_logout():
    session.clear() #borra la sesion
    return redirect ('/')#ultomos pasos

