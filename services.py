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

def get_word_by_id(word_id):
    return Word.query.get(word_id)

def update_word(word_id, new_text, new_note):
    word = Word.query.get(word_id)
    if word:
        word.word_text = new_text
        word.note = new_note
        db.session.commit()
    return word

def delete_word(word_id):
    word = Word.query.get(word_id)
    if word:
        db.session.delete(word)
        db.session.commit()

def get_repos_by_user(user_id):
    return Repository.query.filter_by(user_id=user_id).all()

def get_words_by_repo(repo_id):
    return Word.query.filter_by(repo_id=repo_id).all()
