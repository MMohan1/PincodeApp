import csv
import os
import pandas as pd
data = pd.read_csv('all_india_pin_code.csv')


def sendResult(parms):
    data = pd.read_csv('all_india_pin_code.csv')
    for key,value in parms.iteritems():
        if key == 'pincode' and value:
            data = data[data.pincode == int(value)]
            continue
        if key == 'statename' and value:
            data = data[data.statename == value]
            continue
        if key == 'Districtname' and value:
            data = data[data.Districtname == value]
            continue
        if key == 'regionname' and value:
            data = data[data.regionname == value]
            continue
        if key == 'officename' and value:
            data = data[data.officename == value]
            continue
        if key == 'circlename' and value:
            data = data[data.circlename == value]
            continue
    headers = ['_id','officename','pincode','officeType','Deliverystatus','divisionname','regionname','circlename','Taluk','Districtname','statename']
    parsed_data= []
    for row in data.to_records():
        row[8] = row[5]
        parsed_data.append(dict(zip(headers, row)))
    return parsed_data
          
    
def getIdResult(id):
    data = pd.read_csv('all_india_pin_code.csv')
    data = data.to_records()[id]
    data[8] = data[5]
    parsed_data= []
    headers = ['_id','officename','pincode','officeType','Deliverystatus','divisionname','regionname','circlename','Taluk','Districtname','statename']
    parsed_data.append(dict(zip(headers, data)))
    return parsed_data
    
def Addresult(parms):
    import csv
    header = ['officename','pincode','officeType','Deliverystatus','divisionname','regionname','circlename','Taluk','Districtname','statename']
    with open('all_india_pin_code.csv', 'a') as outcsv:
        writer = csv.DictWriter(outcsv, fieldnames = header)
        writer.writerow(parms)
    return True

def updateresult(parms):
    index = int(parms['_id'])
    del parms['_id']
    data = pd.read_csv('all_india_pin_code.csv')
    if index > 0:
        data.iloc[0:index].to_csv('dumy.csv',index=False)
        header = ['officename','pincode','officeType','Deliverystatus','divisionname','regionname','circlename','Taluk','Districtname','statename']
        with open('dumy.csv', 'a') as outcsv:
            writer = csv.DictWriter(outcsv, fieldnames = header)
            writer.writerow(parms)
        data.iloc[index+1:].to_csv('dumy1.csv',index=False)
        d = pd.read_csv('dumy.csv')
        e= pd.read_csv('dumy1.csv')
        full_data = pd.concat([d,e])
        full_data.iloc[0:].to_csv('dumy.csv',index=False)
    else:
        data.iloc[1:].to_csv('dumy.csv',index=False)
    os.remove('all_india_pin_code.csv')
    os.rename('dumy.csv','all_india_pin_code.csv')    
    return True

def delResult(parms):
    index = int(parms['_id'])
    del parms['_id']
    data = pd.read_csv('all_india_pin_code.csv')
    if index > 0:
        data.iloc[0:index].to_csv('dumy.csv',index=False)
        data.iloc[index+1:].to_csv('dumy1.csv',index=False)
        d = pd.read_csv('dumy.csv')
        e= pd.read_csv('dumy1.csv')
        full_data = pd.concat([d,e])
        full_data.iloc[0:].to_csv('dumy.csv',index=False)
    else:
        data.iloc[1:].to_csv('dumy.csv',index=False)
    os.remove('all_india_pin_code.csv')
    os.rename('dumy.csv','all_india_pin_code.csv')    
    return sendResult(parms)
        

    