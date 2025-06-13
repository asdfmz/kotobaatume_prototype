# routes.py

# 仮ログイン状態として「常にuser_id=1とみなす」構成で、画面遷移だけ動かす

from flask import Blueprint, render_template, request, redirect, session, flash
from models import db
import services

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    return render_template("index.html")

@main_bp.route("/dashboard")
def dashboard():
    user_id = session.get("user_id")
    if not user_id:
        return redirect("/login")
    repos = services.get_repos_by_user(user_id)
    return render_template("dashboard.html", repos=repos)

@main_bp.route("/repos/<int:repo_id>")
def repo_detail(repo_id):
    words = services.get_words_by_repo(repo_id)
    return render_template("repo_detail.html", repo_id=repo_id, words=words)

@main_bp.route("/add_word/<int:repo_id>", methods=["GET", "POST"])
def add_word(repo_id):
    if request.method == "POST":
        word_text = request.form["word_text"]
        note = request.form["note"]
        services.add_word(repo_id, word_text, note)
        return redirect(f"/repos/{repo_id}")
    return render_template("add_word.html", repo_id=repo_id)

@main_bp.route("/edit_word/<int:word_id>", methods=["GET", "POST"])
def edit_word(word_id):
    word = services.get_word_by_id(word_id)
    if not word:
        return "Word not found", 404
    
    if request.method == "POST":
        new_text = request.form["word_text"]
        new_note = request.form["note"]
        services.update_word(word_id, new_text, new_note)
        return redirect(f"/repos/{word.repo_id}")
    
    return render_template("edit_word.html", word=word)

@main_bp.route("/delete_word/<int:word_id>", methods=["POST"])
def delete_word(word_id):
    word = services.get_word_by_id(word_id)
    repo_id = word.repo_id if word else 0
    services.delete_word(word_id)
    return redirect(f"/repos/{repo_id}")

@main_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = services.register_user(username, password)
        if user:
            session["user_id"] = user.id
            return redirect("/dashboard")
        flash("Username already exsists")
    return render_template("signup.html")

@main_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = services.authenticate_user(username, password)
        if user:
            session["user_id"] = user.id
            return redirect("/dashboard")
        flash("Invalid credentials")
    return render_template("login.html")

@main_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")
