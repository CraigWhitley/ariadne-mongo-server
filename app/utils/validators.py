import re


email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
password_regex = r"(?-i)(?=^.{8,}$)((?!.*\s)(?=.*[A-Z])(?=.*[a-z]))((?=(.*\d){1,})|(?=(.*\W){1,}))^.*$"


def validate_email(email):
    """Ensures an email address is in the correct format"""
    return bool(re.match(email_regex, email))


# Password must have at least 8 characters with at least one capital letter,
# at least one lower case letter and at least one number or special character.
def validate_password(password):
    """Ensures password meets security requirements: 1 up 1 down 1 alphanum"""
    return bool(re.match(password_regex, password))
