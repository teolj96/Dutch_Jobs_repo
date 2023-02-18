import csv
import os, re
from bs4 import BeautifulSoup
from bs4.element import Comment

path = r'C:\Users\tljubicic\OneDrive - A1 Group\Dokumente\html_parser'

files = [i for i in os.listdir(path)]
jobs = []
jobs_counter = 0

for file in files:
    with open(path + '\\' + file, 'r', encoding='utf-8') as f:
        doc = BeautifulSoup(f, 'html.parser')

    # JOB TITLE
    try:
        job_title = doc.find('h2', class_="t-24 t-bold jobs-unified-top-card__job-title").string.strip()
    except:
        job_title = ""

    # COMPANY NAME
    try:
        company_name = doc.find('span', class_="jobs-unified-top-card__company-name").a.string.strip()
    except:
        company_name = ""

    # LOCATION
    try:
        location = doc.find('span', class_="jobs-unified-top-card__bullet").string.strip()
    except:
        location = ""

    # HYBRID, REMOTE, ON SITE ?
    try:
        workplace_type = doc.find('span', class_="jobs-unified-top-card__workplace-type").string.strip()
    except:
        workplace_type = ""

    # PART TIME/FULL TIME TYPE
    try:
        try:
            work_type = doc.find_all('li', class_="jobs-unified-top-card__job-insight")[0].span.contents[2].split("·")[0].replace("Â", "")
        except:
            work_type = doc.find_all('li', class_="jobs-unified-top-card__job-insight")[0].span.contents[2].string
    except:
        work_type = ""

    # EXP LEVEL
    try:
        try:
            exp_level = doc.find_all('li', class_="jobs-unified-top-card__job-insight")[0].span.contents[2].split("·")[1].strip()
        except:
            exp_level = doc.find_all('li', class_="jobs-unified-top-card__job-insight")[0].span.contents[2].string
    except:
        exp_level = ""

    # COMPANY SIZE
    try:
        try:
            company_size = doc.find_all('li', class_="jobs-unified-top-card__job-insight")[1].span.contents[2].split("·")[0].replace("Â", "")
        except:
            company_size = doc.find_all('li', class_="jobs-unified-top-card__job-insight")[1].span.contents[2].string
    except:
        company_size = ""

    # COMPANY INDUSTRY
    try:
        try:
            industry = doc.find_all('li', class_="jobs-unified-top-card__job-insight")[1].span.contents[2].split("·")[1].strip()
        except:
            industry = doc.find_all('li', class_="jobs-unified-top-card__job-insight")[1].span.contents[2].string
    except:
        industry = ""

    # DESCRIPTION
    def tag_visible(element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        elif isinstance(element, Comment):
            return False
        elif re.match(r"[\s\r\n]+", str(element)):
            return False
        return True


    def text_from_html(body):
        texts = body.findAll(text=True)
        visible_texts = filter(tag_visible, texts)
       # return u' '.join(t.strip() for t in visible_texts) # NESTO NE VALJA S OVIM KODOM, NE PARSA MI DOBRO NEKI DIO HTML
        return ' '.join(t.strip() for t in visible_texts)

    try:
        description_doc = doc.find("div", class_=re.compile("jobs-description*"))
        description = '"' + text_from_html(description_doc) + '"'
    except:
        description = ""

    # LINK FOR JOB
    try:
        link = doc.find("div", class_="jobs-unified-top-card__content--two-pane").a["href"]
    except:
        link = ""

    jobs.append({'Job Title': job_title,
                 'Company Name': company_name,
                 'Location': location,
                 'Workplace Type': workplace_type,
                 'Work Type': work_type,
                 'Experience': exp_level,
                 'Company Size': company_size,
                 'Industry': industry,
                 'Job Description': description.replace('\n',''),
                 'Job Link': link
                 })

    jobs_counter = jobs_counter + 1
    print(jobs_counter)

columns = ['Job Title', 'Company Name', 'Location', 'Workplace Type', 'Work Type', 'Experience', 'Company Size',
           'Industry', 'Job Description', 'Job Link']

with open('linkedin.csv','w',encoding='utf-8',newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames = columns, delimiter = ',')
    writer.writeheader()
    writer.writerows(jobs)
