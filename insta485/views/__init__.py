"""Views, one for each Insta485 page."""
from insta485.views.index import show_index
from insta485.views.user import show_user, show_followers
from insta485.views.post import show_post
from insta485.views.explore import show_explore
from insta485.views.accounts import show_login, post_logout, show_create
from insta485.views.accounts import show_delete, show_edit, show_password
from insta485.views.likes import post_likes
from insta485.views.comments import post_comments
from insta485.views.upload_post import post_posts
from insta485.views.image import download_image
from insta485.views.post_following import post_following
from insta485.views.post_accounts import post_accounts
