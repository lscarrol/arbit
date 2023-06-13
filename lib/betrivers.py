import model
import selenium

def betrivers_date_parser(string):
    string = string.upper()
    if 'TODAY' in string:
        return get_formatted_date()
    elif 'TOMORROW' in string:
        output = get_tomorrow_date()
        return output
    elif game_is_weekday(string):
        output = get_upcoming_date_weekday(string[:3])
        return output
    elif extract_date(string):
        extracted_date = extract_date(string)
        output = get_upcoming_month_date(extracted_date)
        return output
    else:
        return False

