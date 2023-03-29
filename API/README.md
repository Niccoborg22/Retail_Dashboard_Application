# REST API Documentation
---
This folder includes all the files used to build and deploy the REST API using Flask-RESTx for a web application that manages articles, transactions, customers, and alldata.
## Overview
---
This REST API has been designed to provide access to the following resources stored in the following databases: 
- Customers: Google Cloud MySql database & MongoDb
- Articles: Google Cloud MySql database & MongoDb
- Transactions: Google Cloud MySql database
- AllData: Google Cloud MySql database
The main purpose of the API is to retrieve the data in JSON format. The API uses authentication
## Required Modules
---
The modules required to run the API are the following: 
- Flask: pip install Flask
- Flask-RESTx: pip install flask-restx
- SQLAlchemy: pip install SQLAlchemy
- PyMongo: pip install pymongo
- Pandas: pip install pandas
## Functions
--- 
### Connect()
- *Description*: Connect to the MySQL Google Cloud Database
- *Input*: /
- *Output*: variable 'conn', represents a connection to the database

### Disconnect(conn)
- *Description*: Disconnect to the MySQL Google Cloud Database
- *Input*: variable 'conn', represents a connection to the database
- *Output*: /

## Endpoints
---
### Namespace Customers
#### GET api/v1/customers
- *Description*: Fethces all the customers dataset
- *Authorization*: Requires a valid Bearer token

#### GET api/v1/customers/customer_id
- *Description*: Fethces the customer in the dataset with id = customer_id
- *Authorization*: Requires a valid Bearer token

### Namespace Articles
#### GET api/v1/articles
- *Description*: Fethces all the articles dataset
- *Authorization*: Requires a valid Bearer token

#### GET api/v1/articles/article_id
- *Description*: Fethces the customer in the dataset with id = article_id
- *Authorization*: Requires a valid Bearer token

### Namespace Transactions
#### GET api/v1/transactions
- *Description*: Fethces all the transaction dataset
- *Authorization*: Requires a valid Bearer token

### Namespace Alldata
#### GET api/v1/alldata
- *Description*: Fethces all the alldata dataset
- *Authorization*: Requires a valid Bearer token

#### GET api/v1/alldata/sales_channel/min_age/max_age/section_name
- *Description*: Fethces the entries with sales channel = sales_channel, age between min_age and max_age with section name=section_name from alldata dataset
- *Authorization*: Requires a valid Bearer token

## Error Handling
---
In case of unathorized requests or errors, the API will return a JSON object containing an error message and an appropriate HTTP status code.

## Deployment
---
The API has been deployed in the App Engine in Google Cloud. In order to do so the following additional files have been created: 
- app.yaml: Yaml file necessary for the deployment
- requirements.txt: txt file with all the requirements for the app engine to deploy the application
