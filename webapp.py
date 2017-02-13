from flask import Flask, url_for, flash, render_template, redirect, request, g, send_from_directory
from flask import session as login_session
from database import *
from werkzeug.utils import secure_filename
import locale, os
from datetime import *

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.secret_key = "MY_SUPER_SECRET_KEY"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


engine = create_engine('sqlite:///fizzBuzz.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine, autoflush=False)
session = DBSession()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
@app.route('/login', methods = ['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html')
	elif request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		if email is None or password is None:
			flash('	fill the unfilled boxes')
			return redirect(url_for('login'))
		if verify_password(email, password):
			customer = session.query(Customer).filter_by(email=email).one()
			flash('Login Successful, welcome, %s' % customer.name)
			login_session['name'] = customer.name
			login_session['email'] = customer.email
			login_session['id'] = customer.id
			return redirect(url_for('inventory'))
		else:
			
			flash('Incorrect username/password combination')
			return redirect(url_for('login'))



@app.route('/inventory')
def inventory():
	items = session.query(Product).all()
	return render_template('inventory.html', items=items)

def verify_password(email, password):
	customer = session.query(Customer).filter_by(email=email).first()
	if not customer or not customer.verify_password(password):
		return False
	g.customer = customer
	return True




@app.route('/newCustomer', methods = ['GET','POST'])
def newCustomer():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        birthday = request.form['birthday']
      	print("hello")
      	print(birthday)
      	print(type(birthday))
      	bday = datetime(year=(int)(birthday[0]), month=(int)(birthday[1]), day=(int)(birthday[2]))
        city = request.form['city']
        address = request.form['address']
        if name is None or email is None or password is None or city is None or birthday is None or 'file' not in request.files:
            flash("Fill the unfilled boxes")
            return redirect(url_for('newCustomer'))
        file = request.files['file']
        if file.filename == '':
            flash('select a file')
            return redirect(url_for('newCustomer'))
        if session.query(Customer).filter_by(email = email).first() is not None:
            flash("A user with this email address already exists")
            return redirect(url_for('newCustomer'))
        if file and allowed_file(file.filename):
            customer = Customer(name = name, email=email, address = address, birthday = bday, city = city)
            customer.hash_password(password)
            session.add(customer)
            session.commit()
            filename = str(customer.id) + "_" + secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            customer.set_photo(filename)
            session.add(customer)
            shoppingCart = ShoppingCart(customer=customer)
            session.add(shoppingCart)
            session.commit()
            flash("Welcome to our website!")
            return redirect(url_for('inventory'))
        else:
        	flash("Please upload an image")
        	return redirect(url_for('newCustomer'))
    else:
        return render_template('newCustomer.html')



@app.route("/product/<int:product_id>")
def product(product_id):
	product = session.query(Product).filter_by(id=product_id).one()
	return render_template('product.html', product=product)

	return redirect(url_for('shoppingCart'))



@app.route("/checkout", methods = ['GET', 'POST'])
def checkout():
	if 'id' not in login_session:
		flash("You must be logged in to perform this action")
		return redirect(url_for('login'))
	shoppingCart = session.query(ShoppingCart).filter_by(customer_id=login_session['id']).one()
	if request.method == 'POST':
		order = Order(customer_id=login_session['id'], confirmation=generateConfirmationNumber())
		order.total = calculateTotal(shoppingCart)
		# Remove items from shopping cart and add them to an order
		for item in shoppingCart.products:
			assoc = OrdersAssociation(product=item.product, product_qty=item.quantity)
			order.products.append(assoc)
			session.delete(item)
		session.add_all([order, shoppingCart])
		session.commit()
		return redirect(url_for('confirmation', confirmation=order.confirmation))
	elif request.method == 'GET':
		return render_template('checkout.html', shoppingCart=shoppingCart, total="%.2f" % calculateTotal(shoppingCart))


@app.route('/logout')
def logout():
	if 'id' not in login_session:
		flash("You must be logged in order to log out")
		return redirect(url_for('login'))
	del login_session['name']
	del login_session['email']
	del login_session['id']
	flash("Logged Out Successfully")
	return redirect(url_for('inventory'))

if __name__ == '__main__':
	app.run(debug=True)
