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
    
    return  data

def build_list_avg(f):
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
    return  alfred.avgRainAccrossDays(data)


def sub_lst(l,yr,mnt): 
    ll = [x for x in l if x[2] == yr and x[3] == mnt]
    total = len(ll)
    ##print(ll)
    summ = sum([int(y[6]) for y in ll])
    sumr = sum([float(y[5]) for y in ll])
   # print("the total is ",total,"the sum is ",summ)
    if summ != 28 and summ != 30 and summ != 31:
      #  print("invalid month")
        aaa=1
    
    flag = 0
    #print("vv ",mnt)
    mnt_i = int(mnt)
    if (( mnt_i in [1,3,5,7,8,10,12] and summ == 31) or \
        (mnt_i in [4,6,9,11] and summ==30) or \
        (mnt_i==2 and summ==28)) and (int(yr)%4 != 0):
       # print("This is a valid month")
        flag = 1
    elif (( mnt_i in [1,3,5,7,8,10,12] and summ == 31) or \
          (mnt_i in [4,6,9,11] and summ==30) or \
          (mnt_i==2 and summ==29)) and (int(yr)%4 == 0) or \
          (int(yr)%400 == 0):
      #  print("This is a valid month")
        flag = 1
    else:
       ## print("This is NOT a valid month")
        aaa=1
    
    if flag == 1:
        stt = (yr,mnt,sumr)
    else:
        stt = (yr,mnt,-1)
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
     
#F = Derive_Month_List(data)
#print("ogg ",F)

def Derive_Specific_Mnth_List(W,mnth):
    Lst = [x for x in  W  if x[1]==mnth ]
    return Lst


    
def one_year(l,yr):
    lst = []
    point = [x for x in l if x[0] == yr]
   #print(point)
    for i in point:
        proxy = i[2]
        if proxy != -1:
            #lst.append(i[0])
            lst.append(proxy)
        else:
            print("invalid month")
    return lst

#print(one_year(F,'2017'))
def year_day_sum(l,yr):
    yrs = [x for x in l if x[2] == yr]
    summ = 0
    for i in yrs:
        summ = summ + int(i[6])
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
    #print("this is l ",l)
    flag = 0
    months = ['01','02','03','04','05','06','07','08','09','10','11','12']
    #print()
    summ = 0
    for i in l:
        if i[0] not in years:
            years.append(i[0])
    for k in years:
        ylst = [x for x in dt if x[2] == k]
        tot_days = len(ylst)
        tot = year_day_sum(dt,k)
        #print("this is tot ",tot,"this is the tot days ",  tot_days)
        if tot == tot_days:
            #print("valid year")
            for m in range(0,12):
                #print("wave",l[m])
                if l[m][2] != -1:
                    summ = summ + float(l[m][2])
                    #print("tt is summ ",summ)
            s.append((k,summ))
        #print("this is k",k)        
        #s.append((k,tot))
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
   #print("ddffgg ",s)
    return s
    
def mlAgg(WD, DV, TP, lst):
    F = Derive_Month_List(lst)
    #print("FF ",F[:20])

        #specific month
    if len(TP) > 1:
        data = specified_month(F,TP[1])
       # print("specific month",data[:20])
        flag = 0
    #years
    elif TP[0] == "year":
        data = total_year_list(F, lst)
       # print("total year",data[:20])
        flag = 1
    #months
    elif TP[0] == "month":
        data = F
       # print("derive Month",data[:20])
        flag = 2
    #days
    else:
        #data = asdfasdasd
        print("daily")
        #flag = 3
    #print("d7 ",data[:20])    
    if flag != 2:    
        refined_lst = list_compiled(data,flag)
    else:
        refined_lst = data
    #print("refined is:", refined_lst[:20])
    #print("flag is:", flag)
   # print("this is data ",data[:20],"this is flag",flag)       
    s_data = sort(refined_lst,flag)
    #print("this is s_data ",s_data[:2])
    if WD == 'wet':
       # print("s_data is:", s_data[:9])
        m1 = wet_method1(DV, s_data)
        m2 = wet_method2(DV, s_data)
    else:
        m1 = dry_method1(DV, s_data)
        m2 = dry_method2(DV, s_data)
    #print("m1 ",m1[:1],"m2 ",m2[:1])
    return (m1, m2)
        
    #lst = build_list(stations)
