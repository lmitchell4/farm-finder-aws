
""" Module summary:
Functions:
  profileShow - Show the profile for a given farm.
  profileManage - Show the profile for a given farm in manage mode.
  profileEdit - Edit the profile for a given farm.
"""

from flask import Blueprint, render_template, request, redirect, url_for
from flask import flash
from flask import session as login_session

from itemcatalog.database.dbsetup import Farm
from itemcatalog.database.dbconnect import db_session
from itemcatalog.views.util import imageUploadProfile, imageDeleteProfile

from util import login_required

############################################################################

profile = Blueprint("profile", __name__)

@profile.route("/farms/<int:farm_id>/profile")
def profileShow(farm_id):
  """Show the profile for a given farm."""
  farm = db_session.query(Farm).filter_by(id=farm_id).one()
  username = login_session.get("username")

  return render_template("profile.html",
                          farm=farm,
                          username=username)


@profile.route("/farms/<int:farm_id>/profile/manage")
@login_required
def profileManage(farm_id):
  """Show the profile for a given farm in manage mode."""
  farm = db_session.query(Farm).filter_by(id=farm_id).one()

  user_id = login_session.get("user_id")
  username = login_session.get("username")

  if user_id != farm.user_id:
    return redirect(url_for("error.errorShow"))

  if user_id == farm.user_id:
    return render_template("profileManage.html",
                           farm=farm,
                           username=username)


@profile.route("/farms/<int:farm_id>/profile/edit", methods=["GET","POST"])
@login_required
def profileEdit(farm_id):
  """Edit the profile for a given farm."""
  farm = db_session.query(Farm).filter_by(id=farm_id).one()

  user_id = login_session.get("user_id")
  username = login_session.get("username")

  if user_id != farm.user_id:
    return redirect(url_for("error.errorShow"))

  if user_id == farm.user_id:
    if request.method == "POST":
      if not request.form["name"]:
        return render_template("profileEdit.html",
                               farm=farm,
                               name_error=True,
                               username=username)

      farm.name = request.form["name"]
      farm.location = request.form["location"]
      farm.description = request.form["description"]

      f = request.form
      existing_pic = farm.picture
      remove_pic = "removepicture" in f.keys() and \
                      f["removepicture"] == "no-pic"
      new_pic = request.files["picture"]

      if existing_pic:
        if remove_pic:
          imageDeleteProfile(filename=farm.picture)
          farm.picture = None

        elif new_pic:
          imageDeleteProfile(filename=farm.picture)
          farm.picture = imageUploadProfile(farm_id=farm.id, file=new_pic)

      elif new_pic:
          farm.picture = imageUploadProfile(farm_id=farm.id, file=new_pic)

      db_session.add(farm)
      db_session.commit()
      flash("Profile Successfully Edited")
      return redirect(url_for("profile.profileManage", 
                              farm_id=farm_id))

    else:
      return render_template("profileEdit.html",
                             farm=farm,
                             username=username)
                           