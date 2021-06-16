import random as rn
import pandas as pd
import anytree  as at
import time as tm
import numpy as np

def sys_rand_seed():
    return int(tm.time() * 100000000000) % 100000000000

"""
table = {#"Root":{0:"Root"},
         "Category": {0:"Cat1",1:"Cat2",2:"Cat3"},
         "SubCat":{0:"SubCat1",1:"SubCat2",2:"SubCat3",3:"SubCat4",4:"SubCat5",5:"SubCat6",6:"SubCat7",7:"SubCat8"},
         "Product": {0:"Prod0",1:"Prod1",2:"Prod2",3:"Prod3",4:"Prod4",5:"Prod5",6:"Prod6",7:"Prod7",8:"Prod8",9:"Prod9",10:"Prod10",11:"Prod11",12:"Prod12",13:"Prod13",14:"Prod14",15:"Prod15",16:"Prod16"}
        }

root = at.Node("Root")

allkeys = list(table.keys())
col_data = pd.DataFrame(columns = allkeys)
#def GenMasterTable(table):
totalcount = []
total_row = 1000

for i in range(len(allkeys)):
    totalcount.append(len(list(table[allkeys[i]].values())))   #print(i)
    for index, value in table[allkeys[i]].items():
        if i == 0:
            at.Node(value, parent = root)
        else:
            at.Node(value, parent = at.findall_by_attr(root, table[allkeys[i-1]][rn.randrange(0,totalcount[i-1])])[0])
        if allkeys[i] == allkeys[-1]:
            col = str(at.findall_by_attr(root, value)[0]).replace("Node('/Root/","").replace("')","")
            for inner in range(len(allkeys)):
                col_data.loc[index, allkeys[inner]] = col.split('/')[inner]


min_value = 0
max_value = max(totalcount) - 1


final_df = pd.DataFrame()
#print(col_data.loc[10:])
for index in range(total_row):
	rn.seed(sys_rand_seed() + index)
	final_df[index] = col_data.loc[rn.randint(min_value, max_value)]
   
col_data = col_data.to_dict()  
print(final_df.T)
"""
fileloc =  'C:\Work\Misc Files\Practice - Metadata File.xlsx'#
sheetname = 'Column Metadata'
output_file_location = '\\'.join(fileloc.split('\\')[:-1]) + '\\Output_File\\'
Metadata_df = pd.read_excel(fileloc,sheet_name=sheetname,keep_default_na=False)
Dim_Tables = Metadata_df[Metadata_df['Dim or Fact'] == '1 Dim']
Fact_Tables = Metadata_df[Metadata_df['Dim or Fact'] == '2 Fact']

srow = Fact_Tables[ Fact_Tables['Column Name'] == 'Category']

#print(srow)
lenght = srow["Length of id with preceding zero"][2] if type(
            srow["Length of id with preceding zero"][2]) != str else 0
min_value = srow["Min Value"][2] if type(srow["Min Value"][2]) != str else 0
max_value = srow["Max Value"][2] \
            if type(srow["Max Value"][2]) != str else \
            srow["Number of Unique Values"][2] if type(srow["Number of Unique Values"][2]) != str else\
            srow["No of Rows"][2]
total_rows = srow["No of Rows"][2]
dim_df = {}
default_label = srow["Column Name"][2]

prefix = srow['S or P Value'][2]# if srow['Suffix or Prefix'] == 'P' else ''
suffix = ''#srow['S or P Value']# if srow['Suffix or Prefix'] == 'S' else ''
        
#print(len(srow["S or P Value"][2]))#srow["Suffix or Prefix"][2])


if (srow["Suffix or Prefix"][2] == 'P' or srow["Suffix or Prefix"][2] == 'S' or lenght > 0):
    #Scenario where s/p value is larger than the total lenght of the value
    if ((len(srow["S or P Value"][2]) + len(str(max_value))) > lenght):  
        for index in range(total_rows):
            dim_df[index] = prefix + str(index + 1) + suffix
    #Scenario if no suffix or prefix is present
    elif (len(srow["S or P Value"][2]) == 0 or len(srow["Suffix or Prefix"][2]) == 0):
        #print(2)
        for index in range(total_rows):
            dim_df[index] = default_label + str(min_value + index + 1)
    #Preceding zero cases with suffix and prefix
    elif (len(srow["S or P Value"][2]) + len(str(max_value)) <= lenght):
        #print(3)
        for index in range(total_rows):
            randnum = rn.randint((min_value), (max_value))
            rem_zero = lenght - (len(srow["S or P Value"][2]) + len(str(randnum + 1)))
            zero_str = str(pow(10, rem_zero))[(rem_zero * -1):]
            dim_df[index] = prefix + zero_str + str(randnum+1) + suffix

print(dim_df)