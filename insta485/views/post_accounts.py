"""
Insta485 account post.

URLs include:
/accounts/
"""
import uuid
import hashlib
import os
import pathlib
from flask import session, request, redirect, abort
import insta485
from insta485.model import check_password, user_exists


@insta485.app.route('/accounts/', methods=['POST'])
def post_accounts():
    """Post accounts."""
    operation = request.form['operation']
    if operation == 'login':
        account_login()
    if operation == 'create':
        account_create()
    if operation == 'delete':
        account_delete()
    if operation == 'edit_account':
        account_edit()
    if operation == 'update_password':
        account_password()
    if 'target' not in request.args:
        return redirect('/')
    return redirect(request.args['target'])


def account_login():
    """Login helper."""
    username = request.form['username']
    password = request.form['password']
    if username == '' or password == '':
        abort(400)
    # Check if user exists
    if user_exists(username) is False:
        abort(403)

    # Check if password is correct
    if not check_password(username, password):
        abort(403)

    session['username'] = username


def account_create():
    """Create helper."""
    username = request.form['username']
    password = request.form['password']
    fileobj = request.files['file']

    # If any field is empty
    if (username == '' or password == '' or
            request.form['fullname'] == '' or
            request.form['email'] == '' or fileobj.filename == ''):
        abort(400)

    # If username already exists
    connection = insta485.model.get_db()
    # Check if user exists
    if user_exists(username) is True:
        abort(409)

    # save file to folder
    stem = uuid.uuid4().hex
    suffix = pathlib.Path(fileobj.filename).suffix
    uuid_basename = f"{stem}{suffix}"
    # Save to disk
    path = insta485.app.config["UPLOAD_FOLDER"] / uuid_basename
    fileobj.save(path)

    # convert password
    algorithm = 'sha512'
    salt = uuid.uuid4().hex
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    password_db_string = "$".join([algorithm, salt, hash_obj.hexdigest()])

    # Add new user to database
    connection.execute(
        "INSERT INTO users(username, fullname, email, filename, password) "
        "VALUES(?, ?, ?, ?, ?) ",
        (username, request.form['fullname'],
         request.form['email'], uuid_basename,
         password_db_string)
    )
    session['username'] = username


def account_delete():
    """Delete helper."""
    # Check if user is logged in
    if 'username' not in session:
        abort(403)
    username = session['username']
    connection = insta485.model.get_db()
    # Delete all of user's posts
    cur = connection.execute(
        "SELECT filename "
        "FROM posts "
        "WHERE owner = ? ",
        (username, )
    )
    posts = cur.fetchall()
    for post in posts:
        os.remove(insta485.app.config["UPLOAD_FOLDER"] / post['filename'])

    # Delete user's profile pic
    cur = connection.execute(
        "SELECT filename "
        "FROM users "
        "WHERE username = ? ",
        (username, )
    )
    profile_pic = cur.fetchall()[0]['filename']
    os.remove(insta485.app.config["UPLOAD_FOLDER"] / profile_pic)

    # Remove user from database
    cur = connection.execute(
        "DELETE FROM users "
        "WHERE username = ? ",
        (username, )
    )
    session.clear()


def account_edit():
    """Edit helper."""
    # Check if user is logged in
    if 'username' not in session:
        abort(403)
    connection = insta485.model.get_db()
    username = session['username']
    fullname = request.form['fullname']
    email = request.form['email']
    fileobj = request.files['file']
    filename = fileobj.filename

    # Check if full name and email empty
    if fullname == '' or email == '':
        abort(400)

    if not filename:
        cur = connection.execute(
            "UPDATE users "
            "SET fullname = ?, email = ? "
            "WHERE username = ? ",
            (fullname, email, username, )
        )
    else:
        # save file to folder
        stem = uuid.uuid4().hex
        suffix = pathlib.Path(filename).suffix
        uuid_basename = f"{stem}{suffix}"
        path = insta485.app.config["UPLOAD_FOLDER"] / uuid_basename
        fileobj.save(path)

        # Find old picture and delete it
        cur = connection.execute(
            "SELECT filename "
            "FROM users "
            "WHERE username = ? ",
            (username,)
        )
        old_picture = cur.fetchall()[0]['filename']
        os.remove(insta485.app.config["UPLOAD_FOLDER"] / old_picture)
        # Update database
        cur = connection.execute(
            "UPDATE users "
            "SET fullname = ?, email = ?, filename = ? "
            "WHERE username = ? ",
            (fullname, email, uuid_basename, username, )
        )


def account_password():
    """Password helper."""
    # Check if user is logged in
    if 'username' not in session:
        abort(403)
    connection = insta485.model.get_db()
    old_password = request.form['password']
    new_password1 = request.form['new_password1']
    new_password2 = request.form['new_password2']
    username = session['username']

    # Check if full name and email empty
    if old_password == '' or new_password1 == '' or new_password2 == '':
        abort(400)

    # verify old password
    if not check_password(username, old_password):
        abort(403)

    # Verify that new passwords match
    if new_password1 != new_password2:
        abort(400)

    # update database
    algorithm = 'sha512'
    salt = uuid.uuid4().hex
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + new_password1
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt, password_hash])
    # Add new user to database
    connection.execute(
        "UPDATE users "
        "SET password = ? "
        "WHERE username = ? ",
        (password_db_string, username, )
    )
