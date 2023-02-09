from flask import Flask, render_template,request
import PyPDF2
import pandas as pd
# Open the PDF file
with open(r'C:\\Users\\mordes\Downloads\\ML_PROJECTS\\io_extraction\\13.0000557 Control Cabinet_2021-03-22+Model view_REV_A (2).pdf', 'rb') as pdf_file:
    # Create a PDF reader object
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    # Create a Word document
    data = []

    # Write the contents of each page of the PDF to the Word document
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        data.append(page.extract_text())
        
import re
io_pages=[]
for i in range(len(data)):
    if "PLC Overview" in data[i]:
        io_pages.append(i)
if io_pages:
    input_name=[]
    input_address=[]
    for i in range(len(io_pages)):
        try:
            for match in re.finditer(r"\nI[0-9]\.[0-9]", data[io_pages[i]]):
                 input_address.append(match.group().replace("\n", ""))
            for match in re.finditer(r"\nDI(.*?)\n", data[io_pages[i]]):
                input_name.append(match.group(1).split(" ",2)[-1])  
            
        except IndexError:
            pass
else:
    print("No 'PLC Overview' found in the data")       
        
io_pages=[]
for i in range(len(data)):
    if "PLC Overview" in data[i]:
        io_pages.append(i)
if io_pages:
    output_address=[]
    output_name=[]
    output_result=[]
    for i in range(len(io_pages)):
        try:
            for match in re.finditer(r"\nQ[0-9]\.[0-9]", data[io_pages[i]]):
                 output_address.append(match.group().replace("\n", ""))
            for match in re.finditer(r"\nDQ(.*?)\n", data[io_pages[i]]):
                output_result.append(match.group(1).split(' ',2)[-1])  
            if output_result:
                output_name.extend(output_result)
        except IndexError:
            pass
else:
    print("No 'PLC Overview' found in the data")       




Input_df = pd.DataFrame(
    {"Input_Adrress": input_address, "Input_Name": input_name})
Output_df = pd.DataFrame(
    {"Output_Adrress": output_address, "Output_Name": output_result})
Output_df = Output_df.sort_values(by='Output_Adrress')
result = pd.concat([Input_df, Output_df], axis=0)
result
# Machine_type = re.search(r'ICM( \d\.\d)', data[0]).group()
# order_number = re.search(r'13(.*?{4})', data[0]).group()
Name_of_file = "ICM"+"_"+"624"+".xlsx"
Input_df.to_excel(Name_of_file, sheet_name="Inputs")
Output_df.to_excel(Name_of_file, sheet_name="Outputs")
with pd.ExcelWriter(Name_of_file) as writer:  # doctest: +SKIP
    Input_df.to_excel(writer, sheet_name='Inputs')
    Output_df.to_excel(writer, sheet_name='Outputs')


app = Flask(__name__)


@app.route("/")
def index():

    return render_template("index.html", data1=Input_df.to_html(), data2=Output_df.to_html())




if __name__ == "__main__":
    app.run(debug=True)
