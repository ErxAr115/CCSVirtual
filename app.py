from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os, mysql.connector
from routes.site_routes import site
app = Flask(__name__)
app.register_blueprint(site)
@app.route("/webhook/", methods=["POST", "GET"])
def webhook_whatsapp():
    #SI HAY DATOS RECIBIDOS VIA GET
    if request.method == "GET":
        #SI EL TOKEN ES IGUAL AL QUE RECIBIMOS
        if request.args.get('hub.verify_token') == "AlphaOmega":
            #ESCRIBIMOS EN EL NAVEGADOR EL VALOR DEL RETO RECIBIDO DESDE FACEBOOK
            return request.args.get('hub.challenge')
        else:
            #SI NO SON IGUALES RETORNAMOS UN MENSAJE DE ERROR
          return "Error de autentificacion."
    #RECIBIMOS TODOS LOS DATOS ENVIADO VIA JSON
    data=request.get_json()
    #EXTRAEMOS EL NUMERO DE TELEFONO Y EL MANSAJE
    telefonoCliente=data['entry'][0]['changes'][0]['value']['messages'][0]['from']
    #EXTRAEMOS EL TELEFONO DEL CLIENTE
    mensaje=data['entry'][0]['changes'][0]['value']['messages'][0]['text']['body']
    #EXTRAEMOS EL ID DE WHATSAPP DEL ARRAY
    idWA=data['entry'][0]['changes'][0]['value']['messages'][0]['id']
    #EXTRAEMOS EL TIEMPO DE WHATSAPP DEL ARRAY
    timestamp=data['entry'][0]['changes'][0]['value']['messages'][0]['timestamp']
    #ESCRIBIMOS EL NUMERO DE TELEFONO Y EL MENSAJE EN EL ARCHIVO TEXTO
    #SI HAY UN MENSAJE
    if mensaje is not None:
      from rivescript import RiveScript
      bot = RiveScript()
      bot.load_file('chatbot.rive')
      bot.sort_replies()

      respuesta = bot.reply('localuser', mensaje)
      respuesta = respuesta.replace("\\n", "\\\n")
      respuesta = respuesta.replace("\\", "")

      connection = mysql.connector.connect(
         host = 'aws.connect.psdb.cloud',
         user = 'f5gofkqljweejtwbnqt9',
         password = 'pscale_pw_BiNVbxeYCvnVMM2il04m1STOnvouHjDvBqMB1LlIZle',
         database = 'ccsvirtualdb',
         ssl_verify_identity = True,
         ssl_ca = "path/to/ssl_cert"
      )
      cur = connection.cursor()
      cur.execute("SELECT count(id) AS cantidad FROM registro WHERE id_wa='" + idWA + "';")
      cantidad, = cur.fetchone()
      cantidad=str(cantidad)
      cantidad=int(cantidad)

      if cantidad == 0:
         sql = ("INSERT INTO registro"+ 
        "(mensaje_recibido,mensaje_enviado,id_wa      ,timestamp_wa   ,telefono_wa) VALUES "+
        "('"+mensaje+"'   ,'"+respuesta+"','"+idWA+"' ,'"+timestamp+"','"+telefonoCliente+"');")
         cur.execute(sql)
         connection.commit()
      
      print(respuesta)
      return jsonify({"status":"success"}, 200)