import os
import sqlite3
import subprocess
import xml.etree.ElementTree as ET
from flask import Flask, request

app = Flask(__name__)

# Vulnérabilité 1 : Injection de commande (Command Injection)
@app.route('/ping', methods=['GET'])
def ping():
    host = request.args.get('host')
    os.system("ping " + host)  # ⚠️ Ne jamais construire une commande shell directement avec des données utilisateur

# Vulnérabilité 2 : Injection SQL (SQL Injection)
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = '{}' AND password = '{}'".format(username, password)
    cursor.execute(query)  # ⚠️ Construction directe d'une requête SQL sans paramétrisation
    result = cursor.fetchone()
    if result:
        return "Bienvenue " + username
    else:
        return "Échec de connexion"

# Vulnérabilité 3 : Injection XML (XML External Entity - XXE)
@app.route('/upload-xml', methods=['POST'])
def upload_xml():
    file = request.files['file']
    tree = ET.parse(file)  # ⚠️ Analyse directe d'un XML non sécurisé
    root = tree.getroot()
    return "XML traité"

if __name__ == '__main__':
    app.run(debug=True)