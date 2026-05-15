"""Generated from Jupyter notebook: Sentiment Analysis using VADER

Magics and shell lines are commented out. Run with a normal Python interpreter."""


# --- code cell ---

import nltk


def main():
    nltk.download("vader_lexicon")
    from nltk.sentiment.vader import SentimentIntensityAnalyzer

    sid = SentimentIntensityAnalyzer()


    # --- code cell ---

    # Example

    text = "This was a good movie."
    vader_scores = sid.polarity_scores(text)

    print(vader_scores)


    # --- code cell ---

    import pandas as pd

    df = pd.read_csv("data/review_data.csv")


    # --- code cell ---

    df.head()


    # --- code cell ---

    # %%time  # Jupyter-only

    # Option 1
    df["scores_apply"] = df["reviews.text"].apply(
        lambda text: sid.polarity_scores(str(text))
    )


    # --- code cell ---

    # %%time  # Jupyter-only

    # Option 2
    df["scores_list_comprehension"] = [
        sid.polarity_scores(str(i)) for i in df["reviews.text"]
    ]


    # --- duplicate code cell omitted (identical to earlier cell) ---


    # --- code cell ---

    df = pd.concat([df, df["scores_list_comprehension"].apply(pd.Series)], axis=1)
    df["Category"] = df["reviews.rating"].astype("category")
    df.head()


if __name__ == "__main__":
    main()
