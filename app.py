import os

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    jsonify
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

import re
import json
import sqlite3
from datetime import datetime


# ============================================================
# APP SETUP
# ============================================================

app = Flask(__name__)

app.secret_key = "goodwood-bake-shop-secret-key"


# ============================================================
# USERS
# ============================================================
# All accounts (customer and staff) now live in the "users" table
# in goodwood.db - see create_default_users() above, and login()
# and staff_login() below, which both check the database instead
# of an in-memory dict.


# ============================================================
# DATABASE
# ============================================================

DATABASE = "goodwood.db"


def get_db_connection():

    connection = sqlite3.connect(
        DATABASE
    )

    connection.row_factory = sqlite3.Row

    return connection


def init_database():

    connection = get_db_connection()
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'customer'
        )
        """
    )
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS reviews (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            customer_name TEXT NOT NULL,

            customer_email TEXT,

            message TEXT NOT NULL,

            source TEXT NOT NULL,

            created_at TEXT NOT NULL

        )
        """
    )

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            customer_email TEXT NOT NULL,
            phone TEXT NOT NULL,
            items TEXT NOT NULL,
            subtotal REAL NOT NULL,
            tax REAL NOT NULL,
            total REAL NOT NULL,
            order_type TEXT NOT NULL,
            pickup_date TEXT,
            pickup_time TEXT,
            payment_method TEXT NOT NULL,
            notes TEXT,
            status TEXT NOT NULL DEFAULT 'Pending',
            created_at TEXT NOT NULL
        )
        """
    )



    connection.commit()
    connection.close()

def create_default_users():
    """
    Create the default demo customer and staff accounts
    if they do not already exist.

    Existing accounts are NOT overwritten.
    """

    connection = get_db_connection()


    # --------------------------------------------------------
    # Check whether demo customer already exists
    # --------------------------------------------------------

    customer = connection.execute(
        """
        SELECT id
        FROM users
        WHERE email = ?
        """,
        ("demo@goodwood.com",)
    ).fetchone()


    if customer is None:

        connection.execute(
            """
            INSERT INTO users
            (
                name,
                email,
                password,
                role
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                "Goodwood Customer",
                "demo@goodwood.com",
                generate_password_hash(
                    "Goodwood123"
                ),
                "customer"
            )
        )


    # --------------------------------------------------------
    # Check whether staff account already exists
    # --------------------------------------------------------

    staff = connection.execute(
        """
        SELECT id
        FROM users
        WHERE email = ?
        """,
        ("staff@goodwood.com",)
    ).fetchone()


    if staff is None:

        connection.execute(
            """
            INSERT INTO users
            (
                name,
                email,
                password,
                role
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                "Goodwood Staff",
                "staff@goodwood.com",
                generate_password_hash(
                    "GoodwoodStaff23"
                ),
                "staff"
            )
        )


    connection.commit()

    connection.close()

def save_review(
    name,
    email,
    message,
    source
):

    connection = get_db_connection()

    connection.execute(
        """
        INSERT INTO reviews (
            customer_name,
            customer_email,
            message,
            source,
            created_at
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            name,
            email,
            message,
            source,
            datetime.now().strftime(
                "%d %b %Y, %I:%M %p"
            )
        )
    )

    connection.commit()
    connection.close()


def get_reviews():

    connection = get_db_connection()

    rows = connection.execute(
        """
        SELECT
            id,
            customer_name,
            customer_email,
            message,
            source,
            created_at
        FROM reviews
        ORDER BY id DESC
        """
    ).fetchall()

    connection.close()

    return [
        {
            "id": row["id"],
            "name": row["customer_name"],
            "email": row["customer_email"],
            "message": row["message"],
            "source": row["source"],
            "time": row["created_at"]
        }
        for row in rows
    ]


