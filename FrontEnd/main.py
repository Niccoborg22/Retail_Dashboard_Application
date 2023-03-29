from flask import Flask, render_template, request, session, redirect, url_for
from sqlalchemy import create_engine
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import pandas as pd
import os
from dotenv import load_dotenv

# Load the variables to access the databases
load_dotenv()

# Connect to the Google Cloud mySQL database
db_host = os.getenv('MySQL_db_host')
db_user = os.getenv('MySQL_db_user')
db_pass = os.getenv('MySQL_db_pass')
db_name = os.getenv('MySQL_db_name')

# function to connect to the MySQL database
def connect():
    db = create_engine(
    'mysql+pymysql://{0}:{1}@{2}/{3}' \
        .format(db_user, db_pass, db_host, db_name), \
    connect_args = {'connect_timeout': 10})
    conn = db.connect()
    return conn

# function to disconnect from the MySQL database
def disconnect(conn):
    conn.close()

# function to normalize the data from Google Cloud
def normalize_data(response_json):
    try:
        data = pd.json_normalize(response_json, 'result')
    except Exception as e:
        print(e)
    return data

# Create the Flask application and its secret key
app = Flask('H&M_data', template_folder='FrontEnd/templates', static_folder='FrontEnd/static')
app.config["SECRET_KEY"] = "niccolo22"

@app.route("/")
def index():
    if "user_id" in session:
        return render_template("index.html")
    
    return render_template("register.html")

# Route to register in the app
@app.route("/register")
def register():
    return render_template("register.html")

# Handle the post request in the register route. The data is saved in a Google Cloud Database
@app.route("/register", methods=["POST"])
def handle_register():
    # Save the posts in variables
    username = request.form["username"]
    password = request.form["password"]

    # transform the password in a hashed password 
    hashed_password = generate_password_hash(password)

    # Write the queries
    query = f"""
    INSERT INTO users(username, password)
    VALUES ("{username}", "{hashed_password}")
    """

    user_query = f"""
    SELECT id
    FROM users
    WHERE username='{username}'
    """

    connection = connect()
    connection.execute(query)
    user = connection.execute(user_query).fetchone()

    session["username"] = username
    session["user_id"] = user[0]
    disconnect(connection)

    return redirect(url_for("index"))

# Route to login in the app
@app.route("/login")
def login():
    return render_template("login.html")

# Handle the post request in the login route
@app.route("/login", methods=["POST"])
def handle_login():
    # Save the posts in variables
    username = request.form["username"]
    password = request.form["password"]

    # Write the queries
    query = f"""
    SELECT id, password
    FROM users
    WHERE username='{username}'
    """
    # Execute the queries 
    connection = connect()
    user = connection.execute(query).fetchone()
    if user:
        password_matches = check_password_hash(user[1], password)
    else:
        password_matches = False


    disconnect(connection)

    if user and password_matches:
        session["username"] = username
        session["user_id"] = user[0]
        

        return redirect(url_for("index"))
    else:
        return render_template("register.html")

# Route to logout in the app
@app.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("user_id", None)
    return redirect(url_for("login"))

@app.route("/articles")
def articles():
    if "user_id" in session:
        # Download the articles data
        url = "https://api-dot-retailcapstone.oa.r.appspot.com/api/v1/articles"
        response = requests.get(url, headers={'Authorization': 'Bearer tokenMania'})
        # Check that the request was successful
        if response.status_code == 200:
            json_dict = normalize_data(response.json())
            json_data = json_dict.to_json(orient='records')
            return render_template("articles.html", articles_json=json_data)
        else: 
            return render_template("404.html"), 404
    else:
        return render_template("403.html"), 403 

@app.route("/customers")
def customers():
    if "user_id" in session:
        # Get the data from the API and normalize it
        url = 'https://api-dot-retailcapstone.oa.r.appspot.com/api/v1/customers'
        response = requests.get(url, headers={'Authorization': 'Bearer tokenMania'})
        if response.status_code == 200:
            json_dict = normalize_data(response.json())
            json_data = json_dict.to_json(orient='records')
            # Return the data in JSON format to the HTML
            return render_template("customers.html", customers_json=json_data)
        else: 
            return render_template("404.html"), 404
    else:
        return render_template("403.html"), 403 
    
@app.route("/transactions")
def transactions():
    if "user_id" in session:
        # Get the data from the API and normalize it
        url = 'https://api-dot-retailcapstone.oa.r.appspot.com/api/v1/transactions'
        response = requests.get(url, headers={'Authorization': 'Bearer tokenMania'})
        if response.status_code == 200:
            json_dict = normalize_data(response.json())
            json_data = json_dict.to_json(orient='records')
            # Return the data in JSON format to the HTML
            return render_template("transactions.html", transactions_json=json_data)
        else: 
            return render_template("404.html"), 404
    else:
        return render_template("403.html"), 403 
    
@app.route("/playdatasets")
def playDatasets():
    if "user_id" in session:
        # Get the data from the API and normalize it
        url = 'https://api-dot-retailcapstone.oa.r.appspot.com/api/v1/alldata'
        response = requests.get(url, headers={'Authorization': 'Bearer tokenMania'})
        if response.status_code == 200:
            json_dict = normalize_data(response.json())
            json_data = json_dict.to_json(orient='records')
            # Return the data in JSON format to the HTML
            return render_template("playdatasets.html", alldata_json=json_data)
        else: 
            return render_template("404.html"), 404
    else:
        return render_template("403.html"), 403 

# Errorhandler 404
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Errorhandler 403
@app.errorhandler(403)
def unauthorized(e):
    return render_template('403.html'), 403

# Run the app
if __name__ == '__main__':
    app.run(
        host = '0.0.0.0', 
        port = 8080,
        debug = True)
