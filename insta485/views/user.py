"""
Insta485 user view.

URLs include:
/users/<user_url_slug>/
/users/<user_url_slug>/following/
/users/<user_url_slug>/followers/
"""
from flask import abort, render_template, session, request, redirect, url_for
import insta485
from insta485.model import user_exists


@insta485.app.route('/users/<usr>/')
def show_user(usr):
    """Show user."""
    if 'username' not in session:
        return redirect(url_for('show_login'))

    context = {'logname': session['username'],
               'posts': [], "current_url": request.path, 'username': usr}
    # Connect to database
    connection = insta485.model.get_db()
    logname = session['username']
    username = usr

    # Get fullname
    cur = connection.execute(
        "SELECT fullname "
        "FROM users "
        "WHERE username = ? ",
        (username, )
    )
    context["fullname"] = cur.fetchall()[0]["fullname"]

    # Is user is followed by logname
    cur = connection.execute(
        "SELECT COUNT(*) "
        "FROM following "
        "WHERE username1 = ? AND username2 = ? ",
        (logname, username, )
    )
    is_following = cur.fetchall()[0]["COUNT(*)"]
    context['is_following'] = is_following

    # Count number of following
    cur = connection.execute(
        "SELECT COUNT(*) "
        "FROM following "
        "WHERE username1 = ? ",
        (username, )
    )
    following = cur.fetchall()[0]["COUNT(*)"]
    context["following"] = following

    # Count number of followers
    cur = connection.execute(
        "SELECT COUNT(*) "
        "FROM following "
        "WHERE username2 = ? ",
        (username, )
    )
    followers = cur.fetchall()[0]["COUNT(*)"]
    context["followers"] = followers
    # get all user posts and number of posts
    cur = connection.execute(
        "SELECT postid, filename "
        "FROM posts "
        "WHERE owner = ? "
        "ORDER BY postid ASC ",
        (username, )
    )
    postdata = cur.fetchall()
    for post in postdata:
        img_url = post['filename']
        postid = post['postid']

        posttemp = {'img_url': img_url, 'postid': postid}
        context['posts'].append(posttemp)

    total_posts = len(postdata)
    context['total_posts'] = total_posts
    return render_template("user.html", **context)


@insta485.app.route('/users/<usr>/followers/')
def show_followers(usr):
    """Show followers."""
    if 'username' not in session:
        return redirect(url_for('show_login'))

    context = {'logname': session['username'],
               'followers': [], "current_url": request.path, 'username': usr}
    # Connect to database
    connection = insta485.model.get_db()
    logname = session['username']
    username = usr

    # Check if user exists
    if user_exists(username) is False:
        abort(404)

    # get data for all user's followers
    cur = connection.execute(
        "SELECT username1 "
        "FROM following "
        "WHERE username2 = ? ",
        (username, )
    )
    follwerdata = cur.fetchall()

    for follower in follwerdata:
        followerusername = follower['username1']
        # Get pfp
        cur = connection.execute(
            "SELECT filename "
            "FROM users "
            "WHERE username = ? ",
            (followerusername, )
        )
        follower_img_url = cur.fetchall()[0]['filename']

        # Check if logname follows
        cur = connection.execute(
            "SELECT COUNT(*) "
            "FROM following "
            "WHERE username1 = ? AND username2 = ? ",
            (logname, followerusername, )
        )
        if cur.fetchall()[0]["COUNT(*)"] == 0:
            logname_follow_follower = False
        else:
            logname_follow_follower = True
        follower_temp = {"followerusername": followerusername,
                         "follower_img_url": follower_img_url,
                         "logname_follow_follower": logname_follow_follower}
        context["followers"].append(follower_temp)

    return render_template("followers.html", **context)


@insta485.app.route('/users/<usr>/following/')
def show_following(usr):
    """Show following."""
    if 'username' not in session:
        return redirect(url_for('show_login'))

    context = {'logname': session['username'],
               'followings': [], "current_url": request.path, 'username': usr}
    # Connect to database
    connection = insta485.model.get_db()
    logname = session['username']
    username = usr

    # Check if user exists
    if user_exists(username) is False:
        abort(404)

    # get data for all user's following
    cur = connection.execute(
        "SELECT username2 "
        "FROM following "
        "WHERE username1 = ? ",
        (username, )
    )
    follwingdata = cur.fetchall()

    for following in follwingdata:
        followingusername = following['username2']
        # Get pfp
        cur = connection.execute(
            "SELECT filename "
            "FROM users "
            "WHERE username = ? ",
            (followingusername, )
        )
        following_img_url = cur.fetchall()[0]['filename']

        # Check if logname follows
        cur = connection.execute(
            "SELECT COUNT(*) "
            "FROM following "
            "WHERE username1 = ? AND username2 = ? ",
            (logname, followingusername, )
        )
        if cur.fetchall()[0]["COUNT(*)"] == 0:
            logname_follow_following = False
        else:
            logname_follow_following = True
        following_temp = {"followingusername": followingusername,
                          "following_img_url": following_img_url,
                          "logname_follow_following": logname_follow_following}
        context["followings"].append(following_temp)

    return render_template("following.html", **context)
