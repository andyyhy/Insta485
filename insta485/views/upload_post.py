"""
Insta485 upload post post.

URLs include:
/posts/
"""

import uuid
import os
import pathlib
from flask import session, request, redirect, abort
import insta485


@insta485.app.route('/posts/', methods=['POST'])
def post_posts():
    """Post posts."""
    operation = request.form['operation']
    logname = session['username']
    connection = insta485.model.get_db()

    # Delete post
    if operation == 'delete':
        postid = request.form['postid']

        cur = connection.execute(
            "SELECT filename, owner "
            "FROM posts "
            "WHERE postid = ? ",
            (postid, )
        )
        postinfo = cur.fetchall()[0]
        # Check if user owns post
        if postinfo['owner'] != logname:
            abort(403)
        # Delete post file

        os.remove(insta485.app.config["UPLOAD_FOLDER"] /
                  postinfo['filename'])

        # Delete post from database
        cur = connection.execute(
            "DELETE FROM posts "
            "WHERE postid = ? ",
            (postid, )
        )
    else:
        if 'file' not in request.files:
            abort(400)
        fileobj = request.files['file']
        filename = fileobj.filename

        suffix = pathlib.Path(filename).suffix
        stem = uuid.uuid4().hex
        uuid_basename = f"{stem}{suffix}"
        # Save to disk
        path = insta485.app.config["UPLOAD_FOLDER"] / uuid_basename
        fileobj.save(path)

        # Save to database
        cur = connection.execute(
            "INSERT INTO posts(filename, owner) "
            "VALUES(?, ?) ",
            (uuid_basename, logname, )
        )
    if 'target' not in request.args:
        return redirect('/users/' + logname + '/')
    return redirect(request.args['target'])
