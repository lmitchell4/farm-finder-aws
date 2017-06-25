
""" Module summary:
Functions:
  eventShow - Show the events for a given farm.
  eventManage - Show the events for a given farm in manage mode.
  eventNew - Create a new event.
  eventEdit - Edit an event.
  eventDelete - Delete an event.  
"""

from flask import Blueprint, render_template, request, redirect, url_for
from flask import flash
from flask import session as login_session

from itemcatalog.database.dbsetup import Farm, Event
from itemcatalog.database.dbconnect import db_session

from util import login_required

############################################################################

event = Blueprint("event", __name__)

@event.route("/farms/<int:farm_id>/events")
def eventShow(farm_id):
  """Show the events for a given farm."""
  farm = db_session.query(Farm).filter_by(id=farm_id).one()
  events = db_session.query(Event).filter_by(farm_id=farm_id).all()
  username = login_session.get("username")

  return render_template("events.html",
                         farm=farm,
                         events=events,
                         username=username)

                         
@event.route("/farms/<int:farm_id>/events/manage")
@login_required
def eventManage(farm_id):
  """Show the events for a given farm in manage mode."""
  farm = db_session.query(Farm).filter_by(id=farm_id).one()
  events = db_session.query(Event).filter_by(farm_id=farm_id).all()

  user_id = login_session.get("user_id")
  username = login_session.get("username")

  if user_id == farm.user_id:
    return render_template("eventsManage.html",
                           farm=farm,
                           events=events,
                           username=username)

  else:
    return redirect(url_for("error.errorShow"))


@event.route("/farms/<int:farm_id>/events/new", methods=["GET","POST"])
@login_required
def eventNew(farm_id):
  """Create a new event."""
  farm = db_session.query(Farm).filter_by(id=farm_id).one()

  user_id = login_session.get("user_id")
  username = login_session.get("username")

  if user_id == farm.user_id:
    if request.method == "POST":
      if not request.form["name"]:
        return render_template("eventNew.html",
                               farm=farm,
                               name_error=True,
                               username=username)

      event = Event(name = request.form["name"],
                     description = request.form["description"],
                     farm_id=farm.id,
                     user_id=user_id)

      db_session.add(event)
      flash("New Event Successfully Created: %s" % event.name)
      db_session.commit()
      return redirect(url_for("event_manage.eventManage",farm_id=farm.id))

    else:
      return render_template("eventNew.html",
                             farm=farm,
                             username=username)

  else:
    return redirect(url_for("error.errorShow"))

    
@event.route("/farms/<int:farm_id>/events/<int:event_id>/edit",
            methods=["GET","POST"])
@login_required
def eventEdit(farm_id, event_id):
  """Edit an event."""
  farm = db_session.query(Farm).filter_by(id=farm_id).one()
  event = db_session.query(Event).filter_by(id=event_id).one()

  user_id = login_session.get("user_id")
  username = login_session.get("username")

  if user_id == farm.user_id:
    if request.method == "POST":
      if not request.form["name"]:
        return render_template("eventEdit.html",
                               farm=farm,
                               event=event,
                               name_error=True,
                               username=username)

      event.name = request.form["name"]
      event.description = request.form["description"]

      db_session.add(event)
      db_session.commit()
      flash("Event Successfully Edited: %s" % event.name)
      return redirect(url_for("event_manage.eventManage",farm_id=farm.id))

    else:
      return render_template("eventEdit.html",
                             farm=farm,
                             event=event,
                             username=username)

  else:
    return redirect(url_for("error.errorShow"))


@event.route("/farms/<int:farm_id>/events/<int:event_id>/delete",
            methods=["GET","POST"])
@login_required
def eventDelete(farm_id, event_id):
  """Delete an event."""
  farm = db_session.query(Farm).filter_by(id=farm_id).one()
  event = db_session.query(Event).filter_by(id=event_id).one()

  user_id = login_session.get("user_id")
  username = login_session.get("username")

  if user_id == farm.user_id:
    if request.method == "POST":
      db_session.delete(event)
      db_session.commit()

      flash("Event Successfully Deleted: %s" % (event.name))
      return redirect(url_for("event_manage.eventManage",farm_id=farm.id))

    else:
      return render_template("eventDelete.html",
                             farm=farm,
                             event=event,
                             username=username)

  else:
    return redirect(url_for("error.errorShow"))
