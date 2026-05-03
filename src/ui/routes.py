from flask import Blueprint, render_template, request, redirect, url_for, session

from src.services.user_service import register_user, login_user, get_user_by_email
from src.services.event_service import get_all_events
from src.services.participation_service import (
    add_participation,
    get_user_joined_events,
    leave_participation
)


routes_bp = Blueprint("routes_bp", __name__)


@routes_bp.route("/")
def home():
    """Ana sayfayı görüntüler."""
    return render_template("index.html")


@routes_bp.route("/register", methods=["GET", "POST"])
def register():
    """Kullanıcı kayıt işlemini yönetir."""

    if request.method == "GET":
        return render_template("register.html")

    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    success, message = register_user(username, email, password)

    if success:
        return render_template("register.html", success_message=message)

    return render_template("register.html", error_message=message)


@routes_bp.route("/login", methods=["GET", "POST"])
def login():
    """Kullanıcı giriş işlemini yönetir."""

    warning_message = request.args.get("message")

    if request.method == "GET":
        return render_template("login.html", warning_message=warning_message)

    email = request.form.get("email")
    password = request.form.get("password")

    success, message = login_user(email, password)

    if success:
        user = get_user_by_email(email)

        if user is None:
            return render_template(
                "login.html",
                error_message="Kullanıcı bilgisi alınamadı."
            )

        session["user_email"] = user["email"]
        session["username"] = user["username"]

        return redirect(url_for("routes_bp.events"))

    return render_template("login.html", error_message=message)


@routes_bp.route("/logout")
def logout():
    """Kullanıcı oturumunu sonlandırır."""

    session.clear()
    return redirect(url_for("routes_bp.home"))


@routes_bp.route("/events")
def events():
    """Etkinlikler sayfasını görüntüler."""

    event_list = get_all_events()
    message = request.args.get("message")

    return render_template(
        "events.html",
        events=event_list,
        message=message
    )


@routes_bp.route("/join-event/<int:event_id>", methods=["POST"])
def join_event(event_id):
    """
    Kullanıcının etkinliğe katılmasını sağlar.
    Giriş yapılmamışsa kullanıcı login sayfasına yönlendirilir.
    """

    if "user_email" not in session:
        return redirect(
            url_for(
                "routes_bp.login",
                message="Etkinliğe katılmak için önce giriş yapınız."
            )
        )

    user = get_user_by_email(session["user_email"])

    if user is None:
        session.clear()
        return redirect(
            url_for(
                "routes_bp.login",
                message="Oturum doğrulanamadı. Lütfen tekrar giriş yapınız."
            )
        )

    success, message = add_participation(user["id"], event_id)

    return redirect(url_for("routes_bp.events", message=message))


@routes_bp.route("/leave-event/<int:event_id>", methods=["POST"])
def leave_event(event_id):
    """
    Kullanıcının daha önce katıldığı etkinliği iptal etmesini sağlar.
    """

    if "user_email" not in session:
        return redirect(
            url_for(
                "routes_bp.login",
                message="Etkinlik iptali için önce giriş yapınız."
            )
        )

    user = get_user_by_email(session["user_email"])

    if user is None:
        session.clear()
        return redirect(
            url_for(
                "routes_bp.login",
                message="Oturum doğrulanamadı. Lütfen tekrar giriş yapınız."
            )
        )

    success, message = leave_participation(user["id"], event_id)

    return redirect(url_for("routes_bp.profile", message=message))


@routes_bp.route("/profile")
def profile():
    """
    Kullanıcı profil sayfasını görüntüler.
    Profil sayfasında kullanıcı bilgileri ve katıldığı etkinlikler listelenir.
    """

    if "user_email" not in session:
        return redirect(
            url_for(
                "routes_bp.login",
                message="Profil sayfasını görüntülemek için önce giriş yapınız."
            )
        )

    user = get_user_by_email(session["user_email"])

    if user is None:
        session.clear()
        return redirect(
            url_for(
                "routes_bp.login",
                message="Oturum doğrulanamadı. Lütfen tekrar giriş yapınız."
            )
        )

    joined_events = get_user_joined_events(user["id"])
    message = request.args.get("message")

    return render_template(
        "profile.html",
        user=user,
        events=joined_events,
        message=message
    )


