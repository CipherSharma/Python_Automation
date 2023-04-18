#upload data to sql data base 
import datetime 
from django.apps import apps
import csv
current_date = datetime.datetime.now().date()
formatted_date = current_date.strftime('%d%m%Y')



def import_csv():
    Blogs = apps.get_model('home', 'Blogs')
    with open('{}_verge.csv'.format(formatted_date), 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            title = row[1]
            author = row[2]
            date = row[3]
            url = row[4]

            # Check if the entry already exists in the database
            entry = Blogs.objects.filter(title=title, author=author, url=url, date=date).first()
            if entry is None:
                # If entry does not exist, create a new one
                entry = Blogs(title=title, author=author, url=url, date=date)
                entry.save()
            else:
                # If entry already exists, update its fields
                entry.title = title
                entry.author = author
                entry.url = url
                entry.date = date
                entry.save()
        print("Done")

import_csv()