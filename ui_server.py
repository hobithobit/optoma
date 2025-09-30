from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import card_manager
from esp_bridge import esp
from config import UNLOCK_PIN

app = Flask(__name__)
app.secret_key = "supersecretkey"

@app.route("/")
def index():
    cards = card_manager.list_cards()
    return render_template("index.html", cards=cards)

@app.route("/add", methods=["POST"])
def add():
    uid = request.form["uid"].strip()
    role = request.form["role"]
    if card_manager.add_card(uid, role):
        flash(f"Karta {uid} byla přidána.")
    else:
        flash(f"Karta {uid} už existuje!")
    return redirect(url_for("index"))

@app.route("/remove", methods=["POST"])
def remove():
    uid = request.form["uid"].strip()
    card_manager.remove_card(uid)
    flash(f"Karta {uid} byla odstraněna.")
    return redirect(url_for("index"))

@app.route("/unlock", methods=["POST"])
def unlock():
    pin = request.form["pin"].strip()
    if pin == UNLOCK_PIN:
        flash("✅ Systém odemčen!")
        esp.send_sc_lock()
    else:
        flash("❌ Špatný PIN!")
    return redirect(url_for("index"))

# API pro budoucí master/slave
@app.route("/api/cards", methods=["GET", "POST", "DELETE"])
def api_cards():
    if request.method == "GET":
        return jsonify(card_manager.list_cards())
    elif request.method == "POST":
        data = request.json
        if card_manager.add_card(data["uid"], data.get("role", "user")):
            return jsonify({"status": "ok"})
        return jsonify({"status": "exists"})
    elif request.method == "DELETE":
        data = request.json
        card_manager.remove_card(data["uid"])
        return jsonify({"status": "removed"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
