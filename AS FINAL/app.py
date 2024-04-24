from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

def is_filename_malicious(filename):
    return "malicious" in filename.lower()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        # Fetch form data
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        age = request.form['age']
        email = request.form['email']
        contact_no = request.form['contactNo']
        city = request.form['city']
        pdf_file = request.files['pdfFile']

        # Check if the filename is malicious
        if is_filename_malicious(pdf_file.filename):
            return render_template('maldet.html')

        # Save file
        filename = pdf_file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        pdf_file.save(file_path)

        # Store data in the database (replace with your MySQL connection code)
        # Example: MySQLdb or SQLAlchemy can be used for database operations
        # Example with MySQLdb:
        import MySQLdb
        conn = MySQLdb.connect(host='localhost', user='root', password='', database='registration_db')
        cursor = conn.cursor()
        sql = "INSERT INTO registrations (first_name, last_name, age, email, contact_no, city, pdf_file) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (first_name, last_name, age, email, contact_no, city, filename))
        conn.commit()
        conn.close()

        return render_template('uploadsuccessful.html')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
