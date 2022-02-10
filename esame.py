#==========================================
#          Program's task. 
# Read the povided data and compute, 
# for a given lapse of years the average 
# variation in the number of passengers for each month
#===========================================

#==============================
#  Imported Libraries
#==============================

from dateutil.parser import parse
# The parser module can parse datetime strings in many more formats

#==============================
#  Exception Class
#==============================

class ExamException(Exception):
    pass
#   Class created to be able to raise exceptions

#==============================
#  CSVTimeSeriesFile Class
#==============================

class CSVTimeSeriesFile:
    '''Class that reads the time series and computes 
       the average variation for each month'''

    # Constructor method -> Creates an instance of the file to see if it can be opened.
    def __init__(self, name) -> None:

        # If name is not a string raise generate an error 
        if type(name) is not str:
            raise ExamException(f"Name is not a string, Type of parameter inserted is: {type(name)}")

        # Set the name 
        self.name = name

    # Checking if the string is a date
    def is_date(self,string) -> bool:
        
        '''Returning whatever can be interpreted as a date.'''
        try:
            parse(string)
            return True

        except ValueError:
            return False
 
    # Module that returns lists of lists and performs all the necessary checks
    def get_data(self) -> list:

        # Initialising an empty list for the values to be saved
        full_list = []

        # Trying opening the file and getting the data
        try:
            my_file = open(self.name, 'r')
        except Exception as e:

            # Raise the exception 
            raise ExamException("Can't open the file")

        # If file can be opened start reading line by line 
        for line in my_file:

            # spliting the values
            elements = line.split(',')

            # Skipping the the heading
            if elements[0] != 'date':

                # Setting the date and the value
                try:
                    date = str(elements[0])

                    # Check if the date can't be interpreted as a date
                    if not self.is_date(date):
                        continue

                    # Make the value an integer
                    value = int(elements[1])

                    # Avoiding negative values
                    if value < 0:
                        continue
                except:
                    continue

                # Checking if the timestamps are duplicated
                if len(full_list) > 0:
                    # Checking through the timestamps 
                    for j in full_list:
                        #If date is alredy in the list raise the exception 
                        prev_date = j[0]

                        if date == prev_date:
                            raise ExamException("Duplicated timestamp detected")

                # Check whether they are ordered
                    prev_date = full_list[-1][0]
                        #If prev_date follows date raise and exception
                    if date < prev_date:
                        raise ExamException("Unordered timestamp record detected")

                # Appending the date and value lists to the main list
                full_list.append([date,value])

        # Close the file
        my_file.close()

        # Check if the file is empty or not 
        if not full_list:
            raise ExamException("File is empty")

        return full_list

# Module to compute the average 
def compute_avg_monthly_difference(time_series, first_year, last_year) -> list:

    #Checking if the first and last year are strings, if not raise Exception
    if type(first_year) is not str:
        raise ExamException(f"First_year is not a string. Type of given data: {type(first_year)}")
    if type(last_year) is not str:
        raise ExamException(f"Last_year is not a string. Type of given data: {type(last_year)}")
    
    #Checking if the first and last year are digits, if not raise Exception
    if first_year.isdigit() is False:
        raise ExamException(f"First_year can't be converted to an integer, type of given data: {first_year}")
    if last_year.isdigit() is False:
        raise ExamException(f"Last_year can't be converted to an integer, type of given data: {last_year}")

    # If the years provided are the same raise exception
    if first_year == last_year:
        raise ExamException("First and last year are the same")
    if first_year >= last_year:
        raise ExamException("Il valore di last_layer e/o di first_layer è inesatto")

    # Checking if first_year is present in the data
    if(first_year < time_series[0][0][:4]):
        raise ExamException("First year not present in the file")
    
    # Checking if last_year is present in the data
    if(last_year > time_series[-1][0][:4]):
        raise ExamException("Last year not present in the file")

    # Checking if time_series is a list
    if not isinstance(time_series, list):
        raise ExamException(f"Parameter 'time_series' must be a list of lists, not {type(time_series)}")
    
    # If we are at the right index for the first year or year is already filled with something 
    #Empty list to save the final result
    data = []
    
    #Attributes
    count = 1
    #current_year position in time_series
    current_year = int(time_series[0][0][:4])

    # Create a list with all the values of a year
    for i in time_series:

    #Checking the time_series date and start counting the months form juanary which is is 01, feb 02 and so on 
        if i[0][5:8] == "01" and count >= 13:
            current_year = int(i[0][:4])
    #if count counted more than 13 months current year ended  
        if count >= 13: 
                count = 1
                current_year = int(i[0][:4])
                
        elif int(i[0][:4]) != current_year and count <= 12:
            for count in range(count,13):
                data.append(0)
            count = 1
            current_year = int(i[0][:4])
    #if current_year is higher and lower than last year
        if i[0][:4] >= first_year and i[0][:4] <= last_year:
            if int(i[0][5:8]) != count:
                for count in range(count,int(i[0][5:8])):
                    data.append(0)
                data.append(i[1])
                count = count + 2
            else:
                data.append(i[1])
                
                count = count + 1
      #if current year is higher than last year, break         
        if(current_year > int(last_year)):
            break        

    results = []

    #Every year has 12 month and if the month is non existent,are being filled with 0 and then divided by 12 getting an integer 
    years = int(len(data)/12)

    # Loop over 12 months 
    for i in range(12):
        count = 0
        sum = 0
    
    # Loop over years
        for j in range(1,years):
    
            if (data[i+(12*j)] == 0 or data[i+(12*(j-1))] == 0) and years == 2:
                sum = 0
            else: 
                if (data[i+(12*j)] == 0 or data[i+(12*(j-1))] == 0) and years > 2:
                    count += 1
                    if(years - count < 2):
                        sum = 0
                        j = years
                    else:
                        sum += 0
                # Making the sum of every years by subtracting the current mouth value of the year from the one that cames after
                else:
                    sum += data[i+(12*j)] - data[i+(12*(j-1))]
        try:
            # append the result to the list and divided it by the number of years - 1
            results.append(sum/(years-1-count))
        except:
            results.append(0)

    return results

#==============================
# Main
#==============================

time_series_file = CSVTimeSeriesFile(name="data.csv")

time_series = time_series_file.get_data()

results = compute_avg_monthly_difference(time_series,"1954","1958")

print(results)