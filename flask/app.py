from flask import Flask, request, render_template , jsonify , redirect, url_for, flash
from flask_mysqldb import MySQL,MySQLdb
import os
from werkzeug.utils import secure_filename
from flask_wtf.csrf import CSRFProtect , generate_csrf


app = Flask(__name__)
app.secret_key = '9ol8j2349u82j4k2j34gjhr92834'
csrf = CSRFProtect(app)

# Configure database
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'my_data_base'

mysql = MySQL(app)

@app.route('/', methods=['GET'])
def login():
    return render_template('login.html')


@app.route('/get-categories')
def get_categories():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, name FROM category")
    categories = cur.fetchall()
    cur.close()
    # Convert query result to a list of dictionaries
    categories_list = [{'id': category[0], 'name': category[1]} for category in categories]
    return jsonify(categories_list)




ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'images')


# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/add-product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        category_id = request.form['category_id']  # Changed from 'category' to 'category_id'
        description = request.form['description']
        image = request.files['image']
        
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            try:
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                image.save(image_path)

                cur = mysql.connection.cursor()
                cur.execute("INSERT INTO product(name, price, category_id, description, image_path) VALUES(%s, %s, %s, %s, %s)", 
                            (name, price, category_id, description, filename))  # Note the change to 'category_id'
                mysql.connection.commit()
            except Exception as e:
                mysql.connection.rollback()
                print("Error: ", e)
                return 'Failed to add the product due to a server error.'
            finally:
                cur.close()
            return 'Product added successfully!'
    return render_template('add_producte.html')


@app.route('/home')
def home():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    search_query = request.args.get('search', '')
    category_id = request.args.get('category_id', '')
    
    query = """
    SELECT commands.id, product.name as product_name, product.image_path as product_image_path, product.description as product_description, commands.phone_number 
    FROM commands
    JOIN product ON commands.product_name = product.name
    WHERE commands.phone_number LIKE %s
    """
    params = ['%' + search_query + '%']
    if category_id:
        query += " AND product.category_id = %s"
        params.append(category_id)

    cur.execute(query, params)
    commands = cur.fetchall()
    
    # Fetch categories for the dropdown
    cur.execute("SELECT id, name FROM category")
    categories = cur.fetchall()
    cur.close()
    
    return render_template('home.html', commands=commands, categories=categories, csrf_token=generate_csrf())



@app.route('/client-home')
def client_home():
    search_query = request.args.get('search', '')
    category_id = request.args.get('category_id', '')

    query = "SELECT * FROM product WHERE name LIKE %s"
    params = ['%' + search_query + '%']

    if category_id:
        query += " AND category_id = %s"
        params.append(category_id)

    cur = mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)
    cur.execute(query, params)
    products = cur.fetchall()
    cur.close()

    # Fetch categories for the dropdown
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM category")  # Adjusted to the correct table name
    categories = cur.fetchall()
    cur.close()

    return render_template('client_home.html', products=products, categories=categories)





@app.route('/product/<int:product_id>')
def product_details(product_id):
    cur = mysql.connection.cursor(cursorclass=MySQLdb.cursors.DictCursor)  # Use a dict cursor
    cur.execute("SELECT * FROM product WHERE id = %s", (product_id,))
    product = cur.fetchone()
    cur.close()

    if not product:
        return "Product not found", 404  # If no product is found, return a 404 error

    # If your categories are stored with names in a separate table, join them and fetch the name
    # If not, ensure that your template uses `product.category_id` or similar
    cur = mysql.connection.cursor()
    cur.execute("SELECT name FROM category WHERE id = %s", (product['category_id'],))
    category_name = cur.fetchone()
    if category_name:
        product['category_name'] = category_name[0]
    cur.close()

    return render_template('product_details.html', product=product)

@app.route('/add-command', methods=['GET', 'POST'])
def add_command():
    if request.method == 'POST':
        product_name = request.form['product_name']
        phone_number = request.form['phone']

        # Insert the command into the database
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO commands (product_name, phone_number) VALUES (%s, %s)", (product_name, phone_number))
        mysql.connection.commit()
        cur.close()
        
        return redirect(url_for('home'))  # Redirect to home after command is added
    else:
        # This else block might seem unnecessary here as we now handle product selection on another page
        product_name = request.args.get('product_name', '')
        return render_template('add_command.html', product_name=product_name)
    
@app.route('/select-product', methods=['GET'])
def select_product():
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT id, name FROM product")
    products = cur.fetchall()
    cur.close()
    return render_template('select_product.html', products=products)

@app.route('/owner-login', methods=['GET', 'POST'])
def owner_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Here you should check the credentials against your database or predefined values
        if username == "admin" and password == "ahmed":
            return redirect(url_for('home'))  # Redirect to home if credentials are correct
        else:
            return "Échec de la connexion!"  # Return an error message if credentials are wrong
    return render_template('authentification.html')  # Render the login form for owners

@app.route('/delete-command/<int:command_id>', methods=['POST'])
def delete_command(command_id):
    cur = mysql.connection.cursor()
    try:
        cur.execute("DELETE FROM commands WHERE id = %s", (command_id,))
        mysql.connection.commit()
        flash('Command deleted successfully!', 'success')
    except Exception as e:
        mysql.connection.rollback()
        flash('Failed to delete command.', 'error')
        print(f"Error: {e}")  # Debugging: Output error to console
    finally:
        cur.close()
    
    return redirect(url_for('home'))

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)
