from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.orm import validates

from eblog import db


class RequiredError(Exception):
    def __init__(self, error, status_code) -> None:
        self.error = error
        self.status_code = status_code


post_voter = db.Table(
    "post_voter",
    db.Column(
        "user_id",
        db.Integer,
        db.ForeignKey("user.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    db.Column(
        "post_id",
        db.Integer,
        db.ForeignKey("post.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    user = db.relationship("User", backref=db.backref("post_set"))
    modify_date = db.Column(db.DateTime(), nullable=True)
    voter = db.relationship(
        "User",
        secondary=post_voter,
        backref=db.backref("post_voter_set"),
    )

    def as_dict(self):
        return {
            "id": self.id,
            "subject": self.subject,
            "reply_set": [a.as_dict() for a in self.reply_set],
            "user": self.user.as_dict(),
            "create_date": self.create_date,
            # detail
            "content": self.content,
            "modify_date": self.modify_date,
            "voter": [user.as_dict() for user in self.voter],
        }

    @validates("subject")
    def validate_subject(self, key, subject):
        if not subject:
            raise RequiredError("Subject is required.", 400)
        return subject

    @validates("content")
    def validate_content(self, key, content):
        if not content:
            raise RequiredError("Content is required.", 400)
        return content


reply_voter = db.Table(
    "reply_voter",
    db.Column(
        "user_id",
        db.Integer,
        db.ForeignKey("user.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    db.Column(
        "reply_id",
        db.Integer,
        db.ForeignKey("reply.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Reply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id", ondelete="CASCADE"))
    post = db.relationship("Post", backref=db.backref("reply_set"))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    user = db.relationship("User", backref=db.backref("reply_set"))
    modify_date = db.Column(db.DateTime(), nullable=True)
    voter = db.relationship(
        "User",
        secondary=reply_voter,
        backref=db.backref("reply_voter_set"),
    )

    def as_dict(self):
        return {
            "id": self.id,
            # detail
            "content": self.content,
            "modify_date": self.modify_date,
            "user": self.user.as_dict(),
            "create_date": self.create_date,
            "voter": [user.as_dict() for user in self.voter],
        }

    @validates("content")
    def validate_content(self, key, content):
        if not content:
            raise RequiredError("Content is required.", 400)
        return content


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def as_dict(self):
        return {
            "username": self.username,
            # for auth0 frontend quth
            "email": self.email,
        }
