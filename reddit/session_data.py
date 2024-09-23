from datetime import datetime, timedelta
import random
import string
import pandas as pd

N_OF_SESSIONS = 5000
N_OF_SITES = 500
site_paths = []
for n in range(N_OF_SITES):
    site_paths.append(
        "site:" + "".join(random.choice(string.ascii_uppercase) for _ in range(15))
    )
site_nodes = pd.DataFrame(site_paths, columns=["path"])
site_nodes.to_csv("./site_nodes.csv", index=False)

navigation_edges = pd.DataFrame([], columns=["_id", "_from", "_to", "created_at"])
navigation_edges.astype(
    dtype={"_id": "str", "_from": "str", "_to": "str", "created_at": "datetime64[ms]"}
)
for i in range(N_OF_SESSIONS):
    session = []
    session_id = "session:" + "".join(
        random.choice(string.ascii_uppercase) for _ in range(15)
    )
    for j in range(random.randint(1, 10)):
        prev_site = (
            session[-1][2] if len(session) else random.choice(site_nodes["path"])
        )
        next_site = random.choice(
            list(
                filter(
                    lambda x: x != prev_site if prev_site else True, site_nodes["path"]
                )
            )
        )
        created_at = (
            session[-1][3] + timedelta(seconds=random.randint(1, 30))
            if len(session)
            else datetime.now() - timedelta(seconds=random.randint(1, 60 * 60 * 24))
        )
        session.append([session_id, prev_site, next_site, created_at])
    print(session)
    session_df = pd.DataFrame(session, columns=["_id", "_from", "_to", "created_at"])
    session_df.astype(
        dtype={
            "_id": "str",
            "_from": "str",
            "_to": "str",
            "created_at": "datetime64[ms]",
        }
    )
    navigation_edges = pd.concat([navigation_edges, session_df])

navigation_edges.to_csv("./navigation_edges.csv", index=False)
