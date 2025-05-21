from flask import Flask,render_template,request,url_for,redirect,make_response,session,url_for,flash,jsonify
import mysql.connector
import requests
# from werkzeug import secure_filename
from werkzeug.utils import secure_filename
import chat_bot


import datetime

app = Flask(__name__)
app.secret_key = "flash message"
app.config['SECRET_KEY'] = 'DECORATORS'

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

@app.route("/Bus",methods=["GET","POST"])
def bus():
    if(request.method=="GET"):
        return render_template("Bus.html")
    else:
        From = request.form["From"]
        To = request.form["To"]
        Date = request.form["date"]
        con = mysql.connector.connect(host="localhost",user="root",passwd="Shradha720@",database="deepak")    
        try:       
            mycursor = con.cursor()
            sql = "insert into busdata values (%s,%s,%s)"
            val = (From,To,Date)
            mycursor.execute(sql,val)
            return redirect("ShowProducts/1")
        finally:
            con.close()

@app.route("/seatbooking",methods=["GET","POST"])
def seatbooking():
    if(request.method=="GET"):
        return render_template("seatbooking.html")
    else:
        con = mysql.connector.connect(host="localhost",user="root",passwd="Shradha720@",database="deepak") 
        try:
            mycursor = con.cursor()
            seatno = request.form.getlist["A"]
            size=len(seatno)
            for i in size:
                str=seatno[i]+''+str

            sql = "insert into seatbook (seatno) values (%s)"
            val = (str)
            mycursor.execute(sql,val)
            return redirect("ViewDetails/1")
        finally:
            con.close()


@app.route("/Trains",methods=["GET","POST"])
def train():
    if (request.method=="GET"):
        return render_template("Trains.html")
    else:
        From = request.form["From"]
        To = request.form["To"]
        Date = request.form["date"] 
        Classes = request.form["classes"]
        con = mysql.connector.connect(host="localhost",user="root",passwd="Shradha720@",database="deepak")
        try:
            mycursor = con.cursor()
            sql = "insert into traindata values (%s,%s,%s,%s)"
            val = (From,To,Date,Classes)
            mycursor.execute(sql,val)
            return redirect("ShowProducts/2")
        finally:
            con.close()

@app.route("/Flights",methods=["GET","POST"])
def flights():
    if (request.method=="GET"):
        return render_template("Flights.html")
    else:
        From = request.form["from"]
        To = request.form["to"]
        DepatureDate = request.form["date1"] 
        ReturnDate = request.form["date2"]
        Travellers = request.form["travellers"]
        Class = request.form["class"]
        con = mysql.connector.connect(host="localhost",user="root",passwd="Shradha720@",database="deepak")
        try:
            mycursor = con.cursor()
            sql = "insert into flightdata values (%s,%s,%s,%s,%s,%s)"
            val = (From,To,DepatureDate,ReturnDate,Travellers,Class)
            mycursor.execute(sql,val)
            return redirect("ShowProducts/3")
        finally:
            
            con.close()

@app.route("/Hotels",methods=["GET","POST"])
def hotels():
    if (request.method=="GET"):
        return render_template("Hotels.html")
    else:
        Destination = request.form["destination"]
        CheckIn = request.form["date1"]
        CheckOut = request.form["date2"] 
        Rooms = request.form["rooms"]
        Adults = request.form["adults"]
        Children = request.form["children"]
        con = mysql.connector.connect(host="localhost",user="root",passwd="Shradha720@",database="deepak")
        try:
            mycursor = con.cursor()
            sql = "insert into hoteldata values (%s,%s,%s,%s,%s,%s)"
            val = (Destination,CheckIn,CheckOut,Rooms,Adults,Children)
            mycursor.execute(sql,val)
            return redirect("ShowProducts/4")
        finally:
            con.close()


@app.route("/cookies",methods=["GET","POST"])
def cookieDemo():
    if(request.method=="GET"):
        return render_template("cookie.html")
    else:
        fname = request.form["email"]
        lname = request.form["pwd"]
        uname = fname+" "+lname 
        resp = make_response(render_template("cookie.html"))
        resp.set_cookie("uname", uname,
                    expires=datetime.datetime.now() + datetime.timedelta(days=30))
        return resp


@app.route("/ShowCookie")
def displayCookie():
    uname = request.cookies["uname"]
    return "Hello "+uname


@app.route("/login", methods = ["GET","POST"])
def login():
    if(request.method=="GET"):
        return render_template("/login/login.html")
    else:
        username = request.form["username"]
        password = request.form["password"]
        con = mysql.connector.connect(host="localhost",user="root",passwd="Shradha720@",database="deepak")
        try:
            mycursor = con.cursor()
            mycursor.execute(f"SELECT password,username FROM account where email = '{username}'")
            myresult = mycursor.fetchone()
            if(myresult[0]==password):
                session["login"] = True
                session["username"] = myresult[0]
                session["user"]=myresult[1]
                flash("logged in Successfully!!","success")
                return redirect(url_for('home'))                  
            else:
                session["login"] = False
                session["username"] = ''
                flash("invalid username or password!!","danger")
                return redirect(url_for('login'))
        
        finally:
            con.close()


