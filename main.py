# Huong Pham, RedID: xxx, Final Project GEOG-582, Fall 2020

import pandas as pd
from finalproject_pham.libs.choropleth_pham import PointMap, PolygonMap, get_us_county_map
from finalproject_pham.libs.process_tweets_pham import process_tweet
from finalproject_pham.libs.textblob_pham import TextBlobResults, generate_word_cloud


def main():
    # 1. Read tweet data with geocoded coordinates
    file_path = "./output/df_with_coords.csv"
    # read csv file and put it in a data frame:
    df = pd.read_csv(file_path, keep_default_na=False)

    # 2. Process tweets and add a new column for cleaned tweets
    df['cleaned_text'] = df['text'].apply(process_tweet)

    # 3. Produce textblob results by using textblob_pham module
    generate_word_cloud(df["cleaned_text"], "09-20-2020", file_path)

    # Create a TextBlobResults instance
    tb = TextBlobResults(df, file_path)
    tb.generate_text_blob()
    tb.graph_polarity_scores()
    tb.graph_polarity_vs_subjectivity()
    tb.display_most_sentiment_tweets()
    tb.create_wordcloud_most_sentiment_tweets()
    tb.display_and_create_graph_polarity_top_cities()

    # Create dataframe from textblob results
    out_fp = tb.output_df_to_csv()
    df_textblob = pd.read_csv(out_fp)

    # 4. Plot maps for textblob results by using choropleth_pham module
    # Create PointMap class instance
    point_map = PointMap(df_textblob)
    point_map.split_lat_lon()

    geo_df_textblob = point_map.create_geopanda_dataframe()
    us_county = get_us_county_map()

    # Create PolygonMap class instance
    polygon_map = PolygonMap(geo_df_textblob, us_county)
    polygon_map.join_dfs_and_group_by_polarity_category()
    polygon_map.plot_choropleth()


if __name__ == '__main__':
    main()
