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

def do_signup(details):
  with engine.connect() as conn:
    data = [{"val1": details['email'],"val2": details['name'],"val3": details['pass']}]
    conn.execute(text("insert into signin (email,username,pass) values (:val1,:val2,:val3)"),data)
    conn.commit()
  return

def load_admin():
  with engine.connect() as conn:
    result = conn.execute(text("select * from admin"))

    
    ad = []
    for row in result.all():
      ad.append(row._asdict())
      
  return ad