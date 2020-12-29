# sentiment_sentiment_COVID19_tweets_pham
Sentiment analysis using Python 

Project Background: 

As of 12/17/2020, the U.S. marked the milestone of more than 300,000 coronavirus deaths since the beginning of the pandemic. Almost every two months we have 50,000 more deaths in the U.S. and the mortality rate is getting even higher this month. This virus is deadly, not to mention many devastating social and economic issues it has caused such as unemployment, stress on supply chains, events, business and school closure, working from home, and reduced consumer activities, etc. 

Many seniors said that they have never experienced anything like this in their lives, and neither did I. The COVID-19 pandemic with its bad effects is what triggered me to do a sentiment analysis on COVID-19 tweets. Millions of Americans use Twitter to disseminate news and information on social economic events every day. This is one of the best social media to find out what people concern about and how they react to the COVID-19 pandemic. 

I collected tweets data from the Panacea Lab (data source). My dataset includes all the tweets that relate to COVID-19 all over the world on 09/20/2020. The data I downloaded from Panacea Lab had only one ID column at first. I used Hydrator software to extract Tweet texts and the rest of other metadata. My data originally has 204,000 tweets in English. I pared it down to tweets that have key word “CA” in the user_location column and my dataset went down to 3,600 tweets as a result. 

Because of the privacy reason, The Panacea Lab do not share the coordinates of the tweets. And this is a disadvantage for me to present my analysis results. My solution is to use a geocoding service to geocode the tweet user locations and collect longitudes and latitudes for the tweets. The coordinates will then allow me to put locations of the tweet users on a map and create choropleth maps. Choropleth maps assign different colors for different range of sentiment index values, which can show us which counties have higher total number of tweets, which counties have more positive tweets, more negative tweets, or more neutral tweets than others. 

Code Implementation: 

(i)	  Geocoding tweets by using the OpenStreetMap Nominatim service [geocode_pham.py] and output the results to a csv file [df_with_coords.csv]
(ii)  Process tweet texts in the output csv file by using Regular Expressions [process_tweet_pham.py] and applying TextBlob method for sentiment analysis [textblob_pham.py]
(iii)	Present TextBlob results by making Word Clouds, bar charts, and graphs to show the most common topics for the COVID-19 tweets on 09/20/2020, the most common words for the positive/negative tweets on that day, the relationship between polarity and subjectivity index, the top cities in California that have higher number of tweets and components of their polarity labels. [textblob_pham.py]
(iv)	[choropleth_pham.py] Use GeoPandas library to put all user locations on a same map (Point geometry) and create Choropleth maps (polygon geometry) for CA counties’ polarity label counts [choropleth_pham.py]. I downloaded a US county map from census website, then created a GeoPanda DataFrame from it, called us_county. My next task is to populate this map with colors to present the tweets numbers. In order to accomplish that, I do the following: 
-	Join the TextBlob GeoPanda DataFrame to us_county
-	Group the new GeoPanda DataFrame by “GEOID” and polarity category columns 
-	Group into positive, negative, neutral labels (got three new dataframes)
-	Merge three new DataFrames back to us_county 
-	Create a new column named ‘total’ to sum the total of tweets for each county
-	Use the final us_county to create Choropleth maps
