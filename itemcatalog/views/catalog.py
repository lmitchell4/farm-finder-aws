
""" Module summary:
Functions:
  catalogShow - Show the catalog for a given farm."
  catalogManage - Show the catalog for a given farm in manage mode.
  newItem - Create a new catalog item and add it to the database.
  editCatalogItem - Make changes to an existing catalog item.
  deleteCatalogItem - Delete an existing catalog item.  
"""

from flask import Blueprint, render_template, request, redirect
from flask import url_for, flash
from flask import session as login_session

from itemcatalog.database.dbsetup import Farm, CatalogItem, itemCategories
from itemcatalog.database.dbconnect import db_session
from itemcatalog.views.util import imageUploadItem, imageDeleteItem

from util import login_required

############################################################################

catalog = Blueprint("catalog", __name__)

@catalog.route("/farms/<int:farm_id>")
@catalog.route("/farms/<int:farm_id>/catalog")
def catalogShow(farm_id):
  """Show the catalog for a given farm."""
  farm = db_session.query(Farm).filter_by(id=farm_id).one()
  username = login_session.get("username")
  items_list = db_session.query(CatalogItem).filter_by(farm_id=farm_id).all()

  items = {}
  for item in items_list:
    if items.has_key(item.category):
      items[item.category].append(item)
    else:
      items[item.category] = [item]

  return render_template("catalog.html",
                         farm=farm,
                         items=items,
                         itemCategories=itemCategories,
                         username=username)

                         
@catalog.route("/farms/<int:farm_id>/catalog/manage")
@login_required
def catalogManage(farm_id):
  """Show the catalog for a given farm in manage mode."""
  farm = db_session.query(Farm).filter_by(id=farm_id).one()
  items_list = db_session.query(CatalogItem).filter_by(farm_id = farm_id).all()
  items = {}
  for item in items_list:
    if items.has_key(item.category):
      items[item.category].append(item)
    else:
      items[item.category] = [item]

  user_id = login_session.get("user_id")
  username = login_session.get("username")

  if user_id == farm.user_id:
    return render_template("catalogManage.html",
                           farm=farm,
                           items=items,
                           itemCategories=itemCategories,
                           username=username)

  else:
    return redirect(url_for("error.errorShow"))


@catalog.route("/farms/<int:farm_id>/catalog/new", methods=["GET","POST"])
@login_required
def newItem(farm_id):
  """Create a new catalog item and add it to the database."""
  farm = db_session.query(Farm).filter_by(id = farm_id).one()

  user_id = login_session.get("user_id")
  username = login_session.get("username")

  if user_id == farm.user_id:
    if request.method == "POST":
      name = request.form.get("name")
      description = request.form.get("description")
      price = request.form.get("price")
      category = request.form.get("category")

      name_error = None
      category_error = None

      if not name:
        name_error = True
      if not category:
        category_error = True

      if name_error or category_error:
        return render_template("catalogItemNew.html",
                               name_error=name_error,
                               category_error=category_error,
                               farm=farm,
                               itemCategories=itemCategories,
                               username=username)

      newItem = CatalogItem(name=name,
                            description=description,
                            price=price,
                            category=category,
                            farm_id=farm_id,
                            user_id=farm.user_id,
                            picture=None)
      db_session.add(newItem)
      db_session.commit()

      picture = request.files["picture"]
      if picture:
        db_session.refresh(newItem)
        picture_name = imageUploadItem(farm_id=farm_id,
                                       item_id=newItem.id,
                                       file=picture)
        newItem.picture = picture_name
        db_session.add(newItem)
        db_session.commit()

      flash("New Item Successfully Created: %s" % (newItem.name))
      return redirect(url_for("catalog.catalogManage", farm_id=farm_id))

    else:
      return render_template("catalogItemNew.html",
                             farm=farm,
                             itemCategories=itemCategories,
                             username=username)

  else:
    return redirect(url_for("error.errorShow"))


@catalog.route("/farms/<int:farm_id>/catalog/<int:item_id>/edit",
                    methods=["GET","POST"])
@login_required
def editCatalogItem(farm_id, item_id):
  """Make changes to an existing catalog item."""
  farm = db_session.query(Farm).filter_by(id = farm_id).one()
  item = db_session.query(CatalogItem).filter_by(id = item_id).one()

  user_id = login_session.get("user_id")
  username = login_session.get("username")

  if user_id == item.user_id:
    if request.method == "POST":
      name = request.form.get("name")
      description = request.form.get("description")
      price = request.form.get("price")
      category = request.form.get("category")

      name_error = None
      category_error = None

      if not name:
        name_error = True
      if not category:
        category_error = True

      if name_error or category_error:
        return render_template("catalogItemEdit.html",
                               name_error=name_error,
                               category_error=category_error,
                               farm=farm,
                               item=item,
                               itemCategories=itemCategories,
                               username=username)

      item.name = request.form["name"]
      item.description = request.form["description"]
      item.price = request.form["price"]
      item.category = request.form["category"]

      f = request.form
      existing_pic = item.picture
      remove_pic = "removepicture" in f.keys() and \
                      f["removepicture"] == "no-pic"
      new_pic = request.files["picture"]

      if existing_pic:
        if remove_pic:
          imageDeleteItem(filename=item.picture)
          item.picture = None

        elif new_pic:
          imageDeleteItem(filename=item.picture)
          item.picture = imageUploadItem(farm_id=farm.id,
                                         item_id=item.id,
                                         file=new_pic)

      elif new_pic:
          item.picture = imageUploadItem(farm_id=farm.id,
                                         item_id=item.id,
                                         file=new_pic)

      db_session.add(item)
      db_session.commit()
      flash("Item Successfully Edited: %s" % (item.name))
      return redirect(url_for("catalog.catalogManage", farm_id=farm_id))

    else:
      return render_template("catalogItemEdit.html",
                             farm=farm,
                             item=item,
                             itemCategories=itemCategories,
                             username=username)

  return redirect(url_for("error.errorShow"))

  
@catalog.route("/farms/<int:farm_id>/catalog/<int:item_id>/delete",
                      methods=["GET","POST"])
@login_required                      
def deleteCatalogItem(farm_id, item_id):
  """Delete an existing catalog item."""
  farm = db_session.query(Farm).filter_by(id = farm_id).one()
  item = db_session.query(CatalogItem).filter_by(id = item_id).one()

  user_id = login_session.get("user_id")
  username = login_session.get("username")

  if user_id == item.user_id:
    if request.method == "POST":
      db_session.delete(item)
      db_session.commit()

      if item.picture:
        imageDeleteItem(filename=item.picture)

      flash("Item Successfully Deleted: %s" % (item.name))
      return redirect(url_for("catalog.catalogManage", farm_id=farm_id))

    else:
      return render_template("catalogItemDelete.html",
                             farm=farm,
                             item=item,
                             username=username)

  return redirect(url_for("error.errorShow"))
  