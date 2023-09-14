import requests
from bs4 import BeautifulSoup
from unidecode import unidecode  

# Create and open the text files to export our script data
faculty_links_file = open("bios_url.txt", "w")
faculty_bios_file = open("bios.txt", "w")
faculty_courses_file = open("courses_taught.txt", "w")

# Web Scraping Information from the Engineering Department at Dartmouth
url = "https://engineering.dartmouth.edu/community/faculty#core"

# Send an HTTP GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content of the webpage
    soup = BeautifulSoup(response.content, "html.parser")

    # Scrape all the information off the main page
    faculty_main = soup.find_all("div", class_="columns profile-box")

    # Iterate through each faculty on the main page
    for faculty_element in faculty_main:
        # Find the individual faculty link for everyone on the main page
        faculty_link_element = faculty_element.find("a")

        # Extract links and store it
        faculty_link = faculty_link_element["href"] if faculty_link_element else None

        # Visit the faculty's individual page
        faculty_response = requests.get(faculty_link)

        if faculty_response.status_code == 200:
            faculty_soup = BeautifulSoup(faculty_response.content, "html.parser")

            # Extract faculty name from the individual page using h1 element
            faculty_name_element = faculty_soup.find("img", class_="prof-pic").find_next("h1")
            faculty_name = faculty_name_element.get_text().strip() if faculty_name_element else "Name not found"

            # Convert non-ASCII characters to their closest ASCII equivalents. 
            # (Some faculty has unique characters which will cause errors in Python when running). Therefore we need unidecode function to avoid errors.
            faculty_name = unidecode(faculty_name)

            # Find and extract faculty biography
            faculty_bio_element = faculty_soup.find("div", class_="columns small-12")
            if faculty_bio_element:
                faculty_bio = faculty_bio_element.find("p").get_text().strip()
            else:
                faculty_bio = "Faculty does not have a biography."

            # Find and extract faculty courses
            faculty_courses_elements = faculty_soup.find_all("a", href=True)
            faculty_courses_list = []

            for course_element in faculty_courses_elements:
                course_href = course_element["href"]
                if "/courses/" in course_href:
                    course_name = course_element.get_text()
                    if course_name != "Course Descriptions" and course_name != "Course Schedules":
                        faculty_courses_list.append(course_name)

            # Write the information to respective files. Seperated the names and additional information with two TAB units worth of space
            faculty_links_file.write(faculty_name + "       " + faculty_link + "\n")
            faculty_bios_file.write(faculty_name + "        " + faculty_bio + "\n")
            faculty_courses_file.write(faculty_name + "         " + ", ".join(faculty_courses_list) + "\n")

    # Close the files after writing all the data
    faculty_links_file.close()
    faculty_bios_file.close()
    faculty_courses_file.close()

else:
    print("Failed to retrieve the webpage. Status code:", response.status_code)