import tkinter as tk
import requests
from itertools import cycle

class NewsTicker(tk.Tk):
    def __init__(self, api_key):
        super().__init__()

        # Set up the window
        self.title("News Ticker")
        self.geometry("800x70")
        self.configure(bg="white")

        # Make the window always on top
        self.attributes("-topmost", True)

        # Create a label for the ticker text
        self.ticker_label = tk.Label(self, text="", font=("Helvetica", 18), fg="black", bg="white")
        self.ticker_label.pack(fill=tk.X)

        # Store the headlines and start scrolling
        self.headlines = []
        self.api_key = api_key
        self.fetch_headlines()
        self.scroll_text()

    def fetch_headlines(self):
        """Fetch headlines from NewsAPI."""
        url = "https://newsapi.org/v2/top-headlines"
        params = {
            'apiKey': self.api_key,
            'country': 'us',  # Change to desired country code
            'pageSize': 20    # Number of headlines to fetch
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            articles = data.get('articles', [])
            self.headlines = [article['title'] for article in articles if article.get('title')]
            self.headlines = cycle(self.headlines)  # Cycle through headlines
            self.update_ticker_text()
        except requests.RequestException as e:
            print(f"Error fetching news: {e}")

    def update_ticker_text(self):
        """Update the label with fetched headlines."""
        self.ticker_label.config(text=" - ".join(next(self.headlines) for _ in range(10)))
    
    def scroll_text(self):
        """Scroll the ticker text."""
        # Move text to the left by 2 pixels
        self.ticker_label.place(x=self.ticker_label.winfo_x()-2, y=0)
        
        # If the text has scrolled out of view, reset its position
        if self.ticker_label.winfo_x() < -self.ticker_label.winfo_width():
            self.ticker_label.place(x=self.winfo_width(), y=0)
        
        # Repeat the scroll_text function after 30 milliseconds
        self.after(30, self.scroll_text)

if __name__ == "__main__":
    API_KEY = ''  # Replace with your NewsAPI key
    app = NewsTicker(api_key=API_KEY)
    app.mainloop()