@app.route("/register",methods=["GET","POST"])
def register():
    if(request.method=="GET"):
        return render_template("/login/register.html")
    else:
        username = request.form["username"]
        email = request.form["email"]   
        MobileNumber = request.form["phone"]
        Sex = request.form["sex"]
        password = request.form["password"]
        con = mysql.connector.connect(host="localhost",user="root",passwd="Shradha720@",database="deepak")    
        try:        
            mycursor = con.cursor()
            sql = "insert into account values (%s,%s,%s,%s,%s)"
            val = (username,email,MobileNumber,Sex ,password)
            mycursor.execute(sql,val)
            flash("Registered Successfully","success")
            return redirect(url_for("login"))
        finally:
            con.close() 


@app.route("/adlogin", methods = ["GET","POST"])
def adlogin():
    if(request.method=="GET"):
        return render_template("/admin/adlogin.html")
    else:
        username = request.form["username"]
        password = request.form["password"]
        con = mysql.connector.connect(host="localhost",user="root",passwd="Shradha720@",database="deepak")
        try:
            mycursor = con.cursor()
            mycursor.execute(f"SELECT password FROM admin_account where email = '{username}'")
            myresult = mycursor.fetchone()
            if(myresult[0]==password):
                session["adlogin"] = True
                session["username"] = username
                flash("Admin logged in Successfully","success")
                return redirect(url_for('home'))
            else:
                session["adlogin"] = False
                session["username"] = ''
                flash("invalid Admin username or password!!","danger")
                return redirect(url_for('adlogin'))
              
        finally:
            con.close()


@app.route("/Users")
def Users():
    con = mysql.connector.connect(host="localhost",user="root",passwd="Shradha720@",database="deepak")    
    try: 
        mycursor = con.cursor()
        mycursor.execute("SELECT * FROM account")
        myresult = mycursor.fetchall()
        return render_template("/admin/Users.html",users = myresult)
    finally:
        con.close()

@app.route("/RemoveUser/<Email>",methods=["GET","POST"])
def RemoveUser(Email):
    if(request.method=="GET"):
        return render_template("/admin/RemoveUser.html")
    else:
        action = request.form["action"]
        if(action == "Yes"):
            con = mysql.connector.connect(host="localhost",user="root",passwd="Shradha720@",database="deepak")    
            try: 
                flash("User Deleted Successfully",'success')
                mycursor = con.cursor()
                sql = "delete from account where Email=%s"
                val = (Email,)
                mycursor.execute(sql,val)
            finally:
                con.close()
        return redirect(url_for("Users"))


@app.route("/adlogout")
def adlogout():
    session["adlogin"] = False
    flash(" Admin Logged out Successfully!!","success")
    return redirect(url_for("home"))

@app.route("/logout")
def logout():
    session["login"] = False
    session['Bookings'] = {}
    session.clear()
    flash("User Logged out Successfully!!","success")
    return redirect(url_for("home"))


@app.route("/")
def main(): 
    con = mysql.connector.connect(host="localhost",user="root",passwd="Shradha720@",database="deepak")    
    try: 
        mycursor = con.cursor()
        mycursor.execute("SELECT * FROM category")
        myresult = mycursor.fetchall()
        session["cats"] = myresult       
    finally:
        con.close()
        return render_template("index.html")



@app.route("/Categories")
def showAllCategories():
    con = mysql.connector.connect(host="localhost",user="root",passwd="Shradha720@",database="deepak")    
    try: 
        mycursor = con.cursor()
        mycursor.execute("SELECT * FROM category")
        myresult = mycursor.fetchall()
        return render_template("/admin/category.html",cats = myresult)
    finally:
        con.close()


@app.route("/AddNewCategory",methods=["GET","POST"])
def AddNewDept():
    if(request.method=="GET"):
        return render_template("/admin/AddCategory.html")
    else:
        con = mysql.connector.connect(host="localhost",user="root",passwd="Shradha720@",database="deepak")    
        try: 
            flash("New Category Inserted Successfully",'success')
            mycursor = con.cursor()            
            cname = request.form["cname"]            
            sql = "insert into category (cname) values(%s)"
            val = (cname,)
            mycursor.execute(sql,val)            
            return redirect(url_for("showAllCategories"))
        finally:
            con.close()


