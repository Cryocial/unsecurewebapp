"""
DashDoor — a scrappy food delivery startup.

Backend written by John Intern (supergenius).

    python db.py      # build the database (run once)
    python app.py     # start the server -> http://127.0.0.1:5000

"""
import sqlite3
import os
from flask import (
    Flask, render_template, request, redirect, url_for, session, flash
)
from logic import (
    calculate_subtotal, apply_discount, calculate_tax,
    is_open, validate_quantity, split_bill,
)

app = Flask(__name__)
app.secret_key = "dev-secret-not-for-production"

DB_PATH = os.path.join(os.path.dirname(__file__), "dashdoor.db")
CART = []


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def index():
    if "user" in session:
        return redirect(url_for("home"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        conn = get_db()
        query = (
            "SELECT * FROM users WHERE username = '" + username +
            "' AND password = '" + password + "'"
        )
        try:
            row = conn.execute(query).fetchone()
        except sqlite3.Error as e:
            flash(f"Database error: {e}")
            conn.close()
            return render_template("login.html")
        conn.close()

        if row:
            session["user"] = row["username"]
            session["is_admin"] = bool(row["is_admin"])
            return redirect(url_for("home"))
        flash("Wrong username or password.")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/home")
def home():
    if "user" not in session:
        return redirect(url_for("login"))

    search = request.args.get("q", "").strip()
    conn = get_db()

    if search:
        query = (
            "SELECT * FROM menu WHERE name LIKE '%" + search +
            "%' AND visible = 1"
        )
        try:
            items = conn.execute(query).fetchall()
        except sqlite3.Error as e:
            flash(f"Database error: {e}")
            items = []
    else:
        items = conn.execute(
            "SELECT * FROM menu WHERE visible = 1 ORDER BY id"
        ).fetchall()

    conn.close()
    return render_template("home.html", items=items, cart=CART, search=search)


@app.route("/add", methods=["POST"])
def add_to_cart():
    if "user" not in session:
        return redirect(url_for("login"))

    name = request.form.get("name")
    price = float(request.form.get("price", 0))
    try:
        qty = int(request.form.get("quantity", 1))
    except ValueError:
        qty = 1

    if validate_quantity(qty):
        CART.append({"name": name, "price": price, "quantity": qty})
    else:
        flash(f"Invalid quantity for {name}.")

    return redirect(url_for("home"))


@app.route("/clear")
def clear_cart():
    CART.clear()
    return redirect(url_for("home"))


@app.route("/checkout")
def checkout():
    if "user" not in session:
        return redirect(url_for("login"))

    code = request.args.get("code", "").strip()

    subtotal = calculate_subtotal(CART)
    discounted = apply_discount(subtotal, code) if code else subtotal
    tax = calculate_tax(discounted)
    total = discounted + tax

    # split-the-bill demo: how many people are splitting?
    try:
        people = int(request.args.get("people", 1))
    except ValueError:
        people = 1
    split = None
    if people:
        try:
            split = split_bill(total, people)
        except ZeroDivisionError:
            split = None

    open_now = is_open(request.args.get("hour", type=int)
                       if request.args.get("hour") else 12)

    return render_template(
        "checkout.html",
        cart=CART, subtotal=subtotal, discounted=discounted, tax=tax,
        total=total, code=code, people=people, split=split,
        open_now=open_now,
    )


@app.route("/place_order")
def place_order():
    if "user" not in session:
        return redirect(url_for("login"))

    subtotal = calculate_subtotal(CART)
    total = subtotal + calculate_tax(subtotal)
    summary = ", ".join(f"{i['quantity']}x {i['name']}" for i in CART)

    conn = get_db()
    conn.execute(
        "INSERT INTO orders (username, summary, total) VALUES (?, ?, ?)",
        (session["user"], summary or "(empty)", total),
    )
    conn.commit()
    conn.close()
    CART.clear()
    flash("Order placed!")
    return redirect(url_for("home"))


@app.route("/admin")
def admin():
    if "user" not in session:
        return redirect(url_for("login"))
    if not session.get("is_admin"):
        flash("Staff only.")
        return redirect(url_for("home"))

    conn = get_db()
    orders = conn.execute("SELECT * FROM orders ORDER BY id DESC").fetchall()
    staff_menu = conn.execute(
        "SELECT * FROM menu WHERE visible = 0 ORDER BY id"
    ).fetchall()
    conn.close()
    return render_template("admin.html", orders=orders, staff_menu=staff_menu)


if __name__ == "__main__":
    if not os.path.exists(DB_PATH):
        print("No database found. Run:  python db.py")
    app.run(debug=True, port=5000)
