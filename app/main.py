from flask import Flask, render_template, redirect, url_for, request, session
import sqlite3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'secret'
app.config['UPLOAD_FOLDER'] = 'uploads'
ALLOWED_EXTENSIONS = {'py'}


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def get_file_status(filename):
    conn = sqlite3.connect('../files.db')
    c = conn.cursor()
    c.execute('SELECT status FROM files WHERE filename = ?', (filename,))
    status = c.fetchone()
    conn.close()
    if status:
        return status[0]
    else:
        return 'new'

def save_file(filename, status):
    conn = sqlite3.connect('../files.db')
    c = conn.cursor()
    c.execute('INSERT INTO files (filename, status) VALUES (?, ?)', (filename, status))
    conn.commit()
    conn.close()

def update_file_status(filename, status):
    conn = sqlite3.connect('../files.db')
    c = conn.cursor()
    c.execute('UPDATE files SET status = ? WHERE filename = ?', (status, filename))
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = sqlite3.connect('../users.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (email, password) VALUES (?, ?)",
                  (email, password))
        conn.commit()
        conn.close()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'email' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            status = get_file_status(filename)
            if status == 'new':
                save_file(filename, 'uploaded')
            else:
                update_file_status(filename, 'updated')
            return redirect(url_for('files'))
        else:
            return render_template('upload.html', error='Invalid file type')
    return render_template('upload.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        conn = sqlite3.connect('../users.db')
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE email = ? AND password = ?',
                  (email, password))
        user = c.fetchone()
        conn.close()
        if user:
            session['email'] = email
            return redirect(url_for('profile'))
        else:
            return render_template('login.html', error='Invalid email or password')
    return render_template('login.html')

@app.route('/delete/<filename>')
def delete(filename):
    if 'email' not in session:
        return redirect(url_for('login'))
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    conn = sqlite3.connect('../files.db')
    c = conn.cursor()
    c.execute('DELETE FROM files WHERE filename = ?', (filename,))
    conn.commit()
    conn.close()
    return redirect(url_for('files'))

@app.route('/clear')
def clear():
    if 'email' not in session:
        return redirect(url_for('login'))
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    conn = sqlite3.connect('../files.db')
    c = conn.cursor()
    c.execute('DELETE FROM files')
    conn.commit()
    conn.close()
    return redirect(url_for('files'))

@app.route('/files')
def files():
    if 'email' not in session:
        return redirect(url_for('login'))
    conn = sqlite3.connect('../files.db')
    c = conn.cursor()
    c.execute('SELECT * FROM files')
    files = c.fetchall()
    conn.close()
    return render_template('files.html', files=files)

@app.route('/profile')
def profile():
    if 'email' in session:
        return render_template('profile.html', email=session['email'])
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)


