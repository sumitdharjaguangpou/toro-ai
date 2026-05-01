# news.py - Enhanced with Sentiment Analysis
import feedparser
from urllib.parse import quote_plus

def get_stock_news(stock_name):
    """Fetch stock news with sentiment analysis"""
    try:
        query = quote_plus(stock_name)
        url = f"https://news.google.com/rss/search?q={query}%20stock&hl=en-IN&gl=IN&ceid=IN:en"
        feed = feedparser.parse(url)
        
        # Sentiment keywords
        sentiment_words = {
            'positive': ['surge', 'gain', 'upgrade', 'bullish', 'positive', 'growth', 'record', 'high', 
                        'profit', 'rise', 'up', 'beat', 'outperform', 'buyback', 'dividend', 'approval'],
            'negative': ['drop', 'fall', 'downgrade', 'bearish', 'negative', 'crash', 'low', 'warning',
                        'loss', 'decline', 'down', 'miss', 'underperform', 'investigation', 'fine', 'lawsuit']
        }
        
        news_list = []
        
        if not feed.entries:
            return [{
                "title": "No recent news found",
                "link": "#",
                "source": "",
                "time": "",
                "sentiment": "neutral"
            }]
        
        for entry in feed.entries[:5]:
            title = entry.get("title", "")
            sentiment = "neutral"
            
            # Sentiment detection
            title_lower = title.lower()
            for word in sentiment_words['positive']:
                if word in title_lower:
                    sentiment = "positive"
                    break
            if sentiment != "positive":  # Only check negative if not already positive
                for word in sentiment_words['negative']:
                    if word in title_lower:
                        sentiment = "negative"
                        break
            
            news_list.append({
                "title": title,
                "link": entry.get("link", "#"),
                "source": entry.get("source", {}).get("title", "Unknown"),
                "time": entry.get("published", "No time"),
                "sentiment": sentiment
            })
        
        return news_list

    except Exception as e:
        return [{
            "title": f"Error fetching news: {str(e)}",
            "link": "#",
            "source": "",
            "time": "",
            "sentiment": "neutral"
        }]