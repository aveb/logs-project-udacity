#!/usr/bin/env python2

import psycopg2

# Fetch some student records from the database.
db = psycopg2.connect("dbname=news")
c = db.cursor()
query1 = """
          select articles.title, count(log.path) from articles, log
          where articles.slug = REPLACE(log.path, '/article/', '')
          group by articles.title order by count(log.path) desc limit 3;
        """
c.execute(query1)
rows = c.fetchall()

query2 = """
          select articles_authors.name, count(log.path)
          from articles_authors, log
          where articles_authors.slug = REPLACE(log.path, '/article/', '')
          group by articles_authors.name order by count(log.path) desc;
         """
c.execute(query2)
pop_author = c.fetchall()

query3 = "select d, percentage from percentages where percentage > 1;"
c.execute(query3)
errs = c.fetchall()

# Print top three articles sorted by views
print
print "Top 3 most popular articles by views"
for row in rows:
    print "  ", row[0], "--", row[1], " views"

# Print authors sorted by views
print
print "Author's Popularity by views"
for auth in pop_author:
    print "  ", auth[0], "--", auth[1], " total views"


# Print date where more than 1% 404

print
print "Dates where more than 1 percent of requests returned errors"
for var in range(len(errs)):
    print "  ", errs[var][0].strftime("%B %d, %Y"),\
          "--", round(errs[var][1], 2), "percent"

db.close()