@app.route("/AddCategory",methods=["GET","POST"])
def AddCategory():
    if(request.method=="GET"):
        return render_template("/admin/AddCategory.html")
    else:
        con = mysql.connector.connect(host="localhost",user="root",passwd="Shradha720@",database="deepak")    
        try: 
            flash("New Category Inserted Successfully",'success')
            mycursor = con.cursor()
            sql = "insert into category (cname) values (%s)"
            val = (request.form["cname"],)
            mycursor.execute(sql,val)            
            return redirect(url_for("Category"))
        finally:
            con.close()


@app.route("/EditCategory/<id>",methods=["GET","POST"])
def EditCategory(id):
    if(request.method=="GET"):
        flash("Category Updated Successfully")
        con = mysql.connector.connect(host="localhost",user="root",passwd="Shradha720@",database="deepak")    
        try: 
            mycursor = con.cursor()
            sql = "select * from category where cid=%s"
            val = (id,)
            mycursor.execute(sql,val)
            result = myresult = mycursor.fetchone()
            return render_template("/admin/EditCategory.html",cat=result)
        finally:
            con.close()
    
    else:
        con = mysql.connector.connect(host="localhost",user="root",passwd="Shradha720@",database="deepak")    
        try: 
            mycursor = con.cursor()
            sql = "update category set cname = %s where cid=%s"
            val = (request.form["cname"],id,)
            mycursor.execute(sql,val)
        finally:
            con.close()
        return redirect(url_for("Category"))

@app.route("/DeleteCategory/<id>",methods=["GET","POST"])
def DeleteCategory(id):
    if(request.method=="GET"):
        return render_template("/admin/DeleteCategory.html")
    else:
        action = request.form["action"]
        if(action == "Yes"):
            con = mysql.connector.connect(host="localhost",user="root",passwd="Shradha720@",database="deepak")    
            try: 
                flash("Category Deleted Successfully",'success')
                mycursor = con.cursor()
                sql = "delete from category where cid=%s"
                val = (id,)
                mycursor.execute(sql,val)
            finally:
                con.close()
        return redirect(url_for("Category"))

@app.route("/Category")
def Category():
    con = mysql.connector.connect(host="localhost",user="root",passwd="Shradha720@",database="deepak")    
    try: 
        mycursor = con.cursor()
        mycursor.execute("SELECT * FROM category")
        myresult = mycursor.fetchall()
        return render_template("/admin/Categories.html",cats = myresult)
    finally:
        con.close()



@app.route("/Products")
def showAllProducts():
    con = mysql.connector.connect(host="localhost",user="root",passwd="Shradha720@",database="deepak")    
    try: 
        mycursor = con.cursor()
        mycursor.execute("select p.pid,p.pname,p.price,p.imageurl,c.cname from product p inner join  category c on p.cid = c.cid;")
        myresult = mycursor.fetchall()
        return render_template("/admin/Products.html",prds = myresult)
    finally:
        con.close()

@app.route("/EditProduct/<id>",methods=["GET","POST"])
def EditProduct(id):
    if(request.method=="GET"):
        flash("Product Updated Successfully",'success')
        con = mysql.connector.connect(host="localhost",user="root",passwd="Shradha720@",database="deepak")    
        try: 
            mycursor = con.cursor()
            sql = "select * from product where pid=%s"
            val = (id,)
            mycursor.execute(sql,val)
            result = myresult = mycursor.fetchone()
            return render_template("/admin/EditProduct.html",prd =result)
        finally:
            con.close()
    
    else:
        con = mysql.connector.connect(host="localhost",user="root",passwd="Shradha720@",database="deepak")    
        try: 
            mycursor = con.cursor()
            sql = "update product set pname = %s where pid=%s"
            val = (request.form["pname"],id,)
            mycursor.execute(sql,val)
        finally:
            con.close()
        return redirect(url_for("showAllProducts"))

@app.route("/DeleteProduct/<id>",methods=["GET","POST"])
def DeleteProduct(id):
    if(request.method=="GET"):
        return render_template("/admin/DeleteProduct.html")
    else:
        action = request.form["action"]
        if(action == "Yes"):
            con = mysql.connector.connect(host="localhost",user="root",passwd="Shradha720@",database="deepak")    
            try: 
                flash("Product Deleted Successfully",'success')
                mycursor = con.cursor()
                sql = "delete from product where pid=%s"
                val = (id,)
                mycursor.execute(sql,val)
            finally:
                con.close()
        return redirect(url_for("showAllProducts"))

