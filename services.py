# services.py

from models import db, User, Repository, Word

def create_user(username):
    user = User(username=username)
    db.session.add(user)
    db.session.commit()
    return user

def create_repo(user_id, name, is_public=True):
    repo = Repository(name=name, user_id=user_id, is_public=is_public)
    db.session.add(repo)
    db.session.commit()
    return repo

def add_word(repo_id, word_text, note=""):
    word = Word(repo_id=repo_id, word_text=word_text, note=note)
    db.session.add(word)
    db.session.commit()
    return word

def get_repos_by_user(user_id):
    return Repository.query.filter_by(user_id=user_id).all()

def get_words_by_repo(repo_id):
    return Word.query.filter_by(repo_id=repo_id).all()
