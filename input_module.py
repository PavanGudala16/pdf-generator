import inquirer
from utilities import validate_phone, validate_date
from datetime import datetime, timedelta

def collect_input():
    today = datetime.today().date()
    answers1 = {}
    answers2={}
    
    while True:
        # Initial questions, including default values from previous inputs if available
        questions = [
            inquirer.List('date_choice', message='Choose Date for Offer Letter:', 
                          choices=['Use today\'s date', 'Enter custom date'], 
                          default='Use today\'s date' if not answers1.get('offer_date') else 'Enter custom date'),
            inquirer.Text('custom_date', message='Enter custom date (dd-mm-yyyy):', 
                          default=answers1.get('custom_date', ''), 
                          validate=validate_date, ignore=lambda answers: answers['date_choice'] == 'Use today\'s date'),
            inquirer.List('Title', message='Title:', choices=['Ms', 'Mr'], default=answers1.get('Title', 'Ms')),
            inquirer.Text('Name', message='First Name of the Intern:', default=answers1.get('Name', '')),
            inquirer.Text('Surname', message='Surname of the Intern:', default=answers1.get('Surname', '')),
            inquirer.Text('Address', message='Address of the Intern:', default=answers1.get('Address', '')),
            inquirer.Text('City', message='Enter City and Pincode:', default=answers1.get('City', '')),
            inquirer.Text('Email', message='Email ID:', validate=lambda _, x: '@' in x, default=answers1.get('Email', '')),
            inquirer.Text('Contact', message='Phone Number:', validate=validate_phone, default=answers1.get('Contact', '')),
            inquirer.Text('App_date', message='Date of Application (dd-mm-yyyy):', validate=validate_date, default=answers1.get('App_date', today.strftime("%d-%m-%Y"))),
            inquirer.Text('Aadhar', message='Aadhar Number:', default=answers1.get('Aadhar', '')),
            inquirer.Text('Position', message='Position:', default=answers1.get('Position', '')),
            inquirer.List('Practice', message='Area of Work:', choices=['Enterprise Applications', 'UI/UX', 'DevOps'], default=answers1.get('Practice', 'Enterprise Applications')),
            inquirer.Text('Effort', message='Effort (in number of hours per week):', default=answers1.get('Effort', '')),
            inquirer.List('Place', message='Place of Work:', choices=['Remote', 'On-site'], default=answers1.get('Place', 'Remote')),
            inquirer.Text('Stipend', message='Stipend: ', default=answers1.get('Stipend', 'Not Applicable')),
            inquirer.Text('Start_date', message='Internship Start Date (dd-mm-yyyy):', validate=validate_date, default=answers1.get('Start_date', '')),
        ]
        
        answers1 = inquirer.prompt(questions)

        # Determine the final date for the offer letter
        if  answers1['date_choice'] == 'Use today\'s date':
            offer_date = today.strftime("%d-%m-%Y")
            #del answers1['custom_date']
        else:
            offer_date = answers1['custom_date']
          
            




        # Convert start date to a datetime object and calculate default end date
        startdate = datetime.strptime(answers1['Start_date'], "%d-%m-%Y").date()
        default_enddate_8 = startdate + timedelta(weeks=8)
        default_enddate_16 = startdate + timedelta(weeks=16)
        # Questions for the internship end date with an option for a custom date
        questions_end_date = [    
            inquirer.List('end_date_choice', message='Choose Internship End Date:', 
                          choices=[f'Use calculated end date (8 weeks) ({default_enddate_8.strftime("%d-%m-%Y")})', 
                                   f'Use calculated end date (16 weeks) ({default_enddate_16.strftime("%d-%m-%Y")})', 
                                   'Enter custom date'], 
                          default=f'Use calculated end date (8 weeks) ({default_enddate_8.strftime("%d-%m-%Y")})' 
                                  if not answers2.get('end_date') else 'Enter custom date'),
            inquirer.Text('custom_end_date', message='Enter custom end date (dd-mm-yyyy):', 
                          default=answers2.get('custom_end_date',''), 
                          validate=validate_date, 
                          ignore=lambda answers: answers['end_date_choice'] != 'Enter custom date')
        ]
        answers2 = inquirer.prompt(questions_end_date)

        # Determine the final end date for the internship
        if '8 weeks' in answers2['end_date_choice']:
            end_date = default_enddate_8.strftime("%d-%m-%Y")
        elif '16 weeks' in answers2['end_date_choice']:
            end_date = default_enddate_16.strftime("%d-%m-%Y")
        else:
            end_date = answers2['custom_end_date']



        answers={**answers1,
                  'End_date':end_date,
                  'Offer_date':offer_date }


        # Preview the data entered
        print("\nPreview of the data entered:")
        for key, value in answers.items():
            print(f"{key}: {value}")



        

        # Ask the user if they want to proceed or make changes
        proceed_question = [
            inquirer.List('proceed', message='Do you want to proceed or make changes?', choices=['Proceed', 'Make changes'])
        ]
        proceed_answer = inquirer.prompt(proceed_question)
        

        if proceed_answer['proceed'] == 'Proceed':
            del answers['custom_date']
            del answers['date_choice']
            return answers


