import pandas as pd

def load_bluebike_data():
    return pd.read_csv("data/classifiedbluebike_trips.csv")

def load_traveltime_data():
    return pd.read_csv("data/traveltimes.csv")
