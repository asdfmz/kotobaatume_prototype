# routes.py

# 仮ログイン状態として「常にuser_id=1とみなす」構成で、画面遷移だけ動かす

from flask import Blueprint, render_template, request, redirect
from models import db
import services

main_bp = Blueprint("main", __name__)

@main_bp.route("/")
def index():
    return render_template("index.html")

@main_bp.route("/dashboard")
def dashboard():
    user_id = 1  # 仮ログイン
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