@app.route("/AddProduct",methods=["GET","POST"])
def AddProduct():
    if(request.method=="GET"):
        con = mysql.connector.connect(host="localhost",user="root",passwd="Shradha720@",database="deepak")    
        try: 
            mycursor = con.cursor()
            mycursor.execute("SELECT * FROM Category")
            myresult = mycursor.fetchall()
            return render_template("/admin/AddNewProduct.html",cats = myresult)
        finally:
            con.close()
    else:        
        cname = request.form["cname"]
        price = request.form["price"]
        catid = request.form["catid"]
        

        f = request.files['image']
        f.save("static\\Images\\"+secure_filename(f.filename))
       
        con = mysql.connector.connect(host="localhost",user="root",passwd="Shradha720@",database="deepak")    
        try: 
            flash("New Product Inserted Successfully",'success')
            mycursor = con.cursor()
            sql = "insert into product (pname,price,imageurl,cid) values(%s,%s,%s,%s)"
            val = (cname,price,f.filename,catid)
            mycursor.execute(sql,val)            
            return redirect(url_for("showAllProducts"))
        finally:
            con.close()


@app.route("/ViewDetails/<id>")
def ViewDetails(id): 
    con = mysql.connector.connect(host="localhost",user="root",passwd="Shradha720@",database="deepak")    
    try: 
        mycursor = con.cursor()
        sql = "SELECT * FROM product where pid=%s";
        val = (id,)
        mycursor.execute(sql,val)
        myresult = mycursor.fetchone()
        return render_template("/user/ViewDetails.html",prd = myresult)
    finally:
        con.close()



@app.route("/ShowProducts/<id>")
def ShowProducts(id):
    con = mysql.connector.connect(host="localhost",user="root",passwd="Shradha720@",database="deepak")    
    try: 
        mycursor = con.cursor()
        sql = "SELECT pid,pname,price FROM product where cid=%s";
        val = (id,)
        mycursor.execute(sql,val)
        myresult = mycursor.fetchall()
        return render_template("/user/ShowProducts.html",prds = myresult)
    finally:
        con.close()


@app.route("/AddToCart",methods=["GET","POST"])
def AddToCart():
    if(request.method=="POST"):
        pid=request.form["pid"]
        pname=request.form["pname"]
        price=request.form["price"]
        qty=request.form["qty"]
        item=[pid,pname,price,qty]
        #If Session is not created
        if("MyBooking" not in session):
            Bookings={}
        else:
            Bookings=session["MyBooking"]
        Bookings[pid]=item
        #for updating the session
        session["MyBooking"]=Bookings
        return redirect("/")

@app.route("/ShowAllCartItems")
def ShowAllCartItems():
    if("MyBooking" not in session):
        return "No items in MyBooking"
    else:
        total = 0
        for prd in session["MyBooking"].values():
            total  =  total + float(prd[2])*float(prd[3])
        session["total"] = total
       
        return render_template("/user/ShowAllCartItems.html")


@app.route("/RemoveFromCart",methods=["GET","POST"])
def RemoveFromCart():
    if(request.method=="POST"):
        pid = str(request.form["pid"])
        Bookings = session["MyBooking"]
        del Bookings[pid]
        session["MyBooking"] = Bookings
        return redirect("ShowAllCartItems")



@app.route("/MakePayment",methods=["GET","POST"])
def MakePayment():
    if(request.method=="GET"):
        return render_template("/user/MakePayment.html")
    else:
        cardno = request.form["cardno"]
        cvv = request.form["cvv"]
        expiry = request.form["expiry"]
        sql = "select count(*) from payment where cardno=%s and cvv=%s and expiry=%s"
        val = (cardno,cvv,expiry)
        con = mysql.connector.connect(host="localhost",user="root",passwd="Shradha720@",database="deepak")    
        try: 
            mycursor = con.cursor()
            mycursor.execute(sql,val)
            myresult = mycursor.fetchone()
            print(myresult[0])
            if(myresult[0] == 1):
                flash("Payment done Successfully",'success')
                #Perform transaction
                sql1 = "update Payment set amount=amount - %s where cardno=%s"
                sql2 = "update Payment set amount=amount + %s where cardno=222"
                val1 = (session["total"],cardno)
                mycursor.execute(sql1,val1)
                val2 = (session["total"],)
                mycursor.execute(sql2,val2)
                return redirect("/")
               
            else:
                flash("Invalid credentials",'danger')
                return redirect("/MakePayment")
        finally:
            con.close()
            
@app.route('/')
def index():
    return render_template('index.html')
# openai.api_key = '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'

# @app.route('/chatbot', methods=['POST'])
# def chatbot():
#     user_message = request.json['message']
    
#     # Send the message to OpenAI's API
#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=[{"role": "user", "content": user_message}]
#     )
    
#     bot_reply = response['choices'][0]['message']['content']
#     return jsonify(reply=bot_reply)

@app.route("/chat", methods=["GET"])
def ChatWithLLM():
    render_template('chat.html')
        
@app.route("/chat/query", methods=["POST"])
def Chatwithllmnow():
    data = request.json["ques"]
    ans = chat_bot.ChatWIthLLM(data)
    return ans
    
    
    


if(__name__ == "__main__"):
    app.run(debug=True)