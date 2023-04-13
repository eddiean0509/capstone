from datetime import datetime

from flask import Blueprint, abort, g, jsonify, request, session

from eblog import db
from eblog.auth import AuthError, requires_auth
from eblog.models import Reply, Post, RequiredError, User

# Blueprint
bp = Blueprint("api", __name__, url_prefix="/post")


# Post List
@bp.route("/", methods=["GET"])
def posts():
    # query string
    page = request.args.get("page", type=int, default=1)
    kw = request.args.get("kw", type=str, default="")

    # post list
    post_list = db.select(Post).order_by(Post.create_date.desc())

    # serarch
    if kw:
        search = "%%{}%%".format(kw)
        sub_query = (
            db.session.query(Reply.post_id, Reply.content, User.username)
            .join(User, Reply.user_id == User.id)
            .subquery()
        )
        post_list = (
            post_list.join(User)
            .outerjoin(sub_query, sub_query.c.post_id == post.id)
            .filter(
                Post.subject.ilike(search)
                | Post.content.ilike(search)  # 질문제목
                | User.username.ilike(search)  # 질문내용
                | sub_query.c.content.ilike(search)  # 질문작성자
                | sub_query.c.username.ilike(search)  # 답변내용  # 답변작성자
            )
            .distinct()
        )

    # pagination
    post_list = db.paginate(
        post_list,
        page=page,
        per_page=4,
        error_out=False,
    )

    # api data
    data = {
        # post list
        "posts": [q.as_dict() for q in post_list.items],
        # pagination
        "total": post_list.total,
        "page": post_list.page,
        "per_page": post_list.per_page,
        "has_prev": post_list.has_prev,
        "prev_num": post_list.prev_num,
        "page_nums": list(post_list.iter_pages()),
        "has_next": post_list.has_next,
        "next_num": post_list.next_num,
        # search
        "kw": kw,
    }
    return jsonify(data), 200


# Post Detail
@bp.route("/<int:post_id>", methods=["GET"])
def post_read(post_id):
    post = db.get_or_404(Post, post_id)
    return jsonify(post.as_dict()), 200


# Create Post
@bp.route("/", methods=["POST"])
@requires_auth(permission="post:post")
def post_create():
    subject = request.json.get("subject")
    content = request.json.get("content")

    post = Post(
        subject=subject,
        content=content,
        create_date=datetime.now(),
        user=g.user,
    )
    db.session.add(post)
    db.session.commit()

    return jsonify(post.as_dict()), 200


# Modify Post
@bp.route("/<int:post_id>", methods=["PUT"])
@requires_auth(permission="put:post")
def post_modify(post_id):
    post = db.get_or_404(Post, post_id)
    if g.user != post.user:
        return (
            jsonify(
                {"errors": {"permission denied": ["Do not have permission to edit."]}},
            ),
            403,
        )

    subject = request.json.get("subject")
    content = request.json.get("content")

    post.subject = subject
    post.content = content
    post.modify_date = datetime.now()  # 수정일시 저장
    db.session.commit()

    return jsonify(post.as_dict()), 200


# Delete post
@bp.route("/<int:post_id>", methods=["DELETE"])
@requires_auth(permission="delete:post")
def post_delete(post_id):
    post = db.get_or_404(Post, post_id)

    if g.user != post.user:
        return (
            jsonify(
                {"errors": {"permission denied": ["Do not have permission to delete."]}},
            ),
            403,
        )

    db.session.delete(post)
    db.session.commit()

    return jsonify({}), 200


# Vote Post
@bp.route("/<int:post_id>/vote", methods=["POST"])
@requires_auth(permission="vote:post")
def post_vote(post_id):
    post = db.get_or_404(Post, post_id)
    if g.user == post.user:
        return (
            jsonify(
                {"errors": {"permission denied": ["Cannot recomended your own"]}},
            ),
            403,
        )

    post.voter.append(g.user)
    db.session.commit()

    return jsonify([voter.as_dict() for voter in post.voter]), 200


