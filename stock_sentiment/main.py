import feedparser
import yfinance as yf
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from rich.console import Console
from rich.table import Table

# Initialize
console = Console()
analyzer = SentimentIntensityAnalyzer()

# -----------------------------
# 1. Fetch News (Google RSS)
# -----------------------------
def fetch_news():
    url = "https://news.google.com/rss/search?q=stock+market+india"
    feed = feedparser.parse(url)
    headlines = [entry.title for entry in feed.entries[:20]]
    return headlines

# -----------------------------
# 2. Sentiment Analysis
# -----------------------------
def analyze_sentiment(headlines):
    results = []

    pos, neg, neu = 0, 0, 0

    for h in headlines:
        score = analyzer.polarity_scores(h)['compound']

        if score > 0.05:
            sentiment = "Positive"
            pos += 1
        elif score < -0.05:
            sentiment = "Negative"
            neg += 1
        else:
            sentiment = "Neutral"
            neu += 1

        results.append((h, sentiment, score))

    return results, pos, neg, neu

# -----------------------------
# 3. Fetch Stock Data
# -----------------------------
def get_stock_data():
    stocks = ["RELIANCE.NS", "TCS.NS", "INFY.NS"]

    stock_info = []

    for s in stocks:
        data = yf.Ticker(s)
        hist = data.history(period="1d")

        if not hist.empty:
            change = hist["Close"].iloc[-1] - hist["Open"].iloc[-1]
            stock_info.append((s, round(change, 2)))

    return stock_info

# -----------------------------
# 4. Generate Summary (No LLM)
# -----------------------------
def generate_summary(pos, neg, neu):
    total = pos + neg + neu

    if pos > neg:
        mood = "BULLISH"
    elif neg > pos:
        mood = "BEARISH"
    else:
        mood = "NEUTRAL"

    summary = f"Market sentiment appears {mood} with {pos} positive, {neg} negative headlines."
    return mood, summary

# -----------------------------
# 5. Display Output
# -----------------------------
def display(headlines, results, pos, neg, neu, stocks, mood, summary):
    console.print("\n📊 [bold cyan]STOCK SENTIMENT ENGINE — DAILY BRIEFING[/bold cyan]\n")

    console.print(f"📰 Headlines Analyzed: {len(headlines)}\n")

    console.print(f"🔹 Positive: {pos}")
    console.print(f"🔹 Negative: {neg}")
    console.print(f"🔹 Neutral: {neu}\n")

    console.print(f"📈 Market Sentiment: [bold]{mood}[/bold]\n")

    # Stock Table
    table = Table(title="💹 Top Stocks")

    table.add_column("Stock")
    table.add_column("Change")

    for s, change in stocks:
        table.add_row(s, str(change))

    console.print(table)

    console.print("\n🧠 Summary:")
    console.print(summary)

# -----------------------------
# MAIN
# -----------------------------
def main():
    headlines = fetch_news()
    results, pos, neg, neu = analyze_sentiment(headlines)
    stocks = get_stock_data()
    mood, summary = generate_summary(pos, neg, neu)

    display(headlines, results, pos, neg, neu, stocks, mood, summary)


if __name__ == "__main__":
    main()