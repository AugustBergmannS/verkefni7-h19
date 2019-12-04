from flask import Flask, render_template, session, request
import pymysql

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Leyno'

conn = pymysql.connect(host='tsuts.tskoli.is', port=3306, user='0312023370', password='mypassword', database='0312023370_verk7')



#---------------------routes---------------------

@app.route('/')
def index():
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    p = cur.fetchall()
    
    for i in p:
        print(i[2])
    return render_template("index.tpl")

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        n = request.form['notandanafn']
        p = request.form['password']
    
    cur = conn.cursor()
    cur.execute("SELECT count(user) FROM users where user = %s and pass = %s",(n,p))
    p = cur.fetchone()
    if p[0] == 1:
        session['logged_in'] = n

        return render_template("allt_rett.tpl")
    else:
        return render_template("villa.tpl")

@app.route('/nyskraning')
def nyskra():
    return render_template("nyr_adgangur.tpl")

@app.route('/baetavid', methods=['GET','POST'])
def add():
    if request.method == 'POST':
        n = request.form['notandanafn']
        pw = request.form['password']
        nafn = request.form['nafn']

        cur = conn.cursor()
        cur.execute("SELECT count(*) FROM users where user = %s",(n))
        p = cur.fetchone()
        if p[0] != 1:
            cur.execute("INSERT INTO users(user,pass,nafn) VALUES(%s,%s,%s)",(n,pw,nafn))
            conn.commit()
            cur.close()
            return render_template("adgangur_kominn.tpl")
            
        else:
            return render_template("notandanafn_tekid.tpl")

@app.route('/buid_ad_utskra')
def utskra():
    taema = []
    session['logged_in'] = taema

    return render_template("buid_ad_utskra.tpl")

@app.route('/adgangar')
def vefur():
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    p = cur.fetchall()
    for i in p:
        if i[0] in session['logged_in']:
            nafn = i[2]
        
    return render_template("adgangar.tpl", p=p, n=nafn)


#-------------------run---------------------

@app.errorhandler(404)
def error404(error):
	return render_template("404.tpl"),404

if __name__ == "__main__":
	app.run(debug=True)