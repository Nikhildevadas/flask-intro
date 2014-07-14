from flask import Flask, render_template,redirect,url_for,request,session,flash,g
from functools import wraps
import sqlite3

app=Flask(__name__)
app.secret_key ="my precious"
app.database="blog.db"
def login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			flash('you need to login first...!!')
			return redirect(url_for('login'))
	return wrap

@app.route('/')
@login_required
def show():
	
	cur = g.db.execute('select * from posts')
	posts=[dict(title=row[0], description=row[1]) for row in cur.fetchall()]
	print posts
	return render_template("index.html",posts=posts)
@app.route('/welcome')
def welcome():
	return render_template("welcome.html")

@app.route('/login',methods=['GET','POST'])
def login():
	error=None
	if request.method=='POST':
		if request.form['username']!='admin' or request.form['password'] != 'admin':
			error= "invalid...!! please try again..."
		else:
			session['logged_in']=True
			flash('you were just logged in..!!')
			return redirect(url_for('blog'))
	return render_template('login.html',error=error)

@app.before_request
def before_request():
	g.db=sqlite3.connect("blog.db")
	
@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

@app.route('/logout')
@login_required
def logout():
	session.pop('logged_in',None)
	flash("you were just logged out..!!!")
	return redirect(url_for('welcome'))

@app.route('/blog',methods=['GET','POST'])
@login_required
def blog():
	if request.method=="POST":
		x= request.form["header"]
		y=request.form["details"]
		g.db.execute("INSERT INTO posts values(?,?)", [x,y])
		g.db.commit()
		flash('new entry was sucessfully posted')
		return redirect(url_for('blog'))
	return render_template("blog.html")


if __name__=='__main__':
	app.run(debug=True)
