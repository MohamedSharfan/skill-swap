import os
from flask import redirect, g, render_template, session, request, flash, Flask
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3

app = Flask(__name__)

# Session Configuration
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# SQL Connection
DATABASE = "skill_swap.db"
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db:
        db.close()

# Routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
        if request.method == "POST":
            username = request.form.get("username")
            email = request.form.get("email")
            password = request.form.get("password")
            confirmation = request.form.get("confirmation")

            if not username or not email or not password or not confirmation:
                flash("All fields are required!", "danger")
                return render_template("register.html")

            if password != confirmation:
                flash("Passwords do not match!", "danger")
                return render_template("register.html")

            hash_pw = generate_password_hash(password)

            db = get_db()
            try:
                    db.execute(
                        "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                        (username, email, hash_pw)
                    )
                    db.commit()

            except sqlite3.IntegrityError:
                    flash("Username already exists!", "danger")
                    return render_template("register.html")

            user = db.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()
            session["user_id"] = user["id"]
            return redirect("/")
        else:
            return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    try:
        session.clear()
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")

            if not username or not password:
                flash("Username and Password are required!", "danger")
                return render_template("login.html")

            db = get_db()
            user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

            if not user or not check_password_hash(user[3], password):
                flash("Invalid username or password", "danger")
                return render_template("login.html")

            session["user_id"] = user["id"]
            return redirect("/")
        else:
            return render_template("login.html")
    except sqlite3.Error as e:
        print(f"❌ Error in /login: {e}")
        flash("Server error during login", "danger")
        return render_template("login.html")


@app.route("/skills", methods=["GET", "POST"])
def skills():
    if request.method == "POST":
        user_id = session["user_id"]
        offer = request.form.get("offer")
        want = request.form.get("want")

        db = get_db()
        if offer:
            db.execute("INSERT INTO skills (user_id, skill_name, type) VALUES (?,?,?)",(user_id, offer,"offer"))
        if want:
            db.execute("INSERT INTO skills (user_id, skill_name, type) VALUES (?,?,?)",(user_id, want,"want"))
        db.commit()
        flash("Skills saved successfully!","success")
        return redirect("/") 
    else:
         return render_template("skills.html")
          

    
@app.route("/swap", methods=["GET", "POST"])
def swap():
    if request.method == "POST":
        db = get_db()
        want = request.form.get("want")

        if not want:
            flash("Please enter a skill you want to learn.", "warning")
            return redirect("/swap")

        return redirect(f"/swapping?want={want}")
    else:
        return render_template("swap.html")
    
    

@app.route("/swapping", methods =["GET","POST"])
def swapping():
    if request.method == "POST":
        want = request.form.get("want")
    else:
        want = request.args.get("want")
    db = get_db()
    
    if not want:
        flash("Please enter a skill you want to learn.", "warning")
        return redirect("/swap")
    users = db.execute("SELECT skills.skill_name,skills.type,users.username FROM skills JOIN users ON skills.user_id = users.id WHERE skills.type = 'offer'").fetchall()
    return render_template("swapping.html",users = users, match = want)

@app.route("/chat")
def chat():
    db = get_db()
    matched_user = request.args.get("user")
    
    current_user_id = session.get("user_id")
    if not current_user_id:
        flash("Please log in first.", "warning")
        return redirect("/login")

    current_user_row = db.execute("SELECT username FROM users WHERE id = ?", (current_user_id,)).fetchone()
    if not current_user_row:
        flash("User not found.", "danger")
        return redirect("/login")
    current_user = current_user_row["username"]

    result = db.execute("SELECT email FROM users WHERE username = ?",(matched_user,)).fetchone()
    if result:
        email = result["email"]
    else:
        email = "Not Found"
    users = sorted([current_user, matched_user])
    room_name = f"swap_room_{users[0]}_{users[1]}"

    return render_template("chat.html", room = room_name, username = matched_user, email = email)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# Start the server
if __name__ == '__main__':
    app.run()
