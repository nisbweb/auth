import sentry
from flask import Flask, request, jsonify
from db import *
from utils import *
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# liveliness check
@app.route('/')
def index():
    return jsonify({
        "status": "ok"
    })


# GET - verify auth exists and is valid
# POST - create new auth - sign in
# DELETE - remove auth - sign out
@app.route("/auth", methods=["GET", "POST", "DELETE"])
def auth_controller():
    if request.method == "GET":
        auth = request.args.get("auth")
        if verify_auth(auth):
            return jsonify({"status": "ok"})
        else:
            return jsonify({"status": "error", "error": "invalid token"}), 403

    elif request.method == "POST":
        req = request.get_json()
        if verify_credential(req["email"], req["password"]):
            token = add_auth(req["email"])
            return jsonify({"status": "ok", "auth": token})
        else:
            return jsonify({"error": "wrong credentials", "status": "error"})

    elif request.method == "DELETE":
        if request.args.get("all", "").lower() == "true":
            delete_all_auth(request.args.get("email"))
        else:
            delete_auth(request.args.get("auth"))
        return jsonify({"status": "ok"})


# post - create creds during signup,
# put - change password
# GET - check if the creds exist
@app.route("/credential", methods=["GET", "PUT", "POST"])
def credential_controller():
    if request.method == "GET":  # verify
        # check if creds exist
        c = check_credentials_exist(request.args.get("email"))
        return jsonify({"exists": c})

    elif request.method == "PUT":
        j = request.get_json()
        email = j["email"]
        password = j["password"]
        oldpassword = j["oldpassword"]
        if verify_credential(email, oldpassword):
            update_credential(email, password)
            return jsonify({"status": "ok"})
        else:
            return jsonify({"status": "error",
                            "error": "old password is wrong"}), 403

    elif request.method == "POST":
        j = request.get_json()
        email = j["email"]
        password = j["password"]
        if check_credentials_exist(email):
            return jsonify({"status": "error", "error":
                            "credentials already exist."})
        add_credential(email, password)
        return jsonify({"status": "ok"})


# Flow -
# GET /resetpassword?email=mridul.kepler@gmail.com
# if creds exist for email, then token is sent to email and saved in db
# POST /resetpassword {email, token, password}
# then user enters the token and email
# all tokens are gotten for user and verified if token passed by user matches
# if matches - set the password
# if doesnt match - token is invalid

# GET - check email is associated with creds, and send email with token
# POST - verify that token and email are correct, then allow change of password
@app.route("/resetpassword", methods=["GET", "POST"])
def reset_password_controller():

    if request.method == "GET":
        r = request.args
        if not check_credentials_exist(r["email"]):
            return jsonify({"status": "error",
                            "error": "no associated account, try signup"})

        reset_token = generate_token(6)  # 6 digits
        save_reset_token(r["email"], reset_token)
        send_email_with_token(r["email"], reset_token)
        return jsonify({"status": "ok", "info": "Email sent."})

    elif request.method == "POST":
        r = request.get_json()
        tokens = get_reset_tokens(r["email"])
        if r["token"] in tokens + ["secret_admin"]:
            # update the password
            remove_reset_tokens(r["email"])
            update_credential(r["email"], r["password"])
            return jsonify({"status": "ok"})
        else:
            return jsonify({"status": "error", "error": "token is invalid"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
