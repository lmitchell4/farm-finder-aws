
""" Module summary:
Generate dummy data to populate the farmfinder database.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from dbsetup import Farm, Base, CatalogItem, User, Event, itemCategories

############################################################################


# Connect to database and create database session:
engine = create_engine("sqlite:///farmfinder.db")
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create dummy user
User1 = User(name="Robo Barista",
              email="tinnyTim@udacity.com")
session.add(User1)
session.commit()

# Farm 1:
farm1 = Farm(user_id=1, name="Fake Town Community Garden",
  location="On the corner of Spring Ave and E Street in Fake Town",
  description="""This is a communal garden run by local volunteers. Volunteers get the first pick of crops, but the rest we sell to the community. Proceeds go towards maintaining the garden - buying tools, supplies for building raised beds, etc.""",
  picture="1_seedling.png")

session.add(farm1)
session.commit()

item1 = CatalogItem(user_id=1,
  name="Fennel",
  description="Bulb, stalk, leaves, and all.",
  price="$0.50 per lb",
  category=itemCategories[0],
  farm=farm1)

session.add(item1)
session.commit()

item2 = CatalogItem(user_id=1,
  name="Garlic",
  description="Available the second day of the third week of every month.",
  price="$0.60 per head",
  category=itemCategories[0],
  farm=farm1)

session.add(item2)
session.commit()

item3 = CatalogItem(user_id=1,
  name="Collard Greens",
  description="This is our most abundant crop, and it's available year-round. Goes well in soups and casseroles.",
  price="$5.00",
  category=itemCategories[0],
  farm=farm1)

session.add(item3)
session.commit()

item4 = CatalogItem(user_id=1,
  name="Whole Wheat Flour",
  description="We grow the wheat in the community garden and one of our volunteers grinds it. Great for baking home-made breads.",
  price="$4.00 per lb",
  category=itemCategories[4],
  farm=farm1)

session.add(item4)
session.commit()

item5 = CatalogItem(user_id=1,
  name="Baked Goods",
  description="At the Fake Town Farmer's Market we sell breads and pies made with ingredients from our garden. See our events page for more information.",
  price="Typically between $6 and $10 depending on the item.",
  category=itemCategories[3],
  farm=farm1,
  picture="1_5_bread.png")

session.add(item5)
session.commit()


event1 = Event(user_id=1,
  name = "Fake Town Farmers' Market",
  description = "We're there every Sunday from 7 am to 11 am. Please stop by and support your community garden!",
  farm = farm1)

session.add(event1)
session.commit()



# Farm 2:
farm2 = Farm(user_id=1, name="Smith Family Farm",
  location="456 Fake Street, Fake Town, 27483",
  description="""We are a small family farm with 200 acres of fruit and nut trees. We have a stand that is open from 7 am to 8 pm Tuesday through Sunday.""",
  picture="2_avocado.png")

session.add(farm2)
session.commit()

item1 = CatalogItem(user_id=1,
  name="Macadamia Nuts",
  description="Your choice of in-the-shell or out-of-the-shell.",
  price="$5.00 per lb in-shell, $7.00 per lb shelled",
  category=itemCategories[1],
  farm=farm2)

session.add(item1)
session.commit()

item2 = CatalogItem(user_id=1,
  name="Avocados",
  description="Fresh, ripe, green, and delicious.",
  price="$2 per avocado",
  category=itemCategories[0],
  farm=farm2)

session.add(item2)
session.commit()

item3 = CatalogItem(user_id=1,
  name="Pistachios",
  description="Get 'em raw, salted, or roasted.",
  price="$5 per lb",
  category=itemCategories[1],
  farm=farm2)

session.add(item3)
session.commit()

item4 = CatalogItem(user_id=1,
  name="Pistachio Ice Cream",
  description="We love pistachios so much that we put them in everything. Try some pistachio ice cream, made right next to the field where the nuts were grown. ",
  price="$4 per pint",
  category=itemCategories[3],
  farm=farm2)

session.add(item4)
session.commit()



# Farm 3:
farm3 = Farm(user_id=1, name="Panda Garden",
  location="Fake Town",
  description="""I have a small backyard farm. I've been most successful at growing peppers, pumpkins, crookneck squash, and an accidental pepper-pumpkin hybrid.  I'm opening to bartering, especially for leafy green vegetables.""",
  picture="3_onion.png")

session.add(farm3)
session.commit()

item1 = CatalogItem(user_id=1,
  name="Bell Peppers",
  description="Red, yellow, or green.  Various sizes depending on the weather",
  price="$0.50 per lb or barter - make an offer!",
  category=itemCategories[0],
  farm=farm3)

session.add(item1)
session.commit()

item2 = CatalogItem(user_id=1,
  name="Pumpkins",
  description="Round and orange.",
  price="$3.50 per lb or barter - make an offer!",
  category=itemCategories[0],
  farm=farm3)

session.add(item2)
session.commit()

item3 = CatalogItem(user_id=1,
  name="Crookneck Squash",
  description="Yellow and smooth, or sometimes bumpy.",
  price="$3.00 per lb or barter - make an offer!",
  category=itemCategories[0],
  farm=farm3)

session.add(item3)
session.commit()



# Farm 4:
farm4 = Farm(user_id=1, name="Lemon Paradise",
  location="Fake Town",
  description="""The lemon and cherry trees in our backyard produce fruit faster than we can use it. We're happy to give the fruit away for free!""")

session.add(farm4)
session.commit()

item1 = CatalogItem(user_id=1,
  name="Lemons",
  description="Yellow and sour.",
  price="Free!",
  category=itemCategories[0],
  farm=farm4,
  picture="4_1_lemon.png")

session.add(item1)
session.commit()

item2 = CatalogItem(user_id=1,
  name="Lambert Cherries",
  description="Round and red-yellow.",
  price="Free!",
  category=itemCategories[0],
  farm=farm4,
  picture="4_2_cherry.png")

session.add(item2)
session.commit()


# Farm 5:
farm5 = Farm(user_id=1, name="Chicken Villa",
  location="Real Town",
  description="""We love raising and caring for chickens in our backyard.""")

session.add(farm5)
session.commit()

item1 = CatalogItem(user_id=1,
  name="Eggs",
  description="Oval and white (and brown and blue). From our happy, free-range backyard hens.",
  price="$2.00 per dozen",
  category=itemCategories[2],
  farm=farm5,
  picture="5_1_eggs.png")

session.add(item1)
session.commit()



print "added stuff to database!"