import re
from datetime import date, timedelta, datetime

def extract_date(input_string): #Extracts Weekday Month Day from date
    pattern = r'[A-Za-z]{3}\s[A-Za-z]{3}\s\d{1,2}'
    match = re.search(pattern, input_string)
    if match:
        return match.group(0)[4:]
    else:
        return None

def get_tomorrow_date():
    today = datetime.today()
    tomorrow = today + timedelta(days=1)
    formatted_date = tomorrow.strftime("%m/%d/%y")
    return formatted_date

def get_formatted_date(): #returnstodays date, formatted MM/DD/YY
    today = datetime.today()
    formatted_date = today.strftime("%m/%d/%y")
    return formatted_date

def get_upcoming_date_weekday(weekday):
    weekday_number = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN'].index(weekday.upper())
    today = datetime.today().date()
    days_ahead = (7 + weekday_number - today.weekday()) % 7
    upcoming_date = today + timedelta(days=days_ahead)
    formatted_date = upcoming_date.strftime("%m/%d/%y")
    return formatted_date

def get_upcoming_month_date(month_date):
    # Get the current year
    current_year = datetime.now().year

    # Parse the month and day from the input string
    month, day = month_date.split()

    # Convert month name to month number
    month_number = datetime.strptime(month, '%b').month

    # Format the date as "MM/DD/YY"
    formatted_date = f'{month_number:02d}/{int(day):02d}/{current_year % 100:02d}'

    return formatted_date


def game_is_today(string): #returns True if game is today, else false
    pattern = r'[A-Z]{3} '  # Regex pattern for 3 consecutive uppercase letters followed by a space
    match = re.search(pattern, string)
    if match:
        return False
    else:
        return True

def game_is_weekday(string):
    pattern = r'[A-Z]{3} \d{1,2}:'  # Regex pattern for 3 consecutive uppercase letters, a space, a number, and a colon
    match = re.search(pattern, string)
    if match:
        return True
    else:
        return False 

def game_is_month_day(string): #True if game's date contains month and day (ex: "SEP 10"), else False
    pattern = r'[A-Z]{3} \d{1,2},'  # Regex pattern for 3 consecutive uppercase letters, a space, a number, and a comma
    match = re.search(pattern, string)
    if match:
        return True
    else:
        return False



def _date_parser(string):
    if 'Today' in string:
        return get_formatted_date()
    elif 'Tomorrow' in string:
        output = get_tomorrow_date()
        return output
    
    elif extract_date(string):
        extracted_date = extract_date(string)
        output = get_upcoming_month_date(extracted_date)
        return output
    else:
        return False

def _is_ml_odds(string): #determines whether odds are moneyline
    if ('.' in string) or ('U' in string) or ('O' in string):
        return False
    return True

def dictionarify(lst):
    result = {}

    for item in lst:
        key = item[0]
        team1 = item[1]
        odds1 = item[2]
        team2 = item[3]
        odds2 = item[4]

        if key not in result:
            result[key] = {}
        
        key_tuple = [team1, team2]
        key_tuple.sort()
        key_tuple = tuple(key_tuple)
        result[key][key_tuple] = {
            team1: odds1,
            team2: odds2
        }
    return result