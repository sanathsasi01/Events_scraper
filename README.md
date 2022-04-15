# Events_scraper
A web scraper done with Scrapy python framework.


The tech stack used is Python Scrapy with PostgrSQL.

------ My solution --------

Scrapped the whole events page including date, time, artists, location, title, sub titles, sponsor.

Plots a bar graph at the end of the scripts with the dates of events and the count of events on each of these dates.


------------------------------------------

Virtual environment

    python3 -m venv env

To activate the virtual environment

    env\Scripts\activate.bat

Database name : Events

cd to the project
    
    cd lucernefestival

run the scrapper

    scrapy crawl lucernefestival
  

