from flask import Flask, render_template
import PyPDF2
import pandas as pd
# Open the PDF file
with open(r'C:\Users\mordes\Downloads\ML_PROJECTS\io_extraction\13.0000755 circuit diagram Rev.1.pdf', 'rb') as pdf_file:
    # Create a PDF reader object
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    # Create a Word document
    data = []

    # Write the contents of each page of the PDF to the Word document
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        data.append(page.extract_text())
lobbe = 1

if True:
    import re
    raw_input = []
    for i in data:
        input_result = re.findall(r"I(.*?) =", i)
        if input_result:
            raw_input.append(input_result)
    input_list = []
    for i in range(len(raw_input)):
        if len(raw_input[i]) > 5:
            input_list.extend(raw_input[i])
    input_address = []
    input_name = []
    analog_input_address = []
    analog_input_name = []
    for i in range(len(input_list)):
        if len(input_list[i]) > 8:
            AA = input_list[i].replace("(1", "").replace(
                "( 1", "").replace("2I", "").split(' ', 1)
            input_address.append("I"+AA[0])
            input_name.append((AA[1]))

    raw_output = []
    for i in data:
        output_result = re.findall(r"Q(.*?) =", i)
        if output_result:
            raw_output.append(output_result)
    output_list = []
    for i in range(len(raw_output)):
        if len(raw_output[i]) > 5:
            output_list.extend(raw_output[i])
    output_address = []
    output_name = []
    analog_output_address = []
    analog_output_name = []
    for i in range(len(output_list)):
        if len(output_list[i]) > 8:
            AA = output_list[i].replace("(1", "").replace(
                "( 1", "").replace("2I", "").split(' ', 1)
            output_address.append('Q'+AA[0])
            output_name.append((AA[1]))




Input_df = pd.DataFrame(
    {"Input_Adrress": input_address, "Input_Name": input_name})
Output_df = pd.DataFrame(
    {"Output_Adrress": output_address, "Output_Name": output_name})
Output_df = Output_df.sort_values(by='Output_Adrress')
result = pd.concat([Input_df, Output_df], axis=0)
result
Machine_type = re.search(r'ICM( \d\.\d)', data[0]).group(0)
order_number = re.search(r'13(.\d{7})', data[0]).group(0)
Name_of_file = Machine_type+"_"+order_number+".xlsx"
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
