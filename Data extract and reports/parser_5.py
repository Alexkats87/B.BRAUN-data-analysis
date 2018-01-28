# -*- coding: utf-8 -*-
import os
import re

def get_ce_header(source,target):
    ce_header = []
    while True:
        string = source.readline()
        if  (u"Номер / Дата".encode('utf8')  in string):
            ce_number_and_date = source.readline().split('/')
            break
    ce_header.append(ce_number_and_date[0].strip())
    ce_header.append(ce_number_and_date[1].strip())

    while True:
        string = source.readline()
        if  (u"Заказчик".encode('utf8')  in string):
            customer_number = source.readline().strip()
            break
    ce_header.append(customer_number)

    while True:
        string = source.readline()
        if  (u"Ответственный".encode('utf8')  in string):
            try:
                employee = string.split(' ')[1].decode('utf-8')
                break
            except:
                employee = u"UNKNOWN"
                break
            
    ce_header.append(employee)
    return ce_header




def get_pump_data(source,target,string):
    pump_data = []
    pump_type = u"0"
    
    if  (u"ПЕРФУЗОР СПЕЙС".encode('utf8')  in string):
        pump_type = u"8713030"
        
    elif  (u"ПЕРФУЗОР КОМПАКТ S".encode('utf8')  in string):
        pump_type = u"8714843"
        
    elif  (u"ИНФУЗОМАТ СПЕЙС".encode('utf8')  in string):
        pump_type = u"8713050"

    elif  (u"ИНФУЗОМАТ FMS 230".encode('utf8') in string):
        pump_type = u"8715548"

    elif  (u"ПЕРФУЗОР КОМПАКТ".encode('utf8')  in string):
        pump_type = u"8714827"

    elif  (u"ПЕРФУЗОР ФМ".encode('utf8')  in string):
        pump_type = u"8713901"
        
    pump_data.append(pump_type)
    string = source.readline()
    
    while not (u"Сер. ном.".encode('utf8')  in string): 
        string = source.readline()
        
    if  (u"Сер. ном.".encode('utf8')  in string):
        pump_ser_num = string.split(' ')[-2]
    else:
        pump_ser_num = u"0"
    pump_data.append(pump_ser_num)

    return pump_data



def get_pump_spare_parts(source,target,string):
    pump_spare_parts = []
    pump_spare_parts.append(string[:-1])
    while True:
        string = source.readline()
        if ((u"1,00 ШТ 87".encode('utf8')  in string) or  (u"Итого".encode('utf8')  in string)):
            break
        else:
            if (re.match(r'^34((77)|5[0,2])\d\d\d(\d|A)A?$', string) or  re.match(r'^87131\d\d[A,B,D]?$', string) or  re.match(r'^77000\d\d$', string)  or  re.match(r'^8714991$', string) ) : 
                pump_spare_parts.append(string[:-1])
        
    return pump_spare_parts





#========================  Main =========================================
        

target = open('all_costs_table_1_ce_and_defects_only_TEST+PC+PFM.txt','w')
source=open('all_costs_agregated_1_ce_and_defects_only.txt','r')

ce_header = []
pump_data = []
spare_parts = []
ce_count = 0
pumps_count = 0
flag_allow_read_spare_parts = False
flag_ce_open = False

for i in xrange(0,519000):
        
    full_pump_data = []
    
    string = source.readline()
    if not string:
        print "END"
        break
    
    if (u"АКТ ОБСЛЕДОВАНИЯ".encode('utf8')  in string) :
        ce_header = get_ce_header(source,target)
        ce_count=ce_count+1
        

    if  ( ( ( (u"ПЕРФУЗОР СПЕЙС".encode('utf8')  in string) or (u"ПЕРФУЗОР КОМПАКТ".encode('utf8')  in string) or (u"ИНФУЗОМАТ СПЕЙС".encode('utf8')  in string) or (u"ИНФУЗОМАТ FMS 230".encode('utf8') in string) or (u"ПЕРФУЗОР ФМ".encode('utf8')  in string) ) and (len(string.decode('utf8'))<25)  )):          
        pump_data = get_pump_data(source,target,string)
        pumps_count=pumps_count+1
        flag_allow_read_spare_parts = True
        

    if (u"77000".encode('utf8')  in string) and (len(pump_data)>0) and (flag_allow_read_spare_parts == True):       
        spare_parts =  get_pump_spare_parts(source,target,string)
        #print spare_parts
        full_pump_data = full_pump_data + ce_header + pump_data + spare_parts
        flag_allow_read_spare_parts = False
        #print full_pump_data
        for s in full_pump_data:
            try:
                target.write(s.encode('utf-8') + ',')
            except UnicodeDecodeError:
                print 'Can\'t write pump'
        target.write('\n')



source.close()
target.close()

print 'Total CE:',ce_count
print 'Total pupmps:',pumps_count







 
