import inquirer

def validate_phone(_, phone_str):
    try:
        # Attempt to validate the phone number format
        if not phone_str.isdigit() or len(phone_str) != 10:
            raise inquirer.errors.ValidationError("Invalid phone number format. Please enter a 10-digit numeric phone number.")
        return True  
    except Exception as e:
        raise inquirer.errors.ValidationError(f"Error validating phone number: {str(e)}")



from datetime import datetime

def validate_date(_, date_str):
    try:
        # Attempt to parse the input date string
        date_obj = datetime.strptime(date_str, '%d-%m-%Y')
        return True 
    except ValueError:
        raise inquirer.errors.ValidationError("Invalid date format. Please enter date in dd-mm-yyyy format.")
