#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 16:22:08 2017

@author: miles
"""


import csv
import alfred


def build_list(f):
    '''
    build_list takes in a given list and checks whether the rainfall 
    amount(row[5]) is not empty and the daily period (row[6]) is empty,
    if so it adds one to the daily period to represent one day of data taken
    this will be used later on to measure the validity of a month,year.
    '''        
    fileobj = open(f,"r")
    reader = csv.reader(fileobj)
    data = []

    for i in reader:
        data.append(i)
    for row in data:
        if row[5] != '' and row[6] == '':
            row[6] = 1
            
        if row[5] == '' and row[6] == '':
            row[6] = 0
            row[5] = 0
    
    data.pop(0)
    
    return  data

def build_list_avg(f):
    fileobj = open(f,"r")
    reader = csv.reader(fileobj)
    data = []

    for i in reader:
        data.append(i)
    for row in data:
        if row[5] != '' and row[6] == '':
            row[6] = 1
            
        if row[5] == '' and row[6] == '':
            row[6] = 0
            row[5] = 0
    
    data.pop(0)
    
    # With respect to missing data, we decided to just average the rainfall
    # between the days.
    # e.g. if 05/06/07 had 20mm and 4 days rainfall, we'd make dates
    #      2nd, 3rd, 4th and 5th of June 2007 to have 5mm rain
    return  alfred.avgRainAccrossDays(data)



def sub_lst(l,yr,mnt): 
    '''
    the sub_lst function takes in a list and creates a sublist containing the daily
    values of the specified month in that specified year, from this the function is able
    to check whether a month is valid by taking the sum of the period of days measured column
    and comparing it to the actual known amount of days for that month, the function then outputs
    a single set containing the year, the month and the total rainfall for that month, however if 
    the month is invalid just sets total rainfall to be -1 given that we cannot have negative rainfall 
    '''    
    nw_lst = [x for x in l if x[2] == yr and x[3] == mnt]
    summ_period = sum([int(y[6]) for y in nw_lst])
    sum_rain = sum([float(y[5]) for y in nw_lst])    
    flag = 0
    mnt_i = int(mnt)
    if (( mnt_i in [1,3,5,7,8,10,12] and summ_period == 31) or \
        (mnt_i in [4,6,9,11] and summ_period==30) or \
        (mnt_i==2 and summ_period==28)) and (int(yr)%4 != 0):
        flag = 1
        
    elif (( mnt_i in [1,3,5,7,8,10,12] and summ_period == 31) or \
          (mnt_i in [4,6,9,11] and summ_period==30) or \
          (mnt_i==2 and summ_period==29)) and (int(yr)%4 == 0) or \
          (int(yr)%400 == 0):
        flag = 1

    
    if flag == 1:
        set_output = (yr,mnt,sum_rain)
    else:
        set_output = (yr,mnt,-1)
    return set_output


def Derive_Month_List(l):
    '''
    returns a list of month totals for each year in a given list
    '''
    years = []
    months = ['01','02','03','04','05','06','07','08','09','10','11','12']
    lst = []
    for row in l:
        if row[2] not in years:
            years.append(row[2])
            
    for k in years:
        for m in range(0,12):
            obj = sub_lst(l,k,months[m])
            lst.append(obj)        
    return(lst)
     


def year_day_sum(l,yr):
    '''
    finds the sum of the daily period for that year
    '''
    yrs = [x for x in l if x[2] == yr]
    summ = 0
    for i in yrs:
        summ = summ + int(i[6])
    return summ 
   
def one_year(l,yr):
    '''
    finds the monthly sums for one year
    '''
    lst = []
    yr_lst = [x for x in l if x[0] == yr]
    for row in yr_lst:
        proxy = row[2]
        if proxy != -1:
            lst.append(proxy)

    return lst



def total_year_list(l,raw_l):
    '''
    total_year_list takes an input list of total monthly sums and takes the sum
    of these monthly sums over each year to return a list of yearly totals for
    each year, the function also checks if a year is valid by checking the total
    period sum over that year and seeing whether it is equivilent to the actual yearly total.
    if a invalid year is found the function will not append it to the final output list. 
    '''
    years = []
    total_years = []
    summ = 0
    for i in l:
        if i[0] not in years:
            years.append(i[0])
    for k in years:
        ylst = [x for x in raw_l if x[2] == k]
        tot_days = len(ylst)
        tot = year_day_sum(raw_l,k)
        oneyr = one_year(l,k)
        if tot == tot_days:
            summ = sum(oneyr)
            total_years.append((k,summ))
    return total_years
    
def mlAgg(WD, DV, TP, lst):
    '''
    takes in the given user inputs and creates the correct time aggregation
    the function then outputs both method1 and method2
    '''
    F = Derive_Month_List(lst)

    if len(TP) > 1:
        data = specified_month(F,TP[1])
        flag = 0
    
    elif TP[0] == "year":
        data = total_year_list(F, lst)
        flag = 1
    
    elif TP[0] == "month":
        data = F
        flag = 2
    else:
        data = daily_sum(lst)
        flag = 3
    if flag != 2 and flag != 3:    
        refined_lst = list_compiled(data)
    else:
        refined_lst = data      
    s_data = sort(refined_lst,flag)
    if WD == 'wet':
        m1 = wet_method1(DV, s_data)
        m2 = wet_method2(DV, s_data)
    else:
        m1 = dry_method1(DV, s_data)
        m2 = dry_method2(DV, s_data)
    return (m1, m2)
        
def main_loop(WeatherStations, WetOrDry, DifferenceValue, 
              DifferenceUnit, TimePeriod, Occurences):
    '''
    runs the main loop 
    '''
    
    WS = alfred.convertAllStationsToFileName(WeatherStations)
    for stations in WS:        
        m12i = mlAgg(WetOrDry,DifferenceValue, 
                     TimePeriod, build_list(stations))
        m12a = mlAgg(WetOrDry,DifferenceValue, 
                     TimePeriod, build_list_avg(stations))

        aggs = alfred.returnMX([m12i[0], m12i[1], m12a[0], m12a[1]])
        
        if aggs == 0:
            print("We couldn't find any valid data D: \n\
Please input something different :(")
            main_loop_with_parameters()
            
        alfred.printOutPutNeatly(aggs, stations, WetOrDry, DifferenceValue,
                                 DifferenceUnit, TimePeriod, Occurences)
        
def main_loop_with_parameters():
    p = alfred.main()
    main_loop(p[0], p[1], p[2], p[3], p[4], p[5])



def specified_month(l,mnt):
    mnths = [x for x in l if x[1] == mnt]
    lst = []
    for i in mnths:
        lst.append(i)
    return lst       
    
  
def list_compiled(l):
    ''' 
    changes list into the required format
    '''
    lst = []
    prox_lst = []
    for i in l:
            prox_lst.append(i)
            lst.append(prox_lst)
    return lst        

  
def daily_sum(l):
    lst = []
    for i in l:
        if i[6] != -1:  
            year = i[2]
            month = i[3]
            day = i[4]
            rfall= i[5]
            ll = [year,month,day,rfall]
            lst.append(ll)
    return lst    
        


def sort(l,f):
    '''
    the sort function takes in a list of sets varying in size depending on which
    time aggregation model was used and appends a index value for each element in
    the list. Then after the index value is added the list is sorted by the size
    of the total rainfall value for each element, beginning with the smallest rainfall
    values and ending with the largest rainfall values, a list of lists is then outputted 
    where the first element contains a tuple containing the units of time and total rain sum vales
    and the second element of each list contains a int corresponding to the index of that element
    '''
    sorted_lst = []
    if len(l) > 0:
        lst = l[0]
    else:
        return 0
#    if f == 0:
#        lst = l
    flgg = 0
    if f == 0:
        for i in lst:
            if i[2] != -1:
                st = []
                st.append(i)
                st.append(flgg)
                sorted_lst.append(st)
                flgg = flgg+1 
            
    if f == 1:
        for i in lst:
            if i[1] != -1:
                st = []
                st.append(i)
                st.append(flgg)
                sorted_lst.append(st)
                flgg = flgg+1 
            
    
    if f == 2:
        for i in l:
            if i[2] != -1:
                st = []
                st.append(i)
                st.append(flgg)
                sorted_lst.append(st)
                flgg = flgg+1 
           
    if f == 3:
        for i in l:
            if i[1] != -1:
                st = []
                st.append(i)
                st.append(flgg)
                sorted_lst.append(st)
                flgg = flgg+1 

    if f == 1: #total year list
        sorted_lst.sort(key=lambda tup: (tup[0][1]))
    if f == 0: #specific month
        sorted_lst.sort(key=lambda tup: (tup[0][2]))
    if f == 2: #derive month list
        sorted_lst.sort(key=lambda tup: (tup[0][2]))
    if f == 3: #deive daily sum
        sorted_lst.sort(key=lambda x: float(x[0][3]))
        
    return sorted_lst
        
    

    
def wet_method1(x,l):
    '''
    This function calculates the first method looking at the higher end values.
    By importing the sorted list from the sort function,the method takes each element
    in the list and checks for each pair to the right of it including itself and checks 
    whether the difference of the index values between each pair is greater than the given
    frequency. Once it reaches a point in which this is true, the function returns the point being the X of f point
    and all other points to the right of it returning a list of all points that satisfy the method.   
    '''
    ln = len(l)
    lst = []
    lstf = []
    for i in l:
        lst.append(i[1])
        
    for i in range(0,ln-1):
        flag = 1
        for j in range(i,ln-1):
            if flag == 0:
                break
            for k in range(j+1,ln):
                if abs(lst[j] - lst[k]) < x:
                    flag = 0
                    break
        if flag == 1:
            for p in range(i,ln):
                lstf.append(l[p])
            return lstf         
    

def dry_method1(x,l):
    '''
    for dry method one rather then looking at the higher end values the function looks at
    the lower end vales meaning rather then itterating the list from the left to the right
    checking all pairs this method itterates from right to left finding all values that are
    less then the given frequency rather then more.  
    '''
    ln = len(l)
    lst = []
    lstf = []
    for i in l:
        lst.append(i[1])
    for i in range(ln,2,-1):
        flag = 1
        for j in range(i,1,-1):
            if flag == 0:
                break
            for k in range(j-1,0,-1): 
                if abs(lst[j-1] - lst[k-1]) > x:
                    flag = 0
                    break
                
        if flag == 1:
            for p in range(i,ln):
                lstf.append(l[p])
            return lstf     
        
       

def wet_method2(x,l):
    '''
    method two takes the total imported sorted list, then devides it into equal parts
    equivilent to the frequency, for example if the frequency was 7 the list will
    be divided into seven parts. The method then takes the last section, (in the case 
    of the above example would be the seventh part) and returns all the elements in that section
    with the first element being the X of f element. 
    '''
    fin = []
    ln = len(l)
    pcent = int(ln/x)
    val = ln - pcent
    if pcent < 1:
        val = val-1
    if ln > 0:
        final = l[val]
    else:
        final = 0
        return final
    indx = l.index(final)
    for i in range(indx,ln):
        fin.append(l[i])
    return fin



def dry_method2(x,l):
    '''
    refer back to wet_method2 dry_method2 does the same function accept rater then returning
    the last section returns the first and the X of f element is the last element in this 
    section rather then the first element.
    '''
    fin = []
    ln = len(l)
    final = []
    pcent = int(ln/x)
    if ln > 0:
        final = l[pcent]
    else:
        final = 0
    indx = l.index(final)
    for i in range(indx,ln):
        fin.append(l[i])
    return fin
#-----------------------------------------------------------------------
