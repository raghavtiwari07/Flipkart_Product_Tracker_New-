from flask import Flask, render_template, request, flash, session
import sqlite3
from database_setup import get_db,close_connection,init_db
from firewall_security import security_scan
from main_2 import check_product_availability 
import os

app = Flask(__name__)

# Generate a random secret key
secret_key = os.urandom(24)
app.secret_key= secret_key
# Create an empty DataFrame to store user data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin_login', methods=['POST'])
def admin_login():
    admin_username = request.form['admin_username']
    admin_password = request.form['admin_password']
    
    # Check for security issues in the input data
    if not security_scan(admin_username) or not security_scan(admin_password):
        flash('Security issue detected in input data.')
        return render_template('index.html')
    
    # Check if the credentials match the expected values
    if admin_username == "parv" and admin_password == "parv123":
        # Allow access
        db = get_db()
        cursor = db.execute('SELECT * FROM user_data GROUP BY Email,username;')
        user_data = cursor.fetchall()
        return render_template('admin_login.html', user_data=user_data)
    else:
        # Deny access
        flash('!!! Invalid Credentials, Please try again.!!!')
        return render_template('index.html')


@app.route('/save_user_data', methods=['POST'])
def save_user_data():
    # global global_email  # Declare the global variable
    username = request.form['username']
    email = request.form['email']
    
    if not security_scan(username) or not security_scan(email):
        print(f"Security scan detected potential issues. username: {username}, email: {email}")
        flash('Security scan detected potential issues in your input.')
        return render_template('index.html')
    
    # Store email in session variable
    session['email'] = email
    # global_email = email  # Store the email in the global variable
    print("Connecting to database...")
    db = get_db()
    db.execute('INSERT INTO user_data (username, email) VALUES (?, ?)', [username,email])
    db.commit()
    print('User data saved successfully!')
    return render_template('enter_url.html')

@app.route('/check_product_availability', methods=['POST'])
def check_product_availability_route():
    
    product_url = request.form['url']
    # # Check for security issues in product URL
    if not security_scan(product_url):
        print(f"Security scan detected potential issues. username: {username}, email: {email}")
        flash('Security scan detected potential issues in your input.')
        return render_template('index.html')
    
    # global global_email  # Access the global variable
    global user_data
    # Get email from session variable
    recipient_email = session.get('email', None)
    if recipient_email is None:
        flash('Email not found.')
        return render_template('index.html')
    
    # product_url = request.form['url']
    # recipient_email = global_email  # Use the email from the global variable
    # recipient_email=request.form['email']
    result = check_product_availability(product_url,recipient_email)
    print(result)
    flash(result)
    return render_template("thankyou.html")

@app.route('/save_user_data_2', methods=['POST'])
def save_user_data_2():
    return render_template('enter_url.html')




    # Assuming you have code to send an email here

if __name__ == '__main__':
   
    app.run(debug=True)

