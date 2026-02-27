#Student name: Jianyun Yang
#Student ID: 24181422

def main(csvfile, age_group, country):
    #Open csv file in read mode
    #Read the each line of file and convert it into a list except headline
    with open(csvfile,'r') as file:
        file_content = file.readlines()[1:]
        
        #Create empty lists and dicts to store matched data for following operations
        filtered_list_op1 = []
        filtered_list_op2 = []
        filtered_dict_op3 = {'timespentall':[], 'incomeall':[],'rural':[], 'urban':[], 'sub_urban':[]}
        sums_op3 = {'timespentall':0.0, 'incomeall':0.0, 'rural':0.0, 'urban':0.0, 'sub_urban':0.0}
        filtered_dict_op4 = {}

        #Iterate through each line of file content and split the line by comma and strip '\n' from each line
        #extract headlines and convert values with characters to lower case
        for line in file_content:
            line_value = line.strip().split(',')
            country_name = line_value[6].lower()
            indebt_status = line_value[10].lower()
            student_ID = line_value[0]
            income_value = line_value[9]
            age_value = line_value[1]
            time_spent_hour = line_value[3]
            demographic = line_value[7].lower()
            platform_name = line_value[4].lower()

            #Find the data that matches requiremnts for operation 1 and append them in the list1
            if country_name == country.lower() and indebt_status == "true" and int(time_spent_hour) > 7:
                filtered_value1 = [student_ID, round(float(income_value), 4)]
                filtered_list_op1.append(filtered_value1)

            #Find the data that matches requiremnts for operation 2 and append them in the list2
            if int(age_group[0]) <= int(age_value) <= int(age_group[1]):
                    filtered_value2 = country_name
                    if filtered_value2 not in filtered_list_op2:
                        filtered_list_op2.append(filtered_value2)    

            #Find the data that matches requiremnts for operation3 and append them in the dict3 and addon in sum dict
            if int(age_group[0]) <= int(age_value) <= int(age_group[1]):
                filtered_dict_op3['timespentall'].append(time_spent_hour)
                filtered_dict_op3['incomeall'].append(income_value)
                sums_op3['timespentall'] += float(time_spent_hour)
                sums_op3['incomeall'] += float(income_value)
                filtered_dict_op3[demographic].append(time_spent_hour)
                sums_op3[demographic] += float(time_spent_hour)

            #Find the data that matches requiremnts for operation4 and append them in the dict4
            #Extract platform name and check if in dict. If not, then create a new key with a empty list as value and append age & income in this value list
            if platform_name not in filtered_dict_op4:
                filtered_dict_op4[platform_name] = []
            filtered_dict_op4[platform_name].append([age_value, income_value])

        #Define the first operation function
        #Use bubble sort method to sort the filtered list by first element(student ID) and return it
        def operation1(filtered_list_op1):
            for i in range(len(filtered_list_op1)):
                 for j in range(len(filtered_list_op1) - 1):
                    if int(filtered_list_op1[j][0]) > int(filtered_list_op1[j + 1][0]):
                        filtered_list_op1[j], filtered_list_op1[j + 1] = filtered_list_op1[j + 1], filtered_list_op1[j]
            return filtered_list_op1
        
        #Define the second operation function
        #Sort the filtered list by alphabetically and return it  
        def operation2(filtered_list_op2):
            filtered_list_op2 = sorted(filtered_list_op2)
            return filtered_list_op2
        
        #Define the third operation function
        #Calculate the standard deviation and take boundary condition into consideration to avoid crash
        def operation3(filtered_dict_op3, sums_op3):
            timespent_avg = round(sums_op3['timespentall']/ len(filtered_dict_op3['timespentall']), 4)
            income_avg = sums_op3['incomeall'] / len(filtered_dict_op3['incomeall'])

            squared_difference = 0.0
            for x in filtered_dict_op3['incomeall']:            
                squared_difference += (float(x) - income_avg) ** 2
            
            if len(filtered_dict_op3['timespentall']) > 1:
                variance = squared_difference / (len(filtered_dict_op3['timespentall']) - 1)
            else:
                print("Error: Division by zero in variance calculation.")
                variance = 0.0
            
            standard_dev = round(variance ** 0.5, 4)
            
            if len(filtered_dict_op3['rural']) != 0:
                timespent_rural_avg = sums_op3['rural'] / len(filtered_dict_op3['rural'])
            else:
                print("Error: No timespent data in rural area.")
                timespent_rural_avg = 0.0
            
            if len(filtered_dict_op3['urban']) != 0:
                timespent_urban_avg = sums_op3['urban'] / len(filtered_dict_op3['urban'])
            else:
                print("Error: No timespent data in urban area.")
                timespent_urban_avg = 0.0
            
            if len(filtered_dict_op3['sub_urban']) != 0:
                timespent_suburban_avg = sums_op3['sub_urban'] / len(filtered_dict_op3['sub_urban'])
            else:
                print("Error: No timespent data in sub_urban area.")
                timespent_suburban_avg = 0.0
            
            #find the minimum timespent average from sorted dict and sorted it alphabetically and return the first one
            timespent_avgs_dict = {'rural:':timespent_rural_avg, 'sub_urban:':timespent_suburban_avg, 'urban:':timespent_urban_avg}
            
            timespent_avgs_list = []
            for values in timespent_avgs_dict.values():
                timespent_avgs_list.append(values)
            timespent_avgmin = min(timespent_avgs_list)

            timespent_avgmin_demographic = []
            for demographic, timespent in timespent_avgs_dict.items():
                if timespent == timespent_avgmin:
                    timespent_avgmin_demographic.append(demographic)
            timespent_avgmin_demographic = (sorted(timespent_avgmin_demographic))[0].strip(':')
            
            return [timespent_avg, standard_dev, timespent_avgmin_demographic]

        #Define the fourth operation function
        #Iterate through each platform and get the number of users in each platform and find maximum
        def operation4(filtered_dict_op4):
            platform_users = []
            for values in filtered_dict_op4.values():
                platform_users.append(len(values))
            platform_users_maxnum = max(platform_users)
            
            #Iterate through each key and its value in dict. Find the platform that got maximum users and sorted alphabetically and get the first one
            maxusers_platforms = []
            for platform, values in filtered_dict_op4.items():
                if len(values) == platform_users_maxnum:
                    maxusers_platforms.append(platform)
            maxusers_platformbyalpha = (sorted(maxusers_platforms))[0]
            
            #Iterate through the value list of the platform with maximum users and calculate the age and income sums, averages and diffs
            users_age_sum = 0.0
            users_income_sum = 0.0
            for age, income in filtered_dict_op4[maxusers_platformbyalpha]:
                users_age_sum += float(age)
                users_income_sum += float(income)    
            users_age_avg = users_age_sum / len(filtered_dict_op4[maxusers_platformbyalpha])
            users_income_avg = users_income_sum / len(filtered_dict_op4[maxusers_platformbyalpha])

            ageincome_diff = 0.0
            suqared_age_diff = 0.0
            squared_income_diff = 0.0
            for age, income in filtered_dict_op4[maxusers_platformbyalpha]:
                ageincome_diff += (float(age)-users_age_avg) * (float(income)-users_income_avg)
                suqared_age_diff += (float(age)-users_age_avg) ** 2
                squared_income_diff += (float(income)-users_income_avg) ** 2
            
            #Caluculate the correlation coefficient and take boundary condition into consideration to avoid crash
            if suqared_age_diff * squared_income_diff > 0:
                r = ageincome_diff / ((suqared_age_diff * squared_income_diff) ** 0.5)
                return round(r, 4)
            else:
                print("Error: Division by zero in correlation coefficient calculation.")
                return 0.0

    OP1 = operation1(filtered_list_op1)
    OP2 = operation2(filtered_list_op2)
    OP3 = operation3(filtered_dict_op3, sums_op3)
    OP4 = operation4(filtered_dict_op4)

    return OP1, OP2, OP3, OP4