def main_loop(WeatherStations, WetOrDry, DifferenceValue, 
              DifferenceUnit, TimePeriod, Occurences):
    WS = alfred.convertAllStationsToFileName(WeatherStations)
    for stations in WS:        
        m12i = mlAgg(WetOrDry,DifferenceValue, 
                     TimePeriod, build_list(stations))
        m12a = mlAgg(WetOrDry,DifferenceValue, 
                     TimePeriod, build_list_avg(stations))

        alfred.printOutPutNeatly(alfred.returnMX([m12i[0], m12i[1], \
                                                  m12a[0], m12a[1]], WetOrDry),
                                 stations, WetOrDry, DifferenceValue,
                                 DifferenceUnit, TimePeriod, Occurences)
        
def main_loop_alfred():
    p = alfred.main()
    main_loop(p[0], p[1], p[2], p[3], p[4], p[5])



def specified_month(l,mnt):
    mnths = [x for x in l if x[1] == mnt]
    lst = []
    for i in mnths:
        lst.append(i)
    return lst       
    
#print("kkkkk ",specified_month(F,'04'))

def check_valid_year(l,yr):
    ll = [x for x in l if x[2]]
    i = 0
    while ll[i][6] == 0:
        i = i+1
    fstfnd = i
#    if (fstfnd+1) != ll[i][6]:
        
def list_compiled(l,flag):
    lst = []
    ll = []
   # print("&& ",l)
    for i in l:
        #print(":> ",i)
        if flag == 1:  #total year list
            ll.append(i)
            lst.append(ll)
        if flag == 2:  #month list
             ll.append(i)
             lst.append(ll)
        if flag == 0: #specified month
            ll.append(i)
            lst.append(ll)
    return lst        
    
def daily_sum(l):
    lst = []
    for i in l:
        year = i[2]
        month = i[3]
        day = i[4]
        rfall= i[5]
        ll = [year,month,day,rfall]
        lst.append(ll)
    #print("ruop ",lst)    
    return lst    
        


def sort(l,f):
    y = []
    if len(l) > 0:
        lst = l[0]
    else:
        return 0
    flgg = 0
  # print("uuu ",l)
    #print("lsit is ",lst)
    
    if f == 0:
        for i in lst:
            if i[2] != -1:
                #print("uutt ",i)
                st = []
                st.append(i)
                st.append(flgg)
                #st = (proxy,flgg)
                #print("yooy ",st)
                y.append(st)
                flgg = flgg+1 
                #print("y is ",y)
            else:
                print(i,"invalid")
    if f == 1:
        for i in lst:
            if i[1] != -1:
               # print("uutt ",i)
                st = []
                st.append(i)
                st.append(flgg)
                #st = (proxy,flgg)
                #print("yooy ",st)
                y.append(st)
                flgg = flgg+1 
                #print("y is ",y)
            else:
                print(i,"invalid")    
    
    if f == 2:
        for i in lst:
            if i[1] != -1:
               # print("uutt ",i)
                st = []
                st.append(i[0])
                st.append(flgg)
                #st = (proxy,flgg)
                #print("yooy ",st)
                y.append(st)
                flgg = flgg+1 
                #print("y is ",y)
            else:
                print(i,"invalid")        
                
    #print(type(y))  
    #print("rpp ",y)
    if f == 1: #total year list
        y.sort(key=lambda tup: (tup[0][1]))
    if f == 0: #specific month
        y.sort(key=lambda tup: (tup[0][2]))
    if f == 2: #derive month list
        y.sort(key=lambda tup: (tup[0][2]))
        
    #print("raa  ",y)    
    return y
        
    
    
    
