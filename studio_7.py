import csv

class Participant:
    def __init__(self, age, industry, salary, currency, country, experience, education):
        self.age = age
        self.industry = industry
        self.salary = salary
        self.currency = currency
        self.country = country
        self.experience = experience
        self.education = education

def main():
    rows = load_csv_file("survey.csv")
    participants = create_participants(rows)
    print("Answer #1: ", len(participants))

    industry_groups = group_by_attribute(participants, "industry")
    print(return_average_salary(industry_groups))

def return_average_salary(groups_list):
    average_salaries = []
    for key, group in groups_list.items():
        avg = int(sum([x.salary for x in group]) / len(group))
        average_salaries.append([key, avg])

    return average_salaries
def group_by_attribute(object_list, property):
    groups = {}
    values = get_value_by_property(object_list, property)

    for value in values:
        if value == '':
            continue
        filtered_list = filter_by_value(object_list, property, value)  
        if len(filtered_list) >= 10:
            groups[value] = filtered_list
    
    
    return groups

def filter_by_value(object_list, property, value):
    return list(filter(lambda x: getattr(x, property) == value, object_list))
def get_value_by_property(object_list, property):
    values = []
    for obj in object_list:
        values.append(getattr(obj, property))

    return list(set(values))

def create_participants(rows):
    participants = []
    for row in rows[1:]:
        age = row[1]
        industry = row[2]
        salary = int(row[5].replace(",",""))
        currency = row[7]
        country = row[10]
        experience = row[13]
        education = row[15]
        if(currency == "USD"):
            participants.append(Participant(age, industry, salary, currency, country, experience, education))
    return participants

def load_csv_file(filename):
    rows = []
    with open(filename, "r", encoding="iso-8859-1") as f:
        reader_obj = csv.reader(f)
        for row in reader_obj:
            rows.append(row)
    
    return rows
#--------------------------
if __name__ == "__main__":
    main()