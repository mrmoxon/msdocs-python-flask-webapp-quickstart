import os
from werkzeug.utils import secure_filename
from flask import (Flask, redirect, render_template, request,
                   send_from_directory, flash, url_for, send_file)

app = Flask(__name__)
# app.run(debug=True)

UPLOAD_FOLDER = os.path.join(app.root_path, 'uploads')
DOWNLOAD_FOLDER = os.path.join(app.root_path, 'downloads')
ALLOWED_EXTENSIONS = {'docx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
app.config['SECRET_KEY'] = '3336666782822'

@app.route('/')
def index():
    print('Request for index page received')
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'bselected.ico', mimetype='image/vnd.microsoft.icon')

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    # return '.' in filename and \
    #        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        role = request.form.get('role')
        print(f'Role: {role}')

        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File successfully uploaded and renamed')

            if role:
                print('Request for upload page received with role=%s' % role)
            else:
                flash('No role defined, file saved but not processed')

            return render_template('upload.html', filename=filename)

    # When the route is accessed through GET request, i.e. opening the page
    else:  
        return render_template('upload.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

            

if __name__ == '__main__':
   app.run(debug=True)





# @app.route('/upload', methods=['GET', 'POST'])
# def home():
#     # Clear all flashed messages
#     session.pop('_flashes', None)
#     uploaded_files = session.get('uploaded_files', [])
#     app.logger.info('Activating home() function')

#     # Check if the request method is POST (i.e., data has been sent to the server)
#     if request.method == 'POST':
#         app.logger.info('POST request received at /, refreshing page')

#         # Check if there's a file in the request
#         if 'file' not in request.files:
#             app.logger.warning('No file part in uploaded data')
#             flash('No file part')
#             return redirect(request.url)
#         else:
#             # If there's a file, get it from the request
#             file = request.files['file']
#             app.logger.info('File part in uploaded data')

#         # Check if a filename has been specified for the file
#         if file.filename == '':
#             app.logger.warning('No selected file in uploaded data')
#             flash('No selected file')
#             return redirect(request.url)
#         else:
#             # If there's a filename, log it
#             app.logger.info(f'File part received with filename: {file.filename}')

#         # Check if the file is not None and if its filename is allowed (i.e., has a correct extension)
#         if file and allowed_file(file.filename):
#             # If the file is valid, secure the filename (to avoid any security risks)
#             filename = secure_filename(file.filename)
#             app.logger.info(f'File {filename} is allowed and its name is secured')



#             file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#             # app.logger.info(f'File {filename} saved successfully')



#             # Read the content of the .docx file
#             cv_text = read_docx(filename, app.config['UPLOAD_FOLDER'])

#             if cv_text is None:
#                 app.logger.error('Failed to read the file, stopping execution')
#                 raise Exception('Failed to read the file')

#             app.logger.info(f'File {filename} reading complete!')  # log the content of the file
#             app.logger.info(f'{cv_text}')  # log the content of the file

#             uploaded_files.append(filename) # AFdd the filename to the list of uploaded files
#             session['uploaded_files'] = uploaded_files # Store the list of uploaded files in the session
#             session['message'] = f'File {filename} successfully uploaded'  # Store message in session





#             # Create a filename using the uploaded file's name
#             # filename_base = os.path.splitext(filename)[0]
#             # Extract the base of the filename
#             filename_base, _ = os.path.splitext(filename)
#             # Define the new filename
#             json_filename = f"{filename_base}_cv_data"

#             app.logger.info("Looking for json file: " + json_filename)
#             # Specify the file path
#             file_path = os.path.join(app.config['UPLOAD_FOLDER'], json_filename + ".json")
#             app.logger.info(f"Looking in {file_path} for {json_filename}")

#             # Check if the json file exists
#             if os.path.exists(file_path):
#                 app.logger.info(f"File {json_filename} already exists at {file_path}. Loading data from the file.")

#                 # Open the file and load the data
#                 with open(file_path, 'r') as f:
#                     gpt_output = json.load(f)

#                 # Extract the individual pieces of data
#                 cv_jobs = gpt_output["jobs_data"]
#                 cv_various = gpt_output["various_data"]
#                 cv_profile = gpt_output["profile_data"]

#                 app.logger.info(f"Found cv_jobs, cv_various, cv_profile.")

#             # If the file does not exist, generate the data and save a new json file
#             else:
                
#                 app.logger.info(f"Existing record not found; now generating data using GPT-4.")
#                 desired_role = request.form.get('role', 'desired role')

#                 # Prompts for GPT
#                 jobs_data = [
#                     {"role": "system", "content":"You are a helpful assistant, accurately editing the CV of an anonymous candidate in json format."},
#                     {"role": "user", "content": f"For each job listed in this CV: \n\n{cv_text}\n\n, please provide the following information in the specified format. Manually extract this information without code. Output should have each job in one single JSON format (in a list). \n JSON output I want: \n\n {{'company': 'Company Name', \n 'role': 'Job Title', \n'date': 'Start Date - End Date', \n'achievements': [ \n'List of achievements', \n'Achievement 1', \n'Achievement 2', \n'Achievement 3', \n... \n ], \n 'job description': 'Generic overview of tasks filled under this job title', \n }} \n\n Please note the following: \n'Company Name' should be the name of the company where you worked.\n'Job Title' should be the title of your position at the company.\n'Start Date - End Date' should be the timeframe during which you worked at the company. Please use the format 'mmm yy - mmm yy'; e.g., if September 2019, output should be Sep 19.\n'List of achievements' should include all listed achievements and responsibilities accomplished during your time at the company. Each achievement should be a separate string within the list. Include all listed sentences for each role, and leave them largely unchanged. If achievements are not explicitly mentioned, transform responsibilities into achievements by rephrasing them. Ensure each sentence begins with a different emotive adverb and is written in British English past tense, ending with a full stop. If they're already convincingly impressive and well-worded, leave them unchanged, but if these responsibilities can be improved by rephrasing without adding meaning, then do so.\n'Generic overview of tasks filled under this job title' should be two sentences; first, a concise, generic description of tasks and responsibilities typically held by a person in the role of the mentioned job title. Begin the first sentence with 'Responsibilities include/included...' or 'Required to...' based on the dates and relevance. The second: a description of their overarching responsibilities. This description should not repeat information listed in the achievements, but if relevant points from the achievements can be made generic and incorporated into the job description, then do so.\nAfter extracting the necessary details, please directly format them into JSON without providing an intermediate summary of the extracted information.\nPlease ensure that all information is accurate and complete. Make sure the JSON format response is a single, coherent JSON code without breaks.\n"}
#                 ]

#                 various_data = [
#                     {"role": "system", "content":"You are a helpful assistant, accurately editing the CV of an anonymous candidate in json format."},
#                     {"role": "user", "content": f"Consider the candidate in this CV: \n\n{cv_text}\n\n This person is applying for the role = {desired_role}. Write in JSON format: \n\n {{ \n 'desired_role': 'Desirable'\n'education': 'Educated level and certification',\n'training': [\n'List of professional qualifications',\n'Training 1',\n'Training 2',\n'Training 3',\n...\n]\n'languages': 'Spoken dialects',\n'interests': 'Noted interests',\n'skills': 'List of skills',\n'tech_skills': 'List of technical expertise'\n}}\n,\nPlease note the following:\n'Desirable' should be the name of the role entered above.\n'Educated level and certification' should be the name of the highest level of education achieved by the candidate in the order 'Institution - Qualification (Grade)'. Omit the date. If none are mentioned, output 'x' here.\n'List of professional qualifications' should include any technical software certifications, as well as qualifications and training courses that have been mentioned by the candidate, omit the date. Do not include anything that isn't mentioned explicitly, and if none are mentioned, output 'x' here.\n'Spoken dialects' should be filled only when they mention other languages than English. Include each additional language in the format 'Language - Level', where level equates to Fluent, Basic, Native, etc., depending on how they describe it. Do not output just English alone. If none are mentioned, output 'x' here.\n'Noted interests' should only be filled when they mention their interests directly. This should be one sentence that combines what they have said, using unchanged language. If none are mentioned, output 'x' here.\n'List of skills' should be a sequence of 9-to-12 general professional competencies shown in the text each separated by |. This should include skills relevant to their desired job and should omit personality traits such as 'Communication'. Make these compelling and representative of the candidate. Examples might include 'Strategic Planning', 'Data Analysis', 'Waterfall Methodologies', 'Mentoring', 'Agile Software Development', and 'Negotiation & Conflict Resolution'.\n'List of technical expertise' should include a list of softwares, programming languages, or other proficiencies displayed in the text. If there are less than a few mentioned, output 'x' here.\nAfter extracting the necessary details, please directly format them into JSON without providing an intermediate summary of the extracted information.\n"}
#                 ]

#                 profile_data = [
#                     {"role": "system", "content": "You are a helpful assistant, creating a strong personal profile that accurately describes an anonymous candidate in json format."},
#                     {"role": "user", "content": f"Using this information \n\n{cv_text}\n\n, write a compelling summary/personal statement without definite articles for the desired role: {desired_role}. Use the format \n {{ \"summary\": \"personal statement\"}}, where personal statement is around 200 words, no more. \n\n Begin with the sentence: 'An {{adjective_1}} and {{adjective_2}} {desired_role} with a strong background in {{relevant_industry}}.' Add what they've already written about themselves. If they've written nothing, use their experiences to write a compelling personal summary. Then, finish by mentioning their collaborative approach to teams and interpersonal skills. \n\n After extracting the necessary details, please directly format them into JSON without providing an intermediate summary of the extracted information."}
#                 ]

#                 try:
#                     app.logger.info('Generating "jobs_data" using GPT-4...')
#                     cv_jobs = generate_chat_completion(jobs_data)
#                     app.logger.info('Successfully generated jobs_data.')
#                     app.logger.info(f'{cv_jobs}')

#                     app.logger.info('Generating "various_data" using GPT-4...')
#                     cv_various = generate_chat_completion(various_data)
#                     app.logger.info('Successfully generated various_data.')
#                     app.logger.info(f'{cv_various}')

#                     app.logger.info('Generating "profile_data" using GPT-4...')
#                     cv_profile = generate_chat_completion(profile_data)
#                     app.logger.info('Successfully generated profile_data.')
#                     app.logger.info(f'{cv_profile}')

#                 except Exception as e:
#                     app.logger.error(f'Failed to generate cv data: {e}')




#             # Convert variables from string to json
#             app.logger.info('Converting variables from string to json.')
#             try:
#                 # Extract substring between [ and ] inclusive
#                 start_cv_jobs = cv_jobs.index('[')
#                 end_cv_jobs = cv_jobs.rindex(']') + 1  # adding 1 because indexing is exclusive at the end
#                 cv_jobs = cv_jobs[start_cv_jobs:end_cv_jobs]
#                 # Convert to true json
#                 cv_jobs = json.loads(cv_jobs)
#                 app.logger.info(f'Successfully converted cv_jobs; New: {cv_jobs}')
                
#                 cv_various = json.loads(cv_various)

#                 if isinstance(cv_profile, str):
#                     try:
#                         cv_profile = json.loads(cv_profile)
#                         app.logger.error("Decoded cv_profile on attempt 1.")

#                     except json.JSONDecodeError:
#                         try:
#                             cv_profile = cv_profile.replace("'", '"')
#                             cv_profile = json.loads(cv_profile)
#                             app.logger.error("Decoded cv_profile on attempt 2.")

#                         except json.JSONDecodeError:
#                             app.logger.error("Failed to decode cv_profile.")

#                     app.logger.info(f'Type of cv_jobs after json.loads: {type(cv_jobs)}')
#                     app.logger.info(f'Type of cv_various after json.loads: {type(cv_various)}')
#                     app.logger.info(f'Type of cv_profile after json.loads: {type(cv_profile)}')
                    
#                     app.logger.info(f'Successfully converted gpt outputs to json.')

#                 else:
#                     app.logger.info(f'cv_profile is already json: {cv_profile}')
#             # Exception as e:
#             #         app.logger.info(f'Failed to convert to json: {e}')

#             except Exception as e:
#                 app.logger.info(f"An error occurred during CV processing: {e}")




#             # Save the json outputs to a file

#             gpt_output = {
#                 "jobs_data": cv_jobs,
#                 "various_data": cv_various,
#                 "profile_data": cv_profile
#             }

#             try:
#                 # # Create a filename using the uploaded file's name
#                 # filename_base = os.path.splitext(filename)[0]
#                 # json_filename = f"{filename_base}_cv_data.json"

#                 # # Specify the file path
#                 # file_path = os.path.join(app.config['UPLOAD_FOLDER'], json_filename)

#                 # Combine all the data into a single dictionary


#                 # Write the new data to the file
#                 with open(file_path, 'w') as f:
#                     json.dump(gpt_output, f)

#                 app.logger.info(f"Successfully saved json data to {file_path}")

#             except Exception as e:
#                 app.logger.error(f"An error occurred while saving data to file: {e}")

            




#             # Load the TEMPLATE document with python-docx
#             doc = Document(os.path.join(template_file_path, 'TEMPLATE.docx'))
#             app.logger.info('TEMPLATE document loaded.')  # log the content of the file




#             # Perform placeholder replacements

#             # Replace the placeholders in the CV jobs section
#             app.logger.info('Replacing placeholders in TEMPLATE.docx')
#             cv_jobs = cv_jobs[-5:]

#             for i, job in enumerate(cv_jobs, start=1):
#                 app.logger.info(f'Job #{i}: {job}')
#                 app.logger.info(f'Type of job #{i}: {type(job)}')
#                 # Company
#                 doc = docx_replace_text_with_placeholder(doc, f"Company{i}", job["company"])
#                 # Role
#                 doc = docx_replace_text_with_placeholder(doc, f"Role{i}", job["role"])
#                 # Date
#                 doc = docx_replace_text_with_placeholder(doc, f"Date{i}", job["date"])
                
#                 # Job description
#                 try:
#                     doc = docx_replace_text_with_placeholder(doc, f"JobDesc{i}", job["job description"])
#                 except KeyError:
#                     try:
#                         doc = docx_replace_text_with_placeholder(doc, f"JobDesc{i}", job["job_description"])
#                     except KeyError as e:
#                         app.logger.info(f'Failed to replace job description for Job{i}: {e}')
                
#                 # Achievements
#                 MAX_ACHIEVEMENTS = 9  # Set to the maximum number of achievement placeholders in your template
#                 for j, achievement in enumerate(job["achievements"], start=1):
#                     if j > MAX_ACHIEVEMENTS:
#                         break
#                     try:
#                         doc = docx_replace_text_with_placeholder(doc, f"Achieved{i}_{j}", achievement)
#                         app.logger.info(f'Achievement{j} replaced for Job{i}')
#                     except Exception as e:
#                         app.logger.info(f'Failed to replace achievement for Job{i}: {e}')

#             app.logger.info(f'Job details replaced for Job{i}')



#             # Replace the placeholders in the CV profile section
#             try: 
#                 doc = docx_replace_text_with_placeholder(doc, f"Summary1", cv_profile['summary'])

#             except TypeError as e:
#                 doc = docx_replace_text_with_placeholder(doc, f"Summary1", cv_profile)
            
#             app.logger.info('Summary replaced')

            

#             # Replace the placeholders in the CV various section
#             keys_and_placeholders = [
#                 ("desired_role", "DESIRED"),
#                 ("education", "Education1"),
#                 ("languages", "Language1"),
#                 ("interests", "Interests1"),
#                 ("skills", "Skills1"),
#                 ("tech_skills", "TechSkills1"),
#             ]

#             for key, placeholder in keys_and_placeholders:
#                 if key in cv_various:
#                     app.logger.info(f'{key} exists in cv_various')
#                 else:
#                     app.logger.info(f'{key} does not exist in cv_various')

#                 try:
#                     app.logger.info(f'Type of {key}: {type(cv_various[key])}')
#                     doc = docx_replace_text_with_placeholder(doc, placeholder, str(cv_various[key]))
#                 except Exception as e:
#                     app.logger.info(f'Failed to replace {key} placeholder: {e}')

#             try:
#                 trainings = cv_various["training"]
#                 app.logger.info(f'Type of training: {type(trainings)}')

#                 for i, training in enumerate(trainings, start=1):
#                     doc = docx_replace_text_with_placeholder(doc, f"Training{i}", training)
#                 app.logger.info('Training replaced')

#             except KeyError:
#                 app.logger.info("training does not exist in cv_various")
#             except Exception as e:
#                 app.logger.info(f'Failed to replace training placeholder: {e}')

#             app.logger.info('Various details replaced')

#             # for i, training in enumerate(cv_various["training"], start=1):
#             #     doc = docx_replace_text_with_placeholder(doc, f"Training{i}", training)
#             #     app.logger.info('Training replaced')



#             # Remove excess

#             # Removal Functions            
#             def remove_paragraph(paragraph):
#                 p = paragraph._element
#                 p.getparent().remove(p)
#                 p._p = p._element = None

#             def remove_placeholder_paragraphs(doc, placeholder_prefix):
#                 paragraphs_to_delete = []
#                 # Identify the paragraphs to delete
#                 for i, paragraph in enumerate(doc.paragraphs):
#                     # Only consider paragraphs that still contain the placeholder
#                     if placeholder_prefix in paragraph.text:
#                         paragraphs_to_delete.append(i)
                
#                 # Delete the identified paragraphs in reverse order
#                 # (so that deleting a paragraph doesn't change the index of later paragraphs)
#                 for i in reversed(paragraphs_to_delete):
#                     remove_paragraph(doc.paragraphs[i])
                
#                 return doc

#             # Removal calls
#             doc = remove_placeholder_paragraphs(doc, "Company")
#             doc = remove_placeholder_paragraphs(doc, "Date")
#             doc = remove_placeholder_paragraphs(doc, "JobDesc")
#             doc = remove_placeholder_paragraphs(doc, "Education")
#             doc = remove_placeholder_paragraphs(doc, "Training")
#             doc = remove_placeholder_paragraphs(doc, "Achieved")

#             def remove_empty_paragraphs(doc):
#                 paragraphs_to_delete = []
#                 for i in range(len(doc.paragraphs) - 1):  # -1 to avoid index error on last item
#                     if doc.paragraphs[i].text.strip() == '' and doc.paragraphs[i+1].text.strip() == '':
#                         paragraphs_to_delete.append(i)
#                 for i in reversed(paragraphs_to_delete):
#                     remove_paragraph(doc.paragraphs[i])
#                 return doc
            
#             # doc = handle_empty_subheadings(doc)
#             doc = remove_empty_paragraphs(doc)




#             # Save the document back to the disk
#             new_draft_filename = f'Draft {filename_base} CV2.docx'

#             doc.save(os.path.join(app.config['UPLOAD_FOLDER'], new_draft_filename))
#             app.logger.info(f'File saved as {new_draft_filename}')

#             return redirect(url_for('home'))  # Redirect
        
#         else:
#             app.logger.warning(f'File {file.filename} is either missing or not allowed')

#     # Handling GET requests
#     message = session.pop('message', None)
#     if message:
#         flash(message)

#     return render_template('upload_form.html')




# @app.errorhandler(500)
# def server_error(e):
#     app.logger.exception('An error occurred during a request.')
#     return 'An internal error occurred.', 500
    
# if __name__ == "__main__":
#     app.run()

# # host='127.0.0.1', port=5001, debug=True)