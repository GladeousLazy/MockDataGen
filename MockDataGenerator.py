#################################### Import all the classes (Com. 1) ####################################
import pandas as pd
import copy
import random as rn
import time as tm
import numpy as np
import os
import math
from inspect import currentframe, getframeinfo  #temp_dict,getframeinfo(currentframe()).lineno
from IPython.display import clear_output
############################################# End of Com. 1 #############################################


################################ Data Generator Class Definition (Com. 2) ###############################
class DataGen:
        
    
    #Function to Check if the Folder and File exist, else to interupt and ask user for more details
    def Folder_Check(self):
        
        file_location = '\\'.join(self.fileloc.split('\\')[:-1]) + '\\Output_File\\'
        CHECK_FOLDER = os.path.isdir(file_location)
        if not CHECK_FOLDER:
            os.makedirs(file_location)
            print("created folder : ", file_location)

        else:
            print('"' + file_location + '"' + " folder already exists.")
    
    
    #Seed function to generate close to true random value generator
    def sys_rand_seed(self):
        return int(tm.time() * 100000000000) % 100000000000
    
    
    #Initialize basic variables and  Dictionaries that will be required in the object's lifespan
    def __init__(self):
        
        self.fileloc =  'C:\Work\Python\Mock Data Generator\Mock Data Generator - Metadata File.xlsx'#input('Please enter the Location of the Excel file: ')
        self.sheetname = 'Column Metadata'#input('Please enter the sheet name: ')
        self.Folder_Check()
        
        self.Metadata_df = pd.read_excel(self.fileloc,sheet_name=self.sheetname,keep_default_na=False)
        self.Dim_Tables = self.Metadata_df[self.Metadata_df['Dim or Fact'] == '1 Dim']
        self.Fact_Tables = self.Metadata_df[self.Metadata_df['Dim or Fact'] == '2 Fact']
        
        self.All_Table_Data_Dict = {}
        self.All_Table_Key_Dict = {}
        self.Distinct_Value_Set = {}
        self.Replacement_Dict = {}        

############################################# End of Com. 2 #############################################

#Adding Comment just to see if there is any change#
