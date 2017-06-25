
""" Module summary:
Functions:
  errorShow - Page for when there is an error.
"""

from flask import Blueprint, render_template
from flask import session as login_session

############################################################################

error = Blueprint("error", __name__)

@error.route("/error")
def errorShow():
  """Page for when there is an error."""
  username = login_session.get("username")

  return render_template("error.html", username=username)
