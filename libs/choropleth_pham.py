# Huong Pham, RedID: 824992682, Final Project GEOG-582, Fall 2020

import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt

from mpl_toolkits.axes_grid1 import make_axes_locatable
from shapely.geometry import Point


def get_us_county_map():
    """Read a polygon shapefile and create geopanda dataframe for us_county map"""

    # Download the US county map from TIGER/Line Shapefiles, www.census.gov
    fp_map = "./data/tl_2019_us_county/tl_2019_us_county.shp"

    # Create geopanda dataframe for the shapefile
    us_county = gpd.read_file(fp_map)  # us_county has same crs as geo_df_textblob's: "epsg: 4269"
    print("\nThe first 5 rows of us_county:\n", us_county.head())

    # Plot the map for California (STATEFP = 06)
    us_county[us_county.STATEFP == '06'].plot()
    plt.show()

    return us_county


class PointMap:
    """This is PointMap Class to plot locations of all tweet users on a map"""

    def __init__(self, df_textblob):
        self.df = df_textblob

    def split_lat_lon(self):
        """Split longitude and latitude from coordinates column of the dataframe"""

        lat = []
        lon = []

        # Iterate each row of the coordinates column
        for row in self.df['user_location_coord']:
            try:
                lat.append(row.split(',')[0])
                lon.append(row.split(',')[1])
            except Exception:
                lat.append(np.NaN)
                lon.append(np.NaN)

        # Put longitudes and latitudes in lat, lon columns
        self.df['latitude'] = lat
        self.df['longitude'] = lon

        print("First five rows of textblob df:\n", self.df.head())
        print("Textblob df columns: ", list(self.df.columns))

    def create_geopanda_dataframe(self):
        """Read textblob csv file, create geodataframe, and plot points on a map"""

        # Create an empty geometry list
        geometry = []
        # DataFrame.iterrows is a generator which yields both the index and row (as a Series):
        for i, row in self.df.iterrows():
            lat_iterrow = float(row['latitude'])
            lon_iterrow = float(row['longitude'])
            geometry.append(Point(lon_iterrow, lat_iterrow))

        # Coordinate reference system
        crs = "epsg:4269"  # using crs = {'init': 'epsg:4326'} will raise a deprecation warning from pyproj

        # Create Geopanda textblob dataframe
        geo_df_textblob = gpd.GeoDataFrame(self.df, crs=crs, geometry=geometry)

        # Plot points on a map
        geo_df_textblob.plot()
        plt.savefig("./output/PointMap.png")
        plt.show()

        return geo_df_textblob


