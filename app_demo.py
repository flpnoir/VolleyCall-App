from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime
import itertools

# Simple demo for my assessment.
# No database. I keep data in memory to avoid setup problems on different machines.
# I focused on the core flow: organiser creates a match, players RSVP, and can mark payment.

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "demo-secret"  # ok for local demo only

# Jinja filter: NZ short date dd/mm/yyyy h:mm am/pm
@app.template_filter("nzdt")
def nzdt(value):
    from datetime import datetime
    try:
        dt = datetime.strptime(value, "%Y-%m-%d %H:%M")
    except Exception:
        return value
    d = dt.strftime("%d/%m/%Y")
    t = dt.strftime("%I:%M %p").lower()
    if t.startswith("0"): t = t[1:]
    return f"{d} {t}"

# fake users (just for the demo video)
users = {
    "ernesto@example.com": {"name": "Ernesto", "role": "organiser", "password": "test"},
    "eleonora@example.com": {"name": "Eleonora", "role": "player", "password": "test"},
    "john@example.com": {"name": "John", "role": "player", "password": "test"},
}

# simple id generator for matches
_match_id = itertools.count(2)

# one seed match so the UI is not empty
matches = {
    1: {
        "id": 1,
        "title": "Saturday Social",
        "datetime": "2025-08-30 17:00",
        "location": "Graham Condon",
        "notes": "Mixed, casual. Bring water.",
        "organiser": "ernesto@example.com",
        "attending": set(),
        "paid": set(),
        "capacity": 12
    }
}

def current_user():
    email = session.get("email")
    return users.get(email) if email else None

@app.route("/")
def index():
    return render_template("index.html", user=current_user(), matches=matches)

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email","").strip().lower()
        pw = request.form.get("password","")
        u = users.get(email)
        if u and u["password"] == pw:
            session["email"] = email
            flash("Logged in")
            return redirect(url_for("dashboard"))
        flash("Invalid credentials")
    return render_template("login.html")
    
    @app.route("/register", methods=["GET","POST"])
def register():
    # very simple, in-memory
    if request.method == "POST":
        name = request.form.get("name","").strip()
        email = request.form.get("email","").strip().lower()
        pw = request.form.get("password","")
        role = request.form.get("role") or "player"
        if not name or not email or not pw:
            flash("All fields are required")
            return render_template("register.html")
        if email in users:
            flash("Email already registered")
            return render_template("register.html")
        users[email] = {"name": name, "role": role, "password": pw}
        session["email"] = email
        flash("Account created")
        return redirect(url_for("dashboard"))
    return render_template("register.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out")
    return redirect(url_for("index"))

@app.route("/dashboard")
def dashboard():
    user = current_user()
    if not user:
        return redirect(url_for("login"))
    if user["role"] == "organiser":
        own = [m for m in matches.values() if m["organiser"] == session["email"]]
        return render_template("dashboard_organiser.html", user=user, matches=own)
    upcoming = sorted(matches.values(), key=lambda m: m["id"])
    return render_template("dashboard_player.html", user=user, matches=upcoming)

@app.route("/matches/new", methods=["GET","POST"])
def create_match():
    user = current_user()
    if not user or user["role"] != "organiser":
        flash("Only organisers can create matches")
        return redirect(url_for("login"))
    if request.method == "POST":
        mid = next(_match_id)
        data = {
            "id": mid,
            "title": request.form.get("title") or f"Match {mid}",
            "datetime": f"{request.form.get('date')} {request.form.get('time')}",
            "location": request.form.get("location","").strip(),
            "notes": request.form.get("notes","").strip(),
            "organiser": session["email"],
            "attending": set(),
            "paid": set(),
            "capacity": int(request.form.get("capacity") or 12),
        }
        matches[mid] = data
        flash("Match created")
        return redirect(url_for("match_detail", match_id=mid))
    return render_template("match_new.html", user=user)

@app.route("/matches/<int:match_id>")
def match_detail(match_id):
    m = matches.get(match_id)
    if not m:
        flash("Match not found")
        return redirect(url_for("dashboard"))
    user = current_user()
    return render_template("match_detail.html", m=m, user=user, users=users)

@app.route("/matches/<int:match_id>/rsvp", methods=["POST"])
def rsvp(match_id):
    m = matches.get(match_id)
    user = current_user()
    if not (m and user):
        return redirect(url_for("login"))
    email = session["email"]
    if email in m["attending"]:
        m["attending"].remove(email)
        flash("RSVP removed")
    else:
        if len(m["attending"]) < m["capacity"]:
            m["attending"].add(email)
            flash("RSVP confirmed")
        else:
            flash("Match is full")
    return redirect(url_for("match_detail", match_id=match_id))

@app.route("/matches/<int:match_id>/mark_paid", methods=["POST"])
def mark_paid(match_id):
    m = matches.get(match_id)
    user = current_user()
    if not (m and user):
        return redirect(url_for("login"))
    email = session["email"]
    if email in m["attending"]:
        if email in m["paid"]:
            m["paid"].remove(email)
            flash("Payment status cleared")
        else:
            m["paid"].add(email)
            flash("Payment marked as paid")
    else:
        flash("RSVP first, then mark as paid")
    return redirect(url_for("match_detail", match_id=match_id))

if __name__ == "__main__":
    app.run(debug=True)