def save_order(
    customer_name,
    customer_email,
    phone,
    items,
    subtotal,
    tax,
    total,
    order_type,
    pickup_date,
    pickup_time,
    payment_method,
    notes
):
    connection = get_db_connection()

    cursor = connection.execute(
        """
        INSERT INTO orders (
            customer_name,
            customer_email,
            phone,
            items,
            subtotal,
            tax,
            total,
            order_type,
            pickup_date,
            pickup_time,
            payment_method,
            notes,
            status,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            customer_name,
            customer_email,
            phone,
            json.dumps(items),
            subtotal,
            tax,
            total,
            order_type,
            pickup_date,
            pickup_time,
            payment_method,
            notes,
            "Pending",
            datetime.now().strftime("%d %b %Y, %I:%M %p")
        )
    )

    order_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return order_id


def get_orders():
    connection = get_db_connection()

    rows = connection.execute(
        """
        SELECT
            id,
            customer_name,
            customer_email,
            phone,
            items,
            subtotal,
            tax,
            total,
            order_type,
            pickup_date,
            pickup_time,
            payment_method,
            notes,
            status,
            created_at
        FROM orders
        ORDER BY id DESC
        """
    ).fetchall()

    connection.close()

    orders = []

    for row in rows:
        try:
            items = json.loads(row["items"])
        except (TypeError, json.JSONDecodeError):
            items = []

        orders.append({
            "id": row["id"],
            "customer_name": row["customer_name"],
            "customer_email": row["customer_email"],
            "phone": row["phone"],
            "items": items,
            "subtotal": row["subtotal"],
            "tax": row["tax"],
            "total": row["total"],
            "order_type": row["order_type"],
            "pickup_date": row["pickup_date"],
            "pickup_time": row["pickup_time"],
            "payment_method": row["payment_method"],
            "notes": row["notes"],
            "status": row["status"],
            "created_at": row["created_at"]
        })

    return orders


# Create the database, reviews table and orders table when Flask starts.
init_database()
create_default_users()

def add_pickup_columns():
    """Add pickup date/time columns to an existing database safely."""
    connection = get_db_connection()

    columns = [
        row["name"]
        for row in connection.execute(
            "PRAGMA table_info(orders)"
        ).fetchall()
    ]

    if "pickup_date" not in columns:
        connection.execute(
            "ALTER TABLE orders ADD COLUMN pickup_date TEXT"
        )

    if "pickup_time" not in columns:
        connection.execute(
            "ALTER TABLE orders ADD COLUMN pickup_time TEXT"
        )

    connection.commit()
    connection.close()


add_pickup_columns()


# ============================================================
# PRODUCTS
# ============================================================

products = [

    {"name": "Chocolate Fudge Cake", "category": "Cake", "price": 28,
     "description": "Rich chocolate cake with smooth chocolate frosting.",
     "servings": "8–10 servings", "gluten_free": "No", "dairy_free": "No", "nut_free": "Yes"},

    {"name": "Strawberry Cream", "category": "Cake", "price": 30,
     "description": "Soft vanilla sponge layered with strawberry cream.",
     "servings": "8–10 servings", "gluten_free": "No", "dairy_free": "No", "nut_free": "Yes"},

    {"name": "Red Velvet", "category": "Cake", "price": 32,
     "description": "Classic red velvet sponge with creamy frosting.",
     "servings": "8–10 servings", "gluten_free": "No", "dairy_free": "No", "nut_free": "Yes"},

    {"name": "Classic Vanilla", "category": "Cake", "price": 25,
     "description": "Light vanilla sponge finished with vanilla buttercream.",
     "servings": "8–10 servings", "gluten_free": "No", "dairy_free": "No", "nut_free": "Yes"},

    {"name": "Chocolate Dream", "category": "Cupcakes", "price": 14,
     "description": "Moist chocolate cupcakes with creamy chocolate topping.",
     "servings": "Box of 6", "gluten_free": "No", "dairy_free": "No", "nut_free": "Yes"},

    {"name": "Vanilla Celebration", "category": "Cupcakes", "price": 13,
     "description": "Soft vanilla cupcakes with smooth buttercream.",
     "servings": "Box of 6", "gluten_free": "No", "dairy_free": "No", "nut_free": "Yes"},

    {"name": "Red Velvet Cupcakes", "category": "Cupcakes", "price": 15,
     "description": "Red velvet cupcakes finished with cream cheese frosting.",
     "servings": "Box of 6", "gluten_free": "No", "dairy_free": "No", "nut_free": "Yes"},

    {"name": "Strawberry Swirl", "category": "Cupcakes", "price": 15,
     "description": "Strawberry cupcakes with a fresh creamy swirl.",
     "servings": "Box of 6", "gluten_free": "No", "dairy_free": "No", "nut_free": "Yes"},

    {"name": "Butter Croissant", "category": "Pastry", "price": 3,
     "description": "Golden, flaky and buttery French-style croissant.",
     "servings": "Per piece", "gluten_free": "No", "dairy_free": "No", "nut_free": "Yes"},

    {"name": "Chocolate Danish", "category": "Pastry", "price": 4,
     "description": "Flaky pastry filled with rich chocolate.",
     "servings": "Per piece", "gluten_free": "No", "dairy_free": "No", "nut_free": "Yes"},

    {"name": "Fruit Danish", "category": "Pastry", "price": 4,
     "description": "Crisp pastry topped with sweet seasonal fruit.",
     "servings": "Per piece", "gluten_free": "No", "dairy_free": "No", "nut_free": "Yes"},

    {"name": "Morning Pastry", "category": "Pastry", "price": 3,
     "description": "A light, buttery pastry perfect with morning tea.",
     "servings": "Per piece", "gluten_free": "No", "dairy_free": "No", "nut_free": "Yes"},

    {"name": "Chocolate Chip", "category": "Cookies", "price": 8,
     "description": "Soft-baked cookies packed with chocolate chips.",
     "servings": "Box of 6", "gluten_free": "No", "dairy_free": "No", "nut_free": "Yes"},

    {"name": "Double Chocolate", "category": "Cookies", "price": 9,
     "description": "Deep chocolate cookies for chocolate lovers.",
     "servings": "Box of 6", "gluten_free": "No", "dairy_free": "No", "nut_free": "Yes"},

    {"name": "Oatmeal Crunch", "category": "Cookies", "price": 8,
     "description": "Classic oatmeal cookies with a satisfying crunch.",
     "servings": "Box of 6", "gluten_free": "No", "dairy_free": "No", "nut_free": "Yes"},

    {"name": "Goodwood Cookie Box", "category": "Cookies", "price": 10,
     "description": "A selection of our favourite freshly baked cookies.",
     "servings": "Box of 6", "gluten_free": "No", "dairy_free": "No", "nut_free": "Yes"}

]


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():

    return redirect(
        url_for("login")
    )


# ============================================================
# LOGIN
# ============================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    error = None

    if request.method == "POST":

        # Get form values
        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )


        # ----------------------------------------------------
        # FIND USER IN DATABASE
        # ----------------------------------------------------

        connection = get_db_connection()

        user = connection.execute(
            """
            SELECT
                id,
                name,
                email,
                password,
                role
            FROM users
            WHERE email = ?
            """,
            (email,)
        ).fetchone()

        connection.close()


        # ----------------------------------------------------
        # CHECK LOGIN DETAILS
        # ----------------------------------------------------

        if user and check_password_hash(
            user["password"],
            password
        ):

            # ------------------------------------------------
            # STORE USER IN SESSION
            # ------------------------------------------------

            session["user"] = {
                "email": user["email"],
                "name": user["name"],
                "role": user["role"]
            }


            # Reset cart after login
            # DO NOT CLEAR THE CART HERE
            # session["cart"] = []


            # ------------------------------------------------
            # STAFF
            # ------------------------------------------------

            if user["role"] == "staff":

                return redirect(
                    url_for("dashboard")
                )


            # ------------------------------------------------
            # CUSTOMER
            # ------------------------------------------------

            return redirect(
                url_for("products_page")
            )


        # ----------------------------------------------------
        # INVALID LOGIN
        # ----------------------------------------------------

        error = "Incorrect email or password."


    return render_template(
        "login.html",
        error=error
    )


# ============================================================
# STAFF LOGIN
# ============================================================

@app.route("/staff/login", methods=["GET", "POST"])
def staff_login():

    error = None

    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        # ----------------------------------------------------
        # FIND STAFF USER IN DATABASE
        # ----------------------------------------------------

        connection = get_db_connection()

        user = connection.execute(
            """
            SELECT
                id,
                name,
                email,
                password,
                role
            FROM users
            WHERE email = ?
            """,
            (email,)
        ).fetchone()

        connection.close()

        # ----------------------------------------------------
        # CHECK LOGIN DETAILS
        # ----------------------------------------------------

        if (
            user
            and user["role"] == "staff"
            and check_password_hash(user["password"], password)
        ):

            session["user"] = {
                "email": user["email"],
                "name": user["name"],
                "role": "staff"
            }
# DO NOT CLEAR THE CART HERE
            # session["cart"] = []

            return redirect(
                url_for("dashboard")
            )

        error = "Incorrect staff email or password."

    return render_template(
        "staff_login.html",
        error=error
    )


# ============================================================
# REGISTER
# ============================================================

@app.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    error = None

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        if not name or not email or not password:

            error = "Please fill in all fields."

            return render_template(
                "register.html",
                error=error
            )

        connection = get_db_connection()

        existing_user = connection.execute(
            """
            SELECT id
            FROM users
            WHERE email = ?
            """,
            (email,)
        ).fetchone()


        if existing_user:

            connection.close()

            error = "Customer already exists."

            return render_template(
                "register.html",
                error=error
            )
        connection.execute(
            """
            INSERT INTO users
            (
                name,
                email,
                password,
                role
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                name,
                email,
                generate_password_hash(password),
                "customer"
            )
        )

        connection.commit()
        connection.close()

        return redirect(
            url_for("login")
        )
        # return redirect(
        #     url_for("login")
        # )

    return render_template(
        "register.html",
        error=error
    )


