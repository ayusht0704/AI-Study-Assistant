import streamlit as st
import feedparser
import yfinance as yf
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import plotly.graph_objects as go

st.set_page_config(page_title="Stock Sentiment Engine", layout="wide")

analyzer = SentimentIntensityAnalyzer()

# -----------------------------
# Stock Options
# -----------------------------
stock_options = {
    "Reliance": "RELIANCE.NS",
    "TCS": "TCS.NS",
    "Infosys": "INFY.NS",
    "HDFC Bank": "HDFCBANK.NS",
    "ICICI Bank": "ICICIBANK.NS",
    "Wipro": "WIPRO.NS"
}

# -----------------------------
# Fetch News
# -----------------------------
def fetch_news():
    url = "https://news.google.com/rss/search?q=stock+market+india"
    feed = feedparser.parse(url)
    return [entry.title for entry in feed.entries[:20]]

# -----------------------------
# Sentiment Analysis
# -----------------------------
def analyze(headlines):
    pos = neg = neu = 0
    results = []

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

        results.append((h, sentiment))

    return results, pos, neg, neu

# -----------------------------
# Stock Data
# -----------------------------
def get_stocks(selected_list):
    data_list = []

    for name in selected_list:
        symbol = stock_options[name]
        data = yf.Ticker(symbol)
        hist = data.history(period="1d")

        if not hist.empty:
            change = hist["Close"].iloc[-1] - hist["Open"].iloc[-1]
            data_list.append((name, round(change, 2)))

    return data_list

# -----------------------------
# Candlestick Chart
# -----------------------------
def plot_candles(symbol, name):
    data = yf.Ticker(symbol)
    hist = data.history(period="5d")

    if hist.empty:
        st.warning(f"No data for {name}")
        return

    fig = go.Figure(data=[go.Candlestick(
        x=hist.index,
        open=hist['Open'],
        high=hist['High'],
        low=hist['Low'],
        close=hist['Close']
    )])

    fig.update_layout(
        title=f"{name} Candlestick Chart (Last 5 Days)",
        xaxis_title="Date",
        yaxis_title="Price"
    )

    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# UI
# -----------------------------
st.title("📊 Stock Sentiment Engine")

selected = st.multiselect(
    "📌 Select Stocks",
    options=list(stock_options.keys()),
    default=["Reliance", "TCS"]
)

if st.button("🔄 Refresh Data"):
    headlines = fetch_news()
    results, pos, neg, neu = analyze(headlines)
    stocks = get_stocks(selected)

    # Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Positive", pos)
    col2.metric("Negative", neg)
    col3.metric("Neutral", neu)

    # Market Mood
    if pos > neg:
        mood = "BULLISH 📈"
    elif neg > pos:
        mood = "BEARISH 📉"
    else:
        mood = "NEUTRAL ⚖️"

    st.subheader(f"Market Sentiment: {mood}")

    # Stock Table
    st.subheader("💹 Selected Stocks")
    st.table(stocks)

    # Candlestick Charts
    st.subheader("🕯️ Candlestick Charts")
    for name in selected:
        symbol = stock_options[name]
        plot_candles(symbol, name)

    # Headlines
    st.subheader("📰 Headlines")
    for h, s in results:
        st.write(f"**{s}** — {h}")

    # Summary
    st.subheader("🧠 Summary")
    st.write(f"Market shows {pos} positive, {neg} negative headlines → {mood}")