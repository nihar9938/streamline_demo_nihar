from datetime import date

# List of holiday dates (assuming they are in the format YYYY-MM-DD)
holiday_dates = ['2024-01-01', '2024-05-27', '2024-07-04', '2024-09-02', '2024-11-28', '2024-12-25']

def is_holiday(check_date):
    return str(check_date) in holiday_dates

# Example usage
date_to_check = date(2024, 7, 4)
if is_holiday(date_to_check):
    print(f"{date_to_check} is a holiday.")
else:
    print(f"{date_to_check} is not a holiday.")
