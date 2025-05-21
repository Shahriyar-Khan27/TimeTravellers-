from flask import Flask, render_template, request, url_for, redirect, make_response, session, flash, jsonify
import pymongo
from pymongo import MongoClient
import requests
import stripe
from werkzeug.utils import secure_filename
import chat_bot
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from bson.objectid import ObjectId

app = Flask(__name__)
CORS(app)
app.secret_key = "flash message"
app.config['SECRET_KEY'] = 'DECORATORS'

# MongoDB connection
client = MongoClient('mongodb://localhost:27017')
db = client['SKBookings']  # database name

# Initialize admin account on startup
def initialize_admin():
    admin_exists = db.admin_account.find_one({"email": "admin@example.com"})
    if not admin_exists:
        admin_data = {
            "email": "admin@example.com",
            "password": generate_password_hash("admin123")
        }
        db.admin_account.insert_one(admin_data)
        print("Default admin account created: admin@example.com / admin123")

# Call it directly
initialize_admin()

@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/offers")
def offers():
    return render_template("offers.html")

@app.route("/aboutus")
def aboutus():
    return render_template("about.html")

@app.route("/contactus")
def contactus():
    return render_template("contactus.html")

@app.route("/Bus", methods=["GET", "POST"])
def bus():
    if request.method == "GET":
        return render_template("Bus.html")
    else:
        bus_data = {
            "From": request.form["From"],
            "To": request.form["To"],
            "Date": request.form["date"]
        }
        db.busdata.insert_one(bus_data)
        return redirect("ShowProducts/1")

@app.route("/seatbooking", methods=["GET", "POST"])
def seatbooking():
    if request.method == "GET":
        return render_template("seatbooking.html")
    else:
        seatno = request.form.getlist("A")
        seat_str = ''.join(seatno)
        db.seatbook.insert_one({"seatno": seat_str})
        return redirect("ViewDetails/1")

@app.route("/Trains", methods=["GET", "POST"])
def train():
    if request.method == "GET":
        return render_template("Trains.html")
    else:
        train_data = {
            "From": request.form["From"],
            "To": request.form["To"],
            "Date": request.form["date"],
            "Classes": request.form["classes"]
        }
        db.traindata.insert_one(train_data)
        return redirect("ShowProducts/2")

@app.route("/Flights", methods=["GET", "POST"])
def flights():
    if request.method == "GET":
        return render_template("Flights.html")
    else:
        flight_data = {
            "From": request.form["from"],
            "To": request.form["to"],
            "DepatureDate": request.form["date1"],
            "ReturnDate": request.form["date2"],
            "Travellers": request.form["travellers"],
            "Class": request.form["class"]
        }
        db.flightdata.insert_one(flight_data)
        return redirect("ShowProducts/3")

@app.route("/Hotels", methods=["GET", "POST"])
def hotels():
    if request.method == "GET":
        return render_template("Hotels.html")
    else:
        hotel_data = {
            "Destination": request.form["destination"],
            "CheckIn": request.form["date1"],
            "CheckOut": request.form["date2"],
            "Rooms": request.form["rooms"],
            "Adults": request.form["adults"],
            "Children": request.form["children"]
        }
        db.hoteldata.insert_one(hotel_data)
        return redirect("ShowProducts/4")

@app.route("/cookies", methods=["GET", "POST"])
def cookieDemo():
    if request.method == "GET":
        return render_template("cookie.html")
    else:
        fname = request.form["email"]
        lname = request.form["pwd"]
        uname = fname + " " + lname
        resp = make_response(render_template("cookie.html"))
        resp.set_cookie("uname", uname,
                    expires=datetime.datetime.now() + datetime.timedelta(days=30))
        return resp

@app.route("/ShowCookie")
def displayCookie():
    uname = request.cookies["uname"]
    return "Hello " + uname

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login/login.html")
    else:
        email = request.form["email"]
        password = request.form["password"]
        
        user = db.account.find_one({"email": email})
        
        if user and user["password"] == password:
            session["login"] = True
            session["username"] = user["username"]
            flash("Logged in successfully!", "success")
            return redirect(url_for('home'))
        else:
            session["login"] = False
            session["username"] = ''
            flash("Invalid email or password!", "danger")
            return redirect(url_for('login'))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("/login/register.html")
    else:
        user_data = {
            "username": request.form["username"],
            "email": request.form["email"],
            "MobileNumber": request.form["MobileNumber"],
            "sex": request.form["sex"],
            "password": request.form["password"]
        }
        db.account.insert_one(user_data)
        flash("Registered Successfully", "success")
        return redirect(url_for("login"))

@app.route("/adlogin", methods=["GET", "POST"])
def adlogin():
    if request.method == "GET":
        return render_template("/admin/adlogin.html")
    else:
        username = request.form["username"]
        password = request.form["password"]
        
        admin = db.admin_account.find_one({"email": username})
        
        if admin and check_password_hash(admin["password"], password):
            session["adlogin"] = True
            session["username"] = username
            flash("Admin logged in Successfully", "success")
            return redirect(url_for('home'))
        else:
            flash("Invalid Admin username or password!", "danger")
            return redirect(url_for('adlogin'))

