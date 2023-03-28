import re
import pdfplumber

def extract_data_from_pdf(path):
    # Initialize an empty dictionary for the colleges
    college_dict = {}

    # Open the PDF file
    with pdfplumber.open(path) as pdf_file:
        # Iterate through the pages of the PDF
        i = 0
        for page in pdf_file.pages:
            if i == 1:
                break
            i += 1
            # Extract the text from the page
            text = page.extract_text()

            # Use regular expressions to find the college pattern
            college_pattern = r"\d{4}\s-\s\w+[^\n]*"
            college_match = re.search(college_pattern, text)

            # If a college match is found, use it as the key in the college dictionary
            if college_match:
                college_key = college_match.group().strip()

                # Check if the college key already exists in the dictionary
                if college_key not in college_dict:
                    # If the college key does not exist, add it to the dictionary with an empty dictionary for courses
                    college_dict[college_key] = {}

                # Use regular expressions to find all the course patterns
                course_pattern = r"\d{9}\s-\s\w+[^\n]*"
                course_matches = re.finditer(course_pattern, text)

                # Iterate through each course match
                for course_match in course_matches:
                    course_key = course_match.group().strip()
                    if course_key not in college_dict[college_key]:
                        college_dict[college_key][course_key] = []

                    # Use pdfplumber to extract tables from the page
                    tables = page.extract_tables()

                    # If tables are found, check if they are unique and append them to the list associated with the course key
                    if tables:
                        for table in tables:
                            if table not in college_dict[college_key][course_key]:
                                college_dict[college_key][course_key].append(table)
            else:
                # If a college match is not found, clear the current college dictionary
                college_dict = {}

    # Return the dictionary of colleges and courses
    return college_dict



path = "example.pdf"
college_dict = extract_data_from_pdf(path)

# Display the output in a structured format
for college_key in college_dict:
    print(f"College: {college_key}")
    for course_key in college_dict[college_key]:
        print(f"\tCourse: {course_key}")
        for tables in college_dict[college_key][course_key]:
            for table in tables:
                print("\t\t", end="")
                print(table)
