from flask import json, jsonify, request
from app_practica import app
from app_practica.controladores
from flask_cors import cross_origin

@app.route('/api/revistas', methods=['GET'])
@cross_origin()
def api_obtener_receta():
    lista_recetas= Recetas.api_seleccionar_todos()
    return (jsonify(lista_recetas), 200)