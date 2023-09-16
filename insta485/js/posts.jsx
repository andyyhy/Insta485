import React from "react";
import InfiniteScroll from "react-infinite-scroll-component";
import PropTypes from "prop-types";
import Post from "./post";

class Posts extends React.Component {
  constructor(props) {
    super(props);
    this.fetchData = this.fetchData.bind(this);
    this.state = {
      results: [],
      next: "",
      postTotal: 0,
    };
  }

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
          results: data.results,
          next: data.next,
          postTotal: data.results.length,
        });
        console.log(data.results.length);
      })
      .catch((error) => console.log(error));
  }

  fetchData() {
    setTimeout(() => {
      console.log(this.state);
      const { next } = this.state;
      fetch(next, { credentials: "same-origin" })
        .then((response) => {
          if (!response.ok) throw Error(response.statusText);
          return response.json();
        })
        .then((data) => {
          this.setState((prevState) => ({
            results: prevState.results.concat(data.results),
            next: data.next,
            postTotal: data.results.length + prevState.postTotal,
          }));
          console.log(data.results);
        })
        .catch((error) => console.log(error));
    }, 500);
  }

  render() {
    const { results, next, postTotal } = this.state;

    let hasMore;
    // Determine if there are more posts
    if (next === "") {
      hasMore = false;
    } else {
      hasMore = true;
    }

    return (
      <InfiniteScroll
        key="infiniteScroll"
        dataLength={postTotal}
        next={this.fetchData}
        hasMore={hasMore}
        loader={<h4>Loading...</h4>}
      >
        {results.map((post) => (
          <div className="Posts" key={post.postid}>
            <Post url={post.url} key={post.postid} />
          </div>
        ))}
      </InfiniteScroll>
    );
  }
}
Posts.propTypes = {
  url: PropTypes.string.isRequired,
};
export default Posts;