# ============================================================
# CUSTOMER REVIEWS
# ============================================================

@app.route(
    "/submit-review",
    methods=["POST"]
)
def submit_review():

    if "user" not in session:

        return redirect(
            url_for("login")
        )

    review_text = request.form.get(
        "review",
        ""
    ).strip()

    if not review_text:

        return redirect(
            url_for("products_page")
        )

    user = session["user"]

    save_review(
        user.get(
            "name",
            "Customer"
        ),
        user.get(
            "email",
            ""
        ),
        review_text,
        "Website review form"
    )

    return redirect(
        url_for(
            "products_page",
            review_sent="1"
        )
    )


# ============================================================
# STAFF DASHBOARD
# ============================================================

@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect(url_for("login"))

    if session["user"].get("role") != "staff":
        return redirect(url_for("products_page"))

    current_reviews = get_reviews()
    current_orders = get_orders()

    return render_template(
        "staff_dashboard.html",
        user=session["user"],
        reviews=current_reviews,
        review_count=len(current_reviews),
        orders=current_orders,
        order_count=len(current_orders),
        pending_order_count=sum(
            1 for order in current_orders
            if order["status"] == "Pending"
        ),
        preparing_order_count=sum(
            1 for order in current_orders
            if order["status"] == "Preparing"
        ),
        ready_order_count=sum(
            1 for order in current_orders
            if order["status"] == "Ready for Pickup"
        ),
        completed_order_count=sum(
            1 for order in current_orders
            if order["status"] == "Completed"
        )
    )

