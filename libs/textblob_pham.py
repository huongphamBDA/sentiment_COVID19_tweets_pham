# Huong Pham, RedID: xxx, Final Project GEOG-582, Fall 2020

import os
import sys
import pandas as pd
import seaborn

from textblob import TextBlob
from wordcloud import STOPWORDS, WordCloud
from sklearn.feature_extraction.text import TfidfVectorizer
from matplotlib import pyplot as plt
from IPython.display import display


class TextBlobResults:
    """This is TextBlob class to present TextBlob method results"""

    def __init__(self, df, file_path):
        """
        TextBlob class constructor
        :param df: the dataframe that needs to apply TextBlob method
        :param file_path: the file path of that dataframe
        """
        self.df = df
        self.file_path = file_path

    def generate_text_blob(self):
        """using TextBlob to do sentiment analysis"""
        pol = lambda x: TextBlob(x['cleaned_text']).sentiment.polarity
        sub = lambda x: TextBlob(x['cleaned_text']).sentiment.subjectivity
        self.df['polarity'] = self.df.apply(pol, axis=1)
        self.df['subjectivity'] = self.df.apply(sub, axis=1)

        # analyze polarity index:
        def analyze_polarity(polarity):
            if polarity > 0:
                return "Positive"
            if polarity == 0:
                return "Neutral"
            if polarity < 0:
                return "Negative"

        self.df["polarity_category"] = self.df["polarity"].apply(analyze_polarity)
        print(self.df["polarity_category"].value_counts())

    def graph_polarity_scores(self):
        """display the polarity counts"""
        self.df["polarity_category"].astype("category")
        seaborn.countplot(self.df["polarity_category"])
        plt.title("Polarity Counts")
        plt.savefig("./output/polarity_scores.png")
        plt.show()

    def graph_polarity_vs_subjectivity(self):
        """visualize subjectivity versus polarity on a same chart"""
        plt.figure(figsize=(7, 7))
        seaborn.scatterplot(x="polarity", y="subjectivity", hue='polarity_category', data=self.df)
        plt.title("Subjectivity vs. Polarity")
        plt.savefig("./output/subjectivity_vs_polarity.png")
        plt.show()

    def display_most_sentiment_tweets(self):
        print('\ndisplay the positive tweets:')
        assorted1 = self.df.sort_values(by=["polarity"], axis=0, ascending=False)
        assorted1_head = assorted1[['text', 'cleaned_text', 'polarity']].head(20)
        print(self.file_path)
        assorted1_head.to_csv(sys.stdout)

        print('\ndisplay the negative tweets:')
        assorted2 = self.df.sort_values(by=["polarity"], axis=0, ascending=True)
        assorted2_head = assorted2[['text', 'cleaned_text', 'polarity']].head(20)
        print(self.file_path)
        assorted2_head.to_csv(sys.stdout)

    def create_wordcloud_most_sentiment_tweets(self):
        # create word cloud for 200 most positive words:
        df_ca_sort_polarity = self.df.sort_values(by=["polarity"], axis=0, ascending=False)
        positive_df = df_ca_sort_polarity.head(200)
        # positive_df columns: 'text', 'user_location', 'cleaned_text', 'polarity', 'subjectivity', 'polarity_category'
        generate_word_cloud(positive_df["cleaned_text"], "positive")
        # create word cloud for 200 most negative words:
        df_ca_sort_polarity = self.df.sort_values(by=["polarity"], axis=0, ascending=True)
        negative_df = df_ca_sort_polarity.head(200)
        # negative_df columns: 'text', 'user_location', 'cleaned_text', 'polarity', 'subjectivity', 'polarity_category'
        generate_word_cloud(negative_df["cleaned_text"], "negative")

    def display_and_create_graph_polarity_top_cities(self):
        positives_by_cities = self.df[self.df.user_location != 'unknown'].groupby("polarity_category")[
            "user_location"].value_counts().Positive.sort_values(ascending=False)
        negatives_by_cities = self.df[self.df.user_location != 'unknown'].groupby("polarity_category")[
            "user_location"].value_counts().Negative.sort_values(ascending=False)
        # negatives_by_country = tweets_processed[tweets_processed.Country != 'unknown'].groupby("Label")[
        #     "Country"].value_counts().Positive.sort_values(ascending=False)
        print("\nPositive Polarity by Cities:")
        print(positives_by_cities)
        print("\nNegative Polarity by Cities:")
        print(negatives_by_cities)

        cities = self.df[self.df.user_location != 'unknown']
        top_cities = cities["user_location"].value_counts(sort=True).head(20)

        # Create a mask for top 6 cities (by tweets count)
        mask = self.df["user_location"].isin(top_cities.index[:6]).values

        top_06_cities_list = list(top_cities.index)
        print("Top 20 cities with most tweets: {}".format(top_cities))
        # Create a new DataFrame only includes top six cities
        top_6_cities_df = self.df.iloc[mask, :]

        # Visualize the top six cities
        plt.figure(figsize=(7, 6))
        seaborn.countplot(x="user_location", hue="polarity_category", data=top_6_cities_df,
                          order=top_6_cities_df["user_location"].value_counts().index)
        plt.xlabel("User Location")
        locs, labels = plt.xticks()
        plt.xticks(locs, top_06_cities_list[:6])
        plt.xticks(rotation=20)
        plt.ylabel("Tweet count")
        plt.title("Top 06 Cities\n" + "{}".format(self.file_path))
        plt.savefig("./output/top_cities_polarity_labels.png")
        plt.show()

    def output_df_to_csv(self):
        # output the dataframe to csv file:
        output_dir = "./output"
        # output file:
        out_fname = "textblob_df_with_coords.csv"
        out_fp = os.path.join(output_dir, out_fname)
        self.df.to_csv(out_fp)
        return out_fp


def generate_word_cloud(cleaned_tweet_column, label, file_path=""):
    my_own_stopwords = ["covid", "coronavirus", "pandemic", "california", "will", "americans", "county", "doesn",
                        "take", "trump", "biden", "don", "new", "want", "know", "think", "one", "see"]

    # Combine STOPWORDS from Word Cloud library with my own stopwords:
    stop_words = list(STOPWORDS) + my_own_stopwords

    # Initialize a Tf-idf Vectorizer by creating an instance of the class. Use the most 5000 frequent words
    vectorizer = TfidfVectorizer(max_features=5000, stop_words=stop_words)
    # Tf-idf vectorizer transform text to feature vectors. Each word has a feature index.
    # Each tweet is a vector. In each vector, numbers represent the weight of the word, or tf-idf scores.

    # Fit and transform the vectorizer
    tfidf_matrix = vectorizer.fit_transform(cleaned_tweet_column)
    display(tfidf_matrix)
    # tfidf_matrix.sum(axis=0).T
    # print(tfidf_matrix.sum(axis=0).T.shape)

    # Create a new DataFrame called frequencies
    frequencies = pd.DataFrame(tfidf_matrix.sum(axis=0).T, index=vectorizer.get_feature_names(),
                               columns=['total frequency'])
    # Sort the words by frequency
    frequencies.sort_values(by='total frequency', ascending=False, inplace=True)

    # Initialize the word cloud
    wc = WordCloud(width=1000, height=1000, min_font_size=10, max_words=2000,
                   background_color='white', stopwords=stop_words)
    # Create word cloud for 5000 words in the frequencies dataframe (index)
    mytext = " ".join(frequencies.index)
    wc.generate(mytext)

    # Display the generated image of the word cloud
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.title("Common words in the " + label + " tweets\n" + "{}\n".format(file_path))
    path_fig = os.path.join('./output', '{}.png'.format(label))
    plt.savefig(path_fig)
    plt.show()


def main():
    print('this is textblob_pham module')


if __name__ == "__main__":
    main()

