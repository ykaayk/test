# coding:utf8

from exts import db
import datetime


class BoardModel(db.Model):
    __tablename__ = 'board'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)

    author_id = db.Column(db.Integer, db.ForeignKey('cms_user.id'))

    author = db.relationship('CMSUser', backref='boards')


class HighLightPostModel(db.Model):
    __tablename__ = 'highlight_post'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column(db.DateTime)


class CommentModel(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)
    is_removed = db.Column(db.Boolean, default=False)

    author_id = db.Column(db.String(100), db.ForeignKey('front_user.id'))  # author_id 对应 front.id
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))  # post_id 对应 post.id
    origin_comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'))  # 原始评论

    author = db.relationship('FrontUser', backref='comments')  # 评论的作者，反过来就是：作者的评论s
    post = db.relationship('PostModel', backref='comments')  # 评论所在的帖子，反过来就是：帖子的评论s

    # 评论的子评论
    origin_comment = db.relationship('CommentModel', backref='replies', remote_side=[id])


class PostModel(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now)
    update_time = db.Column(db.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    read_count = db.Column(db.Integer, default=0)
    is_removed = db.Column(db.Boolean, default=False)

    board_id = db.Column(db.Integer, db.ForeignKey('board.id'))
    author_id = db.Column(db.String(100), db.ForeignKey('front_user.id'))
    highlight_id = db.Column(db.Integer, db.ForeignKey('highlight_post.id'))

    board = db.relationship('BoardModel', backref=db.backref('posts', lazy='dynamic'))
    author = db.relationship('FrontUser', backref='posts')
    highlight = db.relationship('HighLightPostModel', backref='post', uselist=False)


class PostStarModel(db.Model):
    __tablename__ = 'post_star'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    create_time = db.Column(db.DateTime)

    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    author_id = db.Column(db.String(100), db.ForeignKey('front_user.id'))

    post = db.relationship('PostModel', backref='stars')
    author = db.relationship('FrontUser', backref='stars')























