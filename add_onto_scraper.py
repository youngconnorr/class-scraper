from bs4 import BeautifulSoup
import requests
import csv
import re
from collections import OrderedDict
import pandas as pd


'''

TODO:
If current course in csv is in a major, then add to its row

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

cur_csv = '24S_&_24W_All_LFS_Courses.csv'
pd_data = pd.read_csv(cur_csv)

pd_data["Majors_Column"] = ""
    


def main():
    faculty_term_1 = get_faculty_classes(TERM1_CLASSES_LINK)
    faculty_term_2 = get_faculty_classes(TERM2_CLASSES_LINK)
    faculty_term_1.extend(faculty_term_2)
    sorted_total = sorted(faculty_term_1)
    ordered_total_classes = OrderedDict.fromkeys(sorted_total, None)


    restricted_courses = get_restricted_courses(VALID_CLASSES, RESTRICTED_COURSES_LINK)   
    find_major_courses(PARENT_FACULTY_LINK)

    check_required_classes_or_restricted(major_content, ordered_total_classes, restricted_courses)
    
    


def check_required_classes_or_restricted(major_content: dict, faculty_classes: OrderedDict, restricted_classes: dict):
    
    def isValid(course):
        return True if re.match(r'^[A-Z]+_V\s\d+', course) else False
                
    '''
    iterate through course column, and then check against major_content[specialization]
    '''
    
    course_column = pd_data["Course Section"]
    
    
    for course in course_column:
        if isValid(course):
            
            for major, specializations in major_content.items():
                for specialization, values in specializations.items():
                    for major_course in values:
                        print("specialization: " + specialization)
                        if major_course in course:
                            print("passed 'in' test")
                            if specialization == "Degree Requirements and Program Options":
                                specialization = "Food and Resource Economics FRE"
                            pd_data.loc[course_column == course, "Majors_Column"] += f" {specialization}"
                            
    pd_data.to_csv('test_csv.csv', index=False)
    print(pd_data.head())
                
            
            

    # for major, specialization in major_content.items():
    #     for specialization, specialization_classes in specialization.items():
    #         for r_program, r_class in restricted_classes.items():
    #             # Check if specialization matches restricted program criteria
    #             is_base_match = specialization[:-6] in r_program
    #             is_dual_degree_match = "Dual Degree" in specialization and "Dual Degree" in r_program
    #             is_fnh_general_match = "Food, Nutrition, and Health Major" in specialization and "FNH General (" in r_program
    #             is_food_science_exception = "Food Science Major" in specialization and "FNH" in r_program
    #             is_nutrition_exception = "Nutritional Sciences Major" in specialization and "Double Major" in r_program
    #             is_food_econ = "Food and Resource" in major and "Food and Resource" in r_program

    #             # Combine conditions
    #             if is_food_econ:
    #                 print("ECON MAJOR:", major)
    #                 print("RESTRICTED MAJOR:", r_program)
    #             if is_base_match or is_dual_degree_match or is_fnh_general_match:
    #                 if is_food_science_exception or is_nutrition_exception:
    #                     continue
    #                 # print("SPECIALIZATION: ", specialization, "\nRESTRICTED PROGRAM: ", r_program, "\n")
                

    #                 '''
    #                 run the restricted program courses against all courses. find out which ones are R's in a list
    #                 then run specializations against all courses and find Y and N's

    #                 then merge lists? (how do you do that?)

                    
    #                 '''
    #                 r_array = []
    #                 valid_class_array = []

    #                 course_pattern = re.compile(r'^[A-Z]+\s\d+') # regex to check valid class
    #                 extracted_r_courses = [course_pattern.search(course).group(0) for course in r_class if course_pattern.search(course)]

    #                 for each_class in faculty_classes.keys():
    #                     parsable_class = each_class.replace("_V", "")
    #                     if parsable_class in extracted_r_courses:
    #                         r_array.append('R')
    #                     else:
    #                         r_array.append('N')
                        
                    
    #                 for each_class in faculty_classes.keys():
    #                     if each_class in specialization_classes:
    #                         valid_class_array.append('Y')
    #                     else:
    #                         valid_class_array.append('N')

                    
    #                 # print(r_array)
    #                 # print(valid_class_array)

    #                 priority = {'Y': 3, 'R': 2, 'N': 1}

    #                 # Merge function
    #                 def merge_values(v1, v2):
    #                     return v1 if priority[v1] >= priority[v2] else v2

                   

    #                 # Merging logic
    #                 merged_classes = [merge_values(l1, l2) for l1, l2 in zip(r_array, valid_class_array)]

    #                 # print(merged_classes)  # Output: ['N', 'Y', 'R', 'N', 'R']

    #                 # merge lists! ITS CORRECT LFG
    #                 major_content[major][specialization] = merged_classes
    #                 '''
    #                 TODO: CHECK OVER THE 2021W AND 2022W COURSES CAUSE THAT MIGHTVE MESSEDUP, 
    #                     - other than that, import pandas and then export to excel!
                    
    #                 '''
                
    
    # # print(major_content)
    # rows = []
    
    # for major, specializations in major_content.items():
    #     for specialization, values in specializations.items():
    #         for value in values:
    #             rows.append({"Major": major, "Specialization": specialization, "values" : value})
             
    # df = pd.DataFrame(rows)
    # print(df)

    # # # Save to Excel
    # df.to_excel("class-data.xlsx")
    # # print("done")
    
    
    # # Create a new workbook and select the active sheet
    
    
    return

    # so create new list, and then swap the old list with the new list and you're done

def get_restricted_courses(valid_classes: list, link: str):
    """Retrieve all restricted courses"""
    def parse_restricted(code, valid_classes: list):
        """Parse through the different formatting for restricted courses"""
        cell_text = code.get_text().strip()
        courseSet = set()

        for c in valid_classes:
            if c in cell_text:
                courseSet.add(cell_text)
        return courseSet

    soup = get_soup(link)

    r_dict = {}
    # split up by accordion-shortcode accordion
    for major_group in soup.find_all("div", class_="accordion-group"):

        major_name = major_group.find("a", class_="accordion-toggle")
        if major_name:
            temp_name = major_name.text.strip()
            r_dict[temp_name] = set()
        else:
            continue
        
        for code in major_group.find_all('li'):
            r_dict[temp_name].update(parse_restricted(code, valid_classes))

    return r_dict
            

        



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
    def get_specialization(soup: BeautifulSoup) -> list:
        
        specialtySet = set()
        
        
        for cell in soup.select('ol.list-buttons > li > a'):
            specialtySet.update(parse_majors(cell))
            
        if specialtySet:
            return list(specialtySet)
        else:
            return []




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
            # print(specialization_links)

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
    
    if ("Major" in cell_text and len(cell_text) < 50) or "Degree Requirements and" in cell_text or "Dual Degree" in cell_text:
        major_set.add(cell) # add the original (with href)
    
    return major_set
        


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