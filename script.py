"""
Scrapes a headline from The Daily Pennsylvanian website and saves it to a 
JSON file that tracks headlines over time.
"""

import os
import sys

import daily_event_monitor

import bs4
import requests
import loguru


def scrape_data():
    """
    Scrapes the main headline from The Daily Pennsylvanian home page.

    Returns:
        str: The headline text if found, otherwise an empty string.
    """
    headers = {
        "User-Agent": "cis3500-scraper"
    }
    req = requests.get("https://www.thedp.com", headers=headers)
    loguru.logger.info(f"Request URL: {req.url}")
    loguru.logger.info(f"Request status code: {req.status_code}")

    data = {}
    return_data = false

    if req.ok:
        soup = bs4.BeautifulSoup(req.text, "html.parser")

        # main headline
        main_headline_element = soup.find("a", class_="frontpage-link")
        data["main_headline"] = "" if main_headline_element is None else main_headline_element.text

        # top featured headline
        featured_header = soup.find("h3", class_="frontpage-section", string="Featured")
        if featured_header:
            top_featured_headline = featured_header.find_next("a", class_="frontpage-link standard-link")
            data["top_featured_headline"] = "" if top_featured_headline is None else top_featured_headline.text

       

        # top news headline
        news_section = soup.find("div", class_="col-sm-6 section-news")
        if news_section:
            top_news_headline = news_section.find("a", class_="frontpage-link medium-link newstop")
            data["top_news_headline"] = "" if top_news_headline is None else top_news_headline.text

        # top opinion headline
        # opinion_header = soup.find("h3", class_="frontpage-section", string="Opinion")
        # if opinion_header:
        #     top_opinion_article = opinion_header.find_next("div", class_="article-summary")
        #     if top_opinion_article:
        #         top_opinion_headline = top_opinion_article.find("a", class_="frontpage-link medium-link font-regular")
        #         data["top_opinion_headline"] = "" if top_opinion_headline is None else top_opinion_headline.text
        
        # top sports headline
        # sports section header
        # sports_header = soup.find("h3", class_="frontpage-section")
    
        # if sports_header and "Sports" in sports_header.text:
        #     # Find the first article summary after the sports header
        #     article_summary = sports_header.find_next("div", class_="article-summary")
            
        #     if article_summary:
        #         # Get the first link in the article summary which should be the headline
        #         top_sports_headline = article_summary.find("a", class_="frontpage-link medium-link font-regular")
        #         data["top_sports_headline"] = "" if top_sports_headline is None else top_sports_headline.text

                
                    
        # # top opinion headline
        # top_opinion_headline = soup.find("a", class_="frontpage-link medium-link font-regular")
        # data["top_opinion_headline"] = "" if top_opinion_headline is None else top_opinion_headline.text

        loguru.logger.info(f"Data: {data}")
        return data


if __name__ == "__main__":

    # Setup logger to track runtime
    loguru.logger.add("scrape.log", rotation="1 day")

    # Create data dir if needed
    loguru.logger.info("Creating data directory if it does not exist")
    try:
        os.makedirs("data", exist_ok=True)
    except Exception as e:
        loguru.logger.error(f"Failed to create data directory: {e}")
        sys.exit(1)

    # Load daily event monitor
    loguru.logger.info("Loading daily event monitor")
    dem = daily_event_monitor.DailyEventMonitor(
        "data/daily_pennsylvanian_headlines.json"
    )

    # Run scrape
    loguru.logger.info("Starting scrape")
    try:
        data = scrape_data()
    except Exception as e:
        loguru.logger.error(f"Failed to scrape data point: {e}")
        data = None

    # Save data
    if data is not None:
        dem.add_today(data)
        dem.save()
        loguru.logger.info("Saved daily event monitor")

    def print_tree(directory, ignore_dirs=[".git", "__pycache__"]):
        loguru.logger.info(f"Printing tree of files/dirs at {directory}")
        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            level = root.replace(directory, "").count(os.sep)
            indent = " " * 4 * (level)
            loguru.logger.info(f"{indent}+--{os.path.basename(root)}/")
            sub_indent = " " * 4 * (level + 1)
            for file in files:
                loguru.logger.info(f"{sub_indent}+--{file}")

    print_tree(os.getcwd())

    loguru.logger.info("Printing contents of data file {}".format(dem.file_path))
    with open(dem.file_path, "r") as f:
        loguru.logger.info(f.read())

    # Finish
    loguru.logger.info("Scrape complete")
    loguru.logger.info("Exiting")
