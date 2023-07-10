from flask import session, render_template, redirect, request
from app_practica.modeladores.modelo_recetas import Receta
from app_practica import app
from flask import flash
#from app_practica.modeladores.modelo_recetas import Recetas

@app.route('/recetas', methods =['GET'])
def desplegar_recetas():
    if "id_usuario" not in session:
        return redirect('/')
    else:
        lista_recetas = Receta.obtener_todas_con_usuarios() #esto se agrega cuando se agreguen la lista renglon 
        return render_template('recetas.html', lista_recetas=lista_recetas) #con esto se envia a la plantilla

@app.route ('/formulario/recetas', methods=['GET'])
def desplegar_formulario_recetas():
    if "id_usuario" not in session:
        return redirect('/')
    else:
        return render_template('formulario_recetas.html')

@app.route ('/crear/receta', methods=['POST'])
def nueva_receta ():
    #print(request.form) para probar que los datos lleguen al form
    data={
        **request.form,
        "id_usuario": session['id_usuario']
    }
    if Receta.validar_formulario_recetas(data )== False: #aqui se conectan las validaciones 
        return redirect('/formulario/recetas')
    else:
        id_receta = Receta.crear_uno(data)
        return redirect('/recetas')

@app.route('/eliminar_receta/<int:id>', methods=['POST']) #boton eliminar funcionalidad
def eliminar_receta (id):
    data ={
        "id" : id
    }
    Receta.elimina_uno(data)
    return redirect("/recetas")

@app.route('/ver_receta/<int:id>', methods=['GET'])
def desplegar_receta(id):
    if "id_usuario" not in session:
        return redirect('/')
    else:
        data = {
            "id": id
        }
        receta =Receta.obtener_uno_con_usuario(data)
        return render_template('receta.html', receta = receta)

@app.route ('/formulario/editar/<int:id>', methods=['GET']) 
def desplegar_editar_receta(id):
    if "id_usuario" not in session:
        return redirect('/')
    else:
        data ={
            "id": id
        }
        receta= Receta.obtener_uno(data)
        return render_template('editar_receta.html', receta =receta )  #esto hace que los datos esten en el formulario al momento de entrar
        
@app.route ('/editar/receta/<int:id>', methods = ['POST'])
def editar_receta(id):
    if Receta.validar_formulario_recetas(request.form) == False:
        return redirect(f'/formulario/editar/{id}')
    else:
        data= {
            **request.form,
            "id":id
        }
        Receta.editar_uno(data)
        return redirect ('/recetas')

#poner en todas las rutas GET if "id_usuario" not in session: return redirect('/' seguir con else: