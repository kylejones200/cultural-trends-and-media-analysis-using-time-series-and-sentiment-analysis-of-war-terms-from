"""Generated from Jupyter notebook: Sentiment Analysis using VADER

Magics and shell lines are commented out. Run with a normal Python interpreter."""
import nltk

def main():
    nltk.download('vader_lexicon')
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    sid = SentimentIntensityAnalyzer()
    text = 'This was a good movie.'
    vader_scores = sid.polarity_scores(text)
    print(vader_scores)
    import pandas as pd
    df = pd.read_csv('data/review_data.csv')
    df.head()
    df['scores_apply'] = df['reviews.text'].apply(lambda text: sid.polarity_scores(str(text)))
    df['scores_list_comprehension'] = [sid.polarity_scores(str(i)) for i in df['reviews.text']]


def main() -> None:
    # --- notebook cell (unparsed) ---
    # # --- code cell ---

    #     df = pd.concat([df, df["scores_list_comprehension"].apply(pd.Series)], axis=1)
    #     df["Category"] = df["reviews.rating"].astype("category")
    #     df.head()


    # if __name__ == "__main__":
    #     main()

if __name__ == "__main__":
    main()
