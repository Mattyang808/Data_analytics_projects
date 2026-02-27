#!/bin/bash

#Check if there are 3 arguments 
if [[ $# -ne 3 ]]
then
    echo "Usage: tobacco_nation <csv data file>  < year | country code >  < Male | Female >"
    exit 1
fi

#Check argument 1 is a existed file with data inside
if [[ ! -s $1 ]]
then
    echo "The named input file $1 does not exist or has zero length"
    exit 1
fi

#Setting current year
current_year=$(date +%Y)

#Check if argument 2 is a 4-digits number or 3-characters-captialized code and argument 3 is Female or Male. 
#Then check if the combination of argument 2 and 3 has data in the file. 
#If does, grep and sort the data to get the line with highest value, and cut the required value, and echo required message. If not, echo error message.
if [[ $2 =~ ^[0-9][0-9][0-9][0-9]$ ]] && [[ $3 == "Female" || $3 == "Male" ]]
then
    if grep ,$2, $1 | grep -q ,$3,
    then
        data_year=$(grep ,$2, $1 | grep ,$3, | sort -t',' -k7 -n -r | head -n 1)
        percentage=$(echo "$data_year" | cut -d',' -f7)
        country=$(echo "$data_year" | cut -d',' -f4)
        country_code=$(echo "$data_year" | cut -d',' -f3)
        if [[ $2 -lt $current_year ]]
        then
            echo "The global maximum percentage of $3 tobacco users in $2 was in $country ($country_code) at $percentage"
        else
            echo "The global maximum percentage of $3 tobacco users in $2 is predicted to be in $country ($country_code) at $percentage"
            exit 0
        fi
    else
        echo "The combination of $2 and $3 does not have data in the $1"
        exit 1
    fi
elif [[ $2 =~ ^[A-Z][A-Z][A-Z]$ ]] && [[ $3 == "Female" || $3 == "Male" ]]
then
    if grep ,$2, $1 | grep -q ,$3,
    then
        data_country=$(grep ,$2, $1 | grep ,$3, | sort -t',' -k7 -n -r | head -n 1)
        percentage=$(echo "$data_country" | cut -d',' -f7)
        country=$(echo "$data_country" | cut -d',' -f4)
        year=$(echo "$data_country" | cut -d',' -f5)
        if [[ $year -lt $current_year ]]
        then
            echo "The global maximum percentage of tobacco users for $country ($2) was $percentage in $year"
        else
            echo "The global maximum percentage of tobacco users for $country ($2) is predicted to be $percentage in $year"
            exit 0
        fi   
    else
        echo "The combination of $2 and $3 does not have data in the $1"
        exit 1
    fi
else
    echo "The second argument must be a year(YYYY) or a country code(XXX), and the third argument must be Female or Male"
    exit 1
fi