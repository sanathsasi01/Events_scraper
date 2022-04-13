from distutils.command.clean import clean
import scrapy
import re
from lucernefestival.items import LucernefestivalItem
import matplotlib.pyplot as plt
from lucernefestival.pipelines import LucernefestivalPipeline 


class Events(scrapy.Spider):

    name = 'lucernefestival'

    start_urls = [
        'https://www.lucernefestival.ch/en/program/summer-festival-22'
    ]

    def clean(self, obj):
        if obj is not None:
            extracted_list = obj.extract()
            string = ''.join(extracted_list).replace('|', ',')
            return re.sub('[^A-Za-z0-9,]+', ' ', string).encode("ascii", "ignore").decode().strip()

    def parse(self, response, **kwargs):
        item = LucernefestivalItem()
        for event in response.css('#event-list div.entry'):

            data_date =  event.xpath("@data-date").get()
            time = event.css('.day-time .time::text').get()

            subtitle = event.css('.wi div.event-info .wi p.subtitle *::text')
            subtitle = self.clean(subtitle)

            title =  event.css('.wi div.event-info .wi p.title *::text')
            title = self.clean(title)

            surtitle = event.css('.wi div.event-info .wi p.surtitle::text')
            surtitle = self.clean(surtitle)

            detail = event.css('.wi div.event-info .wi a.detail::text')
            detail = self.clean(detail)

            sponsor =  event.css('.wi div.event-info .wi p.subtitle span.sponsor::text')
            sponsor = self.clean(sponsor)

            location = event.css('.wi .date-place .location a::text')
            location = self.clean(location)

            if title != "":
                # item['day'] = week_day
                item['event_date'] = data_date
                item['subtitle'] = subtitle
                item['time'] = time
                item['title'] = title
                item['surtitle'] = surtitle
                item['sponsor'] = sponsor
                item['detail'] = detail
                item['location'] = location
                yield item
 
        db = LucernefestivalPipeline()
        rows = db.get_plot_data()

        distinct_dates = [r[0] for r in rows]
        event_count = [r[1] for r in rows]

        fig, ax = plt.subplots()
        
        # plotting a bar chart
        plt.bar(distinct_dates, event_count, tick_label = distinct_dates,
                width = 0.5, color = ['green'])

        # naming the x-axis
        plt.xlabel('Event Dates')
        # naming the y-axis
        plt.ylabel('Event Count')
        # plot title
        plt.title('LUCERNE FESTIVAL ANALYSIS')
        plt.setp( ax.xaxis.get_majorticklabels(), rotation=45, ha="right" )
        plt.gcf().subplots_adjust(bottom=0.15)
        db.close_connection()
        plt.show()