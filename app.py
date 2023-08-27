from flask import Flask, render_template,jsonify, request, redirect, url_for
from database import load_signin, load_user, do_signup, load_admin, check_user, check_admin

app = Flask(__name__)


@app.route("/")
def hello_world():
  return render_template('home.html')

@app.route("/api/users")
def load_all_users():
  users = load_signin()
  return jsonify(users)

@app.route("/SignIn")
def hello_world2():
  return render_template('login.html')

'''@app.route("/SignIn/<id>")
def show_user(id):
  user = load_user(id)
  if not user:
    return "Not Found"
  return render_template('user.html', user=user)'''

@app.route("/student/<id>")
def student(id):
  user = load_user(id)
  return render_template('user.html',user=user)

@app.route("/admin/<id>")
def ad(id):
  admin = load_admin(id)
  return render_template('admin.html',admin=admin)

@app.route("/SignIn/welcome", methods=['post'])
def welcome_user():
  data = request.form
  global user_id,admin_id
  user_id = check_user(data)
  admin_id = check_admin(data)

  if user_id:
    return redirect(url_for('student',id=user_id))
  elif admin_id:
    return redirect(url_for('ad',id=admin_id))
  else:
    return "Incorrect email or password"


@app.route("/signup")
def signup():
  return render_template('signup.html')

@app.route("/signup/success", methods=['post'])
def signup_done():
  data = request.form
  do_signup(data)
  admin = load_admin(admin_id)
  return render_template('signup_done.html',admin=admin)




if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
