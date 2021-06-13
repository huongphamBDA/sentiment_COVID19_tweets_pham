# Huong Pham, RedID: xxxxxxx, Final Project GEOG-582, Fall 2020

import os
import time
import pandas as pd
from geopy.geocoders import Nominatim


fp = "../data/tweets_09_20_2020.csv"

df = pd.read_csv(fp, usecols=['text', 'user_location', 'created_at'], keep_default_na=False)
df = df[df["user_location"].str.contains("CA")]     # (CA: 3608 tweets)

# remove empty user_location values
nan_value = float("NaN")
df.replace("", nan_value, inplace=True)
df.dropna(subset=["user_location"], inplace=True)


def do_geocode(address):
    try:
        geolocator = Nominatim(user_agent="final_project_pham")
        location = geolocator.geocode(address)
        time.sleep(1)
        return location

    except Exception as e:
        print(e)


df['user_location_coord'] = ""

for ind in df.index:
    geocode_res = do_geocode(address=str(df['user_location'][ind]))

    if geocode_res:
        df.at[ind, 'user_location_coord'] = "{}, {}".format(geocode_res.latitude, geocode_res.longitude)
    else:
        df.drop(index=ind)

# delete rows that have empty strings in the coordinates column:
df['user_location_coord'].replace('', pd.np.nan, inplace=True)
df.dropna(subset=['user_location_coord'], inplace=True)

count_row = df.shape[0]
print(f"\nThere are {count_row} tweets in this dataset.")   # get 3400 tweets

# output file that contains coordinates:
df_with_coords_fp = os.path.join("../output", "df_with_coords.csv")
df.to_csv(df_with_coords_fp)


def main():
    print('this is geocode_pham module')


if __name__ == "__main__":
    main()


