"""REST API for posts."""
import flask
import insta485
from insta485.model import authenticate, get_comment_details, \
    get_likes_info, get_post_data, set_username, generate_403


@insta485.app.route('/api/v1/posts/')
def get_posts():
    """Return the 10 newest posts."""
    # Authentication
    context = {}
    if not authenticate():
        context = generate_403()
        return flask.jsonify(**context), 403

    username = set_username()

    # Calculate size and page
    limit = flask.request.args.get("size", default=10, type=int)
    page = flask.request.args.get("page", default=0, type=int)
    offset = page * limit

    if limit < 0 or page < 0:
        context["message"] = "Bad Request"
        context["status_code"] = "400"
        return flask.jsonify(**context), 400

    # Get the newest postid
    connection = insta485.model.get_db()

    cur = connection.execute(
        "SELECT postid "
        "FROM posts "
        "ORDER BY postid DESC ",
    )
    max_postid = cur.fetchall()[0]["postid"]

    # Process postids
    postid_lte = flask.request.args.get(
        "postid_lte", default=max_postid, type=int)

    # Get postids
    cur = connection.execute(
        "SELECT postid "
        "FROM posts "
        "WHERE postid <= ? AND owner IN "
        "(SELECT username2 "
        "FROM following "
        "WHERE username1 = ? OR username2 = ?) "
        "ORDER BY postid DESC "
        "LIMIT ? OFFSET ?",
        (postid_lte, username, username, limit, offset)
    )
    posts = cur.fetchall()

    results = []
    counter = 0
    for post in posts:
        url = "/api/v1/posts/" + str(post["postid"]) + "/"
        results.append({"postid": post["postid"], "url": url})
        counter += 1
    context['results'] = results

    if counter < limit:
        context['next'] = ""
    else:
        context['next'] = "/api/v1/posts/?size=" + \
            str(limit) + "&page=" + str(page+1) + \
            "&postid_lte=" + str(postid_lte)

    if "size" in flask.request.args or \
        "page" in flask.request.args or \
            "postid_lte" in flask.request.args:
        context['url'] = flask.request.full_path
    else:
        context['url'] = flask.request.path
    return flask.jsonify(**context), 200


@insta485.app.route('/api/v1/posts/<postid>/')
def get_post(postid):
    """Return the details for one post."""
    # Authentication
    context = {}
    if not authenticate():
        context = generate_403()
        return flask.jsonify(**context), 403

    username = set_username()

    connection = insta485.model.get_db()
    # Check that post is in database
    cur = connection.execute(
        "SELECT COUNT(*) "
        "FROM posts "
        "WHERE postid = ? ",
        (postid, )
    )
    if cur.fetchall()[0]['COUNT(*)'] == 0:
        context["message"] = "Not Found"
        context["status_code"] = 404
        return flask.jsonify(**context), 404

    # Get Comment details
    commentdata = get_comment_details(postid)
    comments = []
    for comment in commentdata:
        temp = {"owner": comment['owner'], "text": comment['text'],
                "commentid": comment['commentid']}
        if username == temp['owner']:
            temp["lognameOwnsThis"] = True
        else:
            temp["lognameOwnsThis"] = False
        temp["ownerShowUrl"] = "/users/" + comment['owner'] + "/"
        temp["url"] = "/api/v1/comments/" + str(temp["commentid"]) + "/"

        comments.append(temp)
    context["comments"] = comments
    context["comments_url"] = "/api/v1/comments/?postid=" + str(postid)

    # Post info
    postdata = get_post_data(postid)
    context["created"] = postdata['created']
    context["imgUrl"] = "/uploads/" + postdata['filename']

    # likes info
    likes = get_likes_info(postid)
    # Has user liked the post
    cur = connection.execute(
        "SELECT COUNT(*) "
        "FROM likes "
        "WHERE postid = ? AND owner = ?",
        (postid, username, )
    )
    if cur.fetchall()[0]['COUNT(*)'] == 0:
        liked_by_logname = False
    else:
        liked_by_logname = True

    if liked_by_logname:
        # Get the like id
        cur = connection.execute(
            "SELECT likeid "
            "FROM likes "
            "WHERE postid = ? AND owner = ?",
            (postid, username, )
        )
        likeid = cur.fetchall()[0]["likeid"]
        url = "/api/v1/likes/" + str(likeid) + "/"
    else:
        url = None
    context["likes"] = {
        "lognameLikesThis": liked_by_logname, "numLikes": likes, "url": url}

    # Post Owner Info
    context["owner"] = postdata['owner']
    # get pfp url
    cur = connection.execute(
        "SELECT filename "
        "FROM users "
        "WHERE username = ? ",
        (context["owner"], )
    )
    owner_img_url = cur.fetchall()[0]['filename']
    context["ownerImgUrl"] = "/uploads/" + owner_img_url
    context["ownerShowUrl"] = "/users/" + context["owner"] + "/"
    context["postShowUrl"] = "/posts/" + str(postid) + "/"
    context["postid"] = int(postid)
    context["url"] = flask.request.path

    return flask.jsonify(**context), 200
