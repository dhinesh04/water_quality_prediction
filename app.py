from flask import Flask, request, render_template, redirect
from flask_mysqldb import MySQL

app=Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'waterquality'

mysql = MySQL(app)
import pickle
model = pickle.load(open('waterquality.pkl', 'rb'))

@app.route('/form', methods=['GET','POST'])
def input():
    msg=""
    if request.method=="POST":
        details=request.form
        ph = float(details['pH'])
        hardness = float(details['Hardness'])
        solids = float(details['Solids'])
        chloramines = float(details['Chloramines'])
        sulfate = float(details['Sulfate'])
        conductivity = float(details['Conductivity'])
        organic_carbon = float(details['Organic_carbon'])
        trihalomethanes = float(details['Trihalomethanes'])
        turbidity = float(details['Turbidity'])
        
        predict=model.predict([[ph, hardness, solids, chloramines, sulfate, conductivity,
        organic_carbon, trihalomethanes, turbidity]])
        if predict[0]==0:
            msg="Water is safe to drink"
            return render_template('output_safe.html',msg=msg)

        elif predict[0]==1:
            msg="Water is not safe"
            return render_template('output_unsafe.html', msg=msg)

@app.route('/register',methods=['POST','GET'])

def register():
    cur = mysql.connection.cursor()
    if request.method=='POST':
        datau=request.form['username']
        datap=request.form['password']
        cur.execute('INSERT INTO registration VALUES(%s,%s)',(datau,datap))
        mysql.connection.commit()
        cur.close()
        return redirect('/login')
    return render_template('register.html')

@app.route('/login',methods=['POST','GET'])
def login():
    cur = mysql.connection.cursor()
    if request.method=='POST':
        datau=request.form['username']
        datap=request.form['password']
        cur.execute('SELECT * FROM registration WHERE username=%s AND password=%s',(datau,datap))
        mysql.connection.commit()
        s=cur.fetchall()
        cur.close()
        if len(s)==0:
            return render_template('login.html')
        else:
            return render_template('dashboard.html')
    return render_template('login.html')

@app.route('/about')
def about():
    return render_template('about.html')
        

@app.route('/',methods=['POST','GET'])
def main():
    if request.method == 'POST':
        value = request.form
        if 'login' in value:
            return redirect('/login')
        elif 'register' in value:
            return redirect('/register')
    return render_template('home.html')

@app.route('/dashboard',methods=['POST','GET'])
def dashboard():
    if request.method=='POST':
        value = request.form
        if 'forms' in value:
            return render_template('form.html')
        elif 'know_more' in value:
            return redirect('/about')

if __name__ == '__main__':
    app.run(debug=True)