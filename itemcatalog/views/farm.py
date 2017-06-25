
""" Module summary:
Functions:
  farmsShowAll - Show all farms.
  farmsManage - Show all farms belonging to the current user.
  farmNew - Create a new farm and add it to the database.
  farmDelete - Delete an existing farm.  
"""

from flask import Blueprint, render_template, request, redirect, url_for
from flask import flash
from flask import session as login_session

from sqlalchemy import asc

from itemcatalog.database.dbsetup import Farm
from itemcatalog.database.dbconnect import db_session
from itemcatalog.views.util import imageDeleteProfile

from util import login_required

############################################################################

farm = Blueprint("farm", __name__)

@farm.route("/farms")
def farmsShowAll():
  """Show all farms."""
  farms = db_session.query(Farm).order_by(asc(Farm.name))

  user_id = login_session.get("user_id")
  username = login_session.get("username")

  return render_template("farms.html",
                         farms=farms,
                         username=username)


@farm.route("/farms/manage", methods=["GET","POST"])
@login_required
def farmsManage():
  """Show all farms belonging to the current user."""
  user_id = login_session.get("user_id")
  username = login_session.get("username")
  
  # If someone is logged in, show them their farms:
  user_farms = db_session.query(Farm).filter_by(
                user_id=user_id).order_by(asc(Farm.name))
  user_farms = [farm for farm in user_farms]
  return render_template("farmsManage.html",
                         user_farms=user_farms,
                         username=username)
                         

@farm.route("/farms/new", methods=["GET","POST"])
@login_required
def farmNew():
  """Create a new farm and add it to the database."""
  user_id = login_session.get("user_id")
  username = login_session.get("username")
 
  # Check that the user_id argument matches the login_session user_id.
  if request.method == "POST":
    if not request.form["name"]:
      return render_template("farmNew.html",
                             name_error=True,
                             username=username)

    newFarm = Farm(name = request.form["name"],
                   location = request.form["location"],
                   description = request.form["description"],
                   picture = None,
                   user_id=login_session["user_id"])
    db_session.add(newFarm)
    db_session.commit()

    picture = request.files["picture"]
    if picture:
      db_session.refresh(newFarm)
      picture_name = imageUploadProfile(farm_id=newFarm.id, file=picture)
      newFarm.picture = picture_name
      db_session.add(newFarm)
      db_session.commit()

    flash("New Farm %s Successfully Created" % newFarm.name)
    return redirect(url_for("farm.farmsManage"))

  else:
    return render_template("farmNew.html",
                           username=username)

  return render_template("farmNew.html",
                         error=request.files["picture"])


@farm.route("/farms/<int:farm_id>/delete", methods=["GET","POST"])
@login_required
def farmDelete(farm_id):
  """Delete an existing farm."""
  farm = db_session.query(Farm).filter_by(id = farm_id).one()

  user_id = login_session.get("user_id")
  username = login_session.get("username")

  # Check that the login_session user_id matches the farm user_id:
  if user_id == farm.user_id:
    if request.method == "POST":
      if farm.picture:
        imageDeleteProfile(filename=farm.picture)

      db_session.delete(farm)
      db_session.commit()
      flash("Farm Successfully Deleted: %s" % (farm.name))
      return redirect(url_for("farm.farmsManage"))

    else:
      return render_template("farmDelete.html",
                              farm=farm,
                              username=username)

  else:
    return redirect(url_for("catalog.catalogShow",farm_id=farm_id))
