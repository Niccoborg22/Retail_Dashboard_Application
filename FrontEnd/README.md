# Frontend HTML Data Exploration Documentation
---
This folder includes all the files used to build and deploy the Frontend HTML Data Exploration Web Application using Flask
## Overview
---
This folder has been designed to group the Flask Application backend of a web application together with the HTML, CSS and JavaScript of its front-end. The folder is organized in the following way:
- Flask Application
- HTML templates
- CSS static

# Flask Application backend
---
The flask application can be found in the document flaskServer.py
## Required Modules
---
The modules required to run the API are the following: 
- Flask: pip install Flask
- SQLAlchemy: pip install SQLAlchemy
- Pandas: pip install pandas
- Werkzeug: pip install Werkzeug
- Requests: pip install requests

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

### Normalize_data(response_json)
- *Description*: Normalize the data from MySQL Google Cloud Database
- *Input*: variable 'response_json', represents the json file requested from the MySQL Google Cloud Database
- *Output*: variable 'data' representing the normalized data

## Routes
---
### /
- *Description*: If the user has registered/logged in and created a session, render the index page. Otherwise redirect him to the registering page
- *Authorization*: If a session was created, the user is authorized

### /register
- *Description*: Render the register page to allow the user to register in the website
- *Authorization*: Don't need any authentication to access this page

### /register method:POST
- *Description*: When the user posts his username and password, the values are saved in 2 variables. Later the password is hashed and a connection to the database is started by using the function connect(). The hashed password and the username are then saved in the MySQL Google Cloud Database. The connection is later stopped using the disconnect() function. Once everything is done, the index HTML is rendered
- *Authorization*: Don't need any authentication to access this page

### /login
- *Description*: Render the login page to allow the user to login in the website
- *Authorization*: Don't need any authentication to access this page

### /login method:POST
- *Description*: When the user posts his username and password, the values are saved in 2 variables. A connection to the database is started by using the function connect(). Run a query to the MySQL Google Cloud Database named users to check if the username and password that has been hashed are in the database. If the username and hashed password are in the database, a session in created and the user is redirected to the index page. Otherwise the user is redirected to the register page. The connection is later stopped using the disconnect() function.
- *Authorization*: Don't need any authentication to access this page

### /logout
- *Description*: This route removes the "username" and "user_id" keys from the session dictionary if they exist. The user is then redirected the user to the URL for the "login" view using Flask’s url_for function. 
- *Authorization*: Don't need any authentication to access this page

### /articles
- *Description*: A variable called url is created with the url of the API used to get the articles dataset. Using the requests library a get request is performed with the appropriate authorization. If the status code is 200 the response is made into JSON and normalized using the normalize_data() function and saved in a variable named json_data. If a session was created, the articles page is rendered together with the json_data in order for the HTML to render the pages correctly, otherwise a 403 is returned.
- *Authorization*: If a session was created, the user is authorized

### /customers
- *Description*: A variable called url is created with the url of the API used to get the customers dataset. Using the requests library a get request is performed with the appropriate authorization. If the status code is 200 the response is made into JSON and normalized using the normalize_data() function and saved in a variable named json_data. If a session was created, the customers page is rendered together with the json_data in order for the HTML to render the pages correctly, otherwise a 403 is returned.
- *Authorization*: If a session was created, the user is authorized

### /transactions
- *Description*: A variable called url is created with the url of the API used to get the transactions dataset. Using the requests library a get request is performed with the appropriate authorization. If the status code is 200 the response is made into JSON and normalized using the normalize_data() function and saved in a variable named json_data. If a session was created, the transactions page is rendered together with the json_data in order for the HTML to render the pages correctly, otherwise a 403 is returned.
- *Authorization*: If a session was created, the user is authorized

### /playdatasets
- *Description*: A variable called url is created with the url of the API used to get the alldata dataset. Using the requests library a get request is performed with the appropriate authorization. If the status code is 200 the response is made into JSON and normalized using the normalize_data() function and saved in a variable named json_data. If a session was created, the playdatasets page is rendered together with the json_data in order for the HTML to render the pages correctly, otherwise a 403 is returned.
- *Authorization*: If a session was created, the user is authorized

### errorhandler(404)
- *Description*: When a 404 error occurs in the application a rendered template of '404.html' is returned and the HTTP status code is set to 404.

### errorhandler(403)
- *Description*: When a 403 error occurs in the application a rendered template of '404.html' is returned and the HTTP status code is set to 403.

# HTML templates
---
In the templates folder all the HTML pages are saved and stored
## Webpages
---
### base.html
- *Description*: HTML that is extended in the other pages. It creates a header and a footer giving the user possibility of navigating through the different pages

### 403.html
- *Description*: Extends the base page. In the main block returns a text advising you that you need to login to see that page

### 404.html
- *Description*: Extends the base page. In the main block returns a text advising you that something went wrong

### register.html
- *Description*: Extends the base page. In the main block a form is rendered giving the opportunity for the user to enter a username and a password

### login.html
- *Description*: Extends the base page. In the main block a form is rendered giving the opportunity for the user to enter a username and a password

### index.html
- *Description*: Extends the base page. In the main block a welcome title and message is displayed together with 4 images that redirect you to articles, customers, transactions and playdatasets pages

### articles.html
- *Description*: Extends the base page. In the main block a welcome title and message are displayed together with, until all the JavaScript code is displayed a waiting loading screen. Once the JavaScript is loaded 3 KPIs of the articles dataset are displayed together with 2 graphs displaying interesting data about the articles in H&M portfolio

### customers.html
- *Description*: Extends the base page. In the main block a welcome title and message are displayed together with, until all the JavaScript code is displayed a waiting loading screen. Once the JavaScript is loaded 3 KPIs of the customers dataset are displayed together with a graph displaying interesting data about the customers in H&M portfolio

### transactions.html
- *Description*: Extends the base page. In the main block a welcome title and message are displayed together with, until all the JavaScript code is displayed, a waiting loading screen. Once the JavaScript is loaded 3 KPIs of the transactions dataset are displayed together with a graph displaying interesting data about the transactions

### playdatasets.html
- *Description*: Extends the base page. In the main block a welcome title and message are displayed together with a 3 filters that allow the user to select the sales channel, section and age they want to see data for. Once the user clicks the Filter Data button the user will be able to see 2 graphs according to the filters they selected. The user will be able to render new graphs by using the button again

# CSS static
---
In the static folder all the CSS files are saved and stored
## CSS
---
### base.css
- *Description*: Set of CSS that all the webpages follow