@app.route("/Users")
def Users():
    users = list(db.account.find())
    return render_template("/admin/Users.html", users=users)

@app.route("/RemoveUser/<Email>", methods=["GET", "POST"])
def RemoveUser(Email):
    if request.method == "GET":
        return render_template("/admin/RemoveUser.html")
    else:
        action = request.form["action"]
        if action == "Yes":
            db.account.delete_one({"Email": Email})
            flash("User Deleted Successfully", 'success')
        return redirect(url_for("Users"))

@app.route("/adlogout")
def adlogout():
    session["adlogin"] = False
    flash("Admin Logged out Successfully!!", "success")
    return redirect(url_for("home"))

@app.route("/logout")
def logout():
    session["login"] = False
    session['Bookings'] = {}
    session.clear()
    flash("User Logged out Successfully!!", "success")
    return redirect(url_for("home"))

# @app.route("/")
# def main():
#     categories = list(db.category.find())
#     session["cats"] = categories
#     return render_template("index.html")

@app.route("/Categories")
def showAllCategories():
    categories = list(db.category.find())
    return render_template("/admin/category.html", cats=categories)

@app.route("/AddNewCategory", methods=["GET", "POST"])
def AddNewDept():
    if request.method == "GET":
        return render_template("/admin/AddCategory.html")
    else:
        cname = request.form["cname"]
        db.category.insert_one({"cname": cname})
        flash("New Category Inserted Successfully", 'success')
        return redirect(url_for("showAllCategories"))

@app.route("/AddCategory", methods=["GET", "POST"])
def AddCategory():
    if request.method == "GET":
        return render_template("/admin/AddCategory.html")
    else:
        db.category.insert_one({"cname": request.form["cname"]})
        flash("New Category Inserted Successfully", 'success')
        return redirect(url_for("Category"))

@app.route("/EditCategory/<id>", methods=["GET", "POST"])
def EditCategory(id):
    if request.method == "GET":
        category = db.category.find_one({"_id": pymongo.ObjectId(id)})
        flash("Category Updated Successfully")
        return render_template("/admin/EditCategory.html", cat=category)
    else:
        db.category.update_one(
            {"_id": pymongo.ObjectId(id)},
            {"$set": {"cname": request.form["cname"]}}
        )
        return redirect(url_for("Category"))

@app.route("/DeleteCategory/<id>", methods=["GET", "POST"])
def DeleteCategory(id):
    if request.method == "GET":
        return render_template("/admin/DeleteCategory.html")
    else:
        action = request.form["action"]
        if action == "Yes":
            db.category.delete_one({"_id": pymongo.ObjectId(id)})
            flash("Category Deleted Successfully", 'success')
        return redirect(url_for("Category"))

@app.route("/Category")
def Category():
    categories = list(db.category.find())
    return render_template("/admin/Categories.html", cats=categories)

@app.route("/Products")
def showAllProducts():
    # MongoDB aggregation to join product and category collections
    pipeline = [
        {
            "$lookup": {
                "from": "category",
                "localField": "cid",
                "foreignField": "_id",
                "as": "category"
            }
        },
        {
            "$unwind": "$category"
        },
        {
            "$project": {
                "pid": "$_id",
                "pname": 1,
                "price": 1,
                "imageurl": 1,
                "cname": "$category.cname"
            }
        }
    ]
    products = list(db.product.aggregate(pipeline))
    return render_template("/admin/Products.html", prds=products)

@app.route("/EditProduct/<id>", methods=["GET", "POST"])
def EditProduct(id):
    if request.method == "GET":
        product = db.product.find_one({"_id": pymongo.ObjectId(id)})
        flash("Product Updated Successfully", 'success')
        return render_template("admin/EditProduct.html", prd=product)
    else:
        db.product.update_one(
            {"_id": pymongo.ObjectId(id)},
            {"$set": {"pname": request.form["pname"]}}
        )
        return redirect(url_for("showAllProducts"))

@app.route("/DeleteProduct/<id>", methods=["GET", "POST"])
def DeleteProduct(id):
    if request.method == "GET":
        return render_template("/admin/DeleteProduct.html")
    else:
        action = request.form["action"]
        if action == "Yes":
            db.product.delete_one({"_id": pymongo.ObjectId(id)})
            flash("Product Deleted Successfully", 'success')
        return redirect(url_for("showAllProducts"))

@app.route("/AddProduct", methods=["GET", "POST"])
def AddProduct():
    if request.method == "GET":
        categories = list(db.category.find())
        return render_template("/admin/AddNewProduct.html", cats=categories)
    else:
        cname = request.form["cname"]
        price = request.form["price"]
        catid = pymongo.ObjectId(request.form["catid"])
        
        f = request.files['image']
        f.save("static\\Images\\" + secure_filename(f.filename))
        
        product_data = {
            "pname": cname,
            "price": price,
            "imageurl": f.filename,
            "cid": catid
        }
        db.product.insert_one(product_data)
        flash("New Product Inserted Successfully", 'success')
        return redirect(url_for("showAllProducts"))

