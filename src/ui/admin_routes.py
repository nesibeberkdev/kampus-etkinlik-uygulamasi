from flask import Blueprint, render_template, request, redirect, url_for, session

from core.admin_config import AdminConfig
from services.event_service import get_all_events, get_event_by_id, update_event , add_event,delete_event


admin_bp = Blueprint("admin_bp", __name__)


@admin_bp.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    """
    Yönetici giriş işlemini yönetir.
    """

    if request.method == "GET":
        return render_template("admin_login.html")

    email = request.form.get("email")
    password = request.form.get("password")

    if (
        email == AdminConfig.admin_email
        and password == AdminConfig.admin_password
    ):
        session["admin_email"] = email
        return redirect(url_for("admin_bp.admin_panel"))

    return render_template(
        "admin_login.html",
        error_message="Yönetici bilgileri hatalı."
    )


@admin_bp.route("/admin")
def admin_panel():
    """
    Yönetici panelini görüntüler.
    """

    if "admin_email" not in session:
        return redirect(url_for("admin_bp.admin_login"))

    event_list = get_all_events()

    return render_template(
        "admin.html",
        events=event_list
    )


@admin_bp.route("/admin-logout")
def admin_logout():
    """
    Yönetici oturumunu kapatır.
    """

    session.pop("admin_email", None)

    return redirect(url_for("routes_bp.home"))










@admin_bp.route("/admin/edit-event/<int:event_id>", methods=["GET", "POST"])
def edit_event(event_id):
    """
    Yönetici tarafından etkinlik bilgilerini düzenler.
    """

    if "admin_email" not in session:
        return redirect(url_for("admin_bp.admin_login"))

    event = get_event_by_id(event_id)

    if event is None:
        return redirect(url_for("admin_bp.admin_panel"))

    if request.method == "GET":
        return render_template(
            "admin_edit_event.html",
            event=event
        )

    title = request.form.get("title")
    description = request.form.get("description")
    date = request.form.get("date")
    location = request.form.get("location")
    capacity = request.form.get("capacity")
    image_filename = request.form.get("image_filename")

    if capacity == "":
        capacity = None

    success, message = update_event(
        event_id,
        title,
        description,
        date,
        location,
        capacity,
        image_filename
    )

    return redirect(
        url_for(
            "admin_bp.admin_panel",
            message=message
        )
    )

#yeni etkinlik ekleme route'u
@admin_bp.route("/admin/add-event", methods=["GET", "POST"])
def add_event_page():
    """
    Yönetici tarafından yeni etkinlik ekleme işlemini yönetir.
    """

    if "admin_email" not in session:
        return redirect(url_for("admin_bp.admin_login"))

    if request.method == "GET":
        return render_template("admin_add_event.html")

    title = request.form.get("title")
    description = request.form.get("description")
    date = request.form.get("date")
    location = request.form.get("location")
    capacity = request.form.get("capacity")
    image_filename = request.form.get("image_filename")

    if capacity == "":
        capacity = None

    success, message = add_event(
        title,
        description,
        date,
        location,
        capacity,
        image_filename
    )

    return redirect(url_for("admin_bp.admin_panel", message=message))

#Etkinlik silme route'u
@admin_bp.route("/admin/delete-event/<int:event_id>", methods=["POST"])
def delete_event_page(event_id):
    """
    Yönetici tarafından seçilen etkinliği siler.
    """

    if "admin_email" not in session:
        return redirect(url_for("admin_bp.admin_login"))

    success, message = delete_event(event_id)

    return redirect(url_for("admin_bp.admin_panel", message=message))