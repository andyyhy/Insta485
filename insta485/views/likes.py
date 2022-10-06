"""
Insta485 likes post.

URLs include:
/likes/
"""
from flask import session, request, redirect, abort
import insta485


@insta485.app.route('/likes/', methods=['POST'])
def post_likes():
    """Post likes."""
    operation = request.form['operation']
    postid = request.form['postid']
    logname = session['username']
    connection = insta485.model.get_db()

    # Check if the user already liked
    cur = connection.execute(
        "SELECT COUNT(*) "
        "FROM likes "
        "WHERE owner = ? AND postid = ? ",
        (logname, postid, )
    )
    is_liked = cur.fetchall()[0]['COUNT(*)']
    # Process the like
    if operation == 'like':
        if is_liked != 0:
            abort(409)
        cur = connection.execute(
            "INSERT INTO likes(owner, postid) "
            "VALUES(?, ?) ",
            (logname, postid, )
        )
    # Process the unlike
    else:
        if is_liked == 0:
            abort(409)
        cur = connection.execute(
            "DELETE FROM likes "
            "WHERE owner = ? AND postid = ? ",
            (logname, postid, )
        )
    if 'target' not in request.args:
        return redirect('/')
    return redirect(request.args['target'])
