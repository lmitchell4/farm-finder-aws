
""" Module summary:
Classes:
  User - Class for table containing user information.
  Farm - Class for table containing farm information.
  CatalogItem - Class for table containing catalog item information.
  Event - Class for table containing event information.
"""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects.sqlite import TEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
# from sqlalchemy_imageattach.entity import Image, image_attachment

############################################################################


Base = declarative_base()

## Item categories:
itemCategories = ["Fruit and Vegetables",
                  "Nuts and Legumes",
                  "Protein",
                  "Home-made Goods",
                  "Other"]


class User(Base):
  """Class for table containing user information."""
  
  __tablename__ = "user"

  id = Column(Integer, primary_key=True)
  name = Column(String(250), nullable=False)
  email = Column(String(250), nullable=False)
  
  @property
  def serialize(self):
    """Return object data in easily serializeable format."""
    return {
      "id": self.id,
      "name": self.name,
      "email": self.email
    }


class Farm(Base):
  """Class for table containing farm information."""
  
  __tablename__ = "farm"
 
  id = Column(Integer, primary_key=True)
  name = Column(String(250), nullable=False)
  user_id = Column(Integer, ForeignKey("user.id"))
  user = relationship(User)
  location = Column(String(250))
  contact = Column(TEXT)
  description = Column(TEXT)
  picture = Column(String(250))
  
  @property
  def serialize(self):
    """ Return object data in easily serializeable format."""
    return {
      "id": self.id,
      "name": self.name,
      "user": self.user.name,
      "location": self.location,
      "contact": self.contact,
      "description": self.description
      # ,
      # "picture": self.picture
    }


class CatalogItem(Base):
  """Class for table containing catalog item information."""

  __tablename__ = "catalog_item"

  id = Column(Integer, primary_key=True)
  name = Column(String(80), nullable=False)
  description = Column(String(250))
  price = Column(String(8))
  category = Column(String(250))
  farm_id = Column(Integer,ForeignKey("farm.id"))
  farm = relationship(Farm)
  user_id = Column(Integer, ForeignKey("user.id"))
  user = relationship(User)
  picture = Column(String(250))
  
  @property
  def serialize(self):
    """Return object data in easily serializeable format."""
    return {
      "id": self.id,
      "name": self.name,
      "description": self.description,
      "price": self.price,
      "category": self.category,
      "farm_id": self.farm_id,
      "farm": self.farm.name,
      "user": self.user.name,
      "picture": self.picture
    }


class Event(Base):
  """Class for table containing event information."""

  __tablename__ = "event"

  id = Column(Integer, primary_key=True)
  name =Column(String(80), nullable=False)
  description = Column(String(250))
  farm_id = Column(Integer,ForeignKey("farm.id"))
  farm = relationship(Farm)
  user_id = Column(Integer, ForeignKey("user.id"))
  user = relationship(User)
  
  @property
  def serialize(self):
    """Return object data in easily serializeable format."""
    return {
      "id": self.id,
      "name": self.name,
      "description": self.description,
      "farm_id": self.farm_id,
      "farm": self.farm.name,
      "user": self.user.name
    }


if __name__ == "__main__":
  engine = create_engine("sqlite:///farmfinder.db")
  Base.metadata.create_all(engine)
