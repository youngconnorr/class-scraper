from bs4 import BeautifulSoup
import requests
import csv

valid_classes = [
    'AANB',
    'AGEC',
    'ANSC',
    'APBI',
    'AQUA',
    'FNH',
    'FOOD',
    'FRE',
    'GRS',
    'HUNU',
    'LFS',
    'LFS Student Services',
    'LWS',
    'PLNT',
    'SOIL'
    ]

'''

Get majors 
get classes in majors and put in list

iterate through all class list and check if in major_classes:
    if in then yes else no
    
list of majors -> majors -> classes -> if in all_classes yes else no



'''

def check_if_code_done(cell_text: str, cur_class: str):

    spaceNum = 0
    cur_course = ""
    cur_letter = 0
    while (spaceNum < 2):
        if cell_text.index(cur_class) + cur_letter >= len(cell_text):
            return cur_course
        
        if cell_text[cell_text.index(cur_class) + cur_letter] == " ":
            spaceNum += 1
            
        if spaceNum < 2:
            cur_course += cell_text[cell_text.index(cur_class)  + cur_letter]
        else:
            break
        cur_letter += 1
        
    return cur_course
    

def parse_classes(code: BeautifulSoup, valid_classes: list):
    cell_text = code.get_text(strip=True)
    
    courseList = set()

    for c in valid_classes:
        if c in cell_text and len(cell_text) < 100:
            check_if_course_num = cell_text.index(c) + 8
            if (check_if_course_num < len(cell_text)):
                
                if cell_text[check_if_course_num].isnumeric():
                    
                    course = check_if_code_done(cell_text, c)
                    
                    courseList.add(course)
    
    return courseList
    

def get_all_classes(valid_classes: list, soup: BeautifulSoup) -> list:
    
    courseSet = set()
    
    for code in soup.find_all("td"):
        courseSet.update(parse_classes(code, valid_classes))

    for code in soup.find_all("li"):
        courseSet.update(parse_classes(code, valid_classes))
            
    return list(courseSet)

def parse_majors(cell: BeautifulSoup):
    cell_text = cell.get_text(strip=True)
    major_set = set()
    
    if "Major" in cell_text:
        # print(cell_text)
        major_set.add(cell_text)
    
    return major_set
        

def get_specialization_names(soup: BeautifulSoup) -> list:
    
    specialtySet = set()
    
    
    for cell in soup.select('ol.list-buttons > li > a'):
        specialtySet.update(parse_majors(cell))
        
    if specialtySet:
        return list(specialtySet)
    else:
        return -1

def get_specialization_classes(soup: BeautifulSoup) -> list:

    classList = []

    for cell in soup.select('ol.list-buttons > li > a'):
        specialization_content = cell.get('href')
        classSoup = get_soup(specialization_content)

        classList.append(get_all_classes(valid_classes, classSoup))

    return classList # returns each majors classlist




def find_major_courses(lfs_soup: BeautifulSoup):
    major_links = lfs_soup.select('ol.list-buttons > li > a')

    major_content = {}

    '''
    format:

    major_content = {
        "Applied Biology": {
            "Applied Animal Biology": ["Course 1", "Course 2"],
            "Sustainable Agriculture and Environment": ["Course 1", "Course 2"]
        },
        "Food, Nutrition and Health": {
            "Dietetics": ["Course 1", "Course 2"],
            "Food Market Analysis": ["Course 1", "Course 2"],
            "Food Science": ["Course 1", "Course 2"],
            "Nutritional Sciences": ["Course 1", "Course 2"],
            "Food and Nutritional Sciences": ["Course 1", "Course 2"],
            "Food, Nutrition and Health": ["Course 1", "Course 2"]
        }
    }

    
    '''

    major_names = []

    for link in major_links:
        if "B.Sc" not in link.get_text():
            continue
            
        major_name = link.get_text().strip()

        major_content[major_name] = {}


        if link.get('href'):
            link_content = get_soup(f"https://vancouver.calendar.ubc.ca{link.get('href')}")
            # get major and href and then soup, and then get all courses
            # save major names as well into array as first item so it can be called with courses[0]
            specialization_names = get_specialization_names(link_content) # have the individual majors now

            # now all you're missing is classes
            for specialty in specialization_names:
                major_content[major_name][specialty] = []

            # get classes (right now it gets the classes for EVERY MAJOR and puts it into one list)
            # figure out how to get it so it gets each major individually so you can easily store it into a list
            classes = get_specialization_classes(link_content)
                
for cell in soup.select('ol.list-buttons > li > a'):
        specialtySet.update(parse_majors(cell))





def get_soup(link: str):
    html_content = requests.get(link).text
    soup = BeautifulSoup(html_content, "html.parser")

    return soup


def export_to_csv(courses: list, filename: str):
    """
    Export courses to a CSV file
    
    Args:
        courses (list): List of course codes
        filename (str): Name of the CSV file to create
    """
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            # Write header
            csv_writer.writerow(['Course Code'])
            
            # Write each course as a row
            for course in courses:
                csv_writer.writerow([course])
        
        print(f"Courses exported to {filename} successfully!")
    except IOError as e:
        print(f"Error exporting to CSV: {e}")    


def main():
    
    valid_classes = [
    'AANB',
    'AGEC',
    'ANSC',
    'APBI',
    'AQUA',
    'FNH',
    'FOOD',
    'FRE',
    'GRS',
    'HUNU',
    'LFS',
    'LFS Student Services',
    'LWS',
    'PLNT',
    'SOIL'
    ]

    
    lfs_soup_term_1= get_soup("https://courses.landfood.ubc.ca/?term=2024-25-winter-term-1-ubc-v&subject=All")
    lfs_soup_term_2= get_soup("https://courses.landfood.ubc.ca/?term=2024-25-winter-term-2-ubc-v&subject=All")

    # get class list
    found_classes_1 = get_all_classes(valid_classes, lfs_soup_term_1)
    found_classes_2 = get_all_classes(valid_classes, lfs_soup_term_2)

    found_classes_1.extend(found_classes_2)

    total_class = set()
    total_class.add(tuple(found_classes_1))

    print(total_class)
    '''
    Applied Biology (formerly Agroecology)
        Applied Animal Biology
        Sustainable Agriculture and Environment
    Food, Nutrition and Health
        Dietetics
        Food Market Analysis
        Food Science
        Nutritional Sciences
        Food and Nutritional Sciences
        Food, Nutrition and Health
    Global Resource Systems
    
    scrape every major each of their courses and then compare
    inefficient but also more efficient than copy and paste
    '''


    url2 = "https://vancouver.calendar.ubc.ca/faculties-colleges-and-schools/faculty-land-and-food-systems/bsc-applied-biology-apbi"
    html_content = requests.get(url2).text
    soup = BeautifulSoup(html_content, "lxml")
    print(get_majors(soup))
    for i in get_majors(soup):
        print(i.get('href'))
    
    # majors = [a.text.strip() for a in soup.select('ol.list-buttons > li > a')[4:]]
    # print(majors)
    
    
    
    # export_to_csv(found_classes, 'extracted_courses.csv')

                            
if __name__ == "__main__":
    main()