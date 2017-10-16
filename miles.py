#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 16:22:08 2017

@author: miles
"""

#hi alfred!!!!
#hi miles! :D
import numpy as np
import matplotlib.pyplot as mpl
import csv
import alfred
#fileobj = open("Rainfall_Sydney_066062.csv","r")



def build_list(f):
    fileobj = open(f,"r")
    reader = csv.reader(fileobj)
    data = []
    flag = 0

    for i in reader:
        data.append(i)
    for j in data:
        if j[5] != '' and j[6] == '':
           # print("hello",j)
            j[6] = 1
        if j[5] == '' and j[6] == '':
            j[6] = 0
            j[5] = 0
    
    data.pop(0)
    
    # With respect to missing data, we decided to just average the rainfall
    # between the days.
    # e.g. if 05/06/07 had 20mm and 4 days rainfall, we'd make dates
    #      2nd, 3rd, 4th and 5th of June 2007 to have 5mm rain
    return alfred.avgRainAccrossDays(data)

data = build_list("Rainfall_Sydney_066062.csv")

def sub_lst(l,yr,mnt): 
    ll = [x for x in l if x[2] == yr and x[3] == mnt]
    total = len(ll)
    #print(ll)
    summ = sum([int(y[6]) for y in ll])
    sumr = sum([float(y[5]) for y in ll])
    #print("the total is ",total,"the sum is ",summ)
#    if summ != 28 and summ != 30 and summ != 31:
#        #print("invalid month")
#        aaa=1
#    
    #flag = 0
    #mnt_i = int(mnt)
#    if (( mnt_i in [1,3,5,7,8,10,12] and summ == 31) or (mnt_i in [4,6,9,11] and summ==30) or (mnt_i==2 and summ==28)) and (int(yr)%4 != 0):
#        #print("This is a valid month")
#        flag = 1
#    elif (( mnt_i in [1,3,5,7,8,10,12] and summ == 31) or (mnt_i in [4,6,9,11] and summ==30) or (mnt_i==2 and summ==29)) and (int(yr)%4 == 0):
#        #print("This is a valid month")
#        flag = 1
#    else:
#        #print("This is NOT a valid month")
#        aaa=1
#    
#    if flag == 1:
    stt = (yr,mnt,sumr)
#    else:
#        stt = (yr,mnt,-1)
    return stt



def Derive_Month_List(l):
    years = []
    months = ['01','02','03','04','05','06','07','08','09','10','11','12']
    lst = []
    flag = 0
    for i in l:
        if i[2] not in years:
            years.append(i[2])
            
    for k in years:
        for m in range(0,12):
            #print("this is flag ",flag,lst)
            obj = sub_lst(l,k,months[m])
            lst.append(obj)        
    return(lst)
     
F = Derive_Month_List(data)

def Derive_Specific_Mnth_List(W,mnth):
    Lst = [x for x in  W  if x[1]==mnth ]
    return Lst


    
def one_year(l,yr):
    lst = []
    point = [x for x in l if x[0] == yr]
    print(point)
    for i in point:
        proxy = i[2]
        if proxy != -1:
            #lst.append(i[0])
            lst.append(proxy)
        else:
            print("invalid month")
    return lst

#print(one_year(F,'2017'))
def year_sum(l,yr):
    yrs = [x for x in l if x[2] == yr]
    summ = 0
    for i in yrs:
        summ = summ + float(i[5])
    return summ    

#def mounth_sum(l,mnt):
#    mnths = [x for x in l if x[3] = mnt]
#    summ = 0 
#    for i in mnt:
#        summ = summ + float(i[5])
#    return summ       
    

#print("uuoopp ",year_sum(data,'1998'))

def total_year_list(l,dt):
    lst = []
    years = []
    s = []
    print("this is l ",l)
    flag = 0
    months = ['01','02','03','04','05','06','07','08','09','10','11','12']
    #print()
    for i in l:
        if i[0] not in years:
            years.append(i[0])
    for k in years:
        #print("this is k",k)        
        tot = year_sum(dt,k)
        s.append((k,tot))
#        for m in range(0,12):
#            #if l[flag][2] != -1:
#           summ = summ + float(dt[flag][5])
#        #h.append(years[])
#        h.append(summ)
#        flag += 1
#        lst.append(h)
    #print("these are the years ",years)
#    print("the total sum is ",len())    
#    print("the total years are ",len(years))
    print("ddffgg ",s)
    return s
    
def main_loop(WeatherStations, WetOrDry,DifferenceValue, DifferenceUnit, TimePeriod, Occurences):
    WS = alfred.convertAllStationsToFileName(WeatherStations)
    printThingos = []
    for stations in WS:        
        lst = build_list(stations)
        F = Derive_Month_List(lst)
        data = []
        
        #specific month
        if len(TimePeriod) > 1:
            data = specified_month(F,TimePeriod[1])
            flag = 0
        #years
        elif TimePeriod[0] == "year":
            data = total_year_list(F, lst)
            flag = 1
        #months
        else:
            data = F
            flag = 2
        
        refined_lst = list_compiled(data,flag)    
        s_data = sort(refined_lst)
        m1 = wet_method1(DifferenceValue,s_data)
        printThingos.append(m1)
        print(m1)
    return printThingos

def main_loop_alfred():
    p = alfred.main()
    main_loop(p[0], p[1], p[2], p[3], p[4], p[5])



def specified_month(l,mnt):
    mnths = [x for x in l if x[1] == mnt]
    lst = []
    for i in mnths:
        lst.append(i)
    return lst       
    
print("kkkkk ",specified_month(F,'04'))

def check_valid_year(l,yr):
    ll = [x for x in l if x[2]]
    i = 0
    while ll[i][6] == 0:
        i = i+1
    fstfnd = i
#    if (fstfnd+1) != ll[i][6]:
        
def list_compiled(l,flag):
    lst = []
    for i in l:
        if flag == 1:
            lst.append(i[1])
        if flag == 2:
             lst.append(i[2])
        if flag == 0:
            lst.append(i[2])
    return lst        
    
def sort(l):
    y = []
    b = 0
    for i in l:
        #print("i is ",i)
        st = (i,b)
            #print(st)
        y.append(st)
        b = b+1 
        #print("b is ",b)
    #print(type(y))  
    #print(y)
    y.sort(key=lambda tup: float(tup[0]))     
    return y
        
    
    
    
def wet_method1(x,l):
    ln = len(l)
    print(l)
    for i in range(0,ln-2):
        #print("hi this is i ",i,ln)
        flag = 1
        for j in range(i,ln-1):
            if j%1000 == 0:
                print('i=',i,' j=',j)
            if flag == 0:
                break
            for k in range(j+1,ln):
                #print(" j = ",l[j],"k = ",l[k],"the difference is ",abs(l[j][1] - l[k][1]))
                if abs(l[j][1] - l[k][1]) < x:
                    #print(" j = ",l[j],"k = ",l[k],"the difference is ",abs(l[j][1] - l[k][1]))
                    flag = 0
                    break
        if flag == 1:
            return l[i]     
    
    
def dry_method1(x,l):
    ln = len(l)
    print(l)
    for i in range(ln,2,-1):
        print("hi this is i ",i,ln)
        flag = 1
        for j in range(i,1,-1):
            #if j%1000 == 0:
            print('i=',i,' j=',j)
            if flag == 0:
                break
            for k in range(j-1,0,-1): 
                print(k)
                print(" j = ",l[j-1],"k = ",l[k-1],"the difference is ",abs(l[j-1][1] - l[k-1][1]))
                if abs(l[j-1][1] - l[k-1][1]) > x:
                    #print(" j = ",l[j],"k = ",l[k],"the difference is ",abs(l[j][1] - l[k][1]))
                    flag = 0
                    break
        if flag == 1:
            print("yay worked")
            return l[i]     


#-----------------------------------------------------------------------
# THIS IS THE MAINLINE OF THE PROGRAM 

print("\n\n")
print("Welcome to our Weather analysis program")
print("Please wait while I analyse the data")
print("This program is written by Miles Pennifold and Alfred Le")



#F = Derive_Month_List(data)
#print(F[0:10])
#print("higgs ",one_year(F,'1998'))        

print("")
        
#G = Derive_Specific_Mnth_List(F,'01')
#for i in range(0,10):
#    print(G[i])


#print("hi this is the total year list ",total_year_list(F,data))            

#years = [int(x[0])   for x in G if x[2] != -1]   
#y =     [float(x[2]) for x in G if x[2] != -1]    
#years = [int(x[0])   for x in F if x[2] != -1]   
#y =     [float(x[2]) for x in F if x[2] != -1]    




#years = [1968, 1969, ..., 2016, 2017] # list of years in the table above
##y = [28.7, 56.0, ..., 148.3, 0.4] # corresponding list of total rainfall values
#x = np.arange(0, len(y))   
#mpl.plot(x, y, '.b', markersize=5)
#mpl.plot([0, len(y) + 1], [143.8, 143.8], '--k')
#mpl.xticks(x, years, rotation=90)
##mpl.grid(color='r', linestyle='-', linewidth=2)
##mpl.grid()
#mpl.show()

#avg_month_time(data,'06')    

#print(sub_lst(data,'1858','04'))    

main_loop_alfred()