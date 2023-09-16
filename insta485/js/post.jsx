import React from "react";
import PropTypes from "prop-types";
import moment from "moment";

class Post extends React.Component {
  // Display a single post

  constructor(props) {
    // Initialize mutable state
    super(props);
    this.handleUnlike = this.handleUnlike.bind(this);
    this.handlelike = this.handlelike.bind(this);
    this.state = {
      comments: [],
      likes: {},
      imgUrl: "",
      owner: "",
      ownerImg: "",
      ownerUrl: "",
      timestamp: "",
      postUrl: "",
      postid: "",
      newComment: "",
    };
  }

  // Initialize
  componentDidMount() {
    // This line automatically assigns this.props.url to the const variable url
    const { url } = this.props;

    // Call REST API to get the post's information
    fetch(url, { credentials: "same-origin" })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState({
          imgUrl: data.imgUrl,
          owner: data.owner,
          ownerImg: data.ownerImgUrl,
          ownerUrl: data.ownerShowUrl,
          timestamp: data.created,
          postUrl: data.postShowUrl,
          comments: data.comments,
          likes: data.likes,
          postid: data.postid,
        });
      })
      .catch((error) => console.log(error));
  }

  // Handler for unlike
  handleUnlike() {
    const { likes } = this.state;
    fetch(likes.url, { credentials: "same-origin", method: "DELETE" })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .catch((error) => console.log(error));
    this.setState({
      likes: {
        lognameLikesThis: false,
        numLikes: likes.numLikes - 1,
        url: null,
      },
    });
  }

  // Handler for like
  handlelike() {
    const { likes, postid } = this.state;
    fetch(`/api/v1/likes/?postid=${postid}`, {
      credentials: "same-origin",
      method: "POST",
    })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState({
          likes: {
            lognameLikesThis: true,
            numLikes: likes.numLikes + 1,
            url: data.url,
          },
        });
      })
      .catch((error) => console.log(error));
  }

  // Handler for delete comment
  handleDelete(deletedComment) {
    const { comments } = this.state;
    fetch(deletedComment.url, { credentials: "same-origin", method: "DELETE" })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .catch((error) => console.log(error));
    const newComments = comments.filter(
      (comment) => comment.commentid !== deletedComment.commentid
    );
    this.setState({ comments: newComments });
  }

  // Handler for changing comment in comment box
  handleChange(event) {
    this.setState({ newComment: event.target.value });
  }

  // Handler for adding new comment
  handleNew(event) {
    const { newComment, postid } = this.state;
    fetch(`/api/v1/comments/?postid=${postid}`, {
      credentials: "same-origin",
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: newComment }),
    })
      .then((response) => {
        if (!response.ok) throw Error(response.statusText);
        return response.json();
      })
      .then((data) => {
        this.setState((prevState) => ({
          comments: prevState.comments.concat(data),
          newComment: "",
        }));
      })
      .catch((error) => console.log(error));
    event.preventDefault();
  }

  // Helper for rendering one comment
  renderComment(comment) {
    if (comment.lognameOwnsThis) {
      return (
        <p key={comment.commentid}>
          <a key={comment.commentid + 1} href={comment.ownerShowUrl}>
            {comment.owner}
          </a>{" "}
          {comment.text}
          <button
            onClick={this.handleDelete.bind(this, comment)}
            className="delete-comment-button"
            type="button"
            key={comment.commentid + 2}
          >
            delete
          </button>
        </p>
      );
    }

    return (
      <p key={comment.commentid}>
        <a key={comment.commentid} href={comment.ownerShowUrl}>
          {comment.owner}
        </a>{" "}
        {comment.text}
      </p>
    );
  }

  // Helper for rendering all comments
  renderComments() {
    const { comments } = this.state;
    return comments.map((comment) => this.renderComment(comment));
  }

  // Render one post
  render() {
    const {
      imgUrl,
      owner,
      ownerUrl,
      ownerImg,
      timestamp,
      postUrl,
      likes,
      newComment,
      postid,
      comments,
    } = this.state;

    // Determine if like or unlike
    let button;
    let post;
    if (likes.lognameLikesThis) {
      button = (
        <button
          onClick={this.handleUnlike}
          className="like-unlike-button"
          type="button"
          key={likes.likeid}
        >
          unlike
        </button>
      );
      post = <img key={postid + 1} src={imgUrl} alt="post_image" />;
    } else {
      button = (
        <button
          onClick={this.handlelike}
          className="like-unlike-button"
          type="button"
          key={likes.likeid}
        >
          like
        </button>
      );
      post = (
        <img
          key={postid + 1}
          src={imgUrl}
          alt="post_image"
          onDoubleClick={this.handlelike}
        />
      );
    }

    // Determine the wording for likes
    let likesCounter;
    if (likes.numLikes === 1) {
      likesCounter = <p key={likes.likeid}>{likes.numLikes} like</p>;
    } else {
      likesCounter = <p key={likes.likeid}>{likes.numLikes} likes</p>;
    }
    return (
      <div className="post" key={postid}>
        <div className="postHeader" key={postid}>
          <div className="userInfo" key={postid}>
            <a key={postid} href={ownerUrl}>
              <img src={ownerImg} key={postid} alt="Profile Pic" />
            </a>
            <a key={postid + 1} href={ownerUrl}>
              {owner}
            </a>
          </div>
          <div className="timestamp" key={postid + 1}>
            <a key={postid + 2} href={postUrl}>
              {moment.duration(timestamp).humanize()}
            </a>
          </div>
        </div>
        {post}
        <div className="likes" key={likes.likeid}>
          {button}
          {likesCounter}
        </div>
        <div className="comments" key={comments.commentid}>
          {this.renderComments()}
          <form
            key={comments.commentid}
            className="comment-form"
            onSubmit={this.handleNew.bind(this)}
          >
            <input
              type="text"
              key={comments.commentid}
              required
              value={newComment}
              onChange={this.handleChange.bind(this)}
            />
          </form>
        </div>
      </div>
    );
  }
}
Post.propTypes = {
  url: PropTypes.string.isRequired,
};
export default Post;
