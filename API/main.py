# Imports
from flask import Flask, jsonify, request
from sqlalchemy import create_engine
from flask_restx import Api, Namespace, Resource, reqparse, inputs, fields
import pandas as pd
import pymongo
import json
import os
from dotenv import load_dotenv

# Load the variables to access the databases
load_dotenv()

# Create an app with Flask
app = Flask(__name__)

# Create an API authentication
auth_db = {
    'tokenMania'
}

# Connect to the Google Cloud mySQL database
db_host = os.getenv('MySQL_db_host')
db_user = os.getenv('MySQL_db_user')
db_pass = os.getenv('MySQL_db_pass')
db_name = os.getenv('MySQL_db_name')

# Function to connect to the Google Cloud MySQL database
def connect():
    db = create_engine(
    'mysql+pymysql://{0}:{1}@{2}/{3}' \
        .format(db_user, db_pass, db_host, db_name), \
    connect_args = {'connect_timeout': 10})
    conn = db.connect()
    return conn

def disconnect(conn):
    conn.close()

# Connect to the MongoDb database
user = os.getenv('MongoDb_user')
passw = os.getenv('MongoDb_passw')
host = os.getenv('MongoDb_host')
database = os.getenv('MongoDb_database')
client =  pymongo.MongoClient(
    "mongodb+srv://{0}:{1}@{2}/?retryWrites=true&w=majority" \
    .format(user, passw, host))
db = client[database]
collection_customer = db['customer']
collection_articles = db['articles']
collection_transactions = db['transactions']

# Create an API for our application
api = Api(app, version='1.0',
    title = 'KPIs H&M Retail Capstone Project',
    description = 'Set of JSON endpoint to get insightful data from the \'articles\', \'customers\' and \'transactions\' datasets',
    contact = 'nborgato2022@student.ie.edu',
    endpoint = '/api/v1'
)

# Create a namespace to group all the resources and routes related to customers
customers = Namespace('customers',
    description = 'All operations related to customers',
    path='/api/v1')
api.add_namespace(customers)

# Create an API to retrieve all the customers
@customers.route('/customers')
class get_all_users(Resource):
    def get(self):
        # Check for the authorization, return a 401 in case of not authorization
        if "Authorization" not in request.headers:
            return json.dumps({'error': 'unauthorized'}), 401
        else:
            header = request.headers['Authorization']
            token = header.split()[1]
            if token in auth_db:
                conn = connect()
                query = """
                    SELECT *
                    FROM customers
                    LIMIT 10000
                """
                result = conn.execute(query).fetchall()
                disconnect(conn)
                return jsonify({'result': [dict(row) for row in result]})
            else: 
                return json.dumps({'error': 'unauthorized'}), 401


# Create an API to retrieve the customers with customer id = 'customer_id'
@customers.route('/customers/<customer_id>')
@customers.doc(params = {'customer_id':'The ID of the customer'})
class select_customer(Resource):

    @api.response(404, "article not found")
    def get(self, customer_id):
        # Check for the authorization, return a 401 in case of not authorization
        if "Authorization" not in request.headers:
            return json.dumps({'error': 'unauthorized'}), 401
        else:
            header = request.headers['Authorization']
            token = header.split()[1]
            if token in auth_db:
                customer_id_mongodb_df = pd.DataFrame(list(collection_customer.find({"customer_id": customer_id}).limit(1000)))
                if len(customer_id_mongodb_df) > 0:
                    customer_id_mongodb_df['_id'] = customer_id_mongodb_df['_id'].apply(str)
                    customer_id_mongodb_df = customer_id_mongodb_df.where(pd.notnull(customer_id_mongodb_df), None)
                    return customer_id_mongodb_df.to_json(orient='records')
                else:
                    return "No customer found with ID: {}".format(customer_id), 404
            else: 
                return json.dumps({'error': 'unauthorized'}), 401

# Create a namespace to group all the resources and routes related to articles
articles = Namespace('articles',
    description = 'All operations related to articles',
    path='/api/v1')
api.add_namespace(articles)

# Create an API to retrieve all the articles
@articles.route('/articles')
class get_all_articles(Resource):
    def get(self):
        # Check for the authorization, return a 401 in case of not authorization
        if "Authorization" not in request.headers:
            return json.dumps({'error': 'unauthorized'}), 401
        else:
            header = request.headers['Authorization']
            token = header.split()[1]
            if token in auth_db:
                conn = connect()
                query = """
                    SELECT *
                    FROM articles
                    LIMIT 10000
                """
                result = conn.execute(query).fetchall()
                disconnect(conn)
                return jsonify({'result': [dict(row) for row in result]})
            else: 
                return json.dumps({'error': 'unauthorized'}), 401

