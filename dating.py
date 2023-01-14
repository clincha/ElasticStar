from datetime import datetime

date_string = "12/11/2018"
date_string_object = datetime.strptime(date_string, "%d/%m/%Y")

print(date_string_object)