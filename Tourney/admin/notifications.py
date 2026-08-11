from flask import render_template

from Tourney.admin import admin
from Tourney.models import Notifications
from Tourney.utils.decorators import admins_only


@admin.route("/admin/notifications")
@admins_only
def notifications():
    notifs = Notifications.query.order_by(Notifications.id.desc()).all()
    return render_template("admin/notifications.html", notifications=notifs)
