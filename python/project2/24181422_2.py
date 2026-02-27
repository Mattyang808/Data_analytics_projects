
#Student name: Jianyun Yang
#Student ID: 24181422

def main(csvfile):
    try:
        with open(csvfile,'r') as file:
            # Read the rest of the file and convert each line into a list
            file_content = file.readlines()
    except Exception as e:
        print(f"Error opening file: {e}")
        return

    # Read the header line and convert it into a list of lowercase column names
    header = file_content[0].strip().split(',')
    header = [h.lower() for h in header]
    
    try:
        # Find the index of each column
        id_index = header.index('id')
        profession_index = header.index('profession')
        age_index = header.index('age')
        time_spent_hour_index = header.index('time_spent_hour')
        engagement_score_index = header.index('engagement_score')
        platform_index = header.index('platform')
        time_spent_hour_index = header.index('time_spent_hour')
        engagement_score_index = header.index('engagement_score')
        income_index = header.index('income')
    except ValueError as e:
        print(f"Error finding column: {e}")
        return

    #create a dictionary to store the data of student and non-student
    op1_dict_student  = {}
    op1_dict_nonstudent  = {}

    # Create a set to store the user IDs that we've seen so far
    seen_ids = set()

    #find the student and non-student in the file and store id as key, and store age, time_spent_hour, engagement_score in list as value
    for i in range(1, len(file_content)):
        row = file_content[i].strip().split(',')
        row = [r.lower() for r in row]

        # Check if we've seen this user ID before
        if row[id_index] in seen_ids:
            continue

        # Add the user ID to the set of seen IDs
        seen_ids.add(row[id_index])

        # Check for missing or invalid data
        if not row[id_index].isalnum():
            continue
        if not row[age_index].isdigit() or int(row[age_index]) < 0:
            continue
        if not row[time_spent_hour_index].isdigit() or int(row[time_spent_hour_index]) < 0:
            continue
        if not row[engagement_score_index].replace('.', '', 1).isdigit():
            continue

        if row[profession_index] == 'student':
            op1_dict_student[row[id_index]] = [int(row[age_index]), int(row[time_spent_hour_index]), float(row[engagement_score_index])]
        else:
            op1_dict_nonstudent[row[id_index]] = [int(row[age_index]), int(row[time_spent_hour_index]), float(row[engagement_score_index].lower())]

    OP1 = [op1_dict_student, op1_dict_nonstudent]

    #create a dictionary to store the data of each platform
    op2_dict = {}

    #find the data needed of each platform in the file and calculate engagement_time
    for i in range(1, len(file_content)):
        row = file_content[i].strip().split(',')
        row = [r.lower() for r in row]
        platform = row[platform_index].lower()
        time_spent_hour = float(row[time_spent_hour_index])
        engagement_score = float(row[engagement_score_index])
        engagement_time = (time_spent_hour * engagement_score) / 100

        #if the platform is not in the dictionary, add the platform as key and engagement_time as value. If the platform is already in the dictionary, append the engagement_time to the value list
        if platform not in op2_dict:
            op2_dict[platform] = [engagement_time]
        else:
            op2_dict[platform].append(engagement_time)

    #calculate the total, average and standard deviation of engagement_time for each platform
    for platform, engagement_time in op2_dict.items():
        total = round(sum(engagement_time), 4)
        average = round(total / len(engagement_time), 4)
        variance = sum((x - average) ** 2 for x in engagement_time) / (len(engagement_time)-1)
        std_dev = round(variance ** 0.5, 4)
        op2_dict[platform] = [total, average, std_dev]

    OP2 = op2_dict

    #ceate a dictionary to store the age and income of student and non-student
    op3_dict = {'student': {'age':[], 'income':[]}, 'nonstudent': {'age':[], 'income':[]}}

    #find the age and income of student and non-student in the file and store them in the dictionary
    for i in range(1, len(file_content)):
        row = file_content[i].strip().split(',')
        row = [r.lower() for r in row]
        if row[profession_index].lower() == 'student':
            op3_dict['student']['age'].append(row[age_index])
            op3_dict['student']['income'].append(row[income_index])
        else:
            op3_dict['nonstudent']['age'].append(row[age_index])
            op3_dict['nonstudent']['income'].append(row[income_index])

    #initialize the sum of age*income, sum of square of age, sum of square of income
    sum_ageincome_student = 0
    sum_square_age_student = 0
    sum_square_income_student = 0
    sum_ageincome_nonstudent = 0
    sum_square_age_nonstudent = 0
    sum_square_income_nonstudent = 0

    #calculate the cosine similarity scores for student
    for age, income in zip(op3_dict['student']['age'], op3_dict['student']['income']):
        sum_ageincome_student += float(age) * float(income)
        sum_square_age_student += float(age) ** 2
        sum_square_income_student += float(income) ** 2

    sqrt_sum_square_age_student = sum_square_age_student ** 0.5
    sqrt_sum_square_income_student = sum_square_income_student ** 0.5

    result_student = sum_ageincome_student / (sqrt_sum_square_age_student * sqrt_sum_square_income_student)

    #calculate the cosine similarity scores for non-student
    for age, income in zip(op3_dict['nonstudent']['age'], op3_dict['nonstudent']['income']):
        sum_ageincome_nonstudent += float(age) * float(income)
        sum_square_age_nonstudent += float(age) ** 2
        sum_square_income_nonstudent += float(income) ** 2

    sqrt_sum_square_age_nonstudent = sum_square_age_nonstudent ** 0.5
    sqrt_sum_square_income_nonstudent = sum_square_income_nonstudent ** 0.5

    result_nonstudent = sum_ageincome_nonstudent / (sqrt_sum_square_age_nonstudent * sqrt_sum_square_income_nonstudent)

    #round the result to 4 decimal places
    OP3 = [round(result_student, 4), round(result_nonstudent, 4)]

    #create a dictionary to store the data of each platform
    op4_dict = {'student':[], 'nonstudent':[]}

    #find the time_spent_hour and engagement_score of student and nonstudent in the file
    for i in range(1, len(file_content)):
        row = file_content[i].strip().split(',')
        row = [r.lower() for r in row]
        if row[profession_index] == 'student':
            time_spent_hour = float(row[time_spent_hour_index])
            engagement_score = float(row[engagement_score_index])
            engagement_time = (time_spent_hour * engagement_score) / 100
            op4_dict['student'].append(engagement_time)
        else:
            time_spent_hour = float(row[time_spent_hour_index])
            engagement_score = float(row[engagement_score_index])
            engagement_time = (time_spent_hour * engagement_score) / 100
            op4_dict['nonstudent'].append(engagement_time)
    

    #calculate the total, average and standard deviation of engagement_time for student and nonstudent
    total_student = sum(op4_dict['student'])
    average_student = total_student / len(op4_dict['student'])
    variance_student = sum((x - average_student) ** 2 for x in op4_dict['student']) / (len(op4_dict['student'])-1)
    std_dev_student = variance_student ** 0.5

    total_nonstudent = sum(op4_dict['nonstudent'])
    average_nonstudent = total_nonstudent / len(op4_dict['nonstudent'])
    variance_nonstudent = sum((x - average_nonstudent) ** 2 for x in op4_dict['nonstudent']) / (len(op4_dict['nonstudent'])-1)
    std_dev_nonstudent = variance_nonstudent ** 0.5

    pooled_std_dev = (((len(op4_dict['student'])-1) * (std_dev_student ** 2) + (len(op4_dict['nonstudent'])-1) * (std_dev_nonstudent ** 2)) / (len(op4_dict['student']) + len(op4_dict['nonstudent']) - 2)) ** 0.5
    d = (average_student - average_nonstudent) / pooled_std_dev
    OP4 = round(d, 4)

    return OP1, OP2, OP3, OP4



OP1, OP2, OP3,OP4 = main('social_media.csv')
print(len(OP1[0]))
print(OP1[0]['95q155'])
print(len(OP2))
print(OP3)
print(OP4)



