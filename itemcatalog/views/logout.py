
""" Module summary:
Functions:
  clearsession - Clear the session information.
  gdisconnect - Disconnect from user's Google account.
"""

import httplib2
import json

from flask import Blueprint, request, redirect, url_for, flash, make_response
from flask import session as login_session

from itemcatalog.database.dbconnect import db_session

############################################################################

logout = Blueprint("logout", __name__)

@logout.route("/clearSession")
def clearsession():
  """Clear the session information."""
  login_session.clear()
  return "ok"


@logout.route("/gdisconnect", methods=["GET","POST"])
def gdisconnect():
  """Disconnect from user's Google account."""
  # Only disconnect a connected user.
  credentials = login_session.get("credentials")

  if credentials is None:
    response = make_response(
        json.dumps("Current user not connected."), 401)
    response.headers["Content-type"] = "application/json"
    return response

  # Execute HTTP Get request to revoke current token.
  #access_token = credentials.access_token
  access_token = login_session["access_token"]
  url = ("https://accounts.google.com/o/oauth2/revoke?token=%s"
          % access_token)
  h = httplib2.Http()

  # print "This is the user's session just before gdisconnect() starts: ", login_session
  # print "In gdisconnect access token is %s", access_token
  # results=h.request(url, "GET")
  # i=1
  # for r in results:
    # print i
    # print r
    # i+=1

  # #credentials.revoke(httplib2.Http())
  # result = results[0] #h.request(url, "GET")[0]
  # print "SHOWING RESULT: "
  # print result

  login_session.clear()
  return redirect(url_for("farm.farmsShowAll"))
