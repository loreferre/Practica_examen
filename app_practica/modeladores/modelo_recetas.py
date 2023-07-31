from app_practica.config.mysqlconecction import connectToMySQL
from app_practica.modeladores.modelo_user import Usuario
from datetime import datetime
from app_practica import BASE_DATOS
from flask import flash

class Receta:
    def __init__(self, data) :
        self.id = data['id']
        self.nombre = data['nombre']
        self.descripcion = data['descripcion']
        self.instrucciones = data['instrucciones']
        self.fecha_elaboracion = data['fecha_elaboracion']
        self.menos_treinta = data['menos_treinta']        
        self.id_usuario = data['id_usuario']
        self.fecha_creacion = data['fecha_creacion']
        self.fecha_actualizacion = data['fecha_actualizacion']
        self.usuario = None

    def fecha_con_formato(self):
        if isinstance(self.fecha_elaboracion, datetime):
            return self.fecha_elaboracion.strftime('%d-%m-%Y')
        return None

    @classmethod
    def crear_uno(cls, data):
        query = """
                INSERT INTO recetas (nombre, descripcion, instrucciones, fecha_elaboracion, menos_treinta, id_usuario)
                VALUES ( %(nombre)s, %(descripcion)s, %(instrucciones)s, %(fecha_elaboracion)s, %(menos_treinta)s, %(id_usuario)s)
                """
        id_receta = connectToMySQL (BASE_DATOS).query_db (query, data)
        return id_receta
    
    @classmethod #esto se hace al momento de hacer la parte donde se ve la info
    def obtener_todas_con_usuarios (cls,):
        query="""
                SELECT *
                FROM recetas r JOIN usuarios u
                ON r.id_usuario =u.id;"""
        
        resultado = connectToMySQL(BASE_DATOS).query_db(query)
        lista_recetas=[]
        for renglon in resultado:
            receta =Receta(renglon)
            data_usuario = {
                "id" : renglon ['u.id'], #se pone la letra chica solo con los que estan repetidos en las dos tablas
                "nombre" : renglon ['u.nombre'],
                "apellido" :renglon ['apellido'],
                "email" :renglon ['email'],
                "password" :renglon ['password'],
                "fecha_creacion" :renglon ['u.fecha_creacion'],
                "fecha_actualizacion" :renglon ['u.fecha_actualizacion'],                    
            }
            usuario=Usuario(data_usuario)
            receta.usuario = usuario
            lista_recetas.append(receta)
            
        return lista_recetas
    
    @classmethod #Eliminar
    def elimina_uno (cls, data):
        query = """
            DELETE FROM recetas
            WHERE id = %(id)s;
            """
    
        return connectToMySQL(BASE_DATOS).query_db(query, data)
    

    @classmethod
    def obtener_uno(cls, data):
        query = """
            SELECT *
            FROM recetas
            WHERE id = %(id)s;
            """
        resultado = connectToMySQL(BASE_DATOS).query_db(query, data)
        if resultado:  
            receta = Receta(resultado[0])
            return receta
    
    @classmethod
    def editar_uno(cls, data):
        query = """
                UPDATE recetas
                SET nombre= %(nombre)s, descripcion= %(descripcion)s, instrucciones= %(instrucciones)s, fecha_elaboracion= %(fecha_elaboracion)s, menos_treinta=%(menos_treinta)s
                WHERE id = %(id)s;
                """
        
        return connectToMySQL(BASE_DATOS).query_db(query, data)

    @staticmethod #validaciones formulario
    def validar_formulario_recetas(data):
        es_valido = True
        if len(data['nombre'])< 3: 
            es_valido = False
        flash ("Debes escribir el nombre de la receta", "error_nombre")
        if len(data['descripcion'])< 3: 
            es_valido = False
        flash ("Debes escribir la descripcion de la receta", "error_descripcion")
        if len(data['instrucciones'])< 3: 
            es_valido = False
        flash ("Debes escribir las instruciones de la receta", "error_instrucciones")
        if data['fecha_elaboracion'] =="":
            es_valido=False
            flash("Selecciona una fecha para elaboración","error_fecha_elaboracion")
        if "menos_treinta" not in data:
            es_valido=False
            flash('No has seleccionado ninguna opción','error_menos_treinta')
        return es_valido 



