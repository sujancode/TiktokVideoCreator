class Reddit:
    def __init__(self,redditClient,sanitize_text,MoreCommentsINSTANCE) -> None:
        self.redditClient=redditClient
        self.sanitize_text=sanitize_text
        self.MoreCommentsINSTANCE=MoreCommentsINSTANCE

    def get_post_by_id(self,post_id):
        post=self.redditClient.submission(id=post_id)

        return {
            "id":post.id,
            "title":post.title,
            "author":post.author.name,
            "comments":post.num_comments,
            "score":post.score,
            "subreddit":post.subreddit.title
        }

    def get_top_comments_by_post(self,post_id,max_comment_length):
        submission = self.redditClient.submission(id=post_id)
        content={}
        content["thread_url"] = f"https://reddit.com{submission.permalink}"
        content["thread_title"] = submission.title
        content["thread_post"] = submission.selftext
        content["thread_id"] = submission.id
        content["comments"] = []

        for top_level_comment in submission.comments:
            if isinstance(top_level_comment, self.MoreCommentsINSTANCE):
                continue
            if top_level_comment.body in ["[removed]", "[deleted]"]:
                continue  # # see https://github.com/JasonLovesDoggo/RedditVideoMakerBot/issues/78
            if not top_level_comment.stickied:
                sanitised = self.sanitize_text(top_level_comment.body)
                if not sanitised or sanitised == " ":
                    continue
                if len(top_level_comment.body) <= int(max_comment_length):
                    if (
                        top_level_comment.author is not None
                        and self.sanitize_text(top_level_comment.body) is not None
                    ):  # if errors occur with this change to if not.
                        content["comments"].append(
                            {
                                "comment_body": top_level_comment.body,
                                "comment_url": top_level_comment.permalink,
                                "comment_id": top_level_comment.id,
                            }
                        )
        return content
        