# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 12:14:49 2017

@author: u6049237 -0487201989
"""
    
WeatherStations = []
WetOrDry = []
climatePrint = []
DifferenceValue = []
DifferenceUnit = []
TimePeriod = []
TimePeriodPrint = []
Occurences = []
monthList = ["jan", "feb", "mar", "apr", "may", "jun",
               "jul", "aug", "sep", "oct", "nov", "dec",
               "january", "feburary", "march", "april",
               "may", "june", "july", "august", "september",
               "october", "november", "december"]


# For Miles' File-----------------------
# general
def avgRainAccrossDays(data):
    '''
    This is one way to deal with invalid/missing data.
    It basically takes in a list of data, and finds all rainfall values which,
    span over multiple days. It then averages this data accross those days.
    This was made in an attempt to prevent the removal of important data.
    
    **Note, there is another function in miles.py which checks for invalid
      years/months. Both this and the invalid checker are used and put through
      methods a and b. 
      Then another function (returnMX) chooses which of those 4 sets of data 
      to keep.**
    '''
    myDays = data
    
    # index represents current day
    index = 0
    while index < len(data):
        daysSpanned = int(myDays[index][6])
        daysCounter = daysSpanned
        #if the period which it was measured is greater than 1
        if daysSpanned > 1:
            # store the rainfall accross those days, and find the avg
            spannedRain = float(myDays[index][5])
            avgRain = spannedRain / daysSpanned
        
            # for everyday which accumilated to the spannedRainfall value
            # set its rainfall to the avg
            # and its period for collecting rainfall to 1 day
            while daysCounter > 0:
                myDays[index - (daysCounter-1)][5] = avgRain
                myDays[index - (daysCounter-1)][6] = 1
                daysCounter -= 1
            
        index += 1
    
    return myDays

# For opening files
def convertToFileName(Name):
    '''
    For the program to be user friendly, it takes the user input for weather
    stations on a name basis, and not a filename basis. 
    So this takes in the state name, and returns the path to the relevant 
    weather file.
    '''
    if Name == "canberra":
        return "Rainfall_Canberra_070247.csv"
    if Name == "sydney":
        return "Rainfall_Sydney_066062.csv"
    if Name == "queanbeyan":
        return "Rainfall_Queanbeyan_070072.csv"
    return Name

def convertFileNameBack(Name):
    '''
    This does the opposite to "convertToFileName". This is moreso for when the 
    program needs to print out the name of the State based on weather station.
    '''
    if Name == "Rainfall_Canberra_070247.csv":
        return "Canberra"
    if Name == "Rainfall_Sydney_066062.csv":
        return "Sydney"
    if Name == "Rainfall_Queanbeyan_070072.csv":
        return "Queanbeyan"
    return Name
    
def convertAllStationsToFileName(stationList):
    '''
    This takes all the weather stations the user wanted to get data from, and
    does the conversion to file path name.
    '''
    stations = stationList[:]
    updated = []
    for station in stations:
        updated.append(convertToFileName(station))
    
    return updated

# for choosing which threshold togo with
def conservativeValue(tup, WD):
    '''
    This is basically a function to go through all the dates in which the:
        "once in a X days/months/years"
    happened, and returns the threshold value basically.
    '''
    if not type(tup) == type(None):
        Xist = float(tup[0][0][-1])
        for date in tup:
            if ((float(date[0][-1]) <= Xist) and (WD == "wet")) or\
            ((float(date[0][-1]) >= Xist) and (not WD == "wet")):
                Xist = float(date[0][-1])
        return Xist
    
def returnMX(mList, WD):
    '''
    This runs the above function to find the threshold value for all 4 methods
    (removal of invalid A and B, avg A and B) and then returns the one with the
    smallest set of dates.
    Or in other words, if looking for wettest period, it'd return the method
    which gave the highest threshold, and for driest lowest. 
    '''
    consList = []
    newList = []
    for m in mList:
        if not type(m) == type(None):
            consList.append(conservativeValue(m, WD))
            newList.append(m)
    
    if WD == "wet":
        return newList[consList.index(min(consList))]
    return newList[consList.index(max(consList))]

# for printing the result
def printOutPutNeatly(data, WS, WD, DV, DU, TP, O):  
    '''
    This function basically after aggregating gets all the values after
    aggregating and prints out the answer for the user :)
    '''
    RFvalue = conservativeValue(data, WD)
    
    dates = []
    for date in data:
        dates.append(date[0][0:-1])
    
    datesToPrint =  ""

    for date in dates:
        for dateInfo in date:
            datesToPrint += dateInfo
            if not dateInfo == date[-1]:
                datesToPrint += "/"
        datesToPrint += ", "
        
    print("A once in "+ str(DV) +" " + DU +" "+ setClimatePrint(WD) +" "+
          setTimePeriodPrint(TP) + "(for " + convertFileNameBack(WS) +") is " +
          str(RFvalue) + "mm, and this happened on " +O+ ":\n" + datesToPrint)
            
# General Functions----------------------
def isValid(listOfValid, CheckThis):
    '''
    This function gets called a lot.
    It takes a list of valid inputs, as well as the user input, and returns
    True if the user input is a valid input.
    '''
    for item in listOfValid:
        if CheckThis.lower() == item:
            return True
    return False

def printAll():
    '''
    This is purely for debugging.
    It prints out all globals
    '''
    print("Weather Staions: ", WeatherStations)
    print("Wet or Dry: ", WetOrDry )
    print("Difference Value: ", DifferenceValue)
    print("Difference Unit: ", DifferenceUnit)
    print("Time Period: ", TimePeriod)
    print("Occurences: ", Occurences)

    
# Question 1 Functions----------------------
def validAmountOfStations(number):
    if len(number) > 1:
        return False
    for character in number:
        if not ord("1") <= ord(character) <= ord("3"):
            return False
    return True

def validStation(station):
    stations = ["canberra", "sydney", "queanbeyan"]
    return  isValid(stations, station)

def addStation():
    tempStation = input("Please enter in the Name of the Weather station you \
wish to add: ")
    if validStation(tempStation):
        if not tempStation in WeatherStations:
            WeatherStations.append(tempStation.lower())
        else:
            print("Although that is an actual station, you've already added \
that one.")
            addStation()
    else:
        print("Sorry, I don't think '"+ tempStation+ "' is a valid station :(\
n\You can choose 'Canberra', 'Queanbeyan', or 'Sydney'")
        addStation()


# Question 2 Functions----------------------
def validClimate(climate):
    climates = ["wet", "dry"]
    return isValid(climates, climate)

def setClimatePrint(climate):
    if climate == "wet":
        return "rainfall"
    return "driest period"

# Question 3 Functions----------------------
def validDiffValue(value):
    if len(value) > 1:
        for character in value:
            if not ord("0") <= ord(character) <= ord("9"):
                return False
    else:
        if value[0] == "0":
            return False
    return True

# Question 4 Functions----------------------
def convertDigitToMonthName(digit):
    names = monthList[:]
    name = names[digit+11].title()
    return name

def digitToString(m):
    month = str(m)
    if len(month) == 1:
        month = "0"+str(m)
        
    print("this month number is:", month)
    return month
        
def convertMonthToDigit(month):
    months = monthList[:]
    index = months.index(month)
    monthNumber = index%12 + 1
    if monthNumber == 0:
        monthNumber = 12

    return monthNumber

def validTP_Unit(value):
    B1units = monthList[:]
    B2units = ["day", "month", "year"]
             
    if isValid(B1units, value):
        return [True, "B1units"]
    if isValid(B2units, value):
        return [True, "B2units"]
    if validDiffValue(value):
        if 0 <= int(value) <= 12:
            return [True, "B1unitsDigit"]
    return [False]

def setTimePeriodPrint(TP):
    toPrint = ""
    if len(TP) > 1:
        toPrint += "for the month of " + convertDigitToMonthName(int(TP[1]))
    else:
        toPrint += "in a single " + TP[0]
    
    return toPrint
# Question 5 Functions----------------------
def validOcc(occ):
    units = ["dates", "years"]
    return isValid(units, occ)

# Question 6 Functions----------------------
def answerToBool(answer):
    if "y" in answer.lower():
        return True
    return False

def validAnswer(answer):
    answers = ["yes", "no", "y", "n"]
    if isValid(answers, answer):
        return [True, answerToBool(answer)]
    return [False]

def validRedo(number):
    if len(number) > 1:
        return False
    if not ord("1") <= ord(number) <= ord("5"):
        return False
    return True

def redoThis(number):
    if number == 1:
        WeatherStations.clear()
        question1()
    if number == 2:
        WetOrDry.clear()
        climatePrint.clear()
        question2()
    if number == 3:
        DifferenceValue.clear()
        question3()
    if number == 4:
        TimePeriod.clear()
        TimePeriodPrint.clear()
        question4()

def needsToBeFixed():
    print("Oh no! \n\
was it the: \n\
1) Weather Staions\n\
2) Climate\n\
3) 'Once in a ________' value?\n\
4) The time period \n\
(whether we're looking at a specific month, or whole days, months, or years)")
    needsFixing = input("Enter in the number which corresponds to what needs \
fixing:\n")
    if validRedo(needsFixing):
        redoThis(int(needsFixing))
        question5()
    else:
        print("That's not a number between 1 and 4!!! >___<\n")
        needsToBeFixed()


# Questions
def question1():
    '''
    Asks for amount of weather stations, and which ones
    '''
    AmountOfWeatherStations = input("Please enter the number of Weather \
Stations you would like info from: ")
    if validAmountOfStations(AmountOfWeatherStations):
        addStation()
        for x in range(int(AmountOfWeatherStations) -1):
            print("Ready for you to type the name of your next Station!")
            addStation()
    else:
        print("Sorry, I don't think", AmountOfWeatherStations, 
              "is between 1 and 3")
        question1()

def question2():
    '''
    Asks for with they are after the wettest or driest period
    '''
    WetDry = input("Please type 'Wet' or 'Dry': ")
    if validClimate(WetDry):
        WetOrDry.append(WetDry.lower())
        climate = WetOrDry[0]
        climatePrint.append(setClimatePrint(climate))
    else:
        print("Sorry, I don't think you typed 'Wet' or 'Dry'")
        question2()

def question3():
    '''
    Asks for the frequency
    '''
    diff = input("What is a once in ____________ days/months/years "+ 
                 climatePrint[0] +" time. \n")
    if validDiffValue(diff):
        DifferenceValue.append(int(diff))
    else:
        print("I maybe wasn't very clear hahaha, \
but your input should be a number in digit form :)\n\nFill in the Blank: ")
        question3()
        
def question4():
    '''
    Asks for aggregation model
    '''
    month = 0
    TP_unit = input("What is a once in "+ str(DifferenceValue[0]) +" "\
                     + " days/months/years "+ climatePrint[0] +\
                     " for the month of ___________________ \n\n\
What is a once in "+ str(DifferenceValue[0]) +" "\
                     + " days/months/years "+ climatePrint[0] +\
                     " in a ___________________ \n")
    temp = validTP_Unit(TP_unit)[:]
    if temp[0]:
        DifferenceUnit.clear()
        Occurences.clear()
        if "B1units" in temp[1]:
            if not "Digit" in temp[1]:
                month = convertMonthToDigit(TP_unit)
            else:
                month = int(TP_unit)
                
            TimePeriod.append("month")
            TimePeriod.append(digitToString(month))
            DifferenceUnit.append("years")
            Occurences.append("years")
        else:
            TimePeriod.append(TP_unit)
            DifferenceUnit.append(TP_unit + "s")
            if TP_unit == "year":
                Occurences.append("years")
            elif TP_unit == "month":
                Occurences.append("months and years")
            else:
                Occurences.append("dates")
            
        TimePeriodPrint.append(setTimePeriodPrint(TimePeriod))
        
    else:
        print("\n\nI maybe wasn't very clear hahaha.\n\
If you opted for the first blank, this should be a month name or number.\n\
If you opted for the second blank, this should either be 'day', 'month', \
or 'year'")
        question4()
            
def question5():
    '''
    Prints out the user input so far, and asks if anythign needs changing.
    '''
    stations = WeatherStations[:]
    stationString = ""
    index = 0
    while index < len(stations):
        if len(stations) > 1:
            if not index == len(stations) -1:
                stationString += stations[index].title() + ", "
            else:
                stationString += ("and "+stations[index].title() + 
                " weather stations")
        else:
            stationString = stations[index].title() + " weather station"
        index += 1
    
    print("You want to know: \n\
What is a once in "+ str(DifferenceValue[0]) +" " + str(DifferenceUnit[0]) 
+" "+ climatePrint[0] + " "+ str(TimePeriodPrint[0]) + ", and on which "+
str(Occurences[0]) + " did this occur?\n\
For the " + stationString+ ", right? :)")
                    
    answer = input("Enter 'yes' or 'no' \n")
    
    tempAnswer = validAnswer(answer)[:]
    if tempAnswer[0]:
        if tempAnswer[1]:
            print("Yay!")
        else:
            needsToBeFixed()
    else:
        print("Please enter in either 'yes' or 'no'. \
What you wanna solve matters to me <3")
        question5()
        
def main():  
    '''
    This is the guts of the program. When this is run, it asks the user for all
    their input. Then returns the input into "main_loop" in "miles.py"
    to be aggregated.
    '''
    
    print ("This program lets you get the stats for \n\
'once in *however many* days/months/years' events \n\
for rainfall in Canberra, Queanbeyan and Sydney. \n\
We'll need to ask for some input from you \n\
so we can figure out and give back exactly what you wanted. \n\n\
Alrighty! \n\
First question: How many Weather Stations would you like to get info from?")
    question1()
    
    print("\n\nSecond Question: Would you like to find the Wettest or Dryiest \
period?")
    question2()
    
    print("\n\nThird Question: Fill in the blank:")
    question3()
       
    print("\n\nFourth Question: Fill in one of the blanks:")
    question4()
        
    print("\n\nLast Question: Does all of this info sound right to you? :)")
    question5()
    
    print("Please wait while I analyse the data")

    return [WeatherStations, WetOrDry[0], int(DifferenceValue[0]), \
            DifferenceUnit[0], TimePeriod, Occurences[0]]