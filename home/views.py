from .models import Blogs
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from django.http import HttpResponse
import csv
import os
import threading
import datetime 
import time
import schedule


def get_blog_data():
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--window-size=1920,1200")
    driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
    driver.implicitly_wait(1)
    
    url="https://www.theverge.com/"
    driver.get(url)
    
    Id=[]
    title=[]
    url=[]
    author=[]
    date=[]
    print("Start")
    blog_titles = driver.find_elements(By.CSS_SELECTOR,"[class*='group-hover'], [class*='md:text-lg']")

    for i in blog_titles: 
        try:
            if (i.text != "" ):
                title.append(str(i.text))
                if i.get_attribute('href') ==None:
                    text=i.get_attribute('innerHTML')
                    url_value="https://www.theverge.com"+text.split("href")[1].split(">")[0][2:-1]
                    url.append(url_value)
                else: 
                    url.append(i.get_attribute('href'))
            else:
                continue
        except:
            print(i.get_attribute('innerHTML'))
    count=0
    for i in url:
        try:
            driver.get(i)
            author_value=driver.find_elements(By.XPATH,'//*[@class="font-medium uppercase tracking-6"]/a')[0]
            date_value=driver.find_elements(By.XPATH,'//*[@datetime]')[0]
            author.append(author_value.text)
            date.append(date_value.text)
            Id.append(count+1)
            count=count+1
        except:
            del title[count]
            del url[count] 

    rows = zip(Id,title, author, date, url)
    
    current_date = datetime.datetime.now().date()
    formatted_date = current_date.strftime('%d%m%Y')
    print (formatted_date)
    with open('{}_verge.csv'.format(formatted_date), 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Id','Title', 'Author', 'Date', "Url"])
        writer.writerows(rows)
    print("end")
    driver.quit()
    
def import_csv():
    current_date = datetime.datetime.now().date()
    formatted_date = current_date.strftime('%d%m%Y')
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
    os.remove('{}_verge.csv'.format(formatted_date))

def index(request):
    
    schedule.every().day.at("11:50").do(get_blog_data)
    schedule.every().day.at("11:55").do(import_csv)
    def run_schedule():
        while True:
            schedule.run_pending()
            time.sleep(1)
    t = threading.Thread(target=run_schedule)
    t.start() 
     
    response = HttpResponse("Service Started")

    return response
