from flask import Flask, request, jsonify
from db import *
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Does nothing
@app.route('/')
def index():
    return jsonify({
        "status":"ok"
    })

@app.route("/auth", methods=["GET","POST","DELETE"])
def auth_controller():
    if request.method=="GET":
        auth = request.args.get("auth")
        if verify_auth(auth):
            return jsonify({"status":"ok"})
        else:
            return jsonify({"status":"error","error":"invalid token"}),403
        

    elif request.method=="POST":
        req = request.get_json()
        if verify_credential(req["email"],req["password"]):
            token = add_auth(req["email"])
            return jsonify({"status":"ok","auth":token})
        else:
            return jsonify({"error":"wrong credentials","status":"error"})
    
    
    elif request.method=="DELETE":
        if request.args.get("all",False) == True:
            delete_all_auth(request.args.get("email"))
        else:
            delete_auth(request.args.get("auth"))
        return jsonify({"status":"ok"})


@app.route("/credential", methods=["GET","PUT","POST"])
def credential_controller():
    if request.method=="GET": # verify
        pass

    elif request.method=="PUT":
        j = request.get_json()
        email = j["email"]
        password = j["password"]
        oldpassword = j["oldpassword"]
        if verify_credential(email,oldpassword):
            update_credential(email,password)
            return jsonify({"status":"ok"})
        else:
            return jsonify({"status":"error","error":"old password is wrong"}),403

    elif request.method=="POST":
        j = request.get_json()
        email = j["email"]
        password = j["password"]
        add_credential(email,password)
        return jsonify({"status":"ok"})


if __name__ == '__main__':
    # session["login"] = False

    app.run(host='0.0.0.0', debug=True)
