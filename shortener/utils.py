from random import choices
import string


def generate_short_url():
    string_list = choices(
        string.ascii_uppercase + string.ascii_lowercase + string.digits + "".join([str(i) for i in range(10)]), k=5
    )
    new_link = "".join(string_list)
    return new_link
