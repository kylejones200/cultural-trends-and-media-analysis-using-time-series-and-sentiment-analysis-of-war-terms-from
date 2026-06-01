# Cultural Trends and Media Analysis Using Time Series and Sentiment Analysis of War Terms from... Newspapers reflect how a country feels. They capture panic and
patriotism, dread and hope. When wars begin or end, the front page often...

### Cultural Trends and Media Analysis Using Time Series and Sentiment Analysis of War Terms from 1930--1950 in the US with Python
Newspapers reflect how a country feels. They capture panic and patriotism, dread and hope. When wars begin or end, the front page often says more about the mood of the people than the official record ever could.

This post uses historical newspaper archives to track sentiment shifts across four key terms --- war, army, battle, and peace --- from 1930 to
1950. We can examine how American public sentiment moved through World
War II and the surrounding decades by combining sentiment analysis with time series.

### Extracting Newspaper Data from Chronicling America
I used [Chronicling America](https://chroniclingamerica.loc.gov/), a Library of Congress project offering digitized U.S. newspapers from 1789 to 1963. I queried articles that mention war, army, battle, and peace. Then I extracted their publication dates and full text.

The Chronicling America API is very fragile so I ended up running one search term at a time and stored each set of results in separate CSVs (e.g., `war.csv`, `peace.csv`). Then I combined them into a single dataset with a `term` column to distinguish them.


I let [VADER (Valence Aware Dictionary and sEntiment Reasoner)](https://github.com/cjhutto/vaderSentiment) handle the raw newspaper text. This tool returns a compound sentiment score from -1 (very negative) to 1 (very positive).


### Aggregating Sentiment Over Time
I grouped sentiment scores by term and year-end date, then calculated the average sentiment per group. This allowed us to observe how each concept's emotional tone evolved through World War II and beyond.


I focused on the period from 1930 to 1950, a 20-year window bracketing the war, to identify changes in tone across multiple themes.

### Visualizing Sentiment Shifts (1930--1950)
The plot shows the average yearly sentiment for each term.


"peace" remained the most positive term throughout, spiking during wartime victories and at the war's end.

"war" and "battle" showed deeply negative sentiment during active conflict years.

"army" sentiment was more stable, slightly rising toward the war's end as national morale improved.

The vertical lines mark Pearl Harbor attack (Dec 1941) and the end of World War II (Sept 1945).

This view shows how newspapers conveyed emotional tones not just about war, but about broader concepts of violence and resolution.

Looking across these terms reveals several patterns. "battle" and "war" were trending down in early 1930s, likely shaped by memories of WWI and economic instability.

There is a huge positive spike for "war" in 1938 when conflict began in Europe but the US was not actively engaged.

In the late 1940s, "army" and "peace" were associated with more optimistic sentiment, hinting at a cultural return to normalcy.

### Decomposing the Sentiment of "War"
To isolate the emotional pulse surrounding war, I narrowed my focus to just the keyword "war". This lets us examine how the public mood --- as reflected in newspapers --- rose and fell with global events between 1930 and 1950.

I applied seasonal decomposition to this sentiment time series, which separates it into:

- Trend: The long-term rise or fall in sentiment around war
- Seasonal: Recurring annual or cyclical shifts
- Residual: Unpredictable surges, likely from news shocks or geopolitical pivots


The plot shows the results:

- Trend: Sentiment toward war dropped sharply in the early 1940s, reflecting public anxiety during global escalation and U.S. mobilization. It rebounded modestly after 1945, showing relief and resolution.
- Seasonality: There is a clear seasonal pattern recurring every 7 years.
- Residual: Volatility spiked during major wartime events, capturing the emotional shocks of battles, declarations, and turning points.

This decomposition helps distinguish between long-term cultural attitudes about war and short-term reactions to headlines.


### Why It Matters
Sentiment analysis of historical news lets us read between the lines. It helps quantify public mood around military efforts, patriotic language, and national anxiety. This method can extend to economic events, civil rights protests, or election cycles --- any time collective emotion moves.
