from bs4 import BeautifulSoup
from urllib.request import urlopen
import mysql.connector

def sql_connect(entries):
    db_name = "job_db"
    job_db = mysql.connector.connect(host = "localhost", username = "root", password="Password")
    job_cursor = job_db.cursor(buffered=True)
    job_cursor.execute("SHOW DATABASES")
    for db in job_cursor:
        if db_name == db[0]:
            job_cursor.execute("DROP DATABASE job_db")
            break;
    job_cursor.execute("CREATE DATABASE job_db")
    job_cursor.execute("CREATE table job_db.job_details (id INT AUTO_INCREMENT, Job_Title text, Job_Company text, Job_Location text, Job_Salary text, Company_Rating text, Job_Url text, primary key (id))")
    query = "INSERT INTO job_details (Job_Title, Job_Company, Job_Location, Job_Salary, Company_Rating, Job_Url) VALUES(%s, %s, %s, %s, %s, %s)"
    job_cursor.execute("USE job_db")
    job_cursor.executemany(query, entries)
    job_db.commit()
    print("Committed")

def crawl():
    base_url = "https://ca.indeed.com/jobs?q=software+intern&l=Canada"
    entries = []
    for i in range(20):
        if i == 0:
            html = urlopen(base_url)
        else:
            url = base_url + "&start" + str(i) + "0"
            html = urlopen(url)
        htmlBS = BeautifulSoup(html, 'html.parser')
        divs = htmlBS.find_all('div', attrs = {'class': 'jobsearch-SerpJobCard'})
        for div in divs:
            entry = []
            job_url = "https://ca.indeed.com" + div.find('a', attrs={'class':'turnstileLink'}).attrs['href']
            job_title = div.find('a', attrs = {'class': 'jobtitle'})
            job_company = div.find('span', attrs = {'class': 'company'})
            rating = div.find('a', attrs = {'class': 'ratingNumber'})
            job_location = div.find(attrs= {'class':'location'})
            job_salary = div.find('span', attrs = {'class': 'salaryText'})
            entry.append(job_title.text.replace('\n', ''))
            entry.append(job_company.text.replace('\n', ''))
            if job_location:
                entry.append(job_location.text.replace('\n', ''))
            else:
                entry.append(None)
            if job_salary:
                entry.append(job_salary.text.replace('\n', ''))
            else:
                entry.append(None)
            if rating:
                entry.append(rating.text.replace('\n', ''))
            else:
                entry.append(None)
            entry.append(job_url)
            entries.append(entry)
    for i in range(len(entries)):
        entries[i] = tuple(entries[i])
    sql_connect(entries)

if __name__ == "__main__":
    crawl()