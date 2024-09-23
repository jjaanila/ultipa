import pandas as pd

raw = pd.read_csv("./ratings.csv")

users = raw[["User_id", "profileName"]].drop_duplicates("User_id").dropna(subset="User_id")
users.to_csv("./user_nodes.csv", index=False)

books = raw[["Id", "Title", "Price"]].drop_duplicates("Id").dropna(subset="Id")
books.to_csv("./book_nodes.csv", index=False)

reviews = raw[["Id", "User_id", "review/score", "review/helpfulness", "review/time", "review/summary", "review/text"]].dropna(subset="Id").dropna(subset="User_id")
reviews["review/score"].astype(float).fillna(0.0)
reviews["created_at"] = reviews['review/time'].apply(lambda x: pd.to_datetime(x, unit="s"))
reviews = reviews.drop(columns=["review/time"])
reviews = reviews.rename(columns={
    "review/score": "score", "review/helpfulness": "helpfulness", "review/summary": "summary", "review/text": "text"
})
reviews = reviews.dropna()
reviews.to_csv("./review_edges.csv", index=False)
print(pd.read_csv("./review_edges.csv", nrows=100))