@app.route("/ViewDetails/<id>")
def ViewDetails(id):
    product = db.product.find_one({"_id": pymongo.ObjectId(id)})
    return render_template("/user/ViewDetails.html", prd=product)

@app.route("/ShowProducts/<id>")
def ShowProducts(id):
    products = list(db.product.find(
        {"cid": pymongo.ObjectId(id)}, 
        {"pid": "$_id", "pname": 1, "price": 1}
    ))
    return render_template("/user/ShowProducts.html", prds=products)

@app.route("/AddToCart", methods=["GET", "POST"])
def AddToCart():
    if request.method == "POST":
        pid = request.form["pid"]
        pname = request.form["pname"]
        price = request.form["price"]
        qty = request.form["qty"]
        item = [pid, pname, price, qty]
        
        if "MyBooking" not in session:
            Bookings = {}
        else:
            Bookings = session["MyBooking"]
            
        Bookings[pid] = item
        session["MyBooking"] = Bookings
        return redirect("/")

@app.route("/ShowAllCartItems")
def ShowAllCartItems():
    if "MyBooking" not in session:
        return "No items in MyBooking"
    else:
        total = 0
        for prd in session["MyBooking"].values():
            total = total + float(prd[2]) * float(prd[3])
        session["total"] = total
        return render_template("/user/ShowAllCartItems.html")

@app.route("/RemoveFromCart", methods=["GET", "POST"])
def RemoveFromCart():
    if request.method == "POST":
        pid = str(request.form["pid"])
        Bookings = session["MyBooking"]
        del Bookings[pid]
        session["MyBooking"] = Bookings
        return redirect("ShowAllCartItems")

@app.route("/MakePayment", methods=["GET", "POST"])
def MakePayment():
    if request.method == "GET":
        return render_template("/user/MakePayment.html")
    else:
        cardno = request.form["cardno"]
        cvv = request.form["cvv"]
        expiry = request.form["expiry"]
        
        payment = db.payment.find_one({
            "cardno": cardno,
            "cvv": cvv,
            "expiry": expiry
        })
        
        if payment:
            flash("Payment done Successfully", 'success')
            # Update sender's amount
            db.payment.update_one(
                {"cardno": cardno},
                {"$inc": {"amount": -session["total"]}}
            )
            # Update receiver's amount (admin account)
            db.payment.update_one(
                {"cardno": "222"},
                {"$inc": {"amount": session["total"]}}
            )
            return redirect("/")
        else:
            flash("Invalid credentials", 'danger')
            return redirect("/MakePayment")

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/chat", methods=["GET"])
def ChatWithLLM():
    return render_template('chat.html')
        
@app.route("/chat/query", methods=["POST"])
def Chatwithllmnow():
    data = request.json["ques"]
    ans = chat_bot.ChatWIthLLM(data)
    return jsonify({"answer": ans})

# Sample data routes
@app.route("/ShowProducts/1", methods=["POST"])
def show_products_bus():
    products = [
        (1, 'Bus A', 100),
        (2, 'Bus B', 200),
        (3, 'Bus C', 300),
    ]
    return render_template('/user/ShowProducts.html', prds=products)

@app.route("/ShowProducts/2", methods=["POST"])
def show_products_train():
    products = [
        (1, 'Kisan Express', 200),
        (2, 'Gorakhdham Express', 200),
        (3, 'Kalindi Express', 300),
    ]
    return render_template('/user/ShowProducts.html', prds=products)

@app.route("/ShowProducts/3", methods=["POST"])
def show_products_flight():
    products = [
        (1, 'Indigo', 2000),
        (2, 'Spice jet', 4000),
        (3, 'Air India', 10000),
    ]
    return render_template('/user/ShowProducts.html', prds=products)

@app.route("/ShowProducts/4", methods=["POST"])
def show_products_hotels():
    products = [
        (1, 'Noor Mahal, Karnal', 4000),
        (2, 'HSB Grand, Bhiwani', 5500),
        (3, 'Baya Guest house, Bhiwani', 10499),
    ]
    return render_template('/user/ShowProducts.html', prds=products)

@app.route('/ViewDetails/1')
def seats():
    seat_data = {
        'pid': 1,
        'pname': 'Sample Product',
        'price': 100,
        'details': 'This is a sample product description.',
    }
    return render_template('/user/ViewDetails.html', prd=seat_data)

@app.route("/add-cake", methods=["GET", "POST"])
def add_cake():
    if request.method == "POST":
        amount = int(session.get("total", 100))
        
        intent = stripe.PaymentIntent.create(
            amount=amount * 100,
            currency="usd",
            payment_method_types=["card"]
        )

        return render_template("confirm_payment.html", client_secret=intent.client_secret)

    return render_template("add_cake.html")

if __name__ == "__main__":
    app.run(debug=True)

    #Email: admin@example.com
 #Password: admin123