# ============================================================
# CUSTOMER PROFILE
# ============================================================
@app.route("/profile")
def profile():
    """
    Display the profile of the currently logged-in customer.

    The customer can see:
    - Their name
    - Their email
    - Their previous orders

    Orders are filtered using the email stored in the
    current Flask session. This means a customer can only
    see their own orders.
    """

    # --------------------------------------------------------
    # CHECK LOGIN
    # --------------------------------------------------------

    if "user" not in session:
        return redirect(
            url_for("login")
        )


    # --------------------------------------------------------
    # GET CURRENT CUSTOMER
    # --------------------------------------------------------

    user = session["user"]

    customer_email = user.get(
        "email",
        ""
    ).strip().lower()


    # --------------------------------------------------------
    # GET CUSTOMER ORDERS
    # --------------------------------------------------------

    connection = get_db_connection()

    rows = connection.execute(
        """
        SELECT
            id,
            customer_name,
            customer_email,
            phone,
            items,
            subtotal,
            tax,
            total,
            order_type,
            pickup_date,
            pickup_time,
            payment_method,
            notes,
            status,
            created_at

        FROM orders

        WHERE LOWER(customer_email) = ?

        ORDER BY id DESC
        """,
        (customer_email,)
    ).fetchall()

    connection.close()


    # --------------------------------------------------------
    # CONVERT DATABASE ROWS INTO PYTHON DICTIONARIES
    # --------------------------------------------------------

    orders = []

    for row in rows:

        # The items are stored as JSON in the database.
        # Convert them back into a Python list.

        try:
            items = json.loads(
                row["items"]
            )

        except (
            TypeError,
            json.JSONDecodeError
        ):
            items = []


        orders.append({

            "id": row["id"],

            "customer_name":
                row["customer_name"],

            "customer_email":
                row["customer_email"],

            "phone":
                row["phone"],

            "items":
                items,

            "subtotal":
                row["subtotal"],

            "tax":
                row["tax"],

            "total":
                row["total"],

            "order_type":
                row["order_type"],

            "pickup_date":
                row["pickup_date"],

            "pickup_time":
                row["pickup_time"],

            "payment_method":
                row["payment_method"],

            "notes":
                row["notes"],

            "status":
                row["status"],

            "created_at":
                row["created_at"]
        })


    # --------------------------------------------------------
    # DISPLAY PROFILE PAGE
    # --------------------------------------------------------

    return render_template(
        "profile.html",

        user=user,

        orders=orders
    )

# ============================================================
# LOGOUT
# ============================================================

@app.route("/logout")
def logout():

    session.pop("user", None)

    return redirect(
        url_for("login")
    )


# ============================================================
# PRODUCTS PAGE
# ============================================================

@app.route("/products")
def products_page():

    if "user" not in session:

        return redirect(
            url_for("login")
        )

    return render_template(

        "products.html",

        user=session["user"],

        products=products

    )


# ============================================================
# ADD TO CART
# ============================================================

@app.route("/add-to-cart")
def add_to_cart():

    if "user" not in session:

        return redirect(
            url_for("login")
        )

    product_name = request.args.get(
        "product",
        ""
    ).strip()

    product_price = request.args.get(
        "price",
        "0"
    )

    if not product_name:

        return redirect(
            url_for("products_page")
        )

    try:

        product_price = float(
            product_price
        )

    except (
        ValueError,
        TypeError
    ):

        product_price = 0.0

    cart = session.get(
        "cart",
        []
    )

    found = False

    for item in cart:

        if item.get("name") == product_name:

            item["quantity"] = (
                int(
                    item.get(
                        "quantity",
                        1
                    )
                ) + 1
            )

            found = True

            break

    if not found:

        cart.append({

            "name": product_name,

            "price": product_price,

            "quantity": 1

        })

    session["cart"] = cart

    session.modified = True

    return redirect(
        url_for("checkout")
    )


# ============================================================
# REMOVE FROM CART
# ============================================================

@app.route("/remove-from-cart")
def remove_from_cart():

    if "user" not in session:

        return redirect(
            url_for("login")
        )

    product_name = request.args.get(
        "product",
        ""
    )

    cart = session.get(
        "cart",
        []
    )

    session["cart"] = [

        item

        for item in cart

        if item.get("name")
        != product_name

    ]

    session.modified = True

    return redirect(
        url_for("checkout")
    )


# ============================================================
# DECREASE QUANTITY
# ============================================================

@app.route("/decrease-quantity")
def decrease_quantity():

    if "user" not in session:
        return redirect(
            url_for("login")
        )

    product_name = request.args.get(
        "product",
        ""
    ).strip()

    cart = session.get(
        "cart",
        []
    )

    for item in cart:

        if item.get("name") == product_name:

            quantity = int(
                item.get(
                    "quantity",
                    1
                )
            )

            if quantity > 1:
                item["quantity"] = quantity - 1
            else:
                cart.remove(item)

            break

    session["cart"] = cart
    session.modified = True

    return redirect(
        url_for("checkout")
    )


# ============================================================
# CLEAR CART
# ============================================================

@app.route("/clear-cart")
def clear_cart():

    if "user" not in session:

        return redirect(
            url_for("login")
        )

    session["cart"] = []

    session.modified = True

    return redirect(
        url_for("checkout")
    )


# ============================================================
# PLACE ONLINE ORDER
# ============================================================

