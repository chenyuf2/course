import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

filename = "UIUC Courses.csv"
f = open(filename, "w")
headers = "Course Title, Full Title, Prerequisite\n"
f.write(headers)

html = uReq('https://courses.illinois.edu/schedule/2019/spring')
page_soup = soup(html, "html.parser")
main_container = page_soup.find("div", {"class": "table-responsive"})
all_links = []
for link in main_container.findAll("a"):
    if 'href' in link.attrs:
        all_links.append(link.attrs['href'])


for link in all_links:
    html = uReq('https://courses.illinois.edu' + link)
    page_soup = soup(html, "html.parser")
    main_container = page_soup.find(
        "table", {"class": "table table-striped table-bordered table-condensed"})
    links = []
    for link in main_container.findAll("a"):
        if "href" in link.attrs:
            links.append(link.attrs["href"])
    for item in links:
        print(item)
        html = uReq('https://courses.illinois.edu'+item)
        page_soup = soup(html, "html.parser")
        main_container = page_soup.find("div", {"class": "lead app-table-lead"})
        container = page_soup.find("div", {"id": "app-course-info"})
        course_title = main_container.h1.text
        
        Full_title = container.span.text
        
        key_word = "Prerequisite"
        content = page_soup.find(text=lambda text: text and key_word in text)
        if content == None:
            Prerequisite = 'NULL'
        elif len(content.findNextSiblings("a")) == 0:
            Prerequisite = 'NULL'
        else:
            grab_all = content.findNextSiblings("a")
            Prerequisite = ""
            for item in grab_all:
                Prerequisite += item.text + " "

        f.write(course_title + "," + Full_title.replace(","," ") +
                "," + Prerequisite.replace(","," ") + "\n")
f.close()
