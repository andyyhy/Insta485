"""
Insta485 index (main) view.

URLs include:
/
"""
from flask import render_template, session, request, redirect, url_for
import arrow
import insta485


@insta485.app.route('/')
def show_index():
    """Display / route."""
    # Check if logged in
    if 'username' not in session:
        return redirect(url_for('show_login'))
    logname = session['username']
    context = {'logname': session['username'],
               'posts': [], "current_url": request.path}
    # Connect to database
    connection = insta485.model.get_db()
    # get postinfo
    cur = connection.execute(
        "SELECT postid, filename, owner, created "
        "FROM posts "
        "WHERE owner IN "
        "(SELECT username2 "
        "FROM following "
        "WHERE username1 = ? OR username2 = ?) "
        "ORDER BY postid DESC ",
        (logname, logname, )
    )

    for post in cur.fetchall():
        posttemp = {}
        posttemp['imgurl'] = post['filename']
        posttemp['owner'] = post['owner']
        posttemp['timestamp'] = arrow.get(post['created']).humanize()
        posttemp['postid'] = post['postid']
        # get pfp url
        cur = connection.execute(
            "SELECT filename "
            "FROM users "
            "WHERE username = ? ",
            (posttemp['owner'], )
        )
        posttemp['owner_img_url'] = cur.fetchall()[0]['filename']

        # get number of likes
        cur = connection.execute(
            "SELECT COUNT(*) "
            "FROM likes "
            "WHERE postid = ? ",
            (posttemp['postid'], )
        )
        posttemp['likes'] = cur.fetchall()[0]['COUNT(*)']

        # get comments
        comments = []
        cur = connection.execute(
            "SELECT owner, text "
            "FROM comments "
            "WHERE postid = ? "
            "ORDER BY commentid ASC",
            (posttemp['postid'], )
        )
        for comment in cur.fetchall():
            temp = {"owner": comment['owner'], "text": comment['text']}
            comments.append(temp)

        posttemp['comments'] = comments
        # Has user liked the post
        cur = connection.execute(
            "SELECT COUNT(*) "
            "FROM likes "
            "WHERE postid = ? AND owner = ?",
            (posttemp['postid'], logname, )
        )
        if cur.fetchall()[0]['COUNT(*)'] == 0:
            liked_by_logname = "no"
        else:
            liked_by_logname = "yes"
        posttemp['liked_by_logname'] = liked_by_logname
        context['posts'].append(posttemp)

    return render_template("index.html", **context)
