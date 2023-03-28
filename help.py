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
            i+=1
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
                
                # Use regular expressions to find the course pattern
                course_pattern = r"\d{9}\s-\s\w+[^\n]*"
                course_matches = re.finditer(course_pattern, text)
                
                # Loop through all the course matches and add them to the college dictionary
                for course_match in course_matches:
                    course_key = course_match.group().strip()
                    if course_key not in college_dict[college_key]:
                        college_dict[college_key][course_key] = []
                    
                    # Use pdfplumber to extract tables from the page
                    tables = page.extract_tables()
                    
                    # If tables are found, append them to the list associated with the course key
                    if tables:
                        # Check if the tables are already present in the list
                        if tables not in college_dict[college_key][course_key]:
                            college_dict[college_key][course_key].append(tables)
                    else:
                        # If tables are not found, clear the current list of tables
                        college_dict[college_key][course_key] = []
    
    # Return the dictionary of colleges and courses
    return college_dict


path = "example.pdf"
college_dict = extract_data_from_pdf(path)

print(college_dict)