# Reply Detail
@bp.route("/<int:post_id>/reply/<int:reply_id>", methods=["GET"])
def reply_read(post_id, reply_id):
    reply = Reply.query.filter_by(id=reply_id, post_id=post_id).first()
    if not reply:
        abort(404)

    return jsonify(reply.as_dict()), 200


# Modify Reply
@bp.route("/<int:post_id>/reply/<int:reply_id>", methods=["PUT"])
@requires_auth(permission="put:reply")
def reply_modify(post_id, reply_id):
    reply = Reply.query.filter_by(id=reply_id, post_id=post_id).first()
    if not reply:
        abort(404)

    if g.user != reply.user:
        return (
            jsonify(
                {"errors": {"permission denied": ["Do not have permission to edit."]}},
            ),
            403,
        )

    reply.content = request.json.get("content")
    reply.modify_date = datetime.now() 
    db.session.commit()

    return jsonify(reply.as_dict()), 200


# Create Reply
@bp.route("/<int:post_id>/reply", methods=["POST"])
@requires_auth(permission="post:reply")
def reply_create(post_id):
    post = db.get_or_404(Post, post_id)

    reply = Reply(
        content=request.json.get("content"),
        create_date=datetime.now(),
        user=g.user,
    )
    post.reply_set.append(reply)
    db.session.commit()

    return jsonify(reply.as_dict()), 200


# Delete Reply
@bp.route("/<int:post_id>/reply/<int:reply_id>", methods=["DELETE"])
@requires_auth(permission="delete:reply")
def reply_delete(post_id, reply_id):
    reply = Reply.query.filter_by(id=reply_id, post_id=post_id).first()
    if not reply:
        abort(404)

    if g.user != reply.user:
        return (
            jsonify(
                {"errors": {"permission denied": ["Do not have permission to delete."]}},
            ),
            403,
        )

    db.session.delete(reply)
    db.session.commit()

    return jsonify({}), 200


# Vote Reply
@bp.route("/<int:post_id>/reply/<int:reply_id>/vote", methods=["POST"])
@requires_auth(permission="vote:reply")
def reply_vote(post_id, reply_id):
    reply = db.get_or_404(Reply, reply_id)
    if reply.post_id != post_id:
        abort(404)

    if g.user == reply.user:
        return (
            jsonify(
                {"errors": {"permission denied": ["Cannot recomended your own"]},},
            ),
            403,
        )

    reply.voter.append(g.user)
    db.session.commit()

    return jsonify([voter.as_dict() for voter in reply.voter]), 200


# Error handler
@bp.app_errorhandler(400)
def bad_request(error):
    return (
        jsonify(
            {
                "errors": {
                    "400": ["bad request"],
                }
            }
        ),
        400,
    )


@bp.app_errorhandler(404)
def not_found(error):
    return (
        jsonify(
            {
                "errors": {
                    "404": ["not found"],
                }
            }
        ),
        404,
    )


@bp.app_errorhandler(422)
def unprocessable(error):
    return (
        jsonify(
            {
                "errors": {
                    "422": ["unprocessable"],
                }
            }
        ),
        422,
    )


@bp.app_errorhandler(AuthError)
def auth_error(error):
    return (
        jsonify(
            {
                "errors": {
                    "authentication error": [error.error["description"]],
                }
            }
        ),
        error.status_code,
    )


@bp.app_errorhandler(RequiredError)
def validation_error(error):
    return (
        jsonify(
            {
                "errors": {
                    "required error": [error.error],
                }
            }
        ),
        error.status_code,
    )


# App request
@bp.after_app_request
def creds(res):
    res.headers["Access-Control-Allow-Origin"] = "http://localhost:3000"
    res.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    res.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS, PATCH"
    return res


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None

    g.user = db.session.get(User, user_id)
