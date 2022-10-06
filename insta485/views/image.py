"""
Insta485 comments post.

URLs include:
/comments/
"""
import os
from flask import session, abort, send_from_directory
import insta485


@insta485.app.route('/uploads/<path:name>')
def download_image(name):
    """Download image."""
    if 'username' not in session:
        abort(403)
    if not os.path.isfile(insta485.app.config['UPLOAD_FOLDER'] / name):
        abort(404)
    uploadfolder = insta485.app.config['UPLOAD_FOLDER']
    return send_from_directory(uploadfolder, name,
                               as_attachment=False)
