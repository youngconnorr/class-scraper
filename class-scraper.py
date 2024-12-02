from bs4 import BeautifulSoup
import requests
import csv

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
    

def get_classes(valid_classes: list, soup: BeautifulSoup):
    
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
        

def get_majors(soup: BeautifulSoup):
    
    majorSet = set()
    
    
    for cell in soup.select('ol.list-buttons > li > a'):
        majorSet.update(parse_majors(cell))
        
    if majorSet:
        return list(majorSet)
    else:
        return -1


def export_to_csv(courses, filename):
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
    
    lfs_courses_term_1="https://courses.landfood.ubc.ca/?term=2024-25-winter-term-1-ubc-v&subject=All"
    lfs_courses_term_2="https://courses.landfood.ubc.ca/?term=2024-25-winter-term-2-ubc-v&subject=All"

    # grab HTML content using requests
    html_content_1 = requests.get(lfs_courses_term_1).text
    html_content_2 = requests.get(lfs_courses_term_2).text

    # turn into soup
    term_1_soup = BeautifulSoup(html_content_1, "lxml")
    term_2_soup = BeautifulSoup(html_content_2, "lxml")

    # get class list
    found_classes_1 = get_classes(valid_classes, term_1_soup)
    found_classes_2 = get_classes(valid_classes, term_2_soup)
    found_classes_1.extend(found_classes_2)

    total_class = set()
    total_class.add(tuple(found_classes_1))
    
    url2 = "https://vancouver.calendar.ubc.ca/faculties-colleges-and-schools/faculty-land-and-food-systems/bsc-food-nutrition-and-health-fnh"
    html_content = requests.get(url2).text
    soup = BeautifulSoup(html_content, "lxml")
    # print(get_majors(soup))
    
    # majors = [a.text.strip() for a in soup.select('ol.list-buttons > li > a')[4:]]
    # print(majors)
    
    
    
    # export_to_csv(found_classes, 'extracted_courses.csv')

                            
if __name__ == "__main__":
    main()