from sqlalchemy import create_engine, text

engine = create_engine("mysql+pymysql://sql6642397:YR1kqzCbEX@sql6.freesqldatabase.com/sql6642397?charset=utf8mb4")

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