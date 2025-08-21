# GoShare-Beggar

This is a simple Python script that scrapes posts from the PTT Lifeismoney board related to "goshare" using BeautifulSoup and requests. It collects article titles and links, and can also fetch the content of individual articles.

If we found some new articles pops up, we will send a notification to the user via Email.
The notification itself includes artitcle's title, content and a deep link to direct your phone to GoShare app.

We expect to extend this script to include more features such as:
- Sending notifications via other channels (e.g., Telegram, Slack)
- Port this script to a docker image for easier deployment.

# Requirements
- Python 3.x
- `requests` library
- `beautifulsoup4` library