@app.route("/place-order", methods=["POST"])
def place_order():

    if "user" not in session:
        return redirect(url_for("login"))

    cart = session.get("cart", [])

    if not cart:
        return redirect(url_for("checkout"))

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    phone = request.form.get("phone", "").strip()
    order_type = request.form.get("order_type", "").strip()
    pickup_date = request.form.get("pickup_date", "").strip()
    pickup_time = request.form.get("pickup_time", "").strip()
    payment_method = request.form.get("payment", "").strip()
    notes = request.form.get("notes", "").strip()

    if not name or not email or not phone or not order_type or not payment_method:
        return redirect(url_for(
            "checkout",
            order_error="Please complete all required fields."
        ))

    if order_type != "pickup":
        return redirect(url_for(
            "checkout",
            order_error="Please select Pickup."
        ))

    if not pickup_date:
        return redirect(url_for(
            "checkout",
            order_error="Please select a pickup date."
        ))

    # The checkout page uses an HTML time picker.
    # Accept any valid time between 10:00 AM and 5:00 PM.
    if not pickup_time:
        return redirect(url_for(
            "checkout",
            order_error="Please select a pickup time."
        ))

    try:
        selected_time = datetime.strptime(
            pickup_time,
            "%H:%M"
        ).time()

        opening_time = datetime.strptime(
            "10:00",
            "%H:%M"
        ).time()

        closing_time = datetime.strptime(
            "17:00",
            "%H:%M"
        ).time()

        if not (opening_time <= selected_time <= closing_time):
            return redirect(url_for(
                "checkout",
                order_error=(
                    "Please select a pickup time between "
                    "10:00 AM and 5:00 PM."
                )
            ))

    except ValueError:
        return redirect(url_for(
            "checkout",
            order_error="Please select a valid pickup time."
        ))

    if payment_method not in ("card", "pickup"):
        return redirect(url_for(
            "checkout",
            order_error="Please select a payment method."
        ))

    if payment_method == "card":
        card_name = request.form.get("card_name", "").strip()
        card_number = request.form.get("card_number", "").strip()
        expiry = request.form.get("expiry", "").strip()
        cvv = request.form.get("cvv", "").strip()

        if not card_name or not card_number or not expiry or not cvv:
            return redirect(url_for(
                "checkout",
                order_error="Please complete the card details."
            ))

    subtotal = 0.0

    for item in cart:
        price = float(item.get("price", 0))
        quantity = int(item.get("quantity", 1))
        subtotal += price * quantity

    tax = subtotal * 0.10
    total = subtotal + tax

    order_id = save_order(
        name,
        email,
        phone,
        cart,
        subtotal,
        tax,
        total,
        order_type,
        pickup_date,
        pickup_time,
        payment_method,
        notes
    )

    session["cart"] = []
    session.modified = True

    return redirect(url_for(
        "order_confirmation",
        order_id=order_id
    ))


@app.route("/order-confirmation/<int:order_id>")
def order_confirmation(order_id):

    if "user" not in session:
        return redirect(url_for("login"))

    connection = get_db_connection()

    row = connection.execute(
        """
        SELECT *
        FROM orders
        WHERE id = ?
        """,
        (order_id,)
    ).fetchone()

    connection.close()

    if not row:
        return redirect(url_for("products_page"))

    if row["customer_email"] != session["user"].get("email"):
        return redirect(url_for("products_page"))

    try:
        items = json.loads(row["items"])
    except (TypeError, json.JSONDecodeError):
        items = []

    order = dict(row)
    order["items"] = items

    return render_template(
        "order_confirmation.html",
        order=order
    )


# ============================================================
# UPDATE ORDER STATUS
# ============================================================

@app.route("/update-order-status/<int:order_id>", methods=["POST"])
def update_order_status(order_id):

    if "user" not in session:
        return redirect(url_for("login"))

    if session["user"].get("role") != "staff":
        return redirect(url_for("products_page"))

    allowed_statuses = {
        "Pending",
        "Preparing",
        "Ready for Pickup",
        "Completed",
        "Cancelled"
    }

    new_status = request.form.get("status", "").strip()

    if new_status not in allowed_statuses:
        return redirect(url_for("dashboard"))

    connection = get_db_connection()

    connection.execute(
        """
        UPDATE orders
        SET status = ?
        WHERE id = ?
        """,
        (new_status, order_id)
    )

    connection.commit()
    connection.close()

    return redirect(url_for("dashboard"))


# ============================================================
# CHECKOUT
# ============================================================

@app.route("/checkout")
@app.route("/checkout.html")
def checkout():

    if "user" not in session:

        return redirect(
            url_for("login")
        )

    cart = session.get(
        "cart",
        []
    )

    subtotal = 0.0

    for item in cart:

        price = float(
            item.get(
                "price",
                0
            )
        )

        quantity = int(
            item.get(
                "quantity",
                1
            )
        )

        subtotal += (
            price * quantity
        )

    tax = subtotal * 0.10

    total = subtotal + tax

    return render_template(

        "checkout.html",

        user=session["user"],

        cart=cart,

        subtotal=subtotal,

        tax=tax,

        total=total

    )


# ============================================================
# CAKE ENQUIRY
# ============================================================

@app.route(
    "/cake-enquiry",
    methods=["POST"]
)
def cake_enquiry():

    if "user" not in session:

        return redirect(
            url_for("login")
        )

    name = request.form.get(
        "name",
        ""
    ).strip()

    email = request.form.get(
        "email",
        ""
    ).strip()

    cake_type = request.form.get(
        "cake_type",
        ""
    ).strip()

    if (
        not name
        or not email
        or not cake_type
    ):

        return render_template(

            "products.html",

            user=session["user"],

            products=products,

            enquiry_error=(
                "Please complete the required fields."
            )

        )

    return render_template(

        "products.html",

        user=session["user"],

        products=products,

        enquiry_success=(
            "Thank you! Your cake enquiry "
            "has been received. Goodwood "
            "Bake Shop will contact you."
        )

    )


