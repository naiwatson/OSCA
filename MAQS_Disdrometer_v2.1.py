# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 15:01:26 2020

@author: mbexknm5
"""


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from datetime import datetime, timedelta
import dateutil.relativedelta
import glob
import math
from datetime import date
import datetime
import shutil
import os, sys

sample_Freq = '1sec'
av_Freq = '1min' #averaging frequency required of the data
daily_Freq = '1440min'
data_Source = 'externalHarddrive' #input either 'externalHarddrive' or 'server'
version_number = 'v2.1' #version of the code
year_start = 2022 #input the year of study by number
month_start = 2 #input the month of study by number
default_start_day = 1 #default start date set
day_start = default_start_day
validity_status = 'Ratified' #Ratified or Unratified

status = np.where(validity_status == 'Unratified' , '_Unratified_', '_Ratified_')

today = date.today()
current_day = today.strftime("%Y%m%d")

start = datetime.datetime(year_start,month_start,day_start,0,0,0) #start time of the period 
month_After = start + dateutil.relativedelta.relativedelta(months=1)
default_end_date = month_After - timedelta(minutes=1) #last day of month more complex so established here

default_end_day = str(default_end_date.strftime("%Y")) + str(default_end_date.strftime("%m")) + str(default_end_date.strftime("%d"))

year_end = int(default_end_date.strftime("%Y")) #this converts the default_end_day into the end of time selected
month_end = int(default_end_date.strftime("%m"))
day_end = int(default_end_date.strftime("%d"))

end = datetime.datetime(year_end,month_end,day_end,23,59,59) #if new end date needed to can be changed here 

start_year_month_str = str(start.strftime("%Y")) + str(start.strftime("%m")) # convert start and end months to strings
end_year_month_str = str(end.strftime("%Y")) + str(end.strftime("%m"))

end_Date_Check = str(end.strftime("%Y")) + str(end.strftime("%m")) + str(end.strftime("%d"))

date_file_label = np.where(start_year_month_str == end_year_month_str, start_year_month_str, str(start_year_month_str) + "-" + str(end_year_month_str))
#print(date_file_label) #print end date to check it is correct

prior_date_1 = start - timedelta(days=1)
prior_date_1_str = str(prior_date_1.strftime("%Y")) + str(prior_date_1.strftime("%m")) + str(prior_date_1.strftime("%d"))

prior_date_2 = start - timedelta(days=2)
prior_date_2_str = str(prior_date_2.strftime("%Y")) + str(prior_date_2.strftime("%m")) + str(prior_date_2.strftime("%d"))

later_date_1 = end + timedelta(days=1)
later_date_1_str = str(later_date_1.strftime("%Y")) + str(later_date_1.strftime("%m")) + str(later_date_1.strftime("%d"))

later_date_2 = end + timedelta(days=2)
later_date_2_str = str(later_date_2.strftime("%Y")) + str(later_date_2.strftime("%m")) + str(later_date_2.strftime("%d"))

folder = np.where((str(version_number) == 'v0.6'), 'Preliminary', str(validity_status))
print("using a " + str(folder) + "_" + str(version_number) + " folder")

Data_Source_Folder = np.where((data_Source == 'server'), 'Z:/FIRS/FirsData/Disdrometer/', 'D:/FirsData/Disdrometer/')
Data_Output_Folder = np.where((data_Source == 'server'), 'Z:/FIRS/' + str(folder) + '_' + str(version_number) + '/', 'D:/' + str(folder) + '_' + str(version_number) + '/')

Month_files = str(Data_Source_Folder) + str(date_file_label) + '*_distrometer_1min' + '.txt'

Prior_File_1 = str(Data_Source_Folder) + str(prior_date_1_str) + '*_distrometer_1min' + '.txt'
Prior_File_2 = str(Data_Source_Folder) + str(prior_date_2_str) + '*_distrometer_1min' + '.txt'
Later_File_1 = str(Data_Source_Folder) + str(later_date_1_str) + '*_distrometer_1min' + '.txt'
Later_File_2 = str(Data_Source_Folder) + str(later_date_2_str) + '*_distrometer_1min' + '.txt'

print(str(Month_files))

distrometer_csv_files = glob.glob(Month_files) + glob.glob(Prior_File_1) + glob.glob(Prior_File_2) + glob.glob(Later_File_1) + glob.glob(Later_File_2)

if start_year_month_str == '201907':
    month_1 = str(Data_Source_Folder) + '2019070' + '*_distrometer_1min' + '.txt' 
    month_2 = str(Data_Source_Folder) + '2019071' + '*_distrometer_1min' + '.txt' 
    month_3 = str(Data_Source_Folder) + '2019072' + '*_distrometer_1min' + '.txt' 
    month_4 = str(Data_Source_Folder) + '2019073' + '*_distrometer_1min' + '.txt' 
    Later_File_1 = str(Data_Source_Folder) + str(later_date_1_str) + '*_distrometer_1min' + '.txt'
    Later_File_2 = str(Data_Source_Folder) + str(later_date_2_str) + '*_distrometer_1min' + '.txt'
    distrometer_csv_files = glob.glob(Later_File_1) + glob.glob(Later_File_2) + glob.glob(month_1) + glob.glob(month_2) + glob.glob(month_3) + glob.glob(month_4) # 
else:
    pass

distrometer_frames = []

for csv in distrometer_csv_files:
    csv = open(csv, 'r', errors='ignore')#open the file and replace characters with utf-8 codec errors
    df = pd.read_csv(csv, index_col=False, header=None, skiprows=1) #, usecols=[*range(0, 74)],error_bad_lines=False, keep_default_na=False, delimiter=';'
    distrometer_frames.append(df)

# Concatenate frames into a single DataFrame
distrometer_Data = pd.concat(distrometer_frames, sort=True)

distrometer_Data=distrometer_Data[0].str.split(';', expand=True)


distrometer_Data.rename(columns={0: 'Date', 1: 'Time', 9: 'Other Precipitation Classification' , 13: 'Precipitation Classification' }, inplace=True)
distrometer_Data.rename(columns={14: 'Total Precipitation Rate (mm/hr)', 15: 'Liquid Precipitation Rate (mm/hr)', 16: 'Solid Precipitation Rate (mm/hr)', 17: 'Accumulated Precipitation (mm)'  }, inplace=True) #
distrometer_Data.rename(columns={18: 'Visibility in precipitation (m)', 19: 'Radar Reflectivity (dBZ)', 20: 'Measuring Quality (%)' }, inplace=True)
distrometer_Data.rename(columns={21: 'Maximum Diameter Hail (mm)', 22: 'Status Laser', 23: 'Static Signal' }, inplace=True)
distrometer_Data.rename(columns={24: 'Status Laser temperature (analogue)', 25: 'Status Laser temperature (digital)', 26: 'Status Laser current (analogue)' }, inplace=True)
distrometer_Data.rename(columns={27: 'Status Laser current (digital)', 28: 'Status Sensor supply', 29: 'Status Current pane heating laser head' }, inplace=True)
distrometer_Data.rename(columns={30: 'Status Current pane heating receiver head', 31: 'Status Temperature sensor', 32: 'Status Heating supply' }, inplace=True)
distrometer_Data.rename(columns={33: 'Status Current heating housing', 34: 'Status Current heating heads', 35: 'Status Current heating carriers', 36: 'Status Control output laser power' }, inplace=True)
#distrometer_Data.rename(columns={51: 'number_of_drops', 53: 'number_of_hydrometeors_below_speed_of_0.15m/s', 55: 'number_of_hydrometeors_above_speed_of_20m/s' }, inplace=True)
#distrometer_Data.rename(columns={57: 'number_of_hydrometeors_above_speed_of_20m/s', }, inplace=True)

#distrometer_Data.rename(columns={19: 'Minute Precipitation Measurement (mm)'}, inplace=True)

#distrometer_Data.rename(columns={0: 'Date', 1: 'Time', 2: 'Conc (#/cc)', 3: 'Saturator Temperture Alert', 4: 'Condensor Temperture Alert' }, inplace=True)

#distrometer_Data = distrometer_Data.drop(columns=[2, 3, 4])
##distrometer_Data = distrometer_Data.drop(distrometer_Data.iloc[:, 46:512], inplace=True, axis=1) #distrometer_Data = distrometer_Data.drop(distrometer_Data.iloc[:, 46:50], inplace=True, axis=1)
#distrometer_Data = distrometer_Data.drop(distrometer_Data.iloc[:, 22:37], inplace=True, axis=1)

#distrometer_Data.rename(columns={0: 'Date', 1: 'Time', 2: 'Conc (#/cc)', 3: 'Saturator Temperture Alert', 4: 'Condensor Temperture Alert' }, inplace=True)
#distrometer_Data.rename(columns={5: 'Optics Temperature Alert', 6: 'Inlet Flow Alert', 7: 'Aerosol Flow Alert', 8: 'Laser Power Alert' }, inplace=True)
#distrometer_Data.rename(columns={9: 'Liquid Reservoir Alert', 10: 'Aerosol Concentration Flag', 11: 'Calibration Alert', 18: 'CPC Cal Mode' }, inplace=True)


distrometer_Data['Date'] = distrometer_Data['Date'].astype(str)
distrometer_Data['Time'] = distrometer_Data['Time'].astype(str)
distrometer_Data['Date_length'] = distrometer_Data['Date'].str.len()
distrometer_Data['Time_length'] = distrometer_Data['Time'].str.len()
distrometer_Data=distrometer_Data[distrometer_Data.Date_length == 10]
distrometer_Data=distrometer_Data[distrometer_Data.Time_length == 8]
distrometer_Data['datetime'] = distrometer_Data['Date'] + ' ' + distrometer_Data['Time']# added Date and time into new columns
distrometer_Data['datetime'] = [datetime.datetime.strptime(x, '%d/%m/%Y %H:%M:%S') for x in distrometer_Data['datetime']] #converts the dateTime format from string to python dateTime
distrometer_Data.index = distrometer_Data['datetime']
distrometer_Data = distrometer_Data.sort_index()

distrometer_Data.drop(distrometer_Data[(distrometer_Data[460] == '99999')].index,inplace =True)
distrometer_Data.drop(distrometer_Data[(distrometer_Data[2] != '00')].index,inplace =True)
distrometer_Data.drop(distrometer_Data[(distrometer_Data['Total Precipitation Rate (mm/hr)'] == '999.999')].index,inplace =True)
distrometer_Data.drop(distrometer_Data[(distrometer_Data['Total Precipitation Rate (mm/hr)'] == '1')].index,inplace =True)
distrometer_Data.iloc[:,7:8] = distrometer_Data.iloc[:,7:8].astype(float)
distrometer_Data.iloc[:,10:12] = distrometer_Data.iloc[:,10:12].astype(float)
#distrometer_Data.drop(distrometer_Data[(distrometer_Data['Total Precipitation Rate (mm/hr)'].isnull)].index,inplace =True)

distrometer_Data.iloc[:,14:520] = distrometer_Data.iloc[:,14:520].astype(float)

#distrometer_Data.to_csv(str(Data_Output_Folder) + 'maqs-distrometer_' + str(date_file_label)  + str(status) + str(version_number) + '.csv')

distrometer_Data['Accumulated Precipitation (mm)'] = distrometer_Data['Accumulated Precipitation (mm)'].astype(float)
distrometer_Data['Accumulated Precipitation_+1_offset'] = distrometer_Data['Accumulated Precipitation (mm)'].shift(periods=1)
distrometer_Data['Accumulated Precipitation (mm) per min'] = distrometer_Data['Accumulated Precipitation (mm)'] - distrometer_Data['Accumulated Precipitation_+1_offset']

distrometer_Data = distrometer_Data.drop(columns=['Date_length','Time_length', 'Accumulated Precipitation_+1_offset']) #'Time', 'Date', 

#distrometer_Data.iloc[:,7:8] = distrometer_Data.iloc[:,7:8].astype(float)
#distrometer_Data.iloc[:,10:12] = distrometer_Data.iloc[:,10:12].astype(float)
#distrometer_Data.iloc[:,14:16] = distrometer_Data.iloc[:,14:520].astype(float)

print(str(start))
print(str(end))

distrometer_Data = distrometer_Data[start:end]


Midnight_Precipitation_One = distrometer_Data[['Date', 'Time', 'Accumulated Precipitation (mm)', 'datetime']]
Midnight_Precipitation_One.rename(columns={'Accumulated Precipitation (mm)': 'Midnight Precipitation (mm)' }, inplace=True)

Midnight_Precipitation_One['Date_Offset_-1'] = Midnight_Precipitation_One['Date'].shift(periods=-1)
Midnight_Precipitation_One['Date_Offset_+1'] = Midnight_Precipitation_One['Date'].shift(periods=1)
Midnight_Precipitation_One['Date_Offset_-1'] = Midnight_Precipitation_One['Date_Offset_-1'].astype(str)
Midnight_Precipitation_One['Date_Offset_+1'] = Midnight_Precipitation_One['Date_Offset_+1'].astype(str)
Midnight_Precipitation_One['Date'] = Midnight_Precipitation_One['Date'].astype(str)
Midnight_Precipitation_One['Date_Flag'] = np.where((Midnight_Precipitation_One['Date'] == Midnight_Precipitation_One['Date_Offset_-1']) & (Midnight_Precipitation_One['Date'] == Midnight_Precipitation_One['Date_Offset_+1']),2,1)
Midnight_Precipitation_One=Midnight_Precipitation_One.loc[Midnight_Precipitation_One.Date_Flag == 1] 
Midnight_Precipitation_One['Midnight Precipitation_Offset_+1'] = Midnight_Precipitation_One['Midnight Precipitation (mm)'].shift(periods=1)
Midnight_Precipitation_One['Midnight Precipitation (mm)'] = Midnight_Precipitation_One['Midnight Precipitation (mm)'].astype(float)
Midnight_Precipitation_One['Midnight Precipitation_Offset_+1'] = Midnight_Precipitation_One['Midnight Precipitation_Offset_+1'].astype(float)
Midnight_Precipitation_One['Date_Flag'] = np.where((Midnight_Precipitation_One['Date'] == Midnight_Precipitation_One['Date_Offset_+1']),1,2)
Midnight_Precipitation_One['Midnight Precipitation (mm)'] = np.where((Midnight_Precipitation_One['Midnight Precipitation_Offset_+1'] < Midnight_Precipitation_One['Midnight Precipitation (mm)']) & (Midnight_Precipitation_One['Date_Flag'] == 1), Midnight_Precipitation_One['Midnight Precipitation_Offset_+1'], Midnight_Precipitation_One['Midnight Precipitation (mm)'])
Midnight_Precipitation_One = Midnight_Precipitation_One.drop(columns=['Date','Date_Offset_+1','Date', 'Time','Date_Offset_-1', 'Midnight Precipitation_Offset_+1', 'Date_Flag'])
#Midnight_Precipitation_One.to_csv(str(Data_Output_Folder) + 'maqs-distrometer_1_' + str(date_file_label)  + str(status) + str(version_number) + '.csv')

distrometer_Data['Midnight Precipitation Value (mm)'] = np.interp(distrometer_Data['datetime'], Midnight_Precipitation_One['datetime'], Midnight_Precipitation_One['Midnight Precipitation (mm)'])

distrometer_Data['Midnight Precipitation Value (mm)'] = distrometer_Data['Midnight Precipitation Value (mm)'].astype(float)
distrometer_Data.rename(columns={'Accumulated Precipitation (mm)': 'Raw Accumulated Precipitation (mm)' }, inplace=True)
distrometer_Data['Accumulated Precipitation (mm) since midnight'] = distrometer_Data['Raw Accumulated Precipitation (mm)'] - distrometer_Data['Midnight Precipitation Value (mm)']

distrometer_Data['Precipitation Classification'] = distrometer_Data['Precipitation Classification'].str.rstrip().astype(str)  
distrometer_Data['Other Precipitation Classification'] = distrometer_Data['Other Precipitation Classification'].str.rstrip().astype(str) 

distrometer_Data.drop(distrometer_Data[(distrometer_Data['Precipitation Classification'] == '-9999')].index,inplace =True)

#distrometer_Data = distrometer_Data.drop(columns=['Precipitation Classification'])

distrometer_Data['Precipitation Classification Symbols'] = distrometer_Data['Precipitation Classification']

distrometer_Data.rename(columns={'Precipitation Classification': 'Precipitation Classification Full'}, inplace=True)

distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == 'NP', 'No Precipitation', distrometer_Data['Precipitation Classification Full'])

distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '-RA', 'Light Rain', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == 'RA', 'Moderate Rain', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '+RA', 'Heavy Rain', distrometer_Data['Precipitation Classification Full'])

distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '-UP', 'Light Unknown Precipitation', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == 'UP', 'Moderate Unknown Precipitation', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '+UP', 'Heavy Unknown Precipitation', distrometer_Data['Precipitation Classification Full'])

distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '-DZ', 'Light Drizzle', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == 'DZ', 'Moderate Drizzle', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '+DZ', 'Heavy Drizzle', distrometer_Data['Precipitation Classification Full'])

distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '-FZDZ', 'Light Freezing Drizzle', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == 'FZDZ', 'Moderate Freezing Drizzle', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '+FZDZ', 'Heavy Freezing Drizzle', distrometer_Data['Precipitation Classification Full'])

distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '-RADZ', 'Light Drizzle with Rain', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == 'RADZ', 'Moderate Drizzle with Rain', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '+RADZ', 'Heavy Drizzle with Rain', distrometer_Data['Precipitation Classification Full'])

distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '-RA', 'Light Rain', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == 'RA', 'Moderate Rain', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '+RA', 'Heavy Rain', distrometer_Data['Precipitation Classification Full'])

distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '-FZRA', 'Light Freezing Rain', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == 'FZRA', 'Moderate Freezing Rain', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '+FZRA', 'Heavy Freezing Rain', distrometer_Data['Precipitation Classification Full'])

distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '-RASN', 'Light Rain and/or Drizzle with Snow', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == 'RASN', 'Moderate Rain and/or Drizzle with Snow', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '+RASN', 'Heavy Rain and/or Drizzle with Snow', distrometer_Data['Precipitation Classification Full'])

distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '-SN', 'Light Snow', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == 'SN', 'Moderate Snow', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '+SN', 'Heavy Snow', distrometer_Data['Precipitation Classification Full'])

distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '-SG', 'Light Snow Grains', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == 'SG', 'Moderate Snow Grains', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '+SG', 'Heavy Snow Grains', distrometer_Data['Precipitation Classification Full'])

distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '-GS', 'Light Soft Hail', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == 'GS', 'Moderate Soft Hail', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '+GS', 'Heavy Soft Hail', distrometer_Data['Precipitation Classification Full'])

distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == 'PE', 'Ice Pellets', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == 'PL', 'Ice Pellets', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == 'IC', 'Ice Crystals/Needles', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == 'GR', 'Hail', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '-GR', 'Slight Hail', distrometer_Data['Precipitation Classification Full'])

distrometer_Data.rename(columns={'Precipitation Classification Full':'Precipitation Classification'}, inplace=True)

distrometer_Data['Precipitation Classification Symbols'] = distrometer_Data['Other Precipitation Classification']

distrometer_Data.rename(columns={'Other Precipitation Classification': 'Precipitation Classification Full'}, inplace=True)

distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == 'NP', 'No Precipitation', distrometer_Data['Precipitation Classification Full'])

distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '-RA', 'Light Rain', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == 'RA', 'Moderate Rain', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '+RA', 'Heavy Rain', distrometer_Data['Precipitation Classification Full'])

distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '-UP', 'Light Unknown Precipitation', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == 'UP', 'Moderate Unknown Precipitation', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '+UP', 'Heavy Unknown Precipitation', distrometer_Data['Precipitation Classification Full'])

distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '-DZ', 'Light Drizzle', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == 'DZ', 'Moderate Drizzle', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '+DZ', 'Heavy Drizzle', distrometer_Data['Precipitation Classification Full'])

distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '-FZDZ', 'Light Freezing Drizzle', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == 'FZDZ', 'Moderate Freezing Drizzle', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '+FZDZ', 'Heavy Freezing Drizzle', distrometer_Data['Precipitation Classification Full'])

distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '-RADZ', 'Light Drizzle with Rain', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == 'RADZ', 'Moderate Drizzle with Rain', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '+RADZ', 'Heavy Drizzle with Rain', distrometer_Data['Precipitation Classification Full'])

distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '-RA', 'Light Rain', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == 'RA', 'Moderate Rain', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '+RA', 'Heavy Rain', distrometer_Data['Precipitation Classification Full'])

distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '-FZRA', 'Light Freezing Rain', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == 'FZRA', 'Moderate Freezing Rain', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '+FZRA', 'Heavy Freezing Rain', distrometer_Data['Precipitation Classification Full'])

distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '-RASN', 'Light Rain and/or Drizzle with Snow', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == 'RASN', 'Moderate Rain and/or Drizzle with Snow', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '+RASN', 'Heavy Rain and/or Drizzle with Snow', distrometer_Data['Precipitation Classification Full'])

distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '-SN', 'Light Snow', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == 'SN', 'Moderate Snow', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '+SN', 'Heavy Snow', distrometer_Data['Precipitation Classification Full'])

distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '-SG', 'Light Snow Grains', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == 'SG', 'Moderate Snow Grains', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '+SG', 'Heavy Snow Grains', distrometer_Data['Precipitation Classification Full'])

distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '-GS', 'Light Soft Hail', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == 'GS', 'Moderate Soft Hail', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == '+GS', 'Heavy Soft Hail', distrometer_Data['Precipitation Classification Full'])

distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == 'PE', 'Ice Pellets', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == 'PL', 'Ice Pellets', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == 'IC', 'Ice Crystals/Needles', distrometer_Data['Precipitation Classification Full'])
distrometer_Data['Precipitation Classification Full'] = np.where(distrometer_Data['Precipitation Classification Symbols'] == 'GR', 'Hail', distrometer_Data['Precipitation Classification Full'])

distrometer_Data.rename(columns={'Precipitation Classification Full':'Other Precipitation Classification'}, inplace=True)

#distrometer_Data['Minute Precipitation Measurement (mm)'] = distrometer_Data['Minute Precipitation Measurement (mm)'].astype(float)
#distrometer_Data['Minute Precipitation Measurement (mm)'] = np.where(distrometer_Data['Minute Precipitation Measurement (mm)']== -9.9, 0, distrometer_Data['Minute Precipitation Measurement (mm)'])

Midnight_Precipitation = distrometer_Data['Accumulated Precipitation (mm) since midnight']

distrometer_Data = distrometer_Data.drop(columns=['Midnight Precipitation Value (mm)','Precipitation Classification Symbols', 'datetime', 'Accumulated Precipitation (mm) since midnight'])

distrometer_Data['Total Precipitation Rate (mm/hr)'] = distrometer_Data['Total Precipitation Rate (mm/hr)'].astype(float)
distrometer_Data['Liquid Precipitation Rate (mm/hr)'] = distrometer_Data['Liquid Precipitation Rate (mm/hr)'].astype(float)
distrometer_Data['Solid Precipitation Rate (mm/hr)'] = distrometer_Data['Solid Precipitation Rate (mm/hr)'].astype(float)

distrometer_Data['qc_flag'] = np.where(distrometer_Data['Liquid Precipitation Rate (mm/hr)'] < 0, 3, 1)
distrometer_Data['qc_flag'] = np.where(distrometer_Data['Solid Precipitation Rate (mm/hr)'] < 0, 3, distrometer_Data['qc_flag'])
distrometer_Data['qc_flag'] = np.where(distrometer_Data['Liquid Precipitation Rate (mm/hr)'] > 300, 4, distrometer_Data['qc_flag'])
distrometer_Data['qc_flag'] = np.where(distrometer_Data['Solid Precipitation Rate (mm/hr)'] > 300, 5, distrometer_Data['qc_flag'])

distrometer_Data['Status Laser'] = distrometer_Data['Status Laser'].astype(float)
distrometer_Data['Static Signal'] = distrometer_Data['Static Signal'].astype(float)
distrometer_Data['Status Laser temperature (analogue)'] = distrometer_Data['Status Laser temperature (analogue)'].astype(float)
distrometer_Data['Status Laser temperature (digital)'] = distrometer_Data['Status Laser temperature (digital)'].astype(float)
distrometer_Data['Status Laser current (analogue)'] = distrometer_Data['Status Laser current (analogue)'].astype(float)
distrometer_Data['Status Laser current (digital)'] = distrometer_Data['Status Laser current (digital)'].astype(float)
distrometer_Data['Status Sensor supply'] = distrometer_Data['Status Sensor supply'].astype(float)
distrometer_Data['Status Current pane heating laser head'] = distrometer_Data['Status Current pane heating laser head'].astype(float)
distrometer_Data['Status Current pane heating receiver head'] = distrometer_Data['Status Current pane heating receiver head'].astype(float)
distrometer_Data['Status Temperature sensor'] = distrometer_Data['Status Temperature sensor'].astype(float)
distrometer_Data['Status Heating supply'] = distrometer_Data['Status Heating supply'].astype(float)
distrometer_Data['Status Current heating housing'] = distrometer_Data['Status Current heating housing'].astype(float)
distrometer_Data['Status Current heating heads'] = distrometer_Data['Status Current heating heads'].astype(float)
distrometer_Data['Status Current heating carriers'] = distrometer_Data['Status Current heating carriers'].astype(float)
distrometer_Data['Status Control output laser power'] = distrometer_Data['Status Control output laser power'].astype(float)

distrometer_Data['qc_flag'] = np.where(distrometer_Data['Status Laser'] == 1, 2, distrometer_Data['qc_flag'])
distrometer_Data['qc_flag'] = np.where(distrometer_Data['Static Signal'] == 1, 2, distrometer_Data['qc_flag'])
distrometer_Data['qc_flag'] = np.where(distrometer_Data['Status Laser temperature (analogue)'] == 1, 2, distrometer_Data['qc_flag'])
distrometer_Data['qc_flag'] = np.where(distrometer_Data['Status Laser temperature (digital)'] == 1, 2, distrometer_Data['qc_flag'])
distrometer_Data['qc_flag'] = np.where(distrometer_Data['Status Laser current (analogue)'] == 1, 2, distrometer_Data['qc_flag'])
distrometer_Data['qc_flag'] = np.where(distrometer_Data['Status Laser current (digital)'] == 1, 2, distrometer_Data['qc_flag'])
distrometer_Data['qc_flag'] = np.where(distrometer_Data['Status Sensor supply'] == 1, 2, distrometer_Data['qc_flag'])
distrometer_Data['qc_flag'] = np.where(distrometer_Data['Status Current pane heating laser head'] == 1, 2, distrometer_Data['qc_flag'])
distrometer_Data['qc_flag'] = np.where(distrometer_Data['Status Current pane heating receiver head'] == 1, 2, distrometer_Data['qc_flag'])
distrometer_Data['qc_flag'] = np.where(distrometer_Data['Status Temperature sensor'] == 1, 2, distrometer_Data['qc_flag'])
distrometer_Data['qc_flag'] = np.where(distrometer_Data['Status Heating supply'] == 1, 2, distrometer_Data['qc_flag'])
distrometer_Data['qc_flag'] = np.where(distrometer_Data['Status Current heating housing'] == 1, 2, distrometer_Data['qc_flag'])
distrometer_Data['qc_flag'] = np.where(distrometer_Data['Status Current heating heads'] == 1, 2, distrometer_Data['qc_flag'])
distrometer_Data['qc_flag'] = np.where(distrometer_Data['Status Current heating carriers'] == 1, 2, distrometer_Data['qc_flag'])
distrometer_Data['qc_flag'] = np.where(distrometer_Data['Status Control output laser power'] == 1, 2, distrometer_Data['qc_flag'])

#distrometer_Data.drop(distrometer_Data.iloc[:, 22:523], inplace=True, axis=1)

particles_type = 'particles' 

particles_name = 'hydrometeors' #could be particles, hydrometeor, ice particle etc
distrometer_Data.rename(columns={51: 'Total No. of ' + str(particles_name), 53: 'No. of very slow moving ' + str(particles_name) + ' (<0.15m/s)', 55: 'No. of very fast moving ' + str(particles_name) + ' (>20m/s)', 57: 'No. of low diameter ' + str(particles_name) + ' (< 0.15mm)' }, inplace=True)


classification = 'with no hydrometeor'
count_column = 59
volume_column = 60
distrometer_Data.rename(columns={int(count_column): 'No. of ' + str(particles_type) + ' ' + str(classification), int(volume_column): 'Total volume of ' + str(particles_type) + ' ' + str(classification) }, inplace=True)

classification = 'of unknown classification'
count_column = int(count_column) + 2
volume_column = int(volume_column) + 2
distrometer_Data.rename(columns={int(count_column): 'No. of ' + str(particles_type) + ' ' + str(classification), int(volume_column): 'Total volume of ' + str(particles_type) + ' ' + str(classification) }, inplace=True)

class_no = 1
classification = 'from Class ' + str(class_no)
count_column = int(count_column) + 2
volume_column = int(volume_column) + 2
distrometer_Data.rename(columns={int(count_column): 'No. of ' + str(particles_type) + ' ' + str(classification), int(volume_column): 'Total volume of ' + str(particles_type) + ' ' + str(classification) }, inplace=True)

class_no = class_no + 1
classification = 'from Class ' + str(class_no)
count_column = int(count_column) + 2
volume_column = int(volume_column) + 2
distrometer_Data.rename(columns={int(count_column): 'No. of ' + str(particles_type) + ' ' + str(classification), int(volume_column): 'Total volume of ' + str(particles_type) + ' ' + str(classification) }, inplace=True)

class_no = class_no + 1
classification = 'from Class ' + str(class_no)
count_column = int(count_column) + 2
volume_column = int(volume_column) + 2
distrometer_Data.rename(columns={int(count_column): 'No. of ' + str(particles_type) + ' ' + str(classification), int(volume_column): 'Total volume of ' + str(particles_type) + ' ' + str(classification) }, inplace=True)

class_no = class_no + 1
classification = 'from Class ' + str(class_no)
count_column = int(count_column) + 2
volume_column = int(volume_column) + 2
distrometer_Data.rename(columns={int(count_column): 'No. of ' + str(particles_type) + ' ' + str(classification), int(volume_column): 'Total volume of ' + str(particles_type) + ' ' + str(classification) }, inplace=True)

class_no = class_no + 1
classification = 'from Class ' + str(class_no)
count_column = int(count_column) + 2
volume_column = int(volume_column) + 2
distrometer_Data.rename(columns={int(count_column): 'No. of ' + str(particles_type) + ' ' + str(classification), int(volume_column): 'Total volume of ' + str(particles_type) + ' ' + str(classification) }, inplace=True)

class_no = class_no + 1
classification = 'from Class ' + str(class_no)
count_column = int(count_column) + 2
volume_column = int(volume_column) + 2
distrometer_Data.rename(columns={int(count_column): 'No. of ' + str(particles_type) + ' ' + str(classification), int(volume_column): 'Total volume of ' + str(particles_type) + ' ' + str(classification) }, inplace=True)

class_no = class_no + 1
classification = 'from Class ' + str(class_no)
count_column = int(count_column) + 2
volume_column = int(volume_column) + 2
distrometer_Data.rename(columns={int(count_column): 'No. of ' + str(particles_type) + ' ' + str(classification), int(volume_column): 'Total volume of ' + str(particles_type) + ' ' + str(classification) }, inplace=True)

class_no = class_no + 1
classification = 'from Class ' + str(class_no)
count_column = int(count_column) + 2
volume_column = int(volume_column) + 2
distrometer_Data.rename(columns={int(count_column): 'No. of ' + str(particles_type) + ' ' + str(classification), int(volume_column): 'Total volume of ' + str(particles_type) + ' ' + str(classification) }, inplace=True)

class_no = class_no + 1
classification = 'from Class ' + str(class_no)
count_column = int(count_column) + 2
volume_column = int(volume_column) + 2
distrometer_Data.rename(columns={int(count_column): 'No. of ' + str(particles_type) + ' ' + str(classification), int(volume_column): 'Total volume of ' + str(particles_type) + ' ' + str(classification) }, inplace=True)

start_speed_class = 1
current_speed_class = start_speed_class
current_speed_name = 'speed_' + str(current_speed_class)
current_speed = 0.0
list_names = [str(current_speed_name)]
list_speeds = [float(current_speed)]

current_speed_class = current_speed_class + 1
current_speed_name = 'speed_' + str(current_speed_class)
current_speed = np.round((current_speed + 0.2), decimals=1)
list_names.append(str(current_speed_name))
list_speeds.append(float(current_speed))

current_speed_class = current_speed_class + 1
current_speed_name = 'speed_' + str(current_speed_class)
current_speed = np.round((current_speed + 0.2), decimals=1)
list_names.append(str(current_speed_name))
list_speeds.append(float(current_speed))

current_speed_class = current_speed_class + 1
current_speed_name = 'speed_' + str(current_speed_class)
current_speed = np.round((current_speed + 0.2), decimals=1)
list_names.append(str(current_speed_name))
list_speeds.append(float(current_speed))

current_speed_class = current_speed_class + 1
current_speed_name = 'speed_' + str(current_speed_class)
current_speed = np.round((current_speed + 0.2), decimals=1)
list_names.append(str(current_speed_name))
list_speeds.append(float(current_speed))

current_speed_class = current_speed_class + 1
current_speed_name = 'speed_' + str(current_speed_class)
current_speed = np.round((current_speed + 0.2), decimals=1)
list_names.append(str(current_speed_name))
list_speeds.append(float(current_speed))

current_speed_class = current_speed_class + 1
current_speed_name = 'speed_' + str(current_speed_class)
current_speed = np.round((current_speed + 0.4), decimals=1)
list_names.append(str(current_speed_name))
list_speeds.append(float(current_speed))

current_speed_class = current_speed_class + 1
current_speed_name = 'speed_' + str(current_speed_class)
current_speed = np.round((current_speed + 0.4), decimals=1)
list_names.append(str(current_speed_name))
list_speeds.append(float(current_speed))

current_speed_class = current_speed_class + 1
current_speed_name = 'speed_' + str(current_speed_class)
current_speed = np.round((current_speed + 0.4), decimals=1)
list_names.append(str(current_speed_name))
list_speeds.append(float(current_speed))

current_speed_class = current_speed_class + 1
current_speed_name = 'speed_' + str(current_speed_class)
current_speed = np.round((current_speed + 0.4), decimals=1)
list_names.append(str(current_speed_name))
list_speeds.append(float(current_speed))

current_speed_class = current_speed_class + 1
current_speed_name = 'speed_' + str(current_speed_class)
current_speed = np.round((current_speed + 0.4), decimals=1)
list_names.append(str(current_speed_name))
list_speeds.append(float(current_speed))

current_speed_class = current_speed_class + 1
current_speed_name = 'speed_' + str(current_speed_class)
current_speed = np.round((current_speed + 0.4), decimals=1)
list_names.append(str(current_speed_name))
list_speeds.append(float(current_speed))

current_speed_class = current_speed_class + 1
current_speed_name = 'speed_' + str(current_speed_class)
current_speed = np.round((current_speed + 0.8), decimals=1)
list_names.append(str(current_speed_name))
list_speeds.append(float(current_speed))

current_speed_class = current_speed_class + 1
current_speed_name = 'speed_' + str(current_speed_class)
current_speed = np.round((current_speed + 0.8), decimals=1)
list_names.append(str(current_speed_name))
list_speeds.append(float(current_speed))

current_speed_class = current_speed_class + 1
current_speed_name = 'speed_' + str(current_speed_class)
current_speed = np.round((current_speed + 0.8), decimals=1)
list_names.append(str(current_speed_name))
list_speeds.append(float(current_speed))

current_speed_class = current_speed_class + 1
current_speed_name = 'speed_' + str(current_speed_class)
current_speed = np.round((current_speed + 0.8), decimals=1)
list_names.append(str(current_speed_name))
list_speeds.append(float(current_speed))

current_speed_class = current_speed_class + 1
current_speed_name = 'speed_' + str(current_speed_class)
current_speed = np.round((current_speed + 0.8), decimals=1)
list_names.append(str(current_speed_name))
list_speeds.append(float(current_speed))

current_speed_class = current_speed_class + 1
current_speed_name = 'speed_' + str(current_speed_class)
current_speed = np.round((current_speed + 0.8), decimals=1)
list_names.append(str(current_speed_name))
list_speeds.append(float(current_speed))

current_speed_class = current_speed_class + 1
current_speed_name = 'speed_' + str(current_speed_class)
current_speed = np.round((current_speed + 0.8), decimals=0)
list_names.append(str(current_speed_name))
list_speeds.append(float(current_speed))

current_speed_class = current_speed_class + 1
current_speed_name = 'speed_' + str(current_speed_class)
current_speed = np.round((current_speed + 1), decimals=0)
list_names.append(str(current_speed_name))
list_speeds.append(float(current_speed))

current_speed_class = current_speed_class + 1
final_speed_name = 'speed_' + str(current_speed_class)
final_speed = np.round((current_speed + 10), decimals=0)
list_names.append(str(final_speed_name))
list_speeds.append(float(final_speed))

speed_dict = {list_names[i]: list_speeds[i] for i in range(len(list_names))}
#print(speed_dict)

start_diameter_class = 1
current_diameter_class = start_diameter_class
current_diameter_name = 'diameter_' + str(current_diameter_class)
current_diameter = 0.125
list_class = [str(current_diameter_name)]
list_diameter = [float(current_diameter)]

current_diameter_class = current_diameter_class + 1
current_diameter_name = 'diameter_' + str(current_diameter_class)
current_diameter = np.round((current_diameter + 0.125), decimals=3)
list_class.append(str(current_diameter_name))
list_diameter.append(float(current_diameter))

current_diameter_class = current_diameter_class + 1
current_diameter_name = 'diameter_' + str(current_diameter_class)
current_diameter = np.round((current_diameter + 0.125), decimals=3)
list_class.append(str(current_diameter_name))
list_diameter.append(float(current_diameter))

current_diameter_class = current_diameter_class + 1
current_diameter_name = 'diameter_' + str(current_diameter_class)
current_diameter = np.round((current_diameter + 0.125), decimals=3)
list_class.append(str(current_diameter_name))
list_diameter.append(float(current_diameter))

current_diameter_class = current_diameter_class + 1
current_diameter_name = 'diameter_' + str(current_diameter_class)
current_diameter = np.round((current_diameter + 0.25), decimals=3)
list_class.append(str(current_diameter_name))
list_diameter.append(float(current_diameter))

current_diameter_class = current_diameter_class + 1
current_diameter_name = 'diameter_' + str(current_diameter_class)
current_diameter = np.round((current_diameter + 0.25), decimals=3)
list_class.append(str(current_diameter_name))
list_diameter.append(float(current_diameter))

current_diameter_class = current_diameter_class + 1
current_diameter_name = 'diameter_' + str(current_diameter_class)
current_diameter = np.round((current_diameter + 0.25), decimals=3)
list_class.append(str(current_diameter_name))
list_diameter.append(float(current_diameter))

current_diameter_class = current_diameter_class + 1
current_diameter_name = 'diameter_' + str(current_diameter_class)
current_diameter = np.round((current_diameter + 0.25), decimals=3)
list_class.append(str(current_diameter_name))
list_diameter.append(float(current_diameter))

current_diameter_class = current_diameter_class + 1
current_diameter_name = 'diameter_' + str(current_diameter_class)
current_diameter = np.round((current_diameter + 0.25), decimals=3)
list_class.append(str(current_diameter_name))
list_diameter.append(float(current_diameter))

current_diameter_class = current_diameter_class + 1
current_diameter_name = 'diameter_' + str(current_diameter_class)
current_diameter = np.round((current_diameter + 0.25), decimals=3)
list_class.append(str(current_diameter_name))
list_diameter.append(float(current_diameter))

current_diameter_class = current_diameter_class + 1
current_diameter_name = 'diameter_' + str(current_diameter_class)
current_diameter = np.round((current_diameter + 0.5), decimals=3)
list_class.append(str(current_diameter_name))
list_diameter.append(float(current_diameter))

current_diameter_class = current_diameter_class + 1
current_diameter_name = 'diameter_' + str(current_diameter_class)
current_diameter = np.round((current_diameter + 0.5), decimals=3)
list_class.append(str(current_diameter_name))
list_diameter.append(float(current_diameter))

current_diameter_class = current_diameter_class + 1
current_diameter_name = 'diameter_' + str(current_diameter_class)
current_diameter = np.round((current_diameter + 0.5), decimals=3)
list_class.append(str(current_diameter_name))
list_diameter.append(float(current_diameter))

current_diameter_class = current_diameter_class + 1
current_diameter_name = 'diameter_' + str(current_diameter_class)
current_diameter = np.round((current_diameter + 0.5), decimals=3)
list_class.append(str(current_diameter_name))
list_diameter.append(float(current_diameter))

current_diameter_class = current_diameter_class + 1
current_diameter_name = 'diameter_' + str(current_diameter_class)
current_diameter = np.round((current_diameter + 0.5), decimals=3)
list_class.append(str(current_diameter_name))
list_diameter.append(float(current_diameter))

current_diameter_class = current_diameter_class + 1
current_diameter_name = 'diameter_' + str(current_diameter_class)
current_diameter = np.round((current_diameter + 0.5), decimals=3)
list_class.append(str(current_diameter_name))
list_diameter.append(float(current_diameter))

current_diameter_class = current_diameter_class + 1
current_diameter_name = 'diameter_' + str(current_diameter_class)
current_diameter = np.round((current_diameter + 0.5), decimals=3)
list_class.append(str(current_diameter_name))
list_diameter.append(float(current_diameter))

current_diameter_class = current_diameter_class + 1
current_diameter_name = 'diameter_' + str(current_diameter_class)
current_diameter = np.round((current_diameter + 0.5), decimals=3)
list_class.append(str(current_diameter_name))
list_diameter.append(float(current_diameter))

current_diameter_class = current_diameter_class + 1
current_diameter_name = 'diameter_' + str(current_diameter_class)
current_diameter = np.round((current_diameter + 0.5), decimals=3)
list_class.append(str(current_diameter_name))
list_diameter.append(float(current_diameter))

current_diameter_class = current_diameter_class + 1
current_diameter_name = 'diameter_' + str(current_diameter_class)
current_diameter = np.round((current_diameter + 0.5), decimals=3)
list_class.append(str(current_diameter_name))
list_diameter.append(float(current_diameter))

current_diameter_class = current_diameter_class + 1
current_diameter_name = 'diameter_' + str(current_diameter_class)
current_diameter = np.round((current_diameter + 0.5), decimals=3)
list_class.append(str(current_diameter_name))
list_diameter.append(float(current_diameter))

current_diameter_class = current_diameter_class + 1
current_diameter_name = 'diameter_' + str(current_diameter_class)
current_diameter = np.round((current_diameter + 0.5), decimals=3)
list_class.append(str(current_diameter_name))
list_diameter.append(float(current_diameter))

diameter_dict = {list_class[i]: list_diameter[i] for i in range(len(list_class))}
print(diameter_dict)


count_column = int(volume_column) + 1
current_diameter_class = start_diameter_class
diameter_boundary_1 = 'diameter_' + str(current_diameter_class)
diameter_boundary_2 = 'diameter_' + str(int(current_diameter_class) + 1)
current_speed_class = start_speed_class
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)
start_column_name = label

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)
end_column_name = label

summary_column_name = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm'

summary_data = distrometer_Data.loc[:, start_column_name:end_column_name]
summary_data = summary_data.astype(float)
summary_data[str(summary_column_name)] = summary_data[list(summary_data.filter(regex=str(summary_column_name)))].sum(axis=1)
summary_diameter_column = summary_data[str(summary_column_name)]
distrometer_Data[str(summary_column_name)] = pd.Series(summary_diameter_column)

#summary_data.to_csv(str(Data_Output_Folder) + 'maqs-Summary_2_' + str(date_file_label)  + str(status) + str(version_number) + '.csv')


#summary_data.sum(axis=1)
#summary_column = summary_data[str(summary_column_name)]
#distrometer_Data[str(summary_column_name)] = pd.Series(summary_column)

count_column = count_column + 1
current_diameter_class = current_diameter_class + 1
diameter_boundary_1 = 'diameter_' + str(current_diameter_class)
diameter_boundary_2 = 'diameter_' + str(int(current_diameter_class) + 1)
current_speed_class = start_speed_class
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)
start_column_name = label

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)
end_column_name = label

summary_column_name = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm'

summary_data = distrometer_Data.loc[:, start_column_name:end_column_name]
summary_data = summary_data.astype(float)
summary_data[str(summary_column_name)] = summary_data[list(summary_data.filter(regex=str(summary_column_name)))].sum(axis=1)
summary_diameter_column = summary_data[str(summary_column_name)]
distrometer_Data[str(summary_column_name)] = pd.Series(summary_diameter_column)

count_column = count_column + 1
current_diameter_class = current_diameter_class + 1
diameter_boundary_1 = 'diameter_' + str(current_diameter_class)
diameter_boundary_2 = 'diameter_' + str(int(current_diameter_class) + 1)
current_speed_class = start_speed_class
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)
start_column_name = label

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)
end_column_name = label

summary_column_name = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm'

summary_data = distrometer_Data.loc[:, start_column_name:end_column_name]
summary_data = summary_data.astype(float)
summary_data[str(summary_column_name)] = summary_data[list(summary_data.filter(regex=str(summary_column_name)))].sum(axis=1)
summary_diameter_column = summary_data[str(summary_column_name)]
distrometer_Data[str(summary_column_name)] = pd.Series(summary_diameter_column)


count_column = count_column + 1
current_diameter_class = current_diameter_class + 1
diameter_boundary_1 = 'diameter_' + str(current_diameter_class)
diameter_boundary_2 = 'diameter_' + str(int(current_diameter_class) + 1)
current_speed_class = start_speed_class
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)
start_column_name = label

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)
end_column_name = label

summary_column_name = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm'

summary_data = distrometer_Data.loc[:, start_column_name:end_column_name]
summary_data = summary_data.astype(float)
summary_data[str(summary_column_name)] = summary_data[list(summary_data.filter(regex=str(summary_column_name)))].sum(axis=1)
summary_diameter_column = summary_data[str(summary_column_name)]
distrometer_Data[str(summary_column_name)] = pd.Series(summary_diameter_column)

count_column = count_column + 1
current_diameter_class = current_diameter_class + 1
diameter_boundary_1 = 'diameter_' + str(current_diameter_class)
diameter_boundary_2 = 'diameter_' + str(int(current_diameter_class) + 1)
current_speed_class = start_speed_class
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)
start_column_name = label

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)
end_column_name = label

summary_column_name = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm'

summary_data = distrometer_Data.loc[:, start_column_name:end_column_name]
summary_data = summary_data.astype(float)
summary_data[str(summary_column_name)] = summary_data[list(summary_data.filter(regex=str(summary_column_name)))].sum(axis=1)
summary_diameter_column = summary_data[str(summary_column_name)]
distrometer_Data[str(summary_column_name)] = pd.Series(summary_diameter_column)

count_column = count_column + 1
current_diameter_class = current_diameter_class + 1
diameter_boundary_1 = 'diameter_' + str(current_diameter_class)
diameter_boundary_2 = 'diameter_' + str(int(current_diameter_class) + 1)
current_speed_class = start_speed_class
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)
start_column_name = label

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)
end_column_name = label

summary_column_name = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm'

summary_data = distrometer_Data.loc[:, start_column_name:end_column_name]
summary_data = summary_data.astype(float)
summary_data[str(summary_column_name)] = summary_data[list(summary_data.filter(regex=str(summary_column_name)))].sum(axis=1)
summary_diameter_column = summary_data[str(summary_column_name)]
distrometer_Data[str(summary_column_name)] = pd.Series(summary_diameter_column)


count_column = count_column + 1
current_diameter_class = current_diameter_class + 1
diameter_boundary_1 = 'diameter_' + str(current_diameter_class)
diameter_boundary_2 = 'diameter_' + str(int(current_diameter_class) + 1)
current_speed_class = start_speed_class
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)
start_column_name = label

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)
end_column_name = label

summary_column_name = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm'

summary_data = distrometer_Data.loc[:, start_column_name:end_column_name]
summary_data = summary_data.astype(float)
summary_data[str(summary_column_name)] = summary_data[list(summary_data.filter(regex=str(summary_column_name)))].sum(axis=1)
summary_diameter_column = summary_data[str(summary_column_name)]
distrometer_Data[str(summary_column_name)] = pd.Series(summary_diameter_column)


count_column = count_column + 1
current_diameter_class = current_diameter_class + 1
diameter_boundary_1 = 'diameter_' + str(current_diameter_class)
diameter_boundary_2 = 'diameter_' + str(int(current_diameter_class) + 1)
current_speed_class = start_speed_class
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)
start_column_name = label

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)
end_column_name = label

summary_column_name = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm'

summary_data = distrometer_Data.loc[:, start_column_name:end_column_name]
summary_data = summary_data.astype(float)
summary_data[str(summary_column_name)] = summary_data[list(summary_data.filter(regex=str(summary_column_name)))].sum(axis=1)
summary_diameter_column = summary_data[str(summary_column_name)]
distrometer_Data[str(summary_column_name)] = pd.Series(summary_diameter_column)


count_column = count_column + 1
current_diameter_class = current_diameter_class + 1
diameter_boundary_1 = 'diameter_' + str(current_diameter_class)
diameter_boundary_2 = 'diameter_' + str(int(current_diameter_class) + 1)
current_speed_class = start_speed_class
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)
start_column_name = label

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)
end_column_name = label

summary_column_name = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm'

summary_data = distrometer_Data.loc[:, start_column_name:end_column_name]
summary_data = summary_data.astype(float)
summary_data[str(summary_column_name)] = summary_data[list(summary_data.filter(regex=str(summary_column_name)))].sum(axis=1)
summary_diameter_column = summary_data[str(summary_column_name)]
distrometer_Data[str(summary_column_name)] = pd.Series(summary_diameter_column)


count_column = count_column + 1
current_diameter_class = current_diameter_class + 1
diameter_boundary_1 = 'diameter_' + str(current_diameter_class)
diameter_boundary_2 = 'diameter_' + str(int(current_diameter_class) + 1)
current_speed_class = start_speed_class
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)
start_column_name = label

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)
end_column_name = label

summary_column_name = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm'

summary_data = distrometer_Data.loc[:, start_column_name:end_column_name]
summary_data = summary_data.astype(float)
summary_data[str(summary_column_name)] = summary_data[list(summary_data.filter(regex=str(summary_column_name)))].sum(axis=1)
summary_diameter_column = summary_data[str(summary_column_name)]
distrometer_Data[str(summary_column_name)] = pd.Series(summary_diameter_column)


count_column = count_column + 1
current_diameter_class = current_diameter_class + 1
diameter_boundary_1 = 'diameter_' + str(current_diameter_class)
diameter_boundary_2 = 'diameter_' + str(int(current_diameter_class) + 1)
current_speed_class = start_speed_class
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)
start_column_name = label

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)
end_column_name = label

summary_column_name = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm'

summary_data = distrometer_Data.loc[:, start_column_name:end_column_name]
summary_data = summary_data.astype(float)
summary_data[str(summary_column_name)] = summary_data[list(summary_data.filter(regex=str(summary_column_name)))].sum(axis=1)
summary_diameter_column = summary_data[str(summary_column_name)]
distrometer_Data[str(summary_column_name)] = pd.Series(summary_diameter_column)

count_column = count_column + 1
current_diameter_class = current_diameter_class + 1
diameter_boundary_1 = 'diameter_' + str(current_diameter_class)
diameter_boundary_2 = 'diameter_' + str(int(current_diameter_class) + 1)
current_speed_class = start_speed_class
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)
start_column_name = label

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)
end_column_name = label

summary_column_name = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm'

summary_data = distrometer_Data.loc[:, start_column_name:end_column_name]
summary_data = summary_data.astype(float)
summary_data[str(summary_column_name)] = summary_data[list(summary_data.filter(regex=str(summary_column_name)))].sum(axis=1)
summary_diameter_column = summary_data[str(summary_column_name)]
distrometer_Data[str(summary_column_name)] = pd.Series(summary_diameter_column)

count_column = count_column + 1
current_diameter_class = current_diameter_class + 1
diameter_boundary_1 = 'diameter_' + str(current_diameter_class)
diameter_boundary_2 = 'diameter_' + str(int(current_diameter_class) + 1)
current_speed_class = start_speed_class
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)
start_column_name = label

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)
end_column_name = label

summary_column_name = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm'

summary_data = distrometer_Data.loc[:, start_column_name:end_column_name]
summary_data = summary_data.astype(float)
summary_data[str(summary_column_name)] = summary_data[list(summary_data.filter(regex=str(summary_column_name)))].sum(axis=1)
summary_diameter_column = summary_data[str(summary_column_name)]
distrometer_Data[str(summary_column_name)] = pd.Series(summary_diameter_column)

count_column = count_column + 1
current_diameter_class = current_diameter_class + 1
diameter_boundary_1 = 'diameter_' + str(current_diameter_class)
diameter_boundary_2 = 'diameter_' + str(int(current_diameter_class) + 1)
current_speed_class = start_speed_class
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)
start_column_name = label

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)
end_column_name = label

summary_column_name = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm'

summary_data = distrometer_Data.loc[:, start_column_name:end_column_name]
summary_data = summary_data.astype(float)
summary_data[str(summary_column_name)] = summary_data[list(summary_data.filter(regex=str(summary_column_name)))].sum(axis=1)
summary_diameter_column = summary_data[str(summary_column_name)]
distrometer_Data[str(summary_column_name)] = pd.Series(summary_diameter_column)

count_column = count_column + 1
current_diameter_class = current_diameter_class + 1
diameter_boundary_1 = 'diameter_' + str(current_diameter_class)
diameter_boundary_2 = 'diameter_' + str(int(current_diameter_class) + 1)
current_speed_class = start_speed_class
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)
start_column_name = label

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)
end_column_name = label

summary_column_name = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm'

summary_data = distrometer_Data.loc[:, start_column_name:end_column_name]
summary_data = summary_data.astype(float)
summary_data[str(summary_column_name)] = summary_data[list(summary_data.filter(regex=str(summary_column_name)))].sum(axis=1)
summary_diameter_column = summary_data[str(summary_column_name)]
distrometer_Data[str(summary_column_name)] = pd.Series(summary_diameter_column)

count_column = count_column + 1
current_diameter_class = current_diameter_class + 1
diameter_boundary_1 = 'diameter_' + str(current_diameter_class)
diameter_boundary_2 = 'diameter_' + str(int(current_diameter_class) + 1)
current_speed_class = start_speed_class
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)
start_column_name = label

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)
end_column_name = label

summary_column_name = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm'

summary_data = distrometer_Data.loc[:, start_column_name:end_column_name]
summary_data = summary_data.astype(float)
summary_data[str(summary_column_name)] = summary_data[list(summary_data.filter(regex=str(summary_column_name)))].sum(axis=1)
summary_diameter_column = summary_data[str(summary_column_name)]
distrometer_Data[str(summary_column_name)] = pd.Series(summary_diameter_column)


count_column = count_column + 1
current_diameter_class = current_diameter_class + 1
diameter_boundary_1 = 'diameter_' + str(current_diameter_class)
diameter_boundary_2 = 'diameter_' + str(int(current_diameter_class) + 1)
current_speed_class = start_speed_class
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)
start_column_name = label

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)
end_column_name = label

summary_column_name = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm'

summary_data = distrometer_Data.loc[:, start_column_name:end_column_name]
summary_data = summary_data.astype(float)
summary_data[str(summary_column_name)] = summary_data[list(summary_data.filter(regex=str(summary_column_name)))].sum(axis=1)
summary_diameter_column = summary_data[str(summary_column_name)]
distrometer_Data[str(summary_column_name)] = pd.Series(summary_diameter_column)

count_column = count_column + 1
current_diameter_class = current_diameter_class + 1
diameter_boundary_1 = 'diameter_' + str(current_diameter_class)
diameter_boundary_2 = 'diameter_' + str(int(current_diameter_class) + 1)
current_speed_class = start_speed_class
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)
start_column_name = label

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)
end_column_name = label

summary_column_name = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm'

summary_data = distrometer_Data.loc[:, start_column_name:end_column_name]
summary_data = summary_data.astype(float)
summary_data[str(summary_column_name)] = summary_data[list(summary_data.filter(regex=str(summary_column_name)))].sum(axis=1)
summary_diameter_column = summary_data[str(summary_column_name)]
distrometer_Data[str(summary_column_name)] = pd.Series(summary_diameter_column)

count_column = count_column + 1
current_diameter_class = current_diameter_class + 1
diameter_boundary_1 = 'diameter_' + str(current_diameter_class)
diameter_boundary_2 = 'diameter_' + str(int(current_diameter_class) + 1)
current_speed_class = start_speed_class
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)
start_column_name = label

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)
end_column_name = label

summary_column_name = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm'

summary_data = distrometer_Data.loc[:, start_column_name:end_column_name]
summary_data = summary_data.astype(float)
summary_data[str(summary_column_name)] = summary_data[list(summary_data.filter(regex=str(summary_column_name)))].sum(axis=1)
summary_diameter_column = summary_data[str(summary_column_name)]
distrometer_Data[str(summary_column_name)] = pd.Series(summary_diameter_column)

count_column = count_column + 1
current_diameter_class = current_diameter_class + 1
diameter_boundary_1 = 'diameter_' + str(current_diameter_class)
diameter_boundary_2 = 'diameter_' + str(int(current_diameter_class) + 1)
current_speed_class = start_speed_class
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)
start_column_name = label

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)
end_column_name = label

summary_column_name = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm'

summary_data = distrometer_Data.loc[:, start_column_name:end_column_name]
summary_data = summary_data.astype(float)
summary_data[str(summary_column_name)] = summary_data[list(summary_data.filter(regex=str(summary_column_name)))].sum(axis=1)
summary_diameter_column = summary_data[str(summary_column_name)]
distrometer_Data[str(summary_column_name)] = pd.Series(summary_diameter_column)

count_column = count_column + 1
current_diameter_class = current_diameter_class + 1
diameter_boundary_1 = 'diameter_' + str(current_diameter_class)
diameter_boundary_2 = 'diameter_' + str(int(current_diameter_class) + 1)
current_speed_class = start_speed_class
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)
start_column_name = label

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)
end_column_name = label

summary_column_name = 'No. of particles with ' + str(diameter_dict[(str(diameter_boundary_1))]) + 'mm < diameter < ' + str(diameter_dict[(str(diameter_boundary_2))])  + 'mm'

summary_data = distrometer_Data.loc[:, start_column_name:end_column_name]
summary_data = summary_data.astype(float)
summary_data[str(summary_column_name)] = summary_data[list(summary_data.filter(regex=str(summary_column_name)))].sum(axis=1)
summary_diameter_column = summary_data[str(summary_column_name)]
distrometer_Data[str(summary_column_name)] = pd.Series(summary_diameter_column)

count_column = count_column + 1
current_diameter_class = current_diameter_class + 1
diameter_boundary_1 = 'diameter_' + str(current_diameter_class)
diameter_boundary_2 = 'diameter_' + str(int(current_diameter_class) + 1)
current_speed_class = start_speed_class
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with diameter > ' + str(diameter_dict[(str(diameter_boundary_1))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)
start_column_name = label

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with diameter > ' + str(diameter_dict[(str(diameter_boundary_1))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with diameter > ' + str(diameter_dict[(str(diameter_boundary_1))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with diameter > ' + str(diameter_dict[(str(diameter_boundary_1))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with diameter > ' + str(diameter_dict[(str(diameter_boundary_1))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with diameter > ' + str(diameter_dict[(str(diameter_boundary_1))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with diameter > ' + str(diameter_dict[(str(diameter_boundary_1))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with diameter > ' + str(diameter_dict[(str(diameter_boundary_1))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with diameter > ' + str(diameter_dict[(str(diameter_boundary_1))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with diameter > ' + str(diameter_dict[(str(diameter_boundary_1))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with diameter > ' + str(diameter_dict[(str(diameter_boundary_1))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with diameter > ' + str(diameter_dict[(str(diameter_boundary_1))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with diameter > ' + str(diameter_dict[(str(diameter_boundary_1))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with diameter > ' + str(diameter_dict[(str(diameter_boundary_1))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with diameter > ' + str(diameter_dict[(str(diameter_boundary_1))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with diameter > ' + str(diameter_dict[(str(diameter_boundary_1))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with diameter > ' + str(diameter_dict[(str(diameter_boundary_1))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with diameter > ' + str(diameter_dict[(str(diameter_boundary_1))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with diameter > ' + str(diameter_dict[(str(diameter_boundary_1))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)

count_column = count_column + 1
current_speed_class = current_speed_class + 1
speed_boundary_1 = 'speed_' + str(current_speed_class)
speed_boundary_2 = 'speed_' + str(int(current_speed_class) + 1)
label = 'No. of particles with diameter > ' + str(diameter_dict[(str(diameter_boundary_1))])  + 'mm and ' + str(speed_dict[(str(speed_boundary_1))]) + 'm/s < speed < ' + str(speed_dict[(str(speed_boundary_2))]) + 'm/s'
distrometer_Data.rename(columns={int(count_column): str(label) }, inplace=True)
end_column_name = label

summary_column_name = 'No. of particles with diameter > ' + str(diameter_dict[(str(diameter_boundary_1))])  + 'mm'

summary_data = distrometer_Data.loc[:, start_column_name:end_column_name]
summary_data = summary_data.astype(float)
summary_data[str(summary_column_name)] = summary_data[list(summary_data.filter(regex=str(summary_column_name)))].sum(axis=1)
summary_diameter_column = summary_data[str(summary_column_name)]
distrometer_Data[str(summary_column_name)] = pd.Series(summary_diameter_column)

distrometer_Data = distrometer_Data.drop(columns=[521,522])
distrometer_Data = distrometer_Data.drop(columns=[52,54,56,58])

distrometer_Data.drop(distrometer_Data.iloc[:, 22:51], inplace=True, axis=1)
distrometer_Data.drop(distrometer_Data.iloc[:, 0:13], inplace=True, axis=1)

distrometer_Data['Accumulated Precipitation (mm) since midnight'] = pd.Series(Midnight_Precipitation)

#distrometer_Data['Accumulated Precipitation (mm)'] = pd.Series(Midnight_Precipitation)
#distrometer_Data.rename(columns={'Accumulated Precipitation (mm) since midnight':'Accumulated Precipitation (mm)'}, inplace=True)

#distrometer_Data = distrometer_Data.reindex(sorted(distrometer_Data.columns), axis=1)
distrometer_Data.fillna(0, inplace=True)

Prec_Class = distrometer_Data['Precipitation Classification']
qc_distrometer_flag = distrometer_Data['qc_flag']
distrometer_Data = distrometer_Data.drop(columns=['Precipitation Classification', 'qc_flag'])
distrometer_Data = distrometer_Data.astype(float)
distrometer_Data['Precipitation Classification'] = pd.Series(Prec_Class)
distrometer_Data['qc_flag'] = pd.Series(qc_distrometer_flag)

start_Error_1 = datetime.datetime(2019,7,4,9,0,00) # logging in simon building
end_Error_1 = datetime.datetime(2019,7,4,13,0,00) 
distrometer_Data.loc[start_Error_1:end_Error_1, ('qc_flag')] = 2

start_Error_2 = datetime.datetime(2019,7,10,14,40,00) # logging in simon building
end_Error_2 = datetime.datetime(2019,7,11,14,20,00) 
distrometer_Data.loc[start_Error_2:end_Error_2, ('qc_flag')] = 2

if str(start_year_month_str) == '201911':
    distrometer_Data.drop(distrometer_Data.iloc[:, 474:538], inplace=True, axis=1)
else:
    pass

distrometer_Data['Total Rate (mm/hr)'] = distrometer_Data['Liquid Precipitation Rate (mm/hr)'] + distrometer_Data['Solid Precipitation Rate (mm/hr)']

distrometer_Data['Total_+_5_per_cent'] = distrometer_Data['Total Precipitation Rate (mm/hr)'] * 1.05
distrometer_Data['Total_-_5_per_cent'] = distrometer_Data['Total Precipitation Rate (mm/hr)'] * 0.95

distrometer_Data['Total Rate (mm/hr)'] = distrometer_Data['Total Rate (mm/hr)'].astype(float)
distrometer_Data['Total_+_5_per_cent'] = distrometer_Data['Total_+_5_per_cent'].astype(float)
distrometer_Data['Total_-_5_per_cent'] = distrometer_Data['Total_-_5_per_cent'].astype(float)

distrometer_Data['qc_flag'] = np.where((distrometer_Data['Total Rate (mm/hr)'] < distrometer_Data['Total_-_5_per_cent']), 2, distrometer_Data['qc_flag'])
distrometer_Data['qc_flag'] = np.where((distrometer_Data['Total Rate (mm/hr)'] > distrometer_Data['Total_+_5_per_cent']), 2, distrometer_Data['qc_flag'])
distrometer_Data = distrometer_Data.drop(columns=['Total Rate (mm/hr)', 'Total_+_5_per_cent', 'Total_-_5_per_cent'])


distrometer_Data['qc_flag'] = distrometer_Data['qc_flag'].astype(str)

plt.plot(distrometer_Data['Total Precipitation Rate (mm/hr)'], label='Total Rain Rate (mm/hr)')
plt.plot(distrometer_Data['Solid Precipitation Rate (mm/hr)'], label='Solid Rain Rate (mm/hr)')
plt.plot(distrometer_Data['Liquid Precipitation Rate (mm/hr)'], label='Liquid Rain Rate (mm/hr)')
plt.legend()
plt.ylabel('mm/hr')
plt.rc('figure', figsize=(60, 100))
font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 16}

plt.rc('font', **font)
#plt.ylim(10, 30)
plt.figure()
plt.show()


Distrometer_Folder = str(Data_Output_Folder) + str(start.strftime("%Y")) + '/' + str(date_file_label) + '/Disdrometer/'
check_Folder = os.path.isdir(Distrometer_Folder)
if not check_Folder:
    os.makedirs(Distrometer_Folder)
    print("created folder : ", Distrometer_Folder)
else:
    print(Distrometer_Folder, "folder already exists.")

distrometer_Data.to_csv(str(Distrometer_Folder) + 'maqs-disdrometer_precipitation_' + str(date_file_label)  + str(status) + str(version_number) + '.csv')

distrometer_Data['TimeDateSince'] = distrometer_Data.index-datetime.datetime(1970,1,1,0,0,00)
distrometer_Data['TimeSecondsSince'] = distrometer_Data['TimeDateSince'].dt.total_seconds()
distrometer_Data['day_year'] = pd.DatetimeIndex(distrometer_Data['TimeDateSince'].index).dayofyear
distrometer_Data['year'] = pd.DatetimeIndex(distrometer_Data['TimeDateSince'].index).year
distrometer_Data['month'] = pd.DatetimeIndex(distrometer_Data['TimeDateSince'].index).month
distrometer_Data['day'] = pd.DatetimeIndex(distrometer_Data['TimeDateSince'].index).day
distrometer_Data['hour'] = pd.DatetimeIndex(distrometer_Data['TimeDateSince'].index).hour
distrometer_Data['minute'] = pd.DatetimeIndex(distrometer_Data['TimeDateSince'].index).minute
distrometer_Data['second'] = pd.DatetimeIndex(distrometer_Data['TimeDateSince'].index).second




 