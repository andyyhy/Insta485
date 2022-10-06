"""
Insta485 explore view.

URLs include:
/explore/
"""
from flask import render_template, session, request, redirect, url_for
import insta485


@insta485.app.route('/explore/')
def show_explore():
    """Show explore."""
    if 'username' not in session:
        return redirect(url_for('show_login'))
    connection = insta485.model.get_db()
    context = {'logname': session['username'],
               'posts': [], "current_url": request.path}
    # Query database
    logname = session['username']

    cur = connection.execute(
        "SELECT username, filename "
        "FROM users "
        "WHERE username NOT IN "
        "(SELECT username2 "
        "FROM following "
        "WHERE username1 = ? AND username != ?) "
        "AND username != ?",
        (logname, logname, logname)
    )
    user_info = cur.fetchall()

    users = []
    for user in user_info:
        usertemp = {"username": user['username'],
                    "user_img_url": user['filename']}
        users.append(usertemp)
    context['users'] = users
    return render_template("explore.html", **context)