# ============================================================
# FREE LOCAL CHATBOT
# ============================================================

def chatbot_reply(message):

    # --------------------------------------------------------
    # CLEAN MESSAGE
    # --------------------------------------------------------

    text = message.lower().strip()

    clean_text = re.sub(
        r"[^\w\s$]",
        " ",
        text
    )

    clean_text = re.sub(
        r"\s+",
        " ",
        clean_text
    ).strip()


    # ========================================================
    # REVIEW / FEEDBACK FROM CHATBOT
    # ========================================================

    user = session.get(
        "user",
        {}
    )

    # If the chatbot has asked the customer to enter a review,
    # save the next message as the review.
    if session.get("awaiting_review"):

        save_review(
            user.get(
                "name",
                "Customer"
            ),
            user.get(
                "email",
                ""
            ),
            message,
            "Chatbot"
        )

        session["awaiting_review"] = False
        session.modified = True

        return (
            "Thank you for your review! "
            "Your feedback has been sent to our staff."
        )


    # A customer can start the review process in the chatbot.
    review_request_phrases = [
        "leave a review",
        "write a review",
        "give a review",
        "send a review",
        "leave feedback",
        "give feedback",
        "send feedback",
        "customer feedback"
    ]

    if any(
        phrase in clean_text
        for phrase in review_request_phrases
    ):

        session["awaiting_review"] = True
        session.modified = True

        return (
            "Of course! Please type your review or feedback "
            "in your next message. I will send it to our staff."
        )


    # If the customer explicitly starts a message with
    # "review:" or "feedback:", save it immediately.
    if (
        clean_text.startswith("review ")
        or clean_text.startswith("review:")
        or clean_text.startswith("feedback ")
        or clean_text.startswith("feedback:")
    ):

        save_review(
            user.get(
                "name",
                "Customer"
            ),
            user.get(
                "email",
                ""
            ),
            message,
            "Chatbot"
        )

        return (
            "Thank you for your review! "
            "Your feedback has been sent to our staff."
        )


    # ========================================================
    # GREETINGS
    # ========================================================

    greetings = [

        "hi",
        "hello",
        "hey",
        "good morning",
        "good afternoon",
        "good evening"

    ]

    if clean_text in greetings:

        return (
            "Hello! Welcome to Goodwood Bake Shop. "
            "How can I help you today?"
        )


    if (
        "hello" in clean_text
        or "hi there" in clean_text
        or "hey there" in clean_text
    ):

        return (
            "Hello! Welcome to Goodwood Bake Shop. "
            "How can I help you today?"
        )


    # ========================================================
    # THANK YOU
    # ========================================================

    if (
        "thank you" in clean_text
        or "thanks" in clean_text
        or "thank u" in clean_text
    ):

        return (
            "You're welcome! "
            "Please let me know if you need anything else."
        )


    # ========================================================
    # GOODBYE
    # ========================================================

    if (
        "bye" in clean_text
        or "goodbye" in clean_text
    ):

        return (
            "Goodbye! Thank you for visiting "
            "Goodwood Bake Shop."
        )


    # ========================================================
    # OPENING HOURS
    # ========================================================

    opening_hours_questions = [

        "opening hours",
        "opening hour",
        "opening time",
        "open today",
        "open tomorrow",
        "when are you open",
        "when do you open",
        "when are you opening",
        "what time do you open",
        "what time you open",
        "what time are you open",
        "what time does the bakery open",
        "what time does goodwood bake shop open",
        "what time does goodwood open",
        "what time do you close",
        "what time you close",
        "when do you close",
        "when are you closing",
        "closing time",
        "close time",
        "business hours",
        "trading hours",
        "store hours",
        "shop hours",
        "bakery hours",
        "are you open",
        "is the bakery open",
        "is goodwood bake shop open",
        "what are your hours",
        "what hours are you open",
        "tell me your opening hours"

    ]


    if any(
        question in clean_text
        for question in opening_hours_questions
    ):

        return (
            "We are open from 7:00 AM to 2:00 PM "
            "Thursday to Sunday. "
            "Please call Goodwood Bake Shop on "
            "0420543837 if you have any queries"
        )


    # ========================================================
    # LOCATION
    # ========================================================

    if (
        "direction" in clean_text
        or "directions" in clean_text
        or "how do i get there" in clean_text
        or "how to get there" in clean_text
        or "how can i get there" in clean_text
        or "where are you" in clean_text
        or "where is the bakery" in clean_text
        or "where is goodwood" in clean_text
        or "where are you located" in clean_text
        or "where is your shop" in clean_text
        or "where is your bakery" in clean_text
        or "location" in clean_text
        or "address" in clean_text
        or "located" in clean_text
    ):

        return (
            "📍 Goodwood Bakeshop is located at "
            "297 Marrickville Rd, Marrickville NSW 2204.\n\n"
            "🗺️ Open Google Maps Directions:\n"
            "https://www.google.com/maps/dir/?api=1&destination="
            "297+Marrickville+Rd+Marrickville+NSW+2204"
        )


    # ========================================================
    # PHONE / CONTACT
    # ========================================================

    if (
        "phone" in clean_text
        or "telephone" in clean_text
        or "phone number" in clean_text
        or "contact number" in clean_text
        or "call you" in clean_text
        or "how can i contact" in clean_text
    ):

        return (
            "You can contact Goodwood Bake Shop "
            "on 0420543837."
        )


    if "contact" in clean_text:

        return (
            "You can contact Goodwood Bake Shop "
            "on 0420543837 or visit us at "
            "297 Marrickville Rd,Marrickville NSW 2204"
        )


    # ========================================================
    # DIETARY INFORMATION
    # ========================================================

    def _format_dietary(p):
        return (
            "{name} ({category}, ${price}): Gluten-Free {gf}, "
            "Dairy-Free {df}, Nut-Free {nf}."
        ).format(
            name=p["name"], category=p["category"], price=p["price"],
            gf=p["gluten_free"], df=p["dairy_free"], nf=p["nut_free"]
        )

    def _format_price(p):
        return "{name} ${price}".format(name=p["name"], price=p["price"])

    asking_dietary = (
        "gluten" in clean_text
        or "dairy" in clean_text
        or "nut" in clean_text
        or "allergen" in clean_text
    )

    if asking_dietary:

        named_matches = [p for p in products if p["name"].lower() in clean_text]

        if named_matches:
            return " ".join(_format_dietary(p) for p in named_matches)

        gluten_free_items = [p["name"] for p in products if p["gluten_free"] == "Yes"]
        dairy_free_items = [p["name"] for p in products if p["dairy_free"] == "Yes"]
        nut_free_items = [p["name"] for p in products if p["nut_free"] == "Yes"]

        if "gluten" in clean_text:
            if gluten_free_items:
                return "Gluten-free options: " + ", ".join(gluten_free_items) + "."
            return (
                "None of our current menu items are gluten-free. "
                "Please contact Goodwood Bake Shop if this is important "
                "for your dietary needs."
            )

        if "dairy" in clean_text:
            if dairy_free_items:
                return "Dairy-free options: " + ", ".join(dairy_free_items) + "."
            return (
                "None of our current menu items are dairy-free. "
                "Please contact Goodwood Bake Shop if this is important "
                "for your dietary needs."
            )

        if nut_free_items:
            return "Nut-free options: " + ", ".join(nut_free_items) + "."
        return (
            "None of our current menu items are nut-free. "
            "Please contact Goodwood Bake Shop if this is important "
            "for your dietary needs."
        )


    # ========================================================
    # PRODUCTS / MENU
    # ========================================================

    if (
        "products" in clean_text
        or "menu" in clean_text
        or "what do you sell" in clean_text
        or "what do you have" in clean_text
        or "what can i buy" in clean_text
        or "what can i order" in clean_text
        or "what food do you have" in clean_text
    ):

        categories = []
        for p in products:
            if p["category"] not in categories:
                categories.append(p["category"])

        summary_parts = []
        for cat in categories:
            items = [p["name"] for p in products if p["category"] == cat]
            summary_parts.append(cat + ": " + ", ".join(items))

        return (
            "Here is our full menu. " + " | ".join(summary_parts) + ". "
            "You can also ask me about gluten-free, dairy-free, "
            "and nut-free information, or the price of any item."
        )


    # ========================================================
    # CUPCAKES
    # ========================================================

    if "cupcake" in clean_text or "cupcakes" in clean_text:

        named = [p for p in products if p["category"] == "Cupcakes" and p["name"].lower() in clean_text]
        matches = named if named else [p for p in products if p["category"] == "Cupcakes"]

        return "Our cupcakes: " + ", ".join(_format_price(p) for p in matches) + "."


    # ========================================================
    # PASTRIES / CROISSANTS
    # ========================================================

    if (
        "croissant" in clean_text
        or "croissants" in clean_text
        or "pastry" in clean_text
        or "pastries" in clean_text
        or "danish" in clean_text
    ):

        named = [p for p in products if p["category"] == "Pastry" and p["name"].lower() in clean_text]
        matches = named if named else [p for p in products if p["category"] == "Pastry"]

        return "Our pastries: " + ", ".join(_format_price(p) for p in matches) + "."


    # ========================================================
    # COOKIES
    # ========================================================

    if "cookie" in clean_text or "cookies" in clean_text:

        named = [p for p in products if p["category"] == "Cookies" and p["name"].lower() in clean_text]
        matches = named if named else [p for p in products if p["category"] == "Cookies"]

        return "Our cookies: " + ", ".join(_format_price(p) for p in matches) + "."


    # ========================================================
    # CUSTOM CAKES
    # ========================================================

    if (
        "custom cake" in clean_text
        or "custom cakes" in clean_text
        or "birthday cake" in clean_text
        or "special cake" in clean_text
        or "order a cake" in clean_text
        or "cake enquiry" in clean_text
    ):

        return (
            "Yes, you can make a custom cake enquiry. "
            "Please use the cake enquiry form on "
            "the Products page. Goodwood Bake Shop "
            "will contact you about your enquiry."
        )


    # ========================================================
    # CAKES
    # ========================================================

    if "cake" in clean_text:

        named = [p for p in products if p["category"] == "Cake" and p["name"].lower() in clean_text]
        matches = named if named else [p for p in products if p["category"] == "Cake"]

        return (
            "Our cakes: " + ", ".join(_format_price(p) for p in matches) + ". "
            "For something bespoke, please use the cake enquiry "
            "form on the Products page."
        )


    # ========================================================
    # PRICE
    # ========================================================

    if (
        "price" in clean_text
        or "prices" in clean_text
        or "cost" in clean_text
        or "how much" in clean_text
        or "how much is" in clean_text
    ):

        named = [p for p in products if p["name"].lower() in clean_text]
        matches = named if named else products

        return "Our prices: " + ", ".join(_format_price(p) for p in matches) + "."


    # ========================================================
    # ORDER
    # ========================================================

    if (
        "order" in clean_text
        or "buy" in clean_text
        or "purchase" in clean_text
    ):

        return (
            "You can browse our products on the "
            "Products page and select Add to Cart. "
            "You can then review your order at checkout."
        )


    # ========================================================
    # CART
    # ========================================================

    if "cart" in clean_text:

        return (
            "You can add products to your cart by "
            "selecting Add to Cart. Your cart can "
            "then be reviewed at checkout."
        )


    # ========================================================
    # HELP
    # ========================================================

    if (
        "help" in clean_text
        or "how can you help" in clean_text
        or "what can you help me with" in clean_text
    ):

        return (
            "I can help you with products, prices, "
            "custom cakes, orders, contact details, "
            "opening hours, bakery location, and "
            "dietary information."
        )


    # ========================================================
    # FALLBACK
    # ========================================================

    return (
        "I'm here to help with Goodwood Bake Shop. "
        "You can ask me about our products, prices, "
        "custom cakes, opening hours, location, "
        "phone number, dietary information, "
        "or placing an order."
    )


