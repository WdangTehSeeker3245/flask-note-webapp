from flask import Flask,render_template,request,redirect,url_for,jsonify,session
from flask_bcrypt import Bcrypt
from flask_mysqldb import MySQL,MySQLdb
import json

app = Flask(__name__)
bcrypt = Bcrypt(app)

# Change this to your secret key
app.secret_key = 'dummytestapp74'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'adminizaus74'
app.config['MYSQL_DB'] = 'flasknote_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# Intialize MySQL
mysql = MySQL(app)

#### App Route ####
@app.route('/', methods=['GET','POST'])
def login():
    if request.method == 'POST' and 'password' in request.form:
        email = 'faizaln77izaus@gmail.com'
        password = request.form['password']

        # Checking User
        try:
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("SELECT * FROM usermynote WHERE email=%s",(email,))
            user = cur.fetchone()
            pswd = user['password']
            if user:
                authenticated_user = bcrypt.check_password_hash(pswd, password)
                if authenticated_user:
                    session['username'] = user['username']
                    return redirect(url_for('home'))
                else:
                    msg='password false'
                    return render_template('login.html',msg=msg)
            else:
                msg='user not found'
                return render_template('login.html',msg=msg)
        except Exception as e:
            print(e)
        
        
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    session['log'] = 'out'
    return redirect(url_for('login'))

@app.route('/home')
def home():
    try :
        username = session['username']
        police = 'you are not allowed to access this page'
        if username :
            session['log'] = 'in'
            return render_template('home.html')
        else :
            return render_template('people-police.html',police=police)
    except :
        police = 'you are not allowed to access this page'
        return render_template('people-police.html',police=police)

@app.route('/backup')
def backup():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM mynotes')
    data = cur.fetchall()
    with open('backup/mynotes.json', 'w') as f:
        json.dump(data, f)

    return redirect(url_for('home'))
    
@app.route('/searchnote')
def searchnote():
    try :
        username = session['username']
        police = 'you are not allowed to access this page'
        if username :
            query = request.args.get('q')
            return render_template('searchnote.html',query=query)
        else :
            return render_template('people-police.html',police=police)
    except :
        police = 'you are not allowed to access this page'
        return render_template('people-police.html',police=police)

@app.route('/addnote',methods=['GET','POST'])
def addnote():
    try :
        username = session['username']
        police = 'you are not allowed to access this page'
        if username :
            return render_template('addnote.html')
        else :
            return render_template('people-police.html',police=police)
    except :
        police = 'you are not allowed to access this page'
        return render_template('people-police.html',police=police)

@app.route('/viewnote/<id>',methods=['GET'])
def viewnote(id):
    id_note = id
    try:
        username = session['username']
        police = 'you are not allowed to access this page'
        if username :
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute('SELECT * FROM mynotes WHERE id_note=%s',(id_note,))
            data = cur.fetchone()
            return render_template('viewnote.html',data=data)
        else :
            return render_template('people-police.html',police=police)

    except Exception as e:
        print(e)
        police = 'you are not allowed to access this page'
        return render_template('people-police.html',police=police)


@app.route('/editnote/<id>', methods=['GET','POST'])
def editnote(id):
    id_note = id
    try:
        username = session['username']
        police = 'you are not allowed to access this page'
        if username :
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute('SELECT * FROM mynotes WHERE id_note=%s',(id_note,))
            data = cur.fetchone()
            return render_template('editnote.html',data=data)
    except Exception as e:
        print(e)
        police = 'you are not allowed to access this page'
        return render_template('people-police.html',police=police)

@app.route('/deletenote/<id>', methods=['GET'])
def deletenote(id):
    id_note = id
    try:
        username = session['username']
        police = 'you are not allowed to access this page'
        if username :
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute('DELETE FROM mynotes WHERE id_note=%s',(id_note,))
            mysql.connection.commit()
            return render_template('viewnote.html')
    except Exception as e:
        print(e)
        police = 'you are not allowed to access this page'
        return render_template('people-police.html',police=police)


#### AJAX route ####
@app.route('/ajax/fetchnote', methods=['GET'])
def ajaxfetchnote():
    try:
        username = session['username']
        police = 'you are not allowed to access this page'
        if username :
            cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cur.execute('SELECT * FROM mynotes')
            data = cur.fetchall()
            return jsonify(data)
    except Exception as e:
        print(e)
        police = 'you are not allowed to access this page'
        return render_template('people-police.html',police=police)


@app.route('/ajax/insertnote', methods=['POST'])
def ajaxinsertnote():
    if request.method == 'POST':
        data = request.get_json()
        try:
            username = session['username']
            police = 'you are not allowed to access this page'
            if username :
                title =  data['title']
                note = data['note']
                cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cur.execute('INSERT INTO mynotes (title_note,html_note) VALUES (%s,%s)',(title,note))
                mysql.connection.commit()
                msg = {
                    'msg':'Note Created Successfully'
                }
                return jsonify(msg)
        except Exception as e:
            print(e)
            police = 'you are not allowed to access this page'
            return render_template('people-police.html',police=police)
    else:
        msg = {
            'msg':'Some error in request data'
        }
        return jsonify(msg)

@app.route('/ajax/updatenote', methods=['POST'])
def ajaxupdatenote():
    if request.method == 'POST':
        data = request.get_json()
        try:
            username = session['username']
            police = 'you are not allowed to access this page'
            if username :
                id = data['id']
                title =  data['title']
                note = data['note']
                cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cur.execute('UPDATE mynotes SET title_note=%s, html_note=%s WHERE id_note=%s',(title,note,id))
                mysql.connection.commit()
                msg = {
                    'msg':'Note Edited Successfully'
                }
                return jsonify(msg)
        except Exception as e:
            print(e)
            police = 'you are not allowed to access this page'
            return render_template('people-police.html',police=police)
    else:
        msg = {
            'msg':'Some error in request data'
        }
        return jsonify(msg)

@app.route('/ajax/findnote', methods=['POST'])
def ajaxfindnote():
    if request.method == 'POST':
        data = request.get_json()
        try:
            username = session['username']
            police = 'you are not allowed to access this page'
            if username :
                query = data['query']
                q = '%'+query+'%'
                q2 = q
                cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                # cur.execute("SELECT * FROM mynotes WHERE title_note LIKE %s",(q,))
                cur.execute("SELECT * FROM mynotes WHERE title_note LIKE %s OR html_note LIKE %s",(q,q2))
                data = cur.fetchall()
                return jsonify(data)
        except Exception as e:
            print(e)
            police = 'you are not allowed to access this page'
            return render_template('people-police.html',police=police)
    else:
        msg = {
            'msg':'Some error in request data'
        }
        return jsonify(msg)

if __name__ == '__main__':
    app.run(debug=True)
