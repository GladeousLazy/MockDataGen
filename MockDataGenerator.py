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
        CHECK_FOLDER = os.path.isdir(self.output_file_location)
        if not CHECK_FOLDER:
            os.makedirs(self.output_file_location)
            print("created folder : ", self.output_file_location)

        else:
            print('"' + self.output_file_location + '"' + " folder already exists.")
    ############################################# End of Com. 3 #############################################

    

    ######################### Seed function to generate true random number (Com. 4) #########################
    def sys_rand_seed(self):
        return int(tm.time() * 100000000000) % 100000000000
    ############################################# End of Com. 4 #############################################



    ###################################### Initialize Function (Com. 5) ######################################
    def __init__(self):
        
        self.fileloc =  'C:\Work\Python\Mock Data Generator\Mock Data Generator - Metadata File.xlsx'#input('Please enter the Location of the Excel file: ')
        self.sheetname = 'Column Metadata'#input('Please enter the sheet name: ')
        self.output_file_location = '\\'.join(self.fileloc.split('\\')[:-1]) + '\\Output_File\\'
        self.Folder_Check()
        
        self.Metadata_df = pd.read_excel(self.fileloc,sheet_name=self.sheetname,keep_default_na=False)
        self.Dim_Tables = self.Metadata_df[self.Metadata_df['Dim or Fact'] == '1 Dim']
        self.Fact_Tables = self.Metadata_df[self.Metadata_df['Dim or Fact'] == '2 Fact']
        
        self.All_Table_Data_Dict = {}
        self.All_Table_Key_Dict = {}
        self.Distinct_Value_Set = {}
        self.Replacement_Dict = {}
    ############################################# End of Com. 5 #############################################

    def Gen_Serialized_Value(self,dim_df,tot_rows,min_val,max_val):
        for index in range(tot_rows):
            rn.seed(self.sys_rand_seed() + index)
            dim_df[index] = int(rn.randint((min_val), (max_val)))


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

        self.Gen_Serialized_Value(dim_df, srow["No of Rows"], min_age, max_age)
        #for index in range(srow["No of Rows"]):
        #    rn.seed(self.sys_rand_seed() + index)
        #    dim_df[index] = int(rn.randint((min_age), (max_age)))
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

        ################################ Space for variable declaration (Com. 10) ################################
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
        ############################################# End of Com. 10 #############################################


        #################### Handle leading zero or scenario where length is defined (Com.11) ####################
        if (srow["Suffix or Prefix"].upper() == 'P'
                or srow["Suffix or Prefix"].upper() == 'S' or lenght > 0):
            
            #Scenario where s/p value is larger than the total lenght of the value
            if ((len(srow["S or P Value"]) + len(str(max_value))) > lenght):  
                for index in range(total_rows):

                    dim_df[index] = prefix + str(index + 1) + suffix
            
            #Scenario if no suffix or prefix is present
            elif (len(srow["S or P Value"]) == 0 or len(srow["Suffix or Prefix"]) == 0):
                for index in range(total_rows):
                    dim_df[index] = default_label + str(min_value + index + 1)
            #Preceding zero cases with suffix and prefix
            elif (len(srow["S or P Value"]) + len(str(max_value)) <= lenght):
                for index in range(total_rows):
                    rem_zero = lenght - (len(srow["S or P Value"]) +
                                        len(str(min_value + index + 1)))
                    zero_str = str(pow(10, rem_zero))[(rem_zero * -1):]
                    dim_df[index] = prefix + zero_str + str(min_value + index + 1) + suffix
        ############################################# End of Com. 11 #############################################



        ################ If there is a Functional Category Value mentioned in Metadata (Com. 12) #################
        elif (srow["Functional Category"] != ''):
            cat = srow["Functional Category"]
            if (cat == 'Name'):
                self.Generate_Name(dim_df, srow)
            elif (cat == 'Age'):
                self.Generate_Age(dim_df, srow)
        ############################################# End of Col. 12 #############################################

        ############################## Scenario where PK or FK is present (Col. 13) ##############################
        elif (srow["Key type PK or FK"] != ''):
            if (srow["Key type PK or FK"] == 'FK'):

                parent_table = str(srow["Parent Column ID"]).split(".")[0]
                parent_column = str(srow["Parent Column ID"]).split(".")[1]

                #This function is used to get the min and max value in a column

                if parent_table in self.All_Table_Key_Dict:
                    # It will get the values from the reference table which will mostly be Dim Tables
                    min_index = 1
                    max_index = max(self.All_Table_Key_Dict[parent_table][parent_column].values())

                else:
                    self.Create_Dim_Table(parent_table)
                    min_index = 1
                    max_index = self.All_Table_Key_Dict[parent_table][parent_column].max()
                
                self.Gen_Serialized_Value(dim_df, total_rows, min_index, max_index)
                #for index in range(total_rows):
                #    # This loop will fill the data frame with the total number of rows as defined for the table
                #    rn.seed(self.sys_rand_seed() + index)
                #    dim_df[index] = rn.randint(min_index, max_index)

            elif (srow["Key type PK or FK"] == 'PK'):
                dim_df = self.Create_ID_Column(srow)
        ############################################# End of Col. 13 #############################################


        ########################## Else use the header name to generate value (Com. 14) ##########################
        else:
            for index in range(total_rows):
                dim_df[index] = default_label + str(min_value + index + 1)

        return dim_df
        ############################################# End of Com. 14 #############################################


    ############################################# End of Com. 9 #############################################
    
    
    #### Create a Fact Column also handle the Model Selection and apply that logic to the data (Com. 15) ####
    def Create_Fact_Column(self, srow):
        fact_df = {}

        min_value = srow["Min Value"]
        max_value = srow["Max Value"]
        
        self.Gen_Serialized_Value(fact_df, srow["No of Rows"], min_value, max_value)
        #for index in range(srow["No of Rows"]):
        #    rn.seed(self.sys_rand_seed() + index)
        #    fact_df[index] = int(rn.randint(min_value, max_value))

        return fact_df
    ############################################# End of Com. 15 #############################################


    ####################### Create a multiple columns following a Hierarchy (Com. 16) #######################
    def Create_Hier_Columns(self, srow):
        counter = 1  
        max_value = 0
        temp_dict = {}
        total_row = srow['No of Rows'].unique()[0]
        temp_df = {}
        srow = srow.sort_values('Hierarchy Rank')
        #Create a dictionary with the column names
        #Use this dictionary to fill in and create the actual database
        for index, row in srow.iterrows():
            temp_dict[str(row["Column Name"])] = self.Create_Dim_Column(row, nRows=row['Number of Unique Values'])

        for key in temp_dict:

            temp_df[key] = {}
            min_value = 1
            max_value = (len(temp_dict[key]))

            if (max_value < total_row or max_value >
                    total_row):  # This loop is for parent columns mostly

                for index in range(total_row):
                    rn.seed(self.sys_rand_seed() + index)
                    lkup_index = int(rn.randint(min_value, max_value) - 1)
                    temp_df[key][index] = temp_dict[key][lkup_index]

            else:
                for index in range(total_row):
                    temp_df[key][index] = temp_dict[key][index]
        return temp_df
    ############################################# End of Com. 16 #############################################



    ################# Replace Data in target column using src_val: tgt_val format (Com. 17) #################
    def SwapColumnData(self, tgtcol, repcol):
        for r_index, r_value in repcol.items():
            for t_index, t_value in tgtcol.items():
                tgtcol[
                    t_index] = r_value if r_index == t_value else tgtcol[t_index]
        return tgtcol
    ############################################# End of Com. 17 #############################################



    ################### Create a Dim Table using and merging individual columns (Com. 18) ###################
    def Create_Dim_Table(self, table_name):  #Converting DF to Dict pending
        temp_meta = self.Dim_Tables[self.Dim_Tables['Table Name'] == table_name]
        temp_df = {}

        for index, row in temp_meta.iterrows():

            if (row['Structural Category'] == 'ID'):
                temp_df[row['Column Name']] = self.Create_ID_Column(row)

            elif (row['Structural Category'] == 'Dimension'):
                temp_df[row['Column Name']] = self.Create_Dim_Column(row)

            elif (row['Structural Category'] == 'Hierarchy'):

                if row['Column Name'] in temp_df.keys():
                    continue

                else:
                    hier_temp = self.Create_Hier_Columns(self.Dim_Tables[
                        self.Dim_Tables['Hierarchy Name'] == row['Hierarchy Name']])
                    for key in hier_temp:
                        temp_df[key] = hier_temp[key]

            else:
                print("End of loop or exception")
        return temp_df
    ############################################# End of Com. 18 #############################################



    ######################## Create Fact Table in the same way as Dim Table (Com. 19) ########################
    def Create_Fact_Table(self, table_name):
        temp_meta = self.Fact_Tables[self.Fact_Tables['Table Name'] == table_name]
        temp_df = {}

        for index, row in temp_meta.iterrows():

            if (row['Structural Category'] == 'Fact'):
                temp_df[row['Column Name']] = self.Create_Fact_Column(row)

            elif (row['Structural Category'] == 'Dimension'):
                temp_df[row['Column Name']] = self.Create_Dim_Column(row)

            else:
                print("End of loop or exception", )
        return temp_df
    ############################################# End of Com. 19 #############################################



    ############################## Modify data in the existing table (Com. 20) ##############################
    def ModifyDataInTable(self,tablename, file=None, sheetname = 'Sheet1'):

        if file != None:
            '''Replace "Sheet1" with actual sheet name in below expression'''
            file_dict = pd.read_excel(file,
                                    sheet_name=sheetname,
                                    keep_default_na=False).to_dict()
            file_flag = 1
        else:
            file_flag = 0
        self.Replacement_Dict[tablename] = {}
        temp_df = {}

        # Check for Table exist
        if tablename in self.All_Table_Key_Dict.keys():
            self.Distinct_Value_Set[tablename] = self.Generate_Unique_Set(
                self.All_Table_Key_Dict[tablename])
        else:
            print('Table does not exist')
            return None


        #Find unique value within a dictionary
        temp_df = self.Generate_Unique_Set(self.All_Table_Key_Dict[tablename])


        print('\n A dictionary with unique value has been prepared\n')
        print(
            'We will now begin to modify the data. Please help us with the below details\n'
        )

        #Start of Temp Table modification part
        if file_flag == 1:
            for col_name in file_dict:
                self.Replacement_Dict[tablename][col_name] = {}
                for index, value in temp_df[col_name].items():
                    self.Replacement_Dict[tablename][col_name][value] = file_dict[
                        col_name][index]
                    self.Distinct_Value_Set[tablename][col_name][index] = file_dict[
                        col_name][index]
        else:
            option = input(
                'Type 1: If you want to modify a specific column\nType 2: If you want to modify the data in the entire table : '
            )

            while (option.upper() != 'EXIT'):
                if option == '1':
                    col_name = input(
                        'Please enter the name of the column you would like to modify : '
                    )
                    self.Replacement_Dict[tablename][col_name] = {}
                    for index, value in temp_df[col_name].items():
                        self.Replacement_Dict[tablename][col_name][value] = input(
                            "\nPlease enter a replacement for the value '{}' : ".
                            format(value))
                        self.Distinct_Value_Set[tablename][col_name][
                            index] = self.Replacement_Dict[tablename][col_name][value]

                elif option == '2':
                    for col_name in self.All_Table_Key_Dict[tablename]:
                        self.Replacement_Dict[tablename][col_name] = {}
                        for index, value in temp_df[col_name].items():
                            self.Replacement_Dict[tablename][col_name][value] = input(
                                "\nPlease enter a replacement for the value '{}' : "
                                .format(value))
                            self.Distinct_Value_Set[tablename][col_name][
                                index] = self.Replacement_Dict[tablename][col_name][
                                    value]

                else:
                    print('\nPlease enter a value option or type EXIT to exit')

                option = input('\nPlease type in your option : ')

        #Use Distinct value table to fill original table
        for tblnm in self.Replacement_Dict:
            for colname in self.Replacement_Dict[tblnm]:
                self.SwapColumnData(self.All_Table_Key_Dict[tblnm][colname],self.Replacement_Dict[tblnm][colname])
    ############################################# End of Com. 20 #############################################



    ################################### Edit Mode with a sub-menu (Com. 21) ###################################
    def Edit_Mode(self):
        print('''
        Welcome! You have enter edit mode
        Below option can be used to modify data in the current version
        
        1. Data within the table (Option prefered for Dim Table)
        2. Data using a config file (Completed)
        3. The Algo used to change the trend (behavior of fact) data (Future Feature)
        ''')
        '''While the user does not type exit the program will continue
        '''

        option = 'continue'

        while option.upper() != 'EXIT':
            option = input('Please enter an option:').upper()
            if (option == '1'):
                self.ModifyDataInTable(input('Please enter the name of the table'))
            elif (option == '2'):
                file = input(
                    'Please enter the complete location of the file with file name included'
                )
                self.ModifyDataInTable(input('Please enter the name of the table'),
                                file)
            elif (option == '3'):
                None
            else:
                break
    ############################################# End of Com. 21 #############################################


    ###################################### Create table flow (Com. 22) ######################################
    def CreateTables(self):
        for a in self.Dim_Tables["Table Name"].unique():
            self.All_Table_Key_Dict[a] = self.Create_Dim_Table(a)

        for a in self.Fact_Tables["Table Name"].unique():
            self.All_Table_Key_Dict[a] = self.Create_Fact_Table(a)
    ############################################# End of Com. 22 #############################################



    ###################### View the data that was created using the metadata (Com. 23) ######################
    def ViewTableData(self):
        print(
            "Below the the tables that have been created using the metadata file")
        for key in self.All_Table_Key_Dict:
            print(key, ':\n', self.All_Table_Key_Dict[key], end='\n\n\n', sep='')
    ############################################# End of Com. 23 ############################################



    ########################### Export Data into excel and other targets (Com. 24) ###########################
    def ExportData(self):
        for tablename in self.All_Table_Key_Dict:
            temp_ex_df = pd.DataFrame(
                data=self.All_Table_Key_Dict[tablename])
            temp_ex_df.to_excel(self.output_file_location + tablename + ".xlsx")
    ############################################# End of Com. 24 #############################################



    ###################### Main Menu Function to execute all master function (Com. 25) ######################
    def MainMenu(self):
        print('''Welcome!
        This is a mock data generator program. This program will create tables present
        There are 4 functionalities this program will provide
        1.\tGenerate table structure and populate it with mock data
        2.\tAllow user to modify the dataset once the values are generated
        3.\tView Data
        4.\tExport the files and config files at the end of the program flow.
        EXIT\tEnd the program
        ''')
        option = input('Please enter an option: ').upper()

        while(option.upper() != 'EXIT'):
            if(option == '1'):
                self.CreateTables()
                print('Tables have been created')
            elif(option == '2'):
                self.Edit_Mode()
                print('Tables have been modified')
            elif(option == '3'):
                self.ViewTableData()
            elif(option == '4'):
                self.ExportData()
                print('Data has been exported')
            else:
                print('Could not recognize the option entered')
            
            option = input('\nBack into Main Menu\n 1\t- Create table\n 2\t- Edit Tables\n 3\t- View Data\n 4\t- Export Data\n EXIT\t- End the program\n Please enter an option or type EXIT to end program : ')
    ############################################# End of Com. 25 #############################################


def main():
    D1 = DataGen
    D1.MainMenu()


if __name__ == "main":
    main()
    
############################################# End of Com. 2 #############################################


