import re
import pdfplumber
import openpyxl

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
                    college_dict[college_key] = {'grade':[], 'course':[]}

                # Use regular expressions to find all the course patterns
                course_pattern = r"\d{9}\s-\s\w+[^\n]*"
                course_matches = re.finditer(course_pattern, text)
                
                # Iterate through each course match
                for course_match in course_matches:
                    course_key = course_match.group().strip()
                    college_dict[college_key]['course'].append(course_key)

                # Use pdfplumber to extract tables from the page
                tables = page.extract_tables()

                # If tables are found, check if they are unique and append them to the list associated with the course key
                if tables:
                    for table in tables:
                        college_dict[college_key]['grade'].append(table)
            else:
                # If a college match is not found, clear the current college dictionary
                college_dict = {}

    # Return the dictionary of colleges and courses
    return college_dict



path = "example.pdf"
college_dict = extract_data_from_pdf(path)
header = ['College Name', 'Course','Percentage GOPENS', 'Rank GOPENS', 'Percentage GSCS', 'Rank GSCS', 'Percentage GVJS', 'Rank GVJS', 'Percentage GNT1S', 'Rank GNT1S', 'Percentage GNT2S', 'Rank GNT2S', 'Percentage GNT3S', 'Rank GNT3S', 'Percentage GOBCS', 'Rank GOBCS', 'Percentage LOPENS', 'Rank LOPENS', 'Percentage LSCS', 'Rank LSCS', 'Percentage LVJS', 'Rank LVJS', 'Percentage LNT1S', 'Rank LNT1S', 'Percentage LNT2S', 'Rank LNT2S', 'Percentage LNT3S', 'Rank LNT3S', 'Percentage LOBCS', 'Rank LOBCS', 'Percentage DEFOPENS', 'Rank DEFOPENS', 'Percentage DEFOBCS', 'Rank DEFOBCS', 'Percentage TFWS', 'Rank TFWS', 'Percentage DEFRSCS', 'Rank DEFRSCS', 'Percentage DEFROBCS', 'Rank DEFROBCS', 'Percentage EWS', 'Rank EWS', 'Percentage DEFRNT1S', 'Rank DEFRNT1S', 'Percentage DEFRNT3S', 'Rank DEFRNT3S', 'Percentage GOPENH', 'Rank GOPENH', 'Percentage GSCH', 'Rank GSCH', 'Percentage GNT1H', 'Rank GNT1H', 'Percentage GOBCH', 'Rank GOBCH', 'Percentage LOPENH', 'Rank LOPENH', 'Percentage LSCH', 'Rank LSCH', 'Percentage LOBCH', 'Rank LOBCH', 'Percentage GNT3H', 'Rank GNT3H', 'Percentage GOPENO', 'Rank GOPENO', 'Percentage LOPENO', 'Rank LOPENO', 'Percentage LVJO', 'Rank LVJO', 'Percentage GSCO', 'Rank GSCO', 'Percentage GNT2O', 'Rank GNT2O', 'Percentage LSCO', 'Rank LSCO', 'Percentage GSTH', 'Rank GSTH', 'Percentage GVJH', 'Rank GVJH', 'Percentage GNT2H', 'Rank GNT2H', 'Percentage GSTO', 'Rank GSTO', 'Percentage GVJO', 'Rank GVJO', 'Percentage GOBCO', 'Rank GOBCO', 'Percentage LOBCO', 'Rank LOBCO', 'Percentage LNT1H', 'Rank LNT1H', 'Percentage GNT1O', 'Rank GNT1O', 'Percentage LNT2H', 'Rank LNT2H', 'Percentage LNT3H', 'Rank LNT3H', 'Percentage PWDOPENH', 'Rank PWDOPENH', 'Percentage LVJH', 'Rank LVJH', 'Percentage GNT3O', 'Rank GNT3O', 'Percentage LSTH', 'Rank LSTH', 'Percentage MI', 'Rank MI', 'Percentage LNT2O', 'Rank LNT2O']
indexing = ['GOPENS', 'GSCS','GSTS', 'GVJS', 'GNT1S', 'GNT2S', 'GNT3S','LSTS', 'GOBCS', 'LOPENS', 'LSCS', 'PWDOPENS','LVJS', 'LNT1S', 'LNT2S', 'LNT3S', 'LOBCS', 'DEFOPENS', 'DEFOBCS', 'TFWS', 'DEFRSCS', 'DEFROBCS', 'EWS', 'DEFRNT1S', 'DEFRNT3S', 'GOPENH', 'GSCH', 'GNT1H', 'GOBCH', 'LOPENH', 'LSCH', 'LOBCH', 'GNT3H', 'GOPENO', 'LOPENO', 'LVJO', 'GSCO', 'GNT2O', 'LSCO', 'GSTH', 'GVJH', 'GNT2H', 'GSTO', 'GVJO', 'GOBCO', 'LOBCO', 'LNT1H', 'GNT1O', 'LNT2H', 'LNT3H', 'PWDOPENH', 'LVJH', 'GNT3O', 'LSTH', 'MI', 'LNT2O']


# Create a new workbook and select the active worksheet
workbook = openpyxl.Workbook()
worksheet = workbook.active
worksheet.append(header)

for college in college_dict:
    for course, grade in zip(college_dict[college]['course'], college_dict[college]['grade']):
        row = [0] * len(indexing)
        row[0] = college
        row[1] = course
        for cast, rank in zip(grade[0], grade[1]):
            rank = rank.split('(')
            
            if cast and cast in indexing:
                print(cast, rank[-1].replace(')', ''), rank[0])
                i = indexing.index(cast)
                row[i+2] = rank[-1].replace(')', '')
                row[i+3] = rank[0]
        worksheet.append(row)


workbook.save('output.xlsx')
