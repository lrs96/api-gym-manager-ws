
from flask import Flask, jsonify, request
import json
import urllib.request
import random

app = Flask(__name__)

alunos = [{"id": e, "nome": "{}".format(str(e)), "cpf": e, "foto":"https://images.pexels.com/photos/3214950/pexels-photo-3214950.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940", "idade": e } for e in range(1,11)]   

@app.route("/alunos", methods=['GET'])
def get():
    return jsonify(alunos)

@app.route("/alunos/<int:id>", methods=['GET'])
def get_one(id):
    filtro = [e for e in alunos if e["id"] == id]
    if filtro:
        return jsonify(filtro[0])
    else:
        return jsonify({})

@app.route("/alunos", methods=['POST'])
def post():
    global alunos
    try:
        content = request.get_json()

        # gerar id
        ids = [e["id"] for e in alunos]
        if ids:
            nid = max(ids) + 1
        else:
            nid = 1
        content["id"] = nid
        alunos.append(content)
        return jsonify({"status":"OK", "msg":"disciplina adicionada com sucesso"})
    except Exception as ex:
        return jsonify({"status":"ERRO", "msg":str(ex)})

@app.route("/alunos/<int:id>", methods=['DELETE'])
def delete(id):
    global alunos
    try:
        alunos = [e for e in alunos if e["id"] != id]
        return jsonify({"status":"OK", "msg":"disciplina removida com sucesso"})
    except Exception as ex:
        return jsonify({"status":"ERRO", "msg":str(ex)})

@app.route("/push/<string:key>/<string:token>", methods=['GET'])
def push(key, token):
	d = random.choice(alunos)
	data = {
		"to": token,
		"notification" : {
			"title":d["nome"],
			"body":"Você tem nova atividade em "+d['nome']
		},
		"data" : {
			"disciplinaId":d['id']
		}
	}
	req = urllib.request.Request('http://fcm.googleapis.com/fcm/send')
	req.add_header('Content-Type', 'application/json')
	req.add_header('Authorization', 'key='+key)
	jsondata = json.dumps(data)
	jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
	req.add_header('Content-Length', len(jsondataasbytes))
	response = urllib.request.urlopen(req, jsondataasbytes)
	print(response)
	return jsonify({"status":"OK", "msg":"Push enviado"})


if __name__ == "__main__":
    app.run(host='0.0.0.0')