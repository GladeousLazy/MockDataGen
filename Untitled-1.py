import random as rn
import pandas as pd
import anytree  as at

table = {#"Root":{0:"Root"},
         "Category": {0:"Cat1",1:"Cat2",2:"Cat3"},
         "SubCat":{0:"SubCat1",1:"SubCat2",2:"SubCat3",3:"SubCat4",4:"SubCat5",5:"SubCat6",6:"SubCat7",7:"SubCat8"},
         "Product": {0:"Prod0",1:"Prod1",2:"Prod2",3:"Prod3",4:"Prod4",5:"Prod5",6:"Prod6",7:"Prod7",8:"Prod8",9:"Prod9",10:"Prod10",11:"Prod11",12:"Prod12",13:"Prod13",14:"Prod14",15:"Prod15",16:"Prod16",17:"Prod17"}
        }

root = at.Node("Root")

allkeys = list(table.keys())
col_data = pd.DataFrame(columns = allkeys)
#def GenMasterTable(table):
totalcount = []


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
   
   
col_data = col_data.to_dict()  
print(col_data)