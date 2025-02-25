# Robots Analysis for the Daily Pennsylvanian

The Daily Pennsylvanian's `robots.txt` file is available at
[https://www.thedp.com/robots.txt](https://www.thedp.com/robots.txt).

## Contents of the `robots.txt` file on 2/24/25

```
User-agent: *
Crawl-delay: 10
Allow: /

User-agent: SemrushBot
Disallow: /
```

## Explanation

The robots.txt file allows all users except the SemrushBot to scrape all parts of the website. The file specifically disallows the SemrushBot from accessing any of the Daily Pennsylvanian. It also specifies that all crawlers have to wait 10s between requests to the server so that it doesn't get overloaded.