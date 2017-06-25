
""" Module summary:
Functions:
  showIndex - Show site home.
"""

from flask import Blueprint, render_template
from flask import session as login_session

from sqlalchemy import asc

############################################################################

index = Blueprint("index", __name__)

@index.route("/")
def showIndex():
  """Show site home."""
  user_id = login_session.get("user_id")
  username = login_session.get("username")

  return render_template("index.html",
                         username=username)
