"""REST API for posts."""
import flask
import insta485
from insta485.model import authenticate, generate_403


@insta485.app.route('/api/v1/likes/', methods=['POST'])
def post_like():
    """Create one “like” for a specific post."""
    context = {}
    # Authentication
    if not authenticate():
        context = generate_403()
        return flask.jsonify(**context), 403

    postid = flask.request.args.get('postid')
    connection = insta485.model.get_db()
    if "username" not in flask.session:
        username = flask.request.authorization['username']
    else:
        username = flask.session["username"]

    cur = connection.execute(
        "SELECT COUNT(*) "
        "FROM likes "
        "WHERE owner = ? AND postid = ? ",
        (username, postid, )
    )
    is_liked = cur.fetchall()[0]['COUNT(*)']

    if is_liked == 0:
        # Create the new like
        cur = connection.execute(
            "INSERT INTO likes(owner, postid) "
            "VALUES(?, ?) ",
            (username, postid, )
        )
        # Get the likeid
        cur = connection.execute(
            "SELECT last_insert_rowid() "
            "FROM likes "
        )
        likeid = cur.fetchall()[0]["last_insert_rowid()"]
        context["likeid"] = likeid
        context["url"] = "/api/v1/likes/" + str(likeid) + "/"

        return flask.jsonify(**context), 201

    # Get the likeid
    cur = connection.execute(
        "SELECT likeid "
        "FROM likes "
        "WHERE owner = ? AND postid = ? ",
        (username, postid, )
    )
    likeid = cur.fetchall()[0]["likeid"]
    context["likeid"] = likeid
    context["url"] = "/api/v1/likes/" + str(likeid) + "/"

    return flask.jsonify(**context), 200


@insta485.app.route('/api/v1/likes/<likeid>/', methods=['DELETE'])
def delete_like(likeid):
    """Create one “like” for a specific post."""
    # Authentication
    if not authenticate():
        not_authenticate = {}
        not_authenticate = generate_403()
        return flask.jsonify(**not_authenticate), 403

    if "username" not in flask.session:
        username = flask.request.authorization['username']
    else:
        username = flask.session["username"]

    # Check if likeid exists
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT COUNT(*)"
        "FROM likes "
        "WHERE likeid = ? ",
        (likeid, )
    )
    like_exists = cur.fetchall()[0]["COUNT(*)"]
    context = {}
    if like_exists == 0:
        context["message"] = "Not Found"
        context["status_code"] = 404
        return flask.jsonify(**context), 404

    cur = connection.execute(
        "SELECT owner "
        "FROM likes "
        "WHERE likeid = ? ",
        (likeid, )
    )
    owner = cur.fetchall()[0]["owner"]

    if owner != username:
        context["message"] = "Forbidden"
        context["status_code"] = 403
        return flask.jsonify(**context), 403

    cur = connection.execute(
        "DELETE FROM likes "
        "WHERE likeid = ? ",
        (likeid, )
    )
    return flask.jsonify(**context), 204
