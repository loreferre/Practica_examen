from flask import Flask
import re

app = Flask(__name__)
app.secret_key = "esto es secreto"
BASE_DATOS = "bd_recetas" #Se pone el nombre el esquena de mysql con el que se trabja
EMAIL_REGEX = re.compile(r'^([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+$')
NOMBRE_REGEX = re.compile(r'^[A-Z]{1}[a-zA-Z]+$')

#Esto se copia tal cual solo se cambia la bd