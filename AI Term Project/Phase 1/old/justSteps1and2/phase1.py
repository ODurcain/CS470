import pandas as pd
import re
import os
from scipy.io import arff

# dataframe to create one giant table
masterdf = pd.DataFrame()
natopsfilepath = os.path.join(os.getcwd(),"NATOPS")

# read .arff file, create dataframe and concat to master dataframe
def readFile(masterdf,filepath):
    data = arff.loadarff(filepath)
    df = pd.DataFrame(data[0])
    # Set axis to 1 to put dataframes side by side, not on top of each other
    masterdf = pd.concat([masterdf,df],axis=1)
    return masterdf 

# Traverse NATOPS 
for root,dirs,files in os.walk(natopsfilepath):
    for file in files:
        # Only want to look at NATOPSDimension files
        match = re.match(r'NATOPSDimension',file)
        if match:
            targetfilepath = os.path.join(natopsfilepath,file)
            masterdf = readFile(masterdf,targetfilepath)

# dataframe sets the (rows * columns) to (samples * timesteps)
# swap rows and columns to get (time steps * features)
masterdf = masterdf.transpose()
print(masterdf.head())

masterdf.to_csv("mastertable.csv")

        












#     data = arff.loadarff("NATOPSDimension1_TEST.arff")
#     data2 = arff.loadarff("NATOPSDimension5_TRAIN.arff")
#     df = pd.DataFrame(data[0])
#     df2 = pd.DataFrame(data2[0])

#     # Concat dataframes by putting them side to side
#     masterdf = pd.concat([df,df2],axis=1)
#     # Swap rows and columns
#     # df = df.transpose()
#     # df2 = df2.transpose()
#     masterdf = masterdf.transpose()
#     print(df.tail())
#     # print(df2.tail())
#     # print(masterdf.tail())

# readFile()