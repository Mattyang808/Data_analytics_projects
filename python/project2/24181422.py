def main(csvfile):
    # open the file and read the content of the file and and convert each line into a list
    try:
        with open(csvfile, 'r') as file:
            file_content = file.readlines()
            if len(file_content) < 2:
                print("File is empty or contains only headers")
                return
    except:
        print("Can not open file")
        return

    # Read the header line and convert it into a list of lowercase column names
    header = file_content[0].strip().split(',')
    header = [h.lower() for h in header]

    # Find the index of each column
    try:
        id_index = header.index('id')
        profession_index = header.index('profession')
        age_index = header.index('age')
        time_spent_hour_index = header.index('time_spent_hour')
        engagement_score_index = header.index('engagement_score')
        platform_index = header.index('platform')
        income_index = header.index('income')
    except:
        print("Some columns are missing in the file for calculation. Please check the file and try again.")
        return

    # Create a dictionary to store all data
    data = {
        'header': header,
        'file_content': file_content,
        'categories_index': {
            'id': id_index,
            'profession': profession_index,
            'age': age_index,
            'time_spent_hour': time_spent_hour_index,
            'engagement_score': engagement_score_index,
            'platform': platform_index,
            'income': income_index
        }
    }

    #Call the operation functions and return the results
    OP1_result = OP1(data)
    OP2_result = OP2(data)
    OP3_result = OP3(data)
    OP4_result = OP4(data)

    return OP1_result, OP2_result, OP3_result, OP4_result


def OP1(data):
    # Extract the header, file content and categories index from the data
    header, file_content, categories_index = data['header'], data['file_content'], data['categories_index']

    # Create two dictionaries to store the data of students and non-students and one set count the seen ids
    op1_dict_student = {}
    op1_dict_nonstudent = {}
    seen_ids = set()

    # Iterate through the file content and extract the required data
    for row in file_content[1:]:
        row = row.strip().split(',')
        row = [r.lower() for r in row]

        # Take boundery conditions into account
        if len(row) < len(header):
            continue

        if row[categories_index['id']] in seen_ids:
            continue

        seen_ids.add(row[categories_index['id']])

        if not row[categories_index['id']].isalnum():
            continue
        if not row[categories_index['age']].isdigit() or float(row[categories_index['age']]) < 0:
            continue
        if not row[categories_index['time_spent_hour']].isdigit() or float(row[categories_index['time_spent_hour']]) < 0:
            continue
        try:
            engagement_score = float(row[categories_index['engagement_score']])
            if engagement_score < 0:
                continue
        except:
            continue

        # Store the data needed based on the profession
        if row[categories_index['profession']] == 'student':
            op1_dict_student[row[categories_index['id']]] = [int(float(row[categories_index['age']])), int(float(row[categories_index['time_spent_hour']])), engagement_score]
        else:
            op1_dict_nonstudent[row[categories_index['id']]] = [int(float(row[categories_index['age']])), int(float(row[categories_index['time_spent_hour']])), engagement_score]

    return [op1_dict_student, op1_dict_nonstudent]


def OP2(data):
    # Extract the header, file content and categories index from the data
    header, file_content, categories_index = data['header'], data['file_content'], data['categories_index']
    # Create a dictionary to store the data of each platform and one set count the seen ids
    op2_dict = {}
    seen_ids = set()

    # Iterate through the file content and extract the required data
    for row in file_content[1:]:
        row = row.strip().split(',')
        row = [r.lower() for r in row]
        platform = row[categories_index['platform']].lower()

        #take boundery conditions into account
        if len(row) < len(header):
            continue

        if row[categories_index['id']] in seen_ids:
            continue

        seen_ids.add(row[categories_index['id']])
        
        try:
            time_spent_hour = float(row[categories_index['time_spent_hour']])
            engagement_score = float(row[categories_index['engagement_score']])
            if time_spent_hour < 0 or engagement_score < 0:
                continue
        except:
            continue
        
        # Calculate the engagement time and store it based on the platform
        engagement_time = (time_spent_hour * engagement_score) / 100

        if platform not in op2_dict:
            op2_dict[platform] = [engagement_time]
        else:
            op2_dict[platform].append(engagement_time)

    # Calculate the total, average and standard deviation of engagement times for each platform
    for platform, engagement_times in op2_dict.items():
        total = round(sum(engagement_times), 4)

        if len(engagement_times) != 0:
            average = round(total / len(engagement_times), 4)
        else:
            average = 0.0

        if len(engagement_times) != 1:
            variance = sum((x - average) ** 2 for x in engagement_times) / (len(engagement_times) - 1)
        else:
            variance = 0.0

        if variance > 0:
            std_dev = round(variance ** 0.5, 4)
        else:
            std_dev = 0.0

        op2_dict[platform] = [total, average, std_dev]

    return op2_dict


