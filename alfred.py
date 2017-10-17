# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 12:14:49 2017

@author: u6049237 -0487201989
"""

# Weather files
# Formatting of Weather Files
    # Product Code
    # Bureau of Meteorology station number
    # Year
    # Mnnth
    # Day
    # Rainfall Amount (millimeters)
    # Period over which rainfall was measured (days)
    # Quality
    
WeatherStations = []
WetOrDry = []
climatePrint = ["driest period"]
DifferenceValue = []
DifferenceUnit = []
TimePeriod = []
TimePeriodPrint = []
Occurences = []


# For Miles' File-----------------------
# [(a, b, c),  val]

def tupToList(tup):
    list = []
    for thingy in tup:
        print("thingy in input is: ", thingy)
        temp = []
        for element in thingy[0]:
            temp.append(element)
        list.append([temp, thingy[0][0]])
    
    return list

def avgRainAccrossDays(data):
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

def convertToFileName(Name):
    if Name == "canberra":
        return "Rainfall_Canberra_070247.csv"
    if Name == "sydney":
        return "Rainfall_Sydney_066062.csv"
    if Name == "queanbeyan":
        return "Rainfall_Queanbeyan_070072.csv"
    return Name
    
def convertAllStationsToFileName(stationList):
    stations = stationList[:]
    updated = []
    for station in stations:
        updated.append(convertToFileName(station))
    
    return updated

def conservativeValue(tup, WD):
    if not type(tup) == type(None):
        Xist = int(tup[0][0][-1])
        for date in tup:
            if ((int(date[0][-1]) <= Xist) and (WD == "wet")) or\
            ((int(date[0][-1]) >= Xist) and (not WD == "wet")):
                Xist = int(date[0][-1])
        return Xist

def printOutPutNeatly(tup, WS, WD, DV, DU, TP, O):
    lTup = tupToList(tup)
    dateList = lTup[:][0]
    
    RFvalue = conservativeValue(lTup)
    
    datesToPrint =  ""
    for date in dateList:
        date.pop(-1)
        for dateInfo in date:
            datesToPrint += dateInfo
        datesToPrint += "\n"
        
   
    
    print("A once in "+ DV +" " + DU +" "+ setClimatePrint(WD) +" "+\
setTimePeriodPrint(TP) + " is " + RFvalue + ", and this happened on: \n" +\
datesToPrint)
   
    
def returnMX(mList, WD):
    consList = []
    for m in mList:
        consList.append(conservativeValue(tupToList(m)))
        
    if WD == "wet":
        return mList[consList.index(min(consList))]

            
# General Functions----------------------
def isValid(listOfValid, CheckThis):
    for item in listOfValid:
        if CheckThis.lower() == item:
            return True
    return False

def appendFirstEle(toPrint, dates):
    for date in dates:
        toPrint += date[0] + "\n"
        
def printAll():
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

# Question 5 Functions----------------------
monthList = ["jan", "feb", "mar", "apr", "may", "jun",
               "jul", "aug", "sep", "oct", "nov", "dec",
               "january", "feburary", "march", "april",
               "may", "june", "july", "august", "september",
               "october", "november", "december"]
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
        climatePrint.append("driest period")
        question2()
    if number == 3:
        DifferenceValue.clear()
        question3()
    if number == 4:
        TimePeriod.clear()
        TimePeriodPrint.clear()
        question4()
    if number == 5:
        Occurences.clear()
        question5()

def needsToBeFixed():
    print("Oh no! \n\
was it the: \n\
1) Weather Staions\n\
2) Climate\n\
3) 'Once in a ________' value?\n\
4) The time period (whether we're looking at a specific month, or just days \
or years)\n\
5) When this event occurs (dates or years)")
    needsFixing = input("Enter in the number which corresponds to what needs \
fixing:\n")
    if validRedo(needsFixing):
        redoThis(int(needsFixing))
        question6()
    else:
        print("That's not a number between 1 and 5!!! >___<\n")
        needsToBeFixed()


# Questions
def question1():
    AmountOfWeatherStations = input("Please enter the number of Weather \
Stations you would like info from: ")
    if validAmountOfStations(AmountOfWeatherStations):
        addStation()
        for x in range(int(AmountOfWeatherStations) -1):
            print("Ready for you to type the name of your next Station!")
            addStation()
    else:
        print("Sorry, I think", AmountOfWeatherStations, 
              "isn't between 1 and 3")
        question1()

def question2():
    WetDry = input("Please type 'Wet' or 'Dry': ")
    if validClimate(WetDry):
        WetOrDry.append(WetDry.lower())
        climate = WetOrDry[:]
        climatePrint[0] = setClimatePrint(climate)
    else:
        print("Sorry, I don't think you typed 'Wet' or 'Dry'")
        question2()

def question3():
    diff = input("What is a once in ____________ days/months/years "+ 
                 climatePrint[0] +" time. \n")
    if validDiffValue(diff):
        DifferenceValue.append(int(diff))
    else:
        print("I maybe wasn't very clear hahaha, \
but your input should be a number in digit form :)\n\nFill in the Blank: ")
        question3()
        
def question4():
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
        if "B1units" in temp[1]:
            if not "Digit" in temp[1]:
                month = convertMonthToDigit(TP_unit)
            else:
                month = int(TP_unit)
                
            TimePeriod.append("month")
            TimePeriod.append(digitToString(month))
            DifferenceUnit.append("years")
        else:
            TimePeriod.append(TP_unit)
            DifferenceUnit.append(TP_unit + "s")
            
        TimePeriodPrint.append(setTimePeriodPrint(TimePeriod))
        
    else:
        print("\n\nI maybe wasn't very clear hahaha.\n\
If you opted for the first blank, this should be a month name or number.\n\
If you opted for the second blank, this should either be 'day', 'month', \
or 'year'")
        question4()
        
def question5():
    Occ = input("What is a once in "+ str(DifferenceValue[0]) +" "\
                + str(DifferenceUnit[0]) +" "+ climatePrint[0] +\
                " "+ str(TimePeriodPrint[0]) + ", and on which __________\
 did this occur?\n")
    if validOcc(Occ):
        Occurences.append(Occ)
    else:
        print("I maybe wasn't very clear hahaha, \
either type in 'dates', or 'years' :)\n\nFill in the Blank:")
        question5()
    
def question6():
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
What is a once in "+ str(DifferenceValue[0]) +" "\
+ str(DifferenceUnit[0]) +" "+ climatePrint[0] +\
" "+ str(TimePeriodPrint[0]) + ", and on which "+\
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
        question6()
def main():  
    print ("Hi!!! \n\
This program lets you get the stats for \n\
'once in *however many* days/months/years' events \n\
for rainfall in Canberra, Queanbeyan and Sydney. \n\
So to help you out, we'll need to ask for some input from you \n\
so we can figure give back exactly what you wanted. \n\n\
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
    
    print("\n\nFifth Question: Fill in the blank:")
    question5()
    
    print("\n\nLast Question: Does all of this info sound right to you? :)")
    question6()
    
    printAll()
    return [WeatherStations, WetOrDry[0], int(DifferenceValue[0]), \
            DifferenceUnit[0], TimePeriod, Occurences[0]]
    
#main()