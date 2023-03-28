import openpyxl

# Create a new workbook and select the active worksheet
workbook = openpyxl.Workbook()
worksheet = workbook.active

# Define the header row and write it to the worksheet
header = ['College Name', 'Course Name', 'GECA', '', 'MGM', '']
worksheet.append(header)

# Define the data rows and write them to the worksheet
data = ["AAA", 'RRR', {'name':'GECA', 'open': 10, 'close': 12}, {'name':'MGM', 'open': 15, 'close': 19}]
row = [data[0], data[1], data[2]['open'], data[2]['close'], data[3]['open'], data[3]['close']]
worksheet.append(row)

# Save the workbook
workbook.save('output.xlsx')
