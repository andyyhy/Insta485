"""
Insta485 post view.

URLs include:
/users/posts/<postid_url_slug>
"""
from flask import render_template, session, request, redirect, url_for
import arrow
import insta485
from insta485.model import get_comment_details, get_likes_info, get_post_data


@insta485.app.route('/posts/<postid>/')
def show_post(postid):
    """Show post."""
    if 'username' not in session:
        return redirect(url_for('show_login'))

    context = {'logname': session['username'],
               'comments': [], "current_url": request.path,
               'postid': postid}
    # Connect to database
    connection = insta485.model.get_db()
    logname = session['username']

    # Get post img, owner, timestamp
    postdata = get_post_data(postid)
    context['post_img_url'] = postdata['filename']
    post_owner = postdata['owner']
    context['post_owner'] = post_owner
    timestamp = arrow.get(postdata['created']).humanize()
    context['timestamp'] = timestamp

    # get pfp url
    cur = connection.execute(
        "SELECT filename "
        "FROM users "
        "WHERE username = ? ",
        (post_owner, )
    )
    owner_img_url = cur.fetchall()[0]['filename']
    context['owner_img_url'] = owner_img_url

    # get number of likes
    likes = get_likes_info(postid=postid)
    context['likes'] = likes

    # get comments
    comments = []
    commentdata = get_comment_details(postid)
    for comment in commentdata:
        temp = {"owner": comment['owner'], "text": comment['text'],
                "commentid": comment['commentid']}
        comments.append(temp)
    context["comments"] = comments
    # Has user liked the post
    cur = connection.execute(
        "SELECT COUNT(*) "
        "FROM likes "
        "WHERE postid = ? AND owner = ?",
        (postid, logname, )
    )
    if cur.fetchall()[0]['COUNT(*)'] == 0:
        liked_by_logname = "no"
    else:
        liked_by_logname = "yes"
    context["liked_by_logname"] = liked_by_logname

    return render_template("post.html", **context)
