from flask import Flask, render_template,jsonify, request, redirect, url_for
from database import load_signin, load_user, do_signup, load_admin, check_user, check_admin, put_slip_request, load_slip, load_bridge_slip, pass_slip, load_pass_slip

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

@app.route("/SignIn/welcome/student/<id>")
def student(id):
  user = load_user(id)
  return render_template('user.html',user=user)

@app.route("/SignIn/welcome/admin/<id>")
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
  if admin_id:
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

#_____________________________________________________________
#USER

@app.route("/slip")
def slip_request():
  return render_template('passslip_form.html')

@app.route("/slip/requested", methods=['post'])
def slip_requested():
  data = request.form
  req_list = [user_id,data]
  slip = put_slip_request(req_list)
  user = user_id
  return render_template('slip_requested.html',user=user,slip=slip)

@app.route("/slip/view")
def slip_view():
  slip = load_pass_slip(user_id)
  if not slip:
    return "No slips issued currently"
  return render_template('view_slip.html',slips=slip)


#________________________________________________________________
#ADMIN

@app.route("/ad_slip")
def ad_slipy():
  slip_data = load_bridge_slip()
  return render_template('slipdata.html',slips=slip_data)

@app.route("/ad_slip/slips_checked",methods=['post'])
def slips_approved():
  passed = request.form.getlist('allow')
  not_passed = request.form.getlist('deny')
  pass_slip(passed,not_passed)
  return redirect("/ad_slip")
  


if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
