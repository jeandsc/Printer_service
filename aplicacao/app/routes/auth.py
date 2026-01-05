from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth", __name__)

#pagina registro
@auth_bp.route("/register", methods=["GET"])
def register_page():
    return render_template("register.html")

#post
@auth_bp.route("/register", methods=["POST"])
def register_user():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    #campos preenchidos?
    if not username or not password:
        flash("Preencha todos os campos obrigatórios!", "error")
        return redirect(url_for("auth.register_page"))

    # Usuário existe?
    if User.query.filter_by(username=username).first():
        flash("Nome de usuário já existe!", "error")
        return redirect(url_for("auth.register_page"))

    # Hash da senha
    password_hash = generate_password_hash(password)

    # Criar usuário no banco
    user = User(username=username, email=email, password_hash=password_hash)
    db.session.add(user)
    db.session.commit()

    flash("Usuário registrado com sucesso!", "success")
    return redirect(url_for("auth.register_page"))

########################################################## LOGIN
@auth_bp.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")

# Submissão do login (POST)
@auth_bp.route("/login", methods=["POST"])
def login_user():
    username = request.form.get("username")
    password = request.form.get("password")

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password_hash, password):
        # Login bem-sucedido
        session["user_id"] = user.id
        flash("Login realizado com sucesso!", "success")
        return redirect(url_for("home.home_page"))
    else:
        flash("Usuário ou senha incorretos.", "error")
        return redirect(url_for("auth.login_page"))

@auth_bp.route('/logout')
def logout():
    session.pop('user', None)  # Remove o usuário da sessão
    flash('Você saiu da conta.', 'info')
    return redirect(url_for('auth.login_user'))