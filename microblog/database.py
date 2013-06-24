from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

uri = os.environ.get('DATABASE_URL', 'postgres://ozurdipdktghmd:wj1PDha64vao_Ekf5NvuJpYV_0@ec2-54-225-96-191.compute-1.amazonaws.com:5432/d6c9qd41ct33l5')
#postgres://username:password@host:port/database'

engine = create_engine(uri, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
					 autoflush=False,
					 bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
  import microblog.models
  Base.metadata.create_all(bind=engine)