# ============================================================
# CHATBOT REVIEW FORM
# ============================================================

@app.route("/submit-chatbot-review", methods=["POST"])
def submit_chatbot_review():

    if "user" not in session:
        return jsonify({
            "error": "Please log in before leaving a review."
        }), 401

    data = request.get_json(silent=True) or {}

    review_text = data.get("review", "")

    if not isinstance(review_text, str):
        review_text = str(review_text)

    review_text = review_text.strip()

    if not review_text:
        return jsonify({
            "error": "Please leave a review before sending."
        }), 400

    user = session["user"]

    save_review(
        user.get("name", "Customer"),
        user.get("email", ""),
        review_text,
        "Chatbot"
    )

    session["awaiting_review"] = False
    session.modified = True

    return jsonify({
        "message": "Thank you! Your review has been sent to our staff."
    }), 200


# ============================================================
# CHAT ROUTE
# ============================================================

@app.route(
    "/chat",
    methods=["POST"]
)
def chat():

    print(
        "CHAT ROUTE CALLED",
        flush=True
    )

    # --------------------------------------------------------
    # CHECK LOGIN
    # --------------------------------------------------------

    if "user" not in session:

        print(
            "CHAT ERROR: User is not logged in",
            flush=True
        )

        return jsonify({

            "reply":
            "Please log in before using the chatbot."

        }), 401


    # --------------------------------------------------------
    # READ REQUEST
    # --------------------------------------------------------

    data = request.get_json(
        silent=True
    ) or {}


    message = data.get(
        "message",
        ""
    )


    if not isinstance(
        message,
        str
    ):

        message = str(message)


    message = message.strip()


    print(
        "CHAT MESSAGE:",
        repr(message),
        flush=True
    )


    # --------------------------------------------------------
    # EMPTY MESSAGE
    # --------------------------------------------------------

    if not message:

        return jsonify({

            "reply":
            "Please type a question."

        }), 200


    # --------------------------------------------------------
    # GENERATE FREE LOCAL RESPONSE
    # --------------------------------------------------------

    try:

        reply = chatbot_reply(
            message
        )

        print(
            "CHATBOT REPLY:",
            repr(reply),
            flush=True
        )

        return jsonify({

            "reply": reply

        }), 200


    except Exception as e:

        print(
            "CHATBOT ERROR:",
            repr(e),
            flush=True
        )

        return jsonify({

            "reply":
            "Sorry, I could not process that question. "
            "Please try again."

        }), 200


# ============================================================
# 404 ERROR
# ============================================================

@app.errorhandler(404)
def page_not_found(error):

    return """

    <h1>Page Not Found</h1>

    <p>
        The page you are looking for
        does not exist.
    </p>

    <p>
        <a href="/login">
            Go to Login
        </a>
    </p>

    """, 404


# ============================================================
# 500 ERROR
# ============================================================

@app.errorhandler(500)
def internal_error(error):

    return """

    <h1>Something went wrong</h1>

    <p>
        Please try again.
    </p>

    <p>
        <a href="/login">
            Go to Login
        </a>
    </p>

    """, 500


# # ============================================================
# # START APPLICATION
# # ============================================================

# if __name__ == "__main__":

#     print("=" * 55)

#     print(
#         "GOODWOOD BAKE SHOP"
#     )

#     print("=" * 55)

#     print(
#         "FREE LOCAL CHATBOT: ENABLED"
#     )

#     print(
#         "OPENAI API: NOT REQUIRED"
#     )

#     print(
#         "Website: http://127.0.0.1:5000"
#     )

#     print("=" * 55)

#     app.run(

#         debug=False,

#         host="127.0.0.1",

#         port=5000

#     )
# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    print("=" * 55)
    print("GOODWOOD BAKE SHOP")
    print("=" * 55)

    print("FREE LOCAL CHATBOT: ENABLED")
    print("OPENAI API: NOT REQUIRED")

    print("Website: http://0.0.0.0:5001")

    print("=" * 55)

    app.run(
        debug=False,
        host="0.0.0.0",
        port=port
    )