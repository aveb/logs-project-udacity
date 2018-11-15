# Reporter

A tool that anaylzes the ```newsdata.sql``` database and returns:

- Top three articles of all time by page views
- List of Authors ranked by page views
- Dates when more than 1% of HTTP requests returned errors

## Prerequisites

You will need have the following installed on your machine before running ```reporter.py```: 

- You must have Python 2 installed.  You can find detailed instalation instructions and a link to the download [HERE](https://www.python.org/downloads/)
- ```reporter.py``` runs on a linux-based virtual machine called ```VirtualBox```.  You can download it for free [HERE](https://www.virtualbox.org/wiki/Download_Old_Builds_5_1)
- After installing ```VirtualBox```, you will need to download an additional tool: ```Vagrant```.  This software allows you to share files between your host and virtual machine.  You can read more and download ```Vagrant``` [HERE](https://www.vagrantup.com/downloads.html)

## Configuring the Database

The ```Reporter``` tool requires you to first download the ```news``` database and load it into your ```VirtualBox``` VM.  Download the data [HERE](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip).  Unzip the file, then move the file ```newsdata.sql``` into the ```vagrant``` directory located inside your virtual machine.

Two ```views``` must be created first before you can run ```reporter.py```.  Make sure you first connect with the ```news``` database in your terminal.

- First ```view```.  This creates ```articles_authors```, a table that matches all of the authors with the slug of their articles by **joining** the ```authors``` and ```articles``` tables.  This will be used by ```reporter.py``` to report the most popular authors by views.

        news=> create view articles_authors as
            select authors.name, articles.slug
            from authors, articles
            where authors.id = articles.author;

- Second ```View```.  This creates ```percentages```, which calculates the percent of **404 errors** returned each day.  The date is also truncated; making it easier to unpack with python.
    
        news=> create view percentages as 
            select date_trunc('day',time) as d,
            (count(id) filter (where status like '%404%')*100*1.0 / count(id)) 
            as percentage from log group by d;

## Running ```reporter.py```

```reporter.py``` can be run from your terminal using the following command:

        $ python reporter.py
