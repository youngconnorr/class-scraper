from bs4 import BeautifulSoup
import requests
import csv


'''
TODO: PROBLEM WITH FINDING ALL COURSES... LIKE APBI 499, IT JUST DOESN'T EXIST??

TODO:
Get majors 
get classes in majors and put in list

iterate through all class list and check if in major_classes:
    if in then yes else no
    
list of majors -> majors -> classes -> if in all_classes Y else N
list of majors -> majors -> classes -> if in restricted elective: R

'''

VALID_CLASSES = [
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


TERM1_CLASSES_LINK = "https://courses.landfood.ubc.ca/?term=2024-25-winter-term-1-ubc-v&subject=All"
TERM2_CLASSES_LINK = "https://courses.landfood.ubc.ca/?term=2024-25-winter-term-2-ubc-v&subject=All"
PARENT_FACULTY_LINK = "https://vancouver.calendar.ubc.ca/faculties-colleges-and-schools/faculty-land-and-food-systems"
RESTRICTED_COURSES_LINK = "https://www.landfood.ubc.ca/current/undergraduate/degree-planning/restricted-elective/"

major_content = {}


def main():

    faculty_term_1 = get_faculty_classes(TERM1_CLASSES_LINK)
    faculty_term_2 = get_faculty_classes(TERM2_CLASSES_LINK)
    faculty_term_1.extend(faculty_term_2)
    total_classes = set(faculty_term_1)

    restricted_courses = get_restricted_courses(VALID_CLASSES, RESTRICTED_COURSES_LINK)

    find_major_courses(PARENT_FACULTY_LINK)

    # TODO: implement to check whether class is required or restricted
    check_required_classes_or_restricted(major_content, total_classes, restricted_courses)

    # export_to_csv(total_classes, 'extracted_courses.csv')

def check_required_classes_or_restricted(major_content: dict, faculty_classes: set, restricted_classes: set):
    # how to store the new data? honestly just simple list
    # - 0 index is name of major
    # - rest are Y, N, or R
    # do same hashmap structure, but replace the list with Y,N,R

    """find restricted by """

    for major, specialization in major_content.items():
        for specialization, classes in specialization.items():

            s_classes = []

            for c in classes:
                if c in faculty_classes:
                    s_classes.append("Y")
                elif c in restricted_classes:
                    s_classes.append("R")
                else:
                    s_classes.append("N")

            major_content[major][specialization] = s_classes
    
    print(major_content)


    # so create new list, and then swap the old list with the new list and you're done

def get_restricted_courses(valid_classes: list, link: str):
    """Retrieve all restricted courses"""
    def parse_restricted(code, valid_classes: list):
        """Parse through the different formatting for restricted courses"""
        cell_text = code.get_text().strip()
        courseList = set()

        for c in valid_classes:
            if c in cell_text:
                courseList.add(cell_text)
        
        return courseList

    soup = get_soup(link)

    r_course_set = set()
    
    for code in soup.find_all(['td', 'li']):
        r_course_set.update(parse_restricted(code, valid_classes))
    
    # print(r_course_set)
            
    return r_course_set


        



def get_faculty_classes(link: str) -> list:

    soup = get_soup(link)
    # get class list
    all_classes = get_all_classes(VALID_CLASSES, soup)

    return all_classes


def find_major_courses(link: str):
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
    lfs_soup = get_soup(link)
    links_to_majors = lfs_soup.select('ol.list-buttons > li > a')

    for major in links_to_majors:
        if "B.Sc" not in major.get_text():
            continue

        major_name = major.get_text().strip()
        major_content[major_name] = {}

        if major.get('href'):
            major_soup = get_soup(f"https://vancouver.calendar.ubc.ca{major.get('href')}")
            # save major names as well into array as first item so it can be called with courses[0]
            specialization_links = get_specialization(major_soup) # have the individual majors now

            for specialty in specialization_links:
                
                # get classes for specialty
                if specialty.get('href'):
                    s_soup = get_soup(f"https://vancouver.calendar.ubc.ca{specialty.get('href')}")
                    s_classes = get_all_classes(VALID_CLASSES, s_soup)
                
                # get name of specialty
                specialty_name = specialty.get_text().strip()

                major_content[major_name][specialty_name] = s_classes

        
    # print(major_content)

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
            cur_course += cell_text[cell_text.index(cur_class) + cur_letter]
        else:
            break
        cur_letter += 1
        
    return cur_course

    

def get_all_classes(valid_classes: list, soup: BeautifulSoup) -> list:
    """Retrieve all classes from a given soup"""

    def parse_classes(code, valid_classes: list):
        """Perform checks on a given piece of HTML to see if its a valid class"""
        cell_text = code.get_text().strip()
        courseList = set()

        for c in valid_classes:
            if c in cell_text and len(cell_text) < 100:
                check_if_course_num = cell_text.index(c) + 8 # 8 is to see if there is a course number 8 indexes away
                if (check_if_course_num < len(cell_text)):
                    if cell_text[check_if_course_num].isnumeric():
                        course = check_if_code_done(cell_text, c)
                        courseList.add(course)
        
        return courseList
    

    all_courses = set()
    
    for code in soup.find_all(['td', 'li']):
        all_courses.update(parse_classes(code, valid_classes))
            
    return list(all_courses)

def parse_majors(cell: BeautifulSoup):
    cell_text = cell.get_text().strip()
    major_set = set()
    
    if ("Major" in cell_text and len(cell_text) < 50) or "Degree Requirement" in cell_text:
        major_set.add(cell) # add the original (with href)
    
    return major_set
        

def get_specialization(soup: BeautifulSoup) -> list:
    
    specialtySet = set()
    
    
    for cell in soup.select('ol.list-buttons > li > a'):
        specialtySet.update(parse_majors(cell))
        
    if specialtySet:
        return list(specialtySet)
    else:
        return []


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


                            
if __name__ == "__main__":
    main()