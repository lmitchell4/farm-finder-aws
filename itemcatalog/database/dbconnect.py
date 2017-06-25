
""" Module summary:
Variables:
  db_session - A connection to the farmfinder database.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dbsetup import Base

############################################################################


# Connect to database and create database session:
engine = create_engine("sqlite:///itemcatalog/database/farmfinder.db")
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
db_session = DBSession()