def OP3(data):
    # Extract the header, file content and categories index from the data
    header, file_content, categories_index = data['header'], data['file_content'], data['categories_index']
    # Create a dictionary to store the data of students and non-students and one set count the seen ids
    op3_dict = {'student': {'age': [], 'income': []}, 'nonstudent': {'age': [], 'income': []}}
    seen_ids = set()

    # Iterate through the file content and extract the required data
    for row in file_content[1:]:
        row = row.strip().split(',')
        row = [r.lower() for r in row]

        # Take boundery conditions into account
        if len(row) < len(header):
            continue
        
        if row[categories_index['id']] in seen_ids:
            continue

        seen_ids.add(row[categories_index['id']])
        
        try:
            age = float(row[categories_index['age']])
            income = float(row[categories_index['income']])
            if age < 0 or income < 0:
                continue
        except:
            continue

        # Store the data needed based on the profession
        if row[categories_index['profession']] == 'student':
            op3_dict['student']['age'].append(age)
            op3_dict['student']['income'].append(income)
        else:
            op3_dict['nonstudent']['age'].append(age)
            op3_dict['nonstudent']['income'].append(income)

    # define the calculation of the cosine similarity for students and non-students
    def calculate_cosine_similarity(age_list, income_list):
        if not age_list or not income_list:
            return 0.0
        
        sum_ageincome = sum(a * i for a, i in zip(age_list, income_list))
        sum_square_age = sum(a ** 2 for a in age_list)
        sum_square_income = sum(i ** 2 for i in income_list)

        if sum_square_age > 0 and sum_square_income > 0:
            cosine_similarity = sum_ageincome / ((sum_square_age ** 0.5) * (sum_square_income ** 0.5))
        else:
            cosine_similarity = 0.0

        return cosine_similarity

    # Call the function to calculate the cosine similarity
    result_student = calculate_cosine_similarity(op3_dict['student']['age'], op3_dict['student']['income'])
    result_nonstudent = calculate_cosine_similarity(op3_dict['nonstudent']['age'], op3_dict['nonstudent']['income'])

    return [round(result_student, 4), round(result_nonstudent, 4)]


def OP4(data):
    # Extract the header, file content and categories index from the data
    header, file_content, categories_index = data['header'], data['file_content'], data['categories_index']
    # Create a dictionary to store the data of students and non-students and one set count the seen ids
    op4_dict = {'student': [], 'nonstudent': []}
    seen_ids = set()

    # Iterate through the file content and extract the required data
    for row in file_content[1:]:
        row = row.strip().split(',')
        row = [r.lower() for r in row]

        # Take boundery conditions into account
        if len(row) < len(header):
            continue

        if row[categories_index['id']] in seen_ids:
            continue

        seen_ids.add(row[categories_index['id']])
        
        try:
            time_spent_hour = float(row[categories_index['time_spent_hour']])
            engagement_score = float(row[categories_index['engagement_score']])
            if time_spent_hour < 0 or engagement_score < 0:
                continue
        except:
            continue

        # Calculate the engagement time and store it based on the profession
        engagement_time = (time_spent_hour * engagement_score) / 100

        if row[categories_index['profession']] == 'student':
            op4_dict['student'].append(engagement_time)
        else:
            op4_dict['nonstudent'].append(engagement_time)

    # define the calculation of the cohen's d
    def calculate_cohen(engagement_times):
        total = sum(engagement_times)

        if len(engagement_times) != 0:
            average = total / len(engagement_times)
        else:
            average = 0.0

        if len(engagement_times) != 1:
            variance = sum((x - average) ** 2 for x in engagement_times) / (len(engagement_times) - 1)
        else:
            variance = 0.0

        if variance > 0:
            std_dev = variance ** 0.5
        else:
            std_dev = 0.0

        return total, average, std_dev

    # Call the function to calculate the cohen's d
    total_student, average_student, std_dev_student = calculate_cohen(op4_dict['student'])
    total_nonstudent, average_nonstudent, std_dev_nonstudent = calculate_cohen(op4_dict['nonstudent'])

    try:
        pooled_std_dev = (((len(op4_dict['student']) - 1) * (std_dev_student ** 2) +
                        (len(op4_dict['nonstudent']) - 1) * (std_dev_nonstudent ** 2)) /
                        (len(op4_dict['student']) + len(op4_dict['nonstudent']) - 2)) ** 0.5
        d = (average_student - average_nonstudent) / pooled_std_dev
    except:
        d = 0.0

    return round(d, 4)

OP1, OP2, OP3, OP4 = main('invalid_data.csv')
print(len(OP1[0]))
print(OP1[0]['1'])
print(len(OP2))
print(OP3)
print(OP4)