class PolygonMap:
    """This is PylygonMap, to plot choropleth maps for the total of tweets, number of positive tweets,
    number of negative tweets, and number of neutral tweets for California counties."""

    def __init__(self, geo_df_textblob, us_county):
        self.geo_df = geo_df_textblob
        self.map = us_county

    def join_dfs_and_group_by_polarity_category(self):
        """Join the two geopanda dataframes and group by polarity category column"""

        # Join the two GeoDataFrames, using intersection of keys from both dfs and retain only left_df geometry column
        county_with_textblob = gpd.sjoin(self.map, self.geo_df, op="contains")
        print(county_with_textblob.head())

        # Group the new GeoDataFrame by "GEOID" and "polarity_category" columns
        # then create a new column to count the tweet number for each polarity category in each county
        grouped = county_with_textblob.groupby(["GEOID", "polarity_category"])["GEOID"].count().reset_index(
            name="count")
        print("\nThe first five rows of grouped df:\n", grouped.head())

        # Create new, separate geodataframes for positive/negative/neutral/total tweet counts in each county
        # Group into "positive", "negative" and "neutral" (resulting in new dataframes)
        df_positive = grouped.loc[grouped["polarity_category"] == "Positive"]
        df_negative = grouped.loc[grouped["polarity_category"] == "Negative"]
        df_neutral = grouped.loc[grouped["polarity_category"] == "Neutral"]
        print("\nPositive df:\n", df_positive.head())
        print("\nNegative df:\n", df_negative.head())
        print("\nNeutral df:\n", df_neutral.head())

        # Merge three new dataframes into us_county dataframe
        self.map = self.map.merge(df_positive, on='GEOID', how="left")
        self.map = self.map.merge(df_negative, on='GEOID', how="left")
        self.map = self.map.merge(df_neutral, on='GEOID', how="left")
        print("\nFirst five rows of us_county df after merging:\n", self.map.head())
        print(self.map.columns)

        # Delete unnecessary columns and rename new columns in us_county dataframe
        self.map = self.map.drop(columns=["polarity_category_x", "polarity_category_y", "polarity_category"])
        self.map = self.map.rename(columns={"count_x": "positive", "count_y": "negative", "count": "neutral"})
        print("\nFirst five rows of us_county after deleting:\n", self.map.head())
        print("\nAll columns of us_county dataframe:\n", self.map.columns)

        # Replace all NaN elements with 0s
        self.map["negative"].fillna(0, inplace=True)
        self.map["positive"].fillna(0, inplace=True)
        self.map["neutral"].fillna(0, inplace=True)
        print("\nFirst five rows of us_county after replacing NaN with 0s:\n", self.map.head())

        # Create a new column "total" to sum up all the tweets for each county
        self.map["total"] = self.map["positive"] + self.map["negative"] + self.map["neutral"]
        print("\nFirst five rows of us_county after having 'total' column:\n", self.map.head())

        print("max count of negative tweets:", self.map['negative'].max())  # 296.0
        print("max count of positive tweets:", self.map['positive'].max())  # 438.0
        print("max count of neutral tweets:", self.map['neutral'].max())  # 364.0
        print("max count of total of tweets:", self.map['total'].max())  # 1098.0

        return self.map

    def plot_choropleth(self):
        """Plot choropleth maps based on positive/negative/neutral/total tweet counts in each county"""

        # ---- PLOT SEPARATE MAP FOR 'TOTAL' COLUMN ----

        fig, ax = plt.subplots(1, figsize=(12, 7))
        ax.annotate('\nby Huong Pham', xy=(0.6, .05), xycoords='figure fraction', fontsize=10, color='#555555')

        # Uncomment below codes to see names of counties
        # create new column for county coordinates
        self.map['coords'] = self.map['geometry'].apply(lambda x: x.representative_point().coords[:])
        self.map['coords'] = [coords[0] for coords in self.map['coords']]
        # put county names on map
        for ind, row in self.map.iterrows():
            plt.annotate(s=row["NAME"], xy=row["coords"], horizontalalignment="center", fontsize=5)

        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="3%", pad=0.1)
        ax.margins(0.2, 0.2)
        ax.set_xlabel("Longitude", fontsize=10)
        ax.set_ylabel("Latitude", fontsize=10)
        ax.set_title("Choropleth Map - total of tweets, CA counties\n",
                     fontdict={'fontsize': '15', 'fontweight': '3'})
        self.map[self.map.STATEFP == '06'].plot(column="total", legend=True, cax=cax, cmap="YlOrRd_r",
                                                linewidth=0.8, ax=ax, edgecolor='0.8')
        plt.savefig("./output/PolygonMap_tweets_count.png")
        plt.show()

        # ---- PLOT 'TOTAL', 'POSITIVE', 'NEGATIVE', 'NEUTRAL' COLUMNS - ALL ON A SAME MAP ----

        # subplots() returns a Figure and four Axes
        fig, (ax1, ax2, ax3, ax4) = plt.subplots(nrows=1, ncols=4, figsize=(12, 7))
        ax1.axis('off')
        ax2.axis('off')
        ax3.axis('off')
        ax4.axis('off')

        ax1.annotate('Huong Pham, Final Project GEOG 582, Fall 2020',
                     xy=(0.6, .05), xycoords='figure fraction', fontsize=12, color='#555555')

        # 1 - based on total of tweets
        ax1.margins(0.2, 0.2)
        ax1.set_title("total", fontdict={'fontsize': '15', 'fontweight': '3'})
        self.map[self.map.STATEFP == '06'].plot(column="total", cmap="YlOrRd_r", linewidth=0.8, ax=ax1,
                                                edgecolor='0.8')

        # 2 - based on positive tweets
        ax2.margins(0.2, 0.2)
        ax2.set_title("positive", fontdict={'fontsize': '15', 'fontweight': '3'})
        self.map[self.map.STATEFP == '06'].plot(column="positive", cmap="Blues", linewidth=0.8, ax=ax2,
                                                edgecolor='0.8')

        # 3 - based on negative tweets
        ax3.margins(0.2, 0.2)
        ax3.set_title("negative", fontdict={'fontsize': '15', 'fontweight': '3'})
        self.map[self.map.STATEFP == '06'].plot(column="negative", cmap="Reds", linewidth=0.8, ax=ax3,
                                                edgecolor='0.8')

        # 4 - based on neutral tweets
        ax4.margins(0.2, 0.2)
        ax4.set_title("neutral", fontdict={'fontsize': '15', 'fontweight': '3'})
        self.map[self.map.STATEFP == '06'].plot(column="neutral", cmap="Greens", linewidth=0.8, ax=ax4,
                                                edgecolor='0.8')

        plt.savefig("./output/PolygonMaps.png")
        plt.show()


def main():
    print('this is choropleth_pham module')


if __name__ == "__main__":
    main()
