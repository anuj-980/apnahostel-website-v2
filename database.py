from sqlalchemy import create_engine, text
import os

db_connection_str = os.environ['DB_CONN_STR']

engine = create_engine(db_connection_str)

def load_signin():
  with engine.connect() as conn:
    result = conn.execute(text("select * from signin"))

    
    user = []
    for row in result.all():
      user.append(row._asdict())

  return user

def load_user(id):
  with engine.connect() as conn:
    result = conn.execute(
      text("SELECT * FROM signin WHERE id=:val"),{"val": id})
    rows = result.all()
    if len(rows) == 0:
      return None
    else:
      return rows[0]._asdict()

def load_admin(id):
  with engine.connect() as conn:
    result = conn.execute(
      text("SELECT * FROM admin WHERE id=:val"),{"val": id})
    rows = result.all()
    if len(rows) == 0:
      return None
    else:
      return rows[0]._asdict()

def do_signup(details):
  with engine.connect() as conn:
    data = [{"val1": details['email'],"val2": details['name'],"val3": details['pass']}]
    conn.execute(text("insert into signin (email,username,pass) values (:val1,:val2,:val3)"),data)
    conn.commit()
  return

def load_admins():
  with engine.connect() as conn:
    result = conn.execute(text("select * from admin"))

    
    ad = []
    for row in result.all():
      ad.append(row._asdict())
      
  return ad

def check_admin(data):
  admins = load_admins()

  for j in admins:
    if data['email'] == j['ad_email'] and data['pass'] == j['ad_pass']:
      admin=j['id']
      return admin
      break
  else:
    return 0

def check_user(data):
  users = load_signin()
  
  for i in users:
    if data['email'] == i['email'] and data['pass'] == i['pass']:
      user=i['id']
      return user
      break
  else:
    return 0


def put_slip_request(details):
  with engine.connect() as conn:
    id = details[0]
    data = details[1]
    qry_data = [{"val1": id,"val2": data['std_name'],"val3": data['place'],"val4": data['address'],"val5": data['time_go'],"val6": data['time_in'],"val7": data['hostel_name'],"val8": data['clg_name'],"val9": data['room_no']}]
    conn.execute(text("insert into bridge_slip (id,std_name,place,address,time_go,time_in,hostel_name,clg_name,room_no) values (:val1,:val2,:val3,:val4,:val5,:val6,:val7,:val8,:val9)"),qry_data)
    conn.commit()
    
    result = conn.execute(
      text("SELECT * FROM bridge_slip WHERE id=:val"),{"val": id})
    rows = result.all()
    if len(rows) == 0:
      return None
    else:
      slip = rows[len(rows)-1]._asdict()

    slip_id = slip['slip_id']
  return slip_id

def load_slip(s_id):
  with engine.connect() as conn:
    result = conn.execute(
      text("SELECT * FROM bridge_slip WHERE slip_id=:val"),{"val": s_id})
    rows = result.all()
    if len(rows) == 0:
      return None
    else:
      return rows[0]._asdict()

def load_bridge_slip():
  with engine.connect() as conn:
    result = conn.execute(
      text("SELECT * FROM bridge_slip"))
    slips = []
    for row in result.all():
      slips.append(row._asdict())

  return slips

def pass_slip(passed_list,reject_list):
  with engine.connect() as conn:
    qry1 = "insert into pass_slip select * from bridge_slip where slip_id=:val"
    qry2 = "delete from bridge_slip where slip_id=:val"
    for i in passed_list:
      conn.execute(text(qry1),{"val":i})
      conn.execute(text(qry2),{"val":i})
      conn.commit()

    for j in reject_list:
      conn.execute(text(qry2),{"val":j})
      conn.commit()
      
    return