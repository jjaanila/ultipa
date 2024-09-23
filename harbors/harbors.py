from datetime import datetime, timedelta
import random
import re
import pandas as pd

raw = pd.read_csv("./harbors.csv")


def dms2dec(dms_str):
    """Return decimal representation of DMS

    >>> dms2dec(utf8(48°53'10.18"N))
    48.8866111111F

    >>> dms2dec(utf8(2°20'35.09"E))
    2.34330555556F

    >>> dms2dec(utf8(48°53'10.18"S))
    -48.8866111111F

    >>> dms2dec(utf8(2°20'35.09"W))
    -2.34330555556F

    """

    dms_str = re.sub(r"\s", "", dms_str)

    sign = -1 if re.search("[swSW]", dms_str) else 1

    numbers = list(filter(len, re.split("\D+", dms_str, maxsplit=4)))

    degree = numbers[0]
    minute = numbers[1] if len(numbers) >= 2 else "0"
    second = numbers[2] if len(numbers) >= 3 else "0"
    frac_seconds = numbers[3] if len(numbers) >= 4 else "0"

    second += "." + frac_seconds
    return sign * (int(degree) + float(minute) / 60 + float(second) / 3600)


harbors = raw[
    [
        "portNumber",
        "portName",
        "regionName",
        "latitude",
        "longitude",
        "harborSize",
        "repairCode",
    ]
]

harbors = harbors.rename(
    columns={
        "portNumber": "_id",
        "portName": "name",
        "regionName": "region_name",
        "harborSize": "size",
        "repairCode": "repairs",
    }
)


harbors["latitude"] = harbors["latitude"].apply(dms2dec)
harbors["longitude"] = harbors["longitude"].apply(dms2dec)

harbors.to_csv("./harbor_nodes.csv", index=False)
print(pd.read_csv("./harbor_nodes.csv", nrows=100))

ships = pd.DataFrame(
    [
        [1, "Titanic", 59.161788, 20.554950],
        [2, "The Flying Dutchman", 47.948486, -33.802952],
        [3, "Santa Maria", 71.449312, -60.950974],
        [4, "Bismarck", 11.978379, -144.622851],
        [5, "The Mayflower", -16.527435, 97.076370],
    ],
    columns=["_id", "name", "latitude", "longitude"],
)

ships.to_csv("./ship_nodes.csv", index=False)
print(pd.read_csv("./ship_nodes.csv", nrows=100))

left = pd.DataFrame(columns=["_to", "_from", "timestamp"])
headed = pd.DataFrame(columns=["_to", "_from", "scheduled_arrival_at"])
for index, ship in ships.iterrows():
    left.loc[len(left.index)] = [
        ship["_id"],
        harbors.sample(1)["_id"].values[0],
        datetime.now() - timedelta(days=random.randint(1, 24)),
    ]
    headed.loc[len(headed.index)] = [
        ship["_id"],
        harbors.sample(1)["_id"].values[0],
        datetime.now() + timedelta(days=random.randint(1, 8)),
    ]

left.to_csv("./left_edges.csv", index=False)
print(pd.read_csv("./left_edges.csv", nrows=100))

headed.to_csv("./headed_edges.csv", index=False)
print(pd.read_csv("./headed_edges.csv", nrows=100))
