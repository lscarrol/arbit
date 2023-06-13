import model
import selenium

def fanduel_date_parser(string):
    if game_is_today(string): #if the game is not today
        return get_formatted_date()
    elif game_is_weekday(string):
        output = get_upcoming_date_weekday(string[:3])
        return output
    elif game_is_month_day(string):
        if string[6] == ',':
            output = get_upcoming_month_date(string[:6])
        else:
            output = get_upcoming_month_date(string[:5])
        return output
    else:
        return False



