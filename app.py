from flask import Flask, render_template, jsonify, request, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from flask_bcrypt import Bcrypt


#Instanciates a Flask application, this indicates that main.py is the app root 
app = Flask(__name__)
#Instaciates bcrypt
bcrypt = Bcrypt(app)
#App configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'secretkey123'
db = SQLAlchemy(app)

#Get specific customer
@app.route('/api/customers/<int:id>')
@cross_origin()
def get_customer(id):
    from models import Customer
    customer = Customer.query.get(id)
    
    if customer:
        return jsonify(customer.as_dict())
    else: 
        return jsonify({'message: customer not found'}), 404

# Get all customers
@app.route('/api/customers')
@cross_origin()
def get_all_customers():
    from models import Customer
    customers = Customer.query.all()
    result = []
    
    for customer in customers:
        content = {
            'id': customer.id,
            'firstname': customer.firstname,
            'surname': customer.surname,
            'email': customer.email, 
            'phone': customer.phone,
            'address': customer.address
        }
        result.append(content) # Adding in row+1 
        
    return jsonify(result)

# Post a client
@app.route('/api/customers', methods = ['POST'])
@cross_origin()
def save_customer():
    from models import Customer
    #JSON of the request
    data = request.json 
    
    #Instance of Customer with the request
    new_customer = Customer(
        firstname=data['firstname'],
        surname=data['surname'],
        email=data['email'],
        phone=data['phone'],
        address=data['address']
    )
    
    #Add the customer to the db session and commit
    db.session.add(new_customer)
    db.session.commit()
    
    return 'Client saved'
    

# Edit a Client
@app.route('/api/customers<int:id>', methods = ['PUT']) #? Para editar se utiliza PUT
@cross_origin()
def update_customer():
    from models import Customer
    data = request.json
    
    # Search client by id
    existing_customer = Customer.query.get(id)
    
    if existing_customer:
        existing_customer.firstname = data['firstname'],
        existing_customer.surname = data['surname']
        existing_customer.email = data['email']
        existing_customer.phone = data['phone']
        existing_customer.address = data['address']
        
        db.session.commit()
        return 'Client edited'
    return 'Client NOT found', 404
    

# Delete a client
@app.route('/api/customers/<int:id>', methods=['DELETE'])
@cross_origin()
def remove_customer(id):
    from models import Customer
    customer_to_delete = Customer.Query.get(id)
    
    if customer_to_delete:
        db.session.delete(customer_to_delete)
        db.session.commit()
        return 'Client deleted'
    return 'Cliente NOT found', 404


#! RENDERING CONTENT

#? Rendering the index.html on the app home
@app.route('/')
@cross_origin()
def index():
    return render_template('index.html')


#? Rendering the user.html template for the /user route
@app.route('/registration')
@cross_origin()
def registration():
    from forms import RegistrationForm
    form = RegistrationForm() #! Esta es la logica con python de un formulario
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success!')
        return redirect(url_for('index'))
    return render_template('registration.html', title="Register", form=form) #! Aca le hago form=form lo que me da acceso a la variable en el template 


#? Rendering the login.html template for the /login route
@app.route('/login')
@cross_origin()
def login():
    from forms import LoginForm
    form = LoginForm()
    return render_template('login.html', title="Log in", form=form)

    
#? Rendering the user.html template for the /user route
@app.route('/user')
@cross_origin()
def user():
    return render_template('user.html')


#* Running the APP only if I run the main.py file
if __name__ == '__main__': 
    app.run(None, 3000, True) 
    
    ''' None as the first argument means that the server should listen on all available public IPs.
        3000 is the port number on which the server will listen. In this case, it's set to port 3000.
        True as the third argument means that the server should automatically reload when code changes are detected. 
        This is useful during development to see the changes without manually restarting the server.'''    
