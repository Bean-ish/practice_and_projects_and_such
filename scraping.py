import requests
from bs4 import BeautifulSoup

url = 'https://lally.rpi.edu/graduate-business-programs'

# Send a GET request
response = requests.get(url)

# Check request status
if response.status_code == 200:
    # Parsecontent
    soup = BeautifulSoup(response.text, 'html.parser')
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")


##########
# # overview of the structure
# print(soup.prettify)


# academic programs
# Find the section
section = soup.find("section", class_="program-table mx-auto", id="academic-programs")


# Extract all urls from the section
if section:
    links = [a["href"] for a in section.find_all("a", href=True)]
    full_links = [link if link.startswith("http") else url.rsplit('/', 1)[0] + link for link in links]

else:
    print("Section not found.")
    full_links = []



#####
# build scraping function for all urls retrieved
def scrape_page(program_url):
    try:
        res = requests.get(program_url)
        res.raise_for_status()  # raise exception if failed
        page_soup = BeautifulSoup(res.text, "html.parser")

        # extract title
        page_title = page_soup.title.string

        # extract program outcomes
        pot_list = get_prog_otc(page_soup)

        # extract program overview & catalog link
        po_list = get_prog_ov(page_soup)

        # extract program overview & catalog link
        pg_catalog = get_prog_cata(page_soup)
        
        # return a dictionary object with information
        return {"url": program_url, "title": page_title, "program_overview": po_list, "program_outcomes": pot_list, "program_catalog": pg_catalog}
    
    except Exception as e:
        return {"url": program_url, "error": str(e)}



###
# function to extract program overview
def get_prog_ov(parsed_soup):

    h1_tag = parsed_soup.find('h1', string=lambda text: text and "Program Overview" in text.strip())

    # If the <h1> tag is found
    if h1_tag:
        
        section_content = h1_tag.find_parent('section')   # get the parent section of <h1> tag
        paragraphs = section_content.find_all('p')   # find all the <p> tags
        
        po_list = []
        for p in paragraphs:
            po_list.append(p.get_text(strip=True))

    else:
        print("Program Overview heading not found.")
        po_list = []
    
    return po_list


###
# function to find catalog link
def get_prog_cata(parsed_soup):

    a_tag = parsed_soup.find('a', string = lambda text: text and "View curriculum" in text.strip())  # find a tags

    if a_tag:

        cata = []
        link = a_tag.get('href')
        cata.append(link)

    else:
        print("No <a> tags found inside the section.")
        cata = []

    return cata


###
# function to extract program outcomes
def get_prog_otc(parsed_soup):

    h1_tag = parsed_soup.find('h1', string=lambda text: text and "Program Outcome" in text.strip())

    # If the <h1> tag is found
    if h1_tag:
        
        section_content = h1_tag.find_parent('section')   # get the parent section of <h1> tag
        ul_tags = section_content.find_all('ul')   # find all the <ul> tags

        if ul_tags:   # if able to find <ul> tags
        
            pot_list = []
            for ul in ul_tags:
                li_items = ul.find_all('li')
                for li in li_items:
                    pot_list.append(li.get_text(strip=True))
        
        else:
            print("No <ul> tags found inside the section.")

    else:
        print("Program Outcomes heading not found.")
        pot_list = []

    return pot_list



#########
# Scrape program overview, outcomes, catalog data from each link
# Scrape data from each link
scraped_data = [scrape_page(link) for link in full_links]

# print(scraped_data)



######
# output to JSON or CSV