def wet_method1(x,l):
    ln = len(l)
 #   print(l)
    lst = []
    lstf = []
  #  print("this is l ",l)
    for i in l:
        lst.append(i[1])
        
   # print("rrr ",lst)    
    for i in range(0,ln-2):
        #print("hi this is i ",i,ln)
        flag = 1
        for j in range(i,ln-1):
          #  if j%1000 == 0:
          #print('i=',i,' j=',j)
           #     print("FILLER")
            if flag == 0:
                break
            for k in range(j+1,ln):
               # print(" j = ",lst[j],"k = ",lst[k],"the difference is ",abs(lst[j] - lst[k]))
                #print("dd ",lst[j])
                if abs(lst[j] - lst[k]) < x:
                    #print(" j = ",l[j],"k = ",l[k],"the difference is ",abs(l[j][1] - l[k][1]))
                    flag = 0
                    break
        if flag == 1:
           # print("yay worked")
         #   print("this is li ",l[i])
            for p in range(i,ln):
                lstf.append(l[p])
               # print("p is d ",p)
            return lstf         
    
  
def dry_method1(x,l):
    ln = len(l)
    lst = []
    lstf = []
    for i in l:
        lst.append(i[1])
   # print("?? ",lst)
    for i in range(ln,2,-1):
       # print("hi this is i ",i,ln)
        flag = 1
        for j in range(i,1,-1):
            #if j%1000 == 0:
           # print('i=',i,' j=',j)
            if flag == 0:
                break
            for k in range(j-1,0,-1): 
              #  print(k)
               # print(" j = ",lst[j-1],"k = ",lst[k-1],
                      #"the difference is ",abs(lst[j-1] - lst[k-1]))
                if abs(lst[j-1] - lst[k-1]) > x:
                    #print(" j = ",l[j],"k = ",l[k],"the difference is ",abs(l[j][1] - l[k][1]))
                    flag = 0
                    break
        if flag == 1:
           # print("yay worked")
            for p in range(i,ln):
                lstf.append(l[p])
               # print("p is d ",p)
            return lstf     

def wet_method2(x,l):
    fin = []
    ln = len(l)
    #print("this is l",l)
    #print("len is ",ln)
    pcent = int(ln/x)
    #print("pcent is ",pcent)
    val = ln - pcent
    #print("val is ",val)
    if ln > 0:
        final = l[val-1]
    else:
        final = 0
        return final
    indx = l.index(final)
    #print("this is index ",indx) 
    for i in range(indx,ln):
        fin.append(l[i])
    #print("job done ",final)    
    return fin

def dry_method2(x,l):
    fin = []
    ln = len(l)
    final = []
   # print("this is ln ",ln,"this is x ",x)
    pcent = int(ln/x)
    #print("this is da pcent ",pcent)
   # final = l[pcent]
    if ln > 0:
        final = l[pcent-1]
    else:
        final = 0
    indx = l.index(final)
    #print("this is index ",indx) 
    for i in range(indx,ln):
        fin.append(l[i])
    return fin
#-----------------------------------------------------------------------
# THIS IS THE MAINLINE OF THE PROGRAM 

print("\n\n")
print("Welcome to our Weather analysis program")
print("Please wait while I analyse the data")
print("This program is written by Miles Pennifold and Alfred Le")

#data = build_list("Rainfall_Sydney_066062.csv")
#daily_sum(data)
#F = Derive_Month_List(data)
#print(F," iiiiii")
#p = total_year_list(F,data)
##p = specified_month(F,'04')
###p = specified_month(F,'04')
#print("here is p",p)
#
#print(sort(F,2))
##reflst = sort(p,1)
#wet_method2(2,reflst)
#print("higgs ",(reflst))        

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
