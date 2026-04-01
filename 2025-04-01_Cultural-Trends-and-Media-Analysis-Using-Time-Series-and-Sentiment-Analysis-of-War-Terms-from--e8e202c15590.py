# Description: Short example for Cultural Trends and Media Analysis Using Time Series and Sentiment Analysis of War Terms from.



# Define the API endpoint

from nltk.sentiment import SentimentIntensityAnalyzer
from statsmodels.tsa.seasonal import seasonal_decompose
import matplotlib.pyplot as plt
import pandas as pd
import requests

base_url = "https://chroniclingamerica.loc.gov/search/pages/results/"

# Example query parameters
params = {
    'format': 'json',
    'proxtext': 'war',
    'date1': '1910',
    'date2': '1950',
    'rows': 100
}

# Fetch data
response = requests.get(base_url, params=params)
data = response.json()

# Extract relevant fields
articles = []
for item in data['items']:
    articles.append({
        'date': item['date'],
        'title': item['title'],
        'text': item['ocr_eng']  # Extract OCR-processed text
    })

# Convert to DataFrame
df = pd.DataFrame(articles)
df['date'] = pd.to_datetime(df['date'])
df.head()
# Extract relevant fields
articles = []
for item in data['items']:
    articles.append({
        'date': item['date'],
        'title': item['title'],
        'text': item['ocr_eng']  # Extract OCR-processed text
    })
# Convert to DataFrame
df = pd.DataFrame(articles)
df['date'] = pd.to_datetime(df['date'])
df.head()

sia = SentimentIntensityAnalyzer()

combined_df['sentiment'] = combined_df['clean_text'].apply(
    lambda x: sia.polarity_scores(str(x))['compound']
)

aggregated = (combined_df
              .groupby([pd.Grouper(key='date', freq='YE'), 'term'])
              .agg({'sentiment': 'mean'})
              .reset_index())


# Filter for 'war' term only
war_df = aggregated[aggregated['term'] == 'war'].copy()


war_df['year'] = war_df['date'].dt.year


war_sentiment = war_df.groupby('year')['sentiment'].mean().reset_index()


war_sentiment.set_index('year', inplace=True)

# Decompose the sentiment time series for 'war'
decomposition = seasonal_decompose(war_sentiment['sentiment'], model='additive', period=5)

# Plot the decomposition
decomposition.plot()
plt.suptitle("Time Series Decomposition of 'War' Sentiment (1930–1950)", fontsize=14)
plt.savefig("war_sentiment_decomposition.png")
plt.show()
