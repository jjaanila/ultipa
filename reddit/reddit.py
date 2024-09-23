import pandas as pd

raw = pd.read_csv("./soc-redditHyperlinks-body.tsv", sep="\t")

subreddits = pd.DataFrame(
    pd.concat([raw["SOURCE_SUBREDDIT"], raw["TARGET_SUBREDDIT"]]).drop_duplicates()
)
subreddits.to_csv("./subreddit_nodes.csv", index=False)
posts = raw[["SOURCE_SUBREDDIT", "TARGET_SUBREDDIT", "TIMESTAMP", "LINK_SENTIMENT"]]
posts = posts.rename(
    columns={
        "SOURCE_SUBREDDIT": "source_subreddit",
        "TARGET_SUBREDDIT": "target_subreddit",
        "TIMESTAMP": "created_at",
        "LINK_SENTIMENT": "sentiment",
    }
)
posts.to_csv("./post_edges.csv", index=False)

print(pd.read_csv("./subreddit_nodes.csv", nrows=100))
print(pd.read_csv("./post_edges.csv", nrows=100))
