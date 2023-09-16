"""
Insta485 following post.

URLs include:
/following/
"""
from flask import session, request, redirect, abort
import insta485


@insta485.app.route('/following/', methods=['POST'])
def post_following():
    """Post following."""
    operation = request.form['operation']
    logname = session['username']
    username = request.form['username']
    connection = insta485.model.get_db()

    # Check if the user already liked
    cur = connection.execute(
        "SELECT COUNT(*) "
        "FROM following "
        "WHERE username2 = ? AND username1 = ?",
        (username, logname)
    )
    is_following = cur.fetchall()[0]['COUNT(*)']

    if operation == 'follow':
        if is_following != 0:
            abort(409)
        cur = connection.execute(
            "INSERT INTO following(username1, username2) "
            "VALUES (?, ?) ",
            (logname, username, )
        )
    else:
        if is_following == 0:
            abort(409)
        cur = connection.execute(
            "DELETE FROM following "
            "WHERE username1 = ? AND username2 = ? ",
            (logname, username, )
        )
    if 'target' not in request.args:
        return redirect('/')
    return redirect(request.args['target'])
