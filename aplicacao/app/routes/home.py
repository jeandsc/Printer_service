from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from app.models import User, Printer, PrinterState, PrintJob
from app import db


def login_required(f):
    """Decorador simples para proteger rotas"""
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("auth.login_page"))
        return f(*args, **kwargs)
    return decorated
home_bp = Blueprint("home", __name__)

@home_bp.route("/")
def home():
    return render_template("home.html")

@home_bp.route("/home")

def home_page():
    if "user_id" not in session:
        return redirect(url_for("auth.login_page"))

    user = User.query.get(session["user_id"])
    
    print(session)
    return render_template("dashboard.html", user=user)
#Printers

@home_bp.route("/home/printers")
@login_required
def list_printers():
    printers = Printer.query.all()
    print(session)
    return render_template("printers.html", printers=printers)


@home_bp.route("/home/printers/<int:printer_id>/state")
def printer_state(printer_id):

    printer = Printer.query.get_or_404(printer_id)
    return render_template("printer_state.html", printer=printer, states=printer.states)

# Listar jobs na home
@home_bp.route("/jobs")
def list_jobs():
    jobs = PrintJob.query.order_by(PrintJob.created_at.desc()).all()
    return render_template("jobs.html", jobs=jobs)

