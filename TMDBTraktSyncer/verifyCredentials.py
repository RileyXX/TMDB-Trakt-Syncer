import os
import json
try:
    from TMDBTraktSyncer import authTrakt
except:
    import authTrakt

# Define the file path
here = os.path.abspath(os.path.dirname(__file__))
file_path = os.path.join(here, 'credentials.txt')

# Check if the file exists
if not os.path.isfile(file_path):
    # If the file does not exist, create it with default values
    default_values = {
        "trakt_client_id": "empty",
        "trakt_client_secret": "empty",
        "trakt_access_token": "empty",
        "tmdb_v4_token": "empty",
    }
    with open(file_path, "w") as f:
        json.dump(default_values, f)

# Load the values from the file
with open(file_path, "r") as f:
    values = json.load(f)

# Check if any of the values are "empty" and prompt the user to enter them
for key in values.keys():
    if values[key] == "empty" and key != "trakt_access_token":
        values[key] = input(f"Please enter a value for {key}: ").strip()
        with open(file_path, "w") as f:
            json.dump(values, f)

# Get the trakt_access_token value if it exists, or run the authTrakt.py function to get it
trakt_access_token = None
if "trakt_access_token" in values and values["trakt_access_token"] != "empty":
    trakt_access_token = values["trakt_access_token"]
else:
    client_id = values["trakt_client_id"]
    client_secret = values["trakt_client_secret"]
    trakt_access_token = authTrakt.authenticate(client_id, client_secret)
    values["trakt_access_token"] = trakt_access_token
    with open(file_path, "w") as f:
        json.dump(values, f)

# Save the credential values as variables
trakt_client_id = values["trakt_client_id"]
trakt_client_secret = values["trakt_client_secret"]
trakt_access_token = values["trakt_access_token"]
tmdb_v4_token = values["tmdb_v4_token"]