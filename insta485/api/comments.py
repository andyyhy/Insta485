"""REST API for posts."""
import flask
import insta485
from insta485.model import authenticate, generate_403, \
    get_comment_owner, check_comment_exists, set_username


@insta485.app.route('/api/v1/comments/', methods=['POST'])
def post_comment():
    """Add one comment to a post."""
    postid = flask.request.args.get('postid')
    # Authentication
    context = {}
    if not authenticate():
        not_authenticate = generate_403()
        return flask.jsonify(**not_authenticate), 403
    username = set_username()

    # Get comment details
    text = flask.request.json.get('text')
    # Create new comment
    connection = insta485.model.get_db()
    connection.execute(
        "INSERT INTO comments(owner, postid, text) "
        "VALUES(?, ?, ?) ",
        (username, postid, text, )
    )

    # Get commentid
    cur = connection.execute(
        "SELECT last_insert_rowid() "
        "FROM comments "
    )
    commentid = cur.fetchall()[0]["last_insert_rowid()"]
    context["commentid"] = commentid
    context["lognameOwnsThis"] = True
    context["owner"] = username
    context["ownerShowUrl"] = "/users/" + username + "/"
    context["text"] = text
    context["url"] = "/api/v1/comments/" + str(commentid) + "/"

    return flask.jsonify(**context), 201


@insta485.app.route('/api/v1/comments/<commentid>/', methods=['DELETE'])
def delete_comment(commentid):
    """Create one “like” for a specific post."""
    context = {}
    connection = insta485.model.get_db()

    # Authentication
    if not authenticate():
        context["message"] = "Forbidden"
        context["status_code"] = 403
        return flask.jsonify(**context), 403

    if "username" not in flask.session:
        username = flask.request.authorization['username']
    else:
        username = flask.session["username"]

    # Check if comment exists
    comment_exists = check_comment_exists(commentid)

    if comment_exists == 0:
        context["message"] = "Not Found"
        context["status_code"] = 404
        return flask.jsonify(**context), 404

    owner = get_comment_owner(commentid)

    if username != owner:
        context["status_code"] = 403
        context["message"] = "Forbidden"

        return flask.jsonify(**context), 403

    connection.execute(
        "DELETE FROM comments "
        "WHERE commentid = ? ",
        (commentid, )
    )
    return flask.jsonify(**context), 204