# Create an API to retrieve data from the article with article id = article_id
@articles.route('/articles/<int:article_id>')
@articles.doc(params = {'article_id':'The ID of the article' })
class select_articles(Resource):

    @api.response(404, "article not found")
    def get(self, article_id):
        # Check for the authorization, return a 401 in case of not authorization
        if "Authorization" not in request.headers:
            return json.dumps({'error': 'unauthorized'}), 401
        else:
            header = request.headers['Authorization']
            token = header.split()[1]
        if token in auth_db:
            articles_id_mongodb_df = pd.DataFrame(list(collection_articles.find({"article_id": article_id}).limit(1000)))
            if len(articles_id_mongodb_df) > 0:
                articles_id_mongodb_df['_id'] = articles_id_mongodb_df['_id'].apply(str)
                articles_id_mongodb_df = articles_id_mongodb_df.where(pd.notnull(articles_id_mongodb_df), None)
                return articles_id_mongodb_df.to_json(orient='records')
            else:
                return "No article found with ID: {}".format(article_id), 404
        else: 
            return json.dumps({'error': 'unauthorized'}), 401

# Create a namespace to group all the resources and routes related to transactions
transactions = Namespace('transactions',
    description = 'All operations related to transactions',
    path='/api/v1')
api.add_namespace(transactions)

# Create an API to retrieve data from the transactions
@transactions.route('/transactions')
class all_transactions(Resource):
    @api.response(404, "article not found")
    def get(self):
        # Check for the authorization, return a 401 in case of not authorization
        if "Authorization" not in request.headers:
            return json.dumps({'error': 'unauthorized'}), 401
        else:
            header = request.headers['Authorization']
            token = header.split()[1]
            if token in auth_db:
                conn = connect()
                query = """
                    SELECT *
                    FROM sampletransactions
                    LIMIT 10000
                """
                result = conn.execute(query).fetchall()
                disconnect(conn)
                return jsonify({'result': [dict(row) for row in result]})
            else: 
                return json.dumps({'error': 'unauthorized'}), 401

# Create a namespace for retrieving the data all together
alldata = Namespace('alldata',
    description = 'The three datasets all together',
    path='/api/v1')
api.add_namespace(alldata)

# Create an API to retrieve all the data together
@alldata.route('/alldata')
class all_data(Resource):
    @api.response(404, "article not found")
    def get(self):
        # Check for the authorization, return a 401 in case of not authorization
        if "Authorization" not in request.headers:
            return json.dumps({'error': 'unauthorized'}), 401
        else:
            header = request.headers['Authorization']
            token = header.split()[1]
            if token in auth_db:
                conn = connect()
                query = """
                    SELECT *
                    FROM alldata
                    LIMIT 10000
                """
                result = conn.execute(query).fetchall()
                disconnect(conn)
                return jsonify({'result': [dict(row) for row in result]})
            else: 
                return json.dumps({'error': 'unauthorized'}), 401

# Create an API to retrieve all the data according to certain parameters
@alldata.route('/alldata/<sales_channel>/<min_age>/<max_age>/<section_name>')
class filtered_all_data(Resource):
    @api.response(404, "article not found")
    def get(self, sales_channel, min_age, max_age, section_name):
        # Check for the authorization, return a 401 in case of not authorization
        if "Authorization" not in request.headers:
            return json.dumps({'error': 'unauthorized'}), 401
        else:
            header = request.headers['Authorization']
            token = header.split()[1]
            if token in auth_db:
                conn = connect()
                if sales_channel == 3:
                    if section_name == 'all':
                        query = f"""
                            SELECT *
                            FROM alldata
                            WHERE age BETWEEN {min_age} AND {max_age}
                            """
                    else: 
                        query = f"""
                            SELECT *
                            FROM alldata
                            WHERE section_name = {section_name} AND age BETWEEN {min_age} AND {max_age}
                            """
                else: 
                    if section_name == 'all':
                        query = f"""
                            SELECT *
                            FROM alldata
                            WHERE sales_channel_id = {sales_channel} AND age BETWEEN {min_age} AND {max_age}
                            """
                    else: 
                        query = f"""
                            SELECT *
                            FROM alldata
                            WHERE sales_channel_id = {sales_channel} AND age BETWEEN {min_age} AND {max_age} AND section_name = {section_name}
                            """
                result = conn.execute(query).fetchall()
                disconnect(conn)
                return jsonify({'result': [dict(row) for row in result]})
            else: 
                return json.dumps({'error': 'unauthorized'}), 401

# Run the app
if __name__ == '__main__':
    app.run(
        host = '0.0.0.0', 
        port = 8080,
        debug = True)