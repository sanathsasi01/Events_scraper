# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
import psycopg2


class LucernefestivalPipeline:

    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = psycopg2.connect(
            host="localhost",
            database="futureDemand",
            user="postgres",
            password="0480"
        )
        self.cur = self.conn.cursor()

    def create_table(self):
        create_table_query = "CREATE TABLE IF NOT EXISTS Events ( id SERIAL PRIMARY KEY, title VARCHAR(200),time VARCHAR(200), event_date date, surtitle VARCHAR(200), subtitle VARCHAR(200), sponsor VARCHAR(200), detail VARCHAR(200), location VARCHAR(200));"
        self.cur.execute(create_table_query)
        self.conn.commit()

    def get_plot_data(self):
        get_event_query = "SELECT event_date,COUNT(event_date) as count FROM Events GROUP BY event_date"
        # get_event_query = "SELECT DISTINCT event_date FROM Events"
        self.cur.execute(get_event_query)
        rows = self.cur.fetchall()
        return rows

    def close_connection(self):
        self.conn.close()


    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, item):
        self.cur.execute("""
                INSERT INTO Events (time, event_date, title, surtitle, subtitle, sponsor, detail, location) VALUES( %s, %s, %s, %s, %s, %s, %s, %s);
                """,
                (item['time'], item['event_date'], item['title'], item['surtitle'], item['subtitle'], item['sponsor'], item['detail'], item['location']))
        self.conn.commit()
