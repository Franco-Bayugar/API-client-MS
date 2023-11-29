from flask import Flask, render_template, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS, cross_origin

#* Instanciates a Flask application, this indicates that main.py is the app root 
app = Flask(__name__)

#todo: TEMPORARY (to avoid the problem of using a different port than :3000)
cors = CORS(app) 

#* App configuration
app.config['CORS_HEADERS'] = 'Content-Type' # This means that requests from other domains will be allowed to include the header
app.config['MYSQL_HOST'] = 'Localhost' # Data base config. 'LocalHost' will be the database
app.config['MYSQL_USER'] = 'root' # Setting the user-database-name
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'system' # Database name to connect
mysql = MySQL(app) # MySQL instance to interact with the database 

#* App functions

#Get specific customer
#* This functions uses the datatype GET (in the @app.route('URL')) to get a specific customer, returns a dictionary 
@app.route('/api/customers/<int:id>')
@cross_origin()
def getCustomer(id):
    cur = mysql.connection.cursor() # Instanciates a cursor to interact with the database, in the following line I can use SQL query
    cur.execute('SELECT id, firstname, surname, email, phone, adress FROM customers WHERE id ='+ str(id))
    data = cur.fetchall() # Retrieves all the results of the SQL query and stores them in the data variable.
    content = {}
    for row in data:
        content = {'id':row[0], 
                   'firstname':row[1],
                   'surname':row[2],
                   'email': row[3],
                   'phone': row[4],
                   'adress': row[5]}
    return jsonify(content) # Converts to JSON

#Get ALL customer
#* Also uses the GET data type to return all customers as an Array, this later will be reading by JS
@app.route('/api/customers')
@cross_origin()
def getAllCustomers():
    cur = mysql.connection.cursor()
    cur.execute('SELECT id, firstname, surname, email, phone, adress FROM customers')
    data = cur.fetchall() 
    result = [] # Retrieves all the data in an Array
    for row in data:
        content = {'id':row[0], 
                   'firstname':row[1],
                   'surname':row[2],
                   'email': row[3],
                   'phone': row[4],
                   'adress': row[5]}
        result.append(content) # Adding in row+1 
        
    return jsonify(result)

#* Data type POST to store a client; in the end I have to commit or push the connection to the data base
@app.route('/api/customers', methods = ['POST'])
@cross_origin()
def saveCustomer():
    cur = mysql.connection.cursor() #! I don't need to request and ID here, i'm just storing
    cur.execute("INSERT INTO `customers` (`id`, `firstname`, `surname`, `email`, `phone`, `adress`) VALUES (NULL, %s, %s, %s, %s, %s);",
                (request.json['firstname'], request.json['surname'], request.json['email'], request.json['phone'], request.json['adress']))
    
    mysql.connection.commit()
    return 'Client saved'

#* Data type PUT to edit a client;
@app.route('/api/customers', methods = ['PUT']) #? Para editar se utiliza PUT
@cross_origin()
def updateCustomer():
    cur = mysql.connection.cursor()  #! I NEED to request and ID here to update a specific client
    cur.execute("UPDATE `customers` SET `firstname` = %s, `surname` = %s, `email` = %s, `phone` = %s, `adress` = %s WHERE `customers`.`id` = %s;",
                (request.json['firstname'], request.json['surname'], request.json['email'], request.json['phone'], request.json['adress'], request.json['id']))
    
    mysql.connection.commit() #? commit to the data base
    return 'Client saved'


#* Data type DELETE'
@app.route('/api/customers/<int:id>', methods=['DELETE']) #* Data type: Delete
@cross_origin()
def removeCustomer(id):
    cur = mysql.connection.cursor() 
    cur.execute("DELETE FROM `customers` WHERE `customers`.`id` =" + str(id) + ";")
    mysql.connection.commit()
    return 'Client deleted'


#* Rendering the index.html on the app home
@app.route('/')
@cross_origin()
def index():
    return render_template('index.html')


#* Running the APP only if I run the main.py file
if __name__ == '__main__': 
    app.run(None, 3000, True) 
    
    ''' None as the first argument means that the server should listen on all available public IPs.
        3000 is the port number on which the server will listen. In this case, it's set to port 3000.
        True as the third argument means that the server should automatically reload when code changes are detected. 
        This is useful during development to see the changes without manually restarting the server.'''    
