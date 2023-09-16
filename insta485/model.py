"""Insta485 model (database) API."""
import sqlite3
import hashlib
import flask
import insta485


def dict_factory(cursor, row):
    """Convert database row objects to a dictionary keyed on column name.

    This is useful for building dictionaries which are then used to render a
    template.  Note that this would be inefficient for large queries.
    """
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}


def get_db():
    """Open a new database connection.

    Flask docs:
    https://flask.palletsprojects.com/en/1.0.x/appcontext/#storing-data
    """
    if 'sqlite_db' not in flask.g:
        db_filename = insta485.app.config['DATABASE_FILENAME']
        flask.g.sqlite_db = sqlite3.connect(str(db_filename))
        flask.g.sqlite_db.row_factory = dict_factory
        # Foreign keys have to be enabled per-connection.  This is an sqlite3
        # backwards compatibility thing.
        flask.g.sqlite_db.execute("PRAGMA foreign_keys = ON")
    return flask.g.sqlite_db


@insta485.app.teardown_appcontext
def close_db(error):
    """Close the database at the end of a request.

    Flask docs:
    https://flask.palletsprojects.com/en/1.0.x/appcontext/#storing-data
    """
    assert error or not error  # Needed to avoid superfluous style error
    sqlite_db = flask.g.pop('sqlite_db', None)
    if sqlite_db is not None:
        sqlite_db.commit()
        sqlite_db.close()


def http_authenticate():
    """Authenticate user."""
    if not flask.request.authorization:
        print(123123)
        return False
    username = flask.request.authorization['username']
    password = flask.request.authorization['password']

    # Check if user exists
    if user_exists(username) is False:
        return False

    # Check if password is correct
    if check_password(username=username, password=password):
        return True
    return False


def cookie_authenticate():
    """Authenticate user."""
    if 'username' not in flask.session:
        print(123123)
        return False
    return True


def authenticate():
    """Authenticate user."""
    if http_authenticate() or cookie_authenticate():
        return True
    return False


def check_password(username, password):
    """Check if password match."""
    connection = get_db()
    cur = connection.execute(
        "SELECT password "
        "FROM users "
        "WHERE username = ? ",
        (username,)
    )
    correct_password = cur.fetchall()[0]['password']
    # convert password
    algorithm = 'sha512'
    salt = correct_password.split('$')[1]
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + password
    hash_obj.update(password_salted.encode('utf-8'))
    entered_password_hash = hash_obj.hexdigest()

    if correct_password.split('$')[2] != entered_password_hash:
        return False
    return True


def user_exists(username):
    """Check if user exists."""
    connection = insta485.model.get_db()
    # Check if user exists
    # Select count from users
    cur = connection.execute(
        "SELECT COUNT(*) "
        "FROM users "
        # username
        "WHERE username = ? ",
        (username, )
    )
    # if user dont exist return false
    if cur.fetchall()[0]['COUNT(*)'] == 0:
        return False
    return True


def get_comment_details(postid):
    """Get comments."""
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT owner, text, commentid "
        "FROM comments "
        "WHERE postid = ? "
        "ORDER BY commentid ASC",
        (postid, )
    )

    return cur.fetchall()


def get_likes_info(postid):
    """Get likes."""
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT COUNT(*) "
        "FROM likes "
        "WHERE postid = ? ",
        (postid, )
    )
    return cur.fetchall()[0]['COUNT(*)']


def get_post_data(postid):
    """Get post data."""
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT filename, owner, created "
        "FROM posts "
        "WHERE postid = ? ",
        (postid, )
    )
    return cur.fetchall()[0]


def get_comment_owner(commentid):
    """Get comment owner."""
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT owner "
        "FROM comments "
        "WHERE commentid = ? ",
        (commentid, )
    )
    return cur.fetchall()[0]["owner"]


def check_comment_exists(commentid):
    """Check comment exists."""
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT COUNT(*)"
        "FROM comments "
        "WHERE commentid = ? ",
        (commentid, )
    )
    return cur.fetchall()[0]["COUNT(*)"]


def set_username():
    """Set username."""
    if "username" not in flask.session:
        username = flask.request.authorization['username']
    else:
        username = flask.session["username"]
    return username


def generate_403():
    """Generate 403."""
    context = {}
    context["message"] = "Forbidden"
    context["status_code"] = 403

    return context
