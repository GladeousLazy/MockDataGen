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
        
    
    ################################## Check if folder/file exists (Com. 3) ##################################
    
    def Folder_Check(self):
        
        file_location = '\\'.join(self.fileloc.split('\\')[:-1]) + '\\Output_File\\'
        CHECK_FOLDER = os.path.isdir(file_location)
        if not CHECK_FOLDER:
            os.makedirs(file_location)
            print("created folder : ", file_location)

        else:
            print('"' + file_location + '"' + " folder already exists.")

    ############################################# End of Com. 3 #############################################

    

    ######################### Seed function to generate true random number (Com. 4) #########################
    
    def sys_rand_seed():
        return int(tm.time() * 100000000000) % 100000000000
    
    ############################################# End of Com. 4 #############################################

    
    ###################################### Initialize Function (Com. 5) ######################################

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

    ############################################# End of Com. 5 #############################################

    
    ############################## Sub Function to Generate Fake Names (Com. 6) ##############################

    def Generate_Name(self, dim_df, srow):
        for index in range(srow["No of Rows"]):
            dim_df[index] = 'FN' + str(index + 1) + ' ' + 'LN' + str(index + 1)

    ############################################# End of Com. 6 #############################################

    ###################################### Generate Random Age (Com. 7) ######################################

    def Generate_Age(self, dim_df, srow):

        min_age = srow["Min Value"] if srow["Min Value"] != '' or type(
            srow["Min Value"]) != str else 18
        max_age = srow["Max Value"] if srow["Max Value"] != '' or type(
            srow["Max Value"]) != str else 70

        for index in range(srow["No of Rows"]):
            rn.seed(self.sys_rand_seed() + index)
            dim_df[index] = int(rn.randint((min_age), (max_age)))
    ############################################# End of Com. 7 #############################################
    
    
    ########################### Generate ID Value usually a Serial Number (Com. 8) ###########################

    def Create_ID_Column(self, srow):
        id_df = {}
        if (srow["Key type PK or FK"] == 'PK'):
            for index in range(srow["No of Rows"]):
                id_df[index] = index + 1
        else:
            print('Design for ID != PK is pending',
                getframeinfo(currentframe()).lineno)

        return id_df
    ############################################# End of Com. 8 #############################################

    
    
    ############################## Generate Dimension/Discrete Values (Com. 9) ##############################

    def Create_Dim_Column(self, srow, nRows=None):
        """
        The Create_Dim_Columnn() needs to handle the below conditions
        1. Prefix & Suffix - Done
        2. Leading 0's - Done
        3. Using FK to fetch data from PK when needed - Done
        4. If no suffix or Prefix value is present, use the column name - Done
        5. There is a hierarchy or relation between 2 dimension - for After Fact Table is handled
        """

        #--------------------------------------------------------------------------------------------------#
        #Space for variable declaration
        _is_lookup = 0
        prefix = srow['S or P Value'] if srow['Suffix or Prefix'] == 'P' else ''
        suffix = srow['S or P Value'] if srow['Suffix or Prefix'] == 'S' else ''
        default_label = srow["Column Name"]
        lenght = srow["Length of id with preceding zero"] if type(
            srow["Length of id with preceding zero"]) != str else 0
        min_value = srow["Min Value"] if type(srow["Min Value"]) != str else 0
        max_value = srow["Max Value"] if type(
            srow["Max Value"]) != str else srow["No of Rows"]
        total_rows = nRows if nRows != None else srow["No of Rows"]
        dim_df = {}

        #--------------------------------------------------------------------------------------------------#

        #Handle leading zero or scenario where length is defined
        if (srow["Suffix or Prefix"].upper() == 'P'
                or srow["Suffix or Prefix"].upper() == 'S' or lenght > 0):
            if (
                (len(srow["S or P Value"]) + len(str(max_value))) > lenght
            ):  #Scenario where s/p value is larger than the total lenght of the value
                for index in range(total_rows):

                    dim_df[index] = prefix + str(index + 1) + suffix

            elif (len(srow["S or P Value"]) == 0 or len(srow["Suffix or Prefix"])
                == 0):  #Scenario if no suffix or prefix is present
                for index in range(total_rows):
                    dim_df[index] = default_label + str(min_value + index + 1)

            elif (len(srow["S or P Value"]) + len(str(max_value)) <=
                lenght):  #Preceding zero cases with suffix and prefix
                for index in range(total_rows):
                    rem_zero = lenght - (len(srow["S or P Value"]) +
                                        len(str(min_value + index + 1)))
                    zero_str = str(pow(10, rem_zero))[(rem_zero * -1):]
                    dim_df[index] = prefix + zero_str + str(min_value + index +
                                                            1) + suffix

        #--------------------------------------------------------------------------------------------------#

        elif (srow["Functional Category"] != ''):
            cat = srow["Functional Category"]
            if (cat == 'Name'):
                self.Generate_Name(dim_df, srow)
            elif (cat == 'Age'):
                self.Generate_Age(dim_df, srow)

        #Scenario where PK or FK is present
        elif (srow["Key type PK or FK"] != ''):
            if (srow["Key type PK or FK"] == 'FK'):

                parent_table = str(srow["Parent Column ID"]).split(".")[0]
                parent_column = str(srow["Parent Column ID"]).split(".")[1]

                #This function is used to get the min and max value in a column

                if parent_table in self.All_Table_Key_Dict:
                    # It will get the values from the reference table which will mostly be Dim Tables
                    min_index = 1
                    max_index = max(
                        self.All_Table_Key_Dict[parent_table][parent_column].values())

                else:
                    self.Create_Dim_Table(parent_table)
                    min_index = 1
                    max_index = self.All_Table_Key_Dict[parent_table][
                        parent_column].max()

                for index in range(total_rows):
                    # This loop will fill the data frame with the total number of rows as defined for the table
                    rn.seed(self.sys_rand_seed() + index)
                    dim_df[index] = rn.randint(min_index, max_index)

            elif (srow["Key type PK or FK"] == 'PK'):
                dim_df = self.Create_ID_Column(srow)
        else:
            for index in range(total_rows):
                dim_df[index] = default_label + str(min_value + index + 1)

        return dim_df
    ############################################# End of Com. 9 #############################################



    

############################################# End of Com. 2 #############################################

#Adding Comment just to see if there is any change#
