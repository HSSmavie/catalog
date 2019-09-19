from flask import Flask,redirect,url_for,render_template,request,flash
from flask_mail import Mail,Message
from random import randint
from project_database import Register,Base,User
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from flask_login import LoginManager,login_user,current_user,logout_user,login_required,UserMixin

#engine=create_engine('sqlite:///iiit.db')
engine=create_engine('sqlite:///iii.db',connect_args={'check_same_thread':False},echo=True)
Base.metadata.bind=engine
DBsession=sessionmaker(bind=engine)
session=DBsession()

app=Flask(__name__)

login_manager=LoginManager(app)
login_manager.login_view='login'
login_manager.login_message_category='info'

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']='N151255@rguktn.ac.in'
app.config['MAIL_PASSWORD']='YouNeverKnowIt4Life'
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True

app.secret_key='abc'

mail=Mail(app)
otp=randint(000000,999999)
#@app.route("/sample")
def demo():
    return "Welcome to RGUKT"
app.add_url_rule('/sample','hello',demo)

@app.route("/demo_msg")
def d():
    return "<h1>Hello Demo Page</h1>"

@app.route("/info/details")
def a():
    return "Hello details"

@app.route("/details/<name>/<int:age>/<float:sal>")
def info(name,age,sal):
    return "hello {} and {} and {}".format(name,age,sal)

@app.route("/adm")
def mam():
    return "Hi mam"
def admin():
    return "Hello Admin"


@app.route("/student")
def student():
    return "Hello Student"

@app.route("/staff")
def staff():
    return "Hello staff"

@app.route("/info/<name>")
def admin_info(name):
    if name=='admin':
        return redirect(url_for('admin'))
    elif name=='student':
        return redirect(url_for('student'))
    elif name=='staff':
        return redirect(url_for('staff'))
    else:
        return "No url"

@app.route("/data/<name>/<int:age>/<float:sal>")
def demo_html(name,age,sal):
    return render_template('sample.html',n=name,a=age,s=sal)

@app.route("/trable")
def demo_table():
    name="hema"
    age="20"
    sal="124254425.3242"
    return render_template('sample_1.html',n=name,a=age,s=sal)

data=[{'name':'Hema','age':20,'sal':123343432.341},{'name':'Devi','age':20,'sal':123343413432.341},{'name':'Sushmitha','age':20,'sal':34123123343432.341},{'name':'Anitha','age':20,'sal':234123343432.341}]
@app.route("/dummy_data")
def demo_dummy():
    return render_template('sample_2.html',d=data)


@app.route("/num_tab/<int:num>")
def numtab_info(num):
    return render_template('sample_3.html',n=num)

@app.route("/file_upload",methods=['GET','POST'])
def file_upload():
    return render_template("file_upload.html")

@app.route("/success",methods=['GET','POST'])
def success():
    if request.method=='POST':
        f=request.files['file']
        f.save(f.filename)

        return render_template("success.html",f_name=f.filename)

@app.route("/email",methods=['POST','GET'])
def email_send():
    return render_template("email.html")

@app.route("/email_verify",methods=['POST','GET'])
def verify_email():
    email=request.form['email']
    msg=Message("One Time Password",sender="N151255@rguktn.ac.in",recipients=[email])
    msg.body=str(otp)
    mail.send(msg)
    return render_template("v_email.html")

@app.route("/email_success",methods=['POST','GET'])
def success_email():
    user_otp=request.form['otp']
    if otp==int(user_otp):
        return render_template("email_success.html")
    return "Invalid OTP"

#DATABASE
@app.route("/show")
def showData():
    register=session.query(Register).all()
    return render_template('show.html',reg=register)

@app.route("/login")
def loginData():
     
    return render_template('login.html')


@app.route("/account",methods=['POST','GET'])
@login_required
def account():
     
    return render_template('account.html')

@app.route("/reg",methods=['POST','GET'])
def reg():
    if request.method=='POST':
        userData=User(name=request.form['name'],
            email=request.form['email'],
            password=request.form['password'],
        session.add(userData)
        session.commit()
        return redirect(url_for('navData'))
    else:
        return render_template('register.html')


@app.route("/new",methods=['POST','GET'])
def addData():
    if request.method=='POST':
        newData=Register(name=request.form['name'],
            surname=request.form['surname'],
            mobile=request.form['mobile'],
            email=request.form['email'],
            branch=request.form['branch'],
            roll=request.form['roll'])
        session.add(newData)
        session.commit()
        flash("New Data added...")
        return redirect(url_for('showData'))
    else:
        return render_template('new.html')

@app.route("/navigation")
def navData():
    return render_template('navigation.html')

@app.route("/edit/<int:register_id>",methods=['POST','GET'])
def editData(register_id):
    editedData=session.query(Register).filter_by(id=register_id).one()
    if request.method=='POST':
        editedData.name=request.form['name']
        editedData.surname=request.form['surname']
        editedData.mobile=request.form['mobile']
        editedData.email=request.form['email']
        editedData.branch=request.form['branch']
        editedData.roll=request.form['roll']

        session.add(editedData)
        session.commit()
        flash("Data edited...{}".format(editedData.name))

        return redirect(url_for('showData'))

    else:
        return render_template('edit.html',register=editedData)

@app.route("/delete/<int:register_id>",methods=['POST','GET'])
def deleteData(register_id):
    deletedData=session.query(Register).filter_by(id=register_id).one()
    if request.method=='POST':
        
        session.delete(deletedData)
        session.commit()
        flash("Data Deleted...{}".format(deletedData.name))

        return redirect(url_for('showData'))
    else:
        return render_template('delete.html',register=deletedData)

@app.route("/login",methods=['POST','GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('showData'))

    try:
        if request.method=='POST':
            user=session.query(User).filter_by(email=request.form['email'],password=request.form['password']).first()

            if user:
                login_user(user)
                return redirect(url_for('showData'))
            else:
                flash("Invalid login..")
        else:
            return render_template('login.html',title="login")
    except Exception as e:
        flash("Login Failed...")

    else:
        return render_template('login.html',title='login')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('navData'))

@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(int(user_id))


if __name__=='__main__':
    app.run(debug=True)