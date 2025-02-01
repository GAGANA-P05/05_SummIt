from flask import Flask, render_template, request, redirect
from flask_login import LoginManager, login_required, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = "my-secrets"

login_manager = LoginManager()
login_manager.init_app(app)

@app.route("/")
def home():
    return redirect("/dashboard")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", first_name=current_user.first_name, last_name=current_user.last_name)

@app.route("/meeting")
def meeting():
    return render_template("meeting.html", username=current_user.username)

@app.route("/join", methods=["GET", "POST"])
def join():
    if request.method == "POST":
        room_id = request.form.get("roomID")
        return redirect(f"/meeting?roomID={room_id}")
    return render_template("join.html")

if __name__ == "__main__":
    app.run(debug=True)
