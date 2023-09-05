from flask import Flask, render_template, request, redirect, url_for
import datetime as dt
import sqlite3

app = Flask(__name__)

def add_user(name, gender, age, phone, desc1, desc2, timestamp, status):
    with sqlite3.connect('AIKOREA.db') as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO reservation (name, gender, age, phone, desc1, desc2, timestamp, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                       (name, gender, age, phone, desc1, desc2, timestamp, status))
        conn.commit()

@app.route("/", methods=["GET"])
def main():
    return render_template("./AIKOREA_KIOSK.html")

@app.route("/add", methods=["POST"])
def add():
    name = request.form.get('name')
    gender = request.form.get('gender')
    age = request.form.get('age')
    phone = request.form.get('phone')
    desc1 = request.form.get('desc1')
    desc2 = request.form.get('desc2')
    timestamp = dt.datetime.now()
    add_user(name, gender, age, phone, desc1, desc2, timestamp, "0")
    return "ok"

@app.route("/list", methods=["GET"])
def list_reservations():
    with sqlite3.connect('AIKOREA.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM reservation ORDER BY timestamp DESC")
        reservations = cursor.fetchall()
    return render_template("list.html", reservations=reservations)

@app.route("/update", methods=["POST"])
def update_status():
    timestamp = request.form.get('timestamp')
    status = request.form.get('status')
    with sqlite3.connect('AIKOREA.db') as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE reservation SET status=? WHERE timestamp=?", (status, timestamp))
        conn.commit()
    return redirect(url_for('list_reservations'))

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host="0.0.0.0", port=81)
