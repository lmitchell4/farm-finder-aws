
""" Module summary:
Functions for creating JSON API endpoints:
  farmsJSON - Create JSON version of each farm.
  farmJSON - Create JSON version of a particular farm.
  catalogJSON - Create JSON version of a farm catalog.
  itemJSON - Create JSON version of each item in a catalog.
  eventsJSON - Create JSON version of events from a particular farm.
  eventJSON - Create JSON version of a particular event from a particular
              farm.
"""

from flask import Blueprint, jsonify

from database.dbsetup import Farm, CatalogItem, Event
from database.dbconnect import db_session

############################################################################

apis = Blueprint("apis", __name__)

# Create JSON API endpoints:
@apis.route("/farms/JSON")
def farmsJSON():
  """Create JSON version of each farm."""
  farms = db_session.query(Farm).all()
  return jsonify(farms=[f.serialize for f in farms])


@apis.route("/farms/<int:farm_id>/JSON")
def farmJSON(farm_id):
  """Create JSON version of a particular farm."""
  farm = db_session.query(Farm).filter_by(id=farm_id).one()
  return jsonify(farm=farm.serialize)


@apis.route("/farms/<int:farm_id>/catalog/JSON")
def catalogJSON(farm_id):
  """Create JSON version of a farm catalog."""
  items = db_session.query(CatalogItem).filter_by(farm_id=farm_id).all()
  return jsonify(catalog=[i.serialize for i in items])


@apis.route("/farms/<int:farm_id>/catalog/<int:menu_id>/JSON")
def itemJSON(farm_id, menu_id):
  """Create JSON version of each item in a catalog."""
  item = db_session.query(CatalogItem).filter_by(
            farm_id=farm_id, id=menu_id).one()
  return jsonify(item=item.serialize)


@apis.route("/farms/<int:farm_id>/events/JSON")
def eventsJSON(farm_id):
  """Create JSON version of events from a particular farm."""
  events = db_session.query(Event).filter_by(farm_id=farm_id).all()
  return jsonify(events=[e.serialize for e in events])


@apis.route("/farms/<int:farm_id>/events/<int:event_id>/JSON")
def eventJSON(farm_id, event_id):
  """Create JSON version of a particular event from a particular farm."""
  event = db_session.query(Event).filter_by(
            farm_id=farm_id, id=event_id).one()
  return jsonify(event=event.serialize)
