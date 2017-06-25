
""" Module summary:
Functions:
  showLogin - Load the login page.
  gconnect - Sign in to user's Google account.
"""

import random, string
import httplib2
import json
import requests

from flask import Blueprint, render_template, request, redirect, url_for
from flask import flash, make_response
from flask import session as login_session

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError

from itemcatalog.database.dbsetup import User
from itemcatalog.database.dbconnect import db_session
from itemcatalog.views.util import createUser, getUserID

############################################################################

login = Blueprint("login", __name__)

# Google API client id:
G_CLIENT_ID = json.loads(
    open("itemcatalog/client_secrets.json","r").read())["web"]["client_id"]


# Define url handlers:
@login.route("/login")
def showLogin():
  """Load the login page."""
  user_id = login_session.get("user_id")

  if user_id:
    return redirect(url_for("farm.farmsManage"))

  state = "".join(random.choice(string.ascii_uppercase +
                  string.digits) for x in xrange(32))
  login_session["state"] = state
  return render_template("login.html", STATE=state, G_CLIENT_ID=G_CLIENT_ID)


@login.route("/gconnect", methods=["POST"])
def gconnect():
  """Sign in to user's Google account."""
  if request.args.get("state") != login_session["state"]:
    response = make_response(json.dumps("Invalid state parameter"), 401)
    response.headers["Content-Type"] = "application/json"
    return response

  else:
    # Obtain authorization code
    code = request.data

    try:
      # Upgrade the authorization code into a credentials object
      oauth_flow = flow_from_clientsecrets("itemcatalog/client_secrets.json",
                                           scope="")
      oauth_flow.redirect_uri = "postmessage"
      credentials = oauth_flow.step2_exchange(code)

    except FlowExchangeError:
      response = make_response(
          json.dumps("Failed to upgrade the authorization code."), 401)
      response.headers["Content-Type"] = "application/json"
      return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ("https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s"
            % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, "GET")[1])

    # If there was an error in the access token info, abort.
    if result.get("error") is not None:
      response = make_response(json.dumps(result.get("error")), 500)
      response.headers["Content-Type"] = "application/json"
      return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token["sub"]
    if result["user_id"] != gplus_id:
      response = make_response(
          json.dumps("Token's user ID doesn't match given user ID."), 401)
      response.headers["Content-Type"] = "application/json"
      return response

    # Verify that the access token is valid for this app.
    if result["issued_to"] != G_CLIENT_ID:
      response = make_response(
          json.dumps("Token's client ID does not match apps's."), 401)
      print "Token's client ID does not match app's."
      response.headers["Content-Type"] = "application/json"
      return response

    # Check to see if user is already logged in:
    stored_credentials = login_session.get("credentials")
    stored_gplus_id = login_session.get("gplus_id")
    if stored_credentials is not None and gplus_id == stored_gplus_id:
      response = make_response(
          json.dumps("Current user is already connected."), 200)
      response.headers["Content-Type"] = "application/json"
      return response

    # Store the access token in the session for later use:
    login_session["credentials"] = credentials.to_json() # credentials
    # Added because of serializable error:
    login_session["access_token"] = credentials.access_token
    login_session["gplus_id"] = gplus_id

    # Get user info:
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {"access_token": credentials.access_token, "alt": "json"}
    answer = requests.get(userinfo_url, params=params)
    data = json.loads(answer.text)

    # Use generic name "username", but also add "g_username" as a sign
    # that they created an account through their Google account.
    login_session["username"] = data["name"]
    login_session["g_username"] = data["name"]
    login_session["picture"] = data["picture"]
    login_session["email"] = data["email"]

    # See if user exists, if it doesn't make a new one.
    user_id = getUserID(login_session["email"])
    if not user_id:
      user_id = createUser(login_session)

    login_session["user_id"] = user_id

    output = ""
    output += "<div class='col-xs-offset-2 padding-none'>"
    output += "Login Successful!</br>"
    output += "<h1>Welcome, "
    output += login_session["g_username"]
    output += "!</h1>"
    output += "<img id='login-photo' src='"
    output += login_session["picture"]
    output += "'>"
    output += "</br>Redirecting..."
    output += "</div>"

    flash("You are now logged in as %s" % login_session["g_username"])
    return output
