from flask import Flask, render_template,jsonify, request
from database import load_signin, load_user

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
  users = load_signin()
  return render_template('login.html', users=users)

'''@app.route("/SignIn/<id>")
def show_user(id):
  user = load_user(id)
  if not user:
    return "Not Found"
  return render_template('user.html', user=user)'''

@app.route("/SignIn/welcome", methods=['post'])
def welcome_user():
  data = request.form
  users = load_signin()

  for i in users:
    if data['email'] == i['email'] and data['pass'] == i['pass']:
      return render_template('user.html',user=i)
  else:
    return "Incorrect email or password"

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
