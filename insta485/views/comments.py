"""
Insta485 comments post.

URLs include:
/comments/
"""
from flask import session, request, redirect, abort
import insta485
from insta485.model import get_comment_owner


@insta485.app.route('/comments/', methods=['POST'])
def post_comments():
    """Post comments."""
    operation = request.form['operation']
    logname = session['username']
    connection = insta485.model.get_db()

    if operation == 'create':
        postid = request.form['postid']
        text = request.form['text']

        # Check if comment is empty
        if text == '':
            abort(400)
        # Create new comment
        connection.execute(
            "INSERT INTO comments(owner, postid, text) "
            "VALUES(?, ?, ?) ",
            (logname, postid, text, )
        )

    else:
        commentid = request.form['commentid']
        # Check if comment belongs to user
        comment_owner = get_comment_owner(commentid)
        if comment_owner != logname:
            abort(403)

        # Delete comment
        connection.execute(
            "DELETE FROM comments "
            "WHERE commentid = ? ",
            (commentid, )
        )

    if 'target' not in request.args:
        return redirect('/')
    return redirect(request.args['target'])
