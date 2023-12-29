import pandas as pd
import re
import os
from scipy.io import arff
import zipfile

# Unzip NATOS.zip
natopsfilepath = os.path.join(os.getcwd(),"NATOPS.zip")
with zipfile.ZipFile(natopsfilepath,"r") as zip:
    zip.extractall()
natopsfilepath = os.path.join(os.getcwd(),"NATOPS")

# filepath: filepath to .arff file
# dimension: Dimension 1, Dimension 2,... etc
def format(filepath,dimension,index):
    ''' Formats a .arff into a dataframe and returns it '''

    # data is a tuple, the data (array of tuple) we actually want is in data[0]
    data = arff.loadarff(filepath)

    # list of data per time step
    timestep = []
    classattribute = []
    sampleid = []

    
    # concat the values in each sample to timestep
    counter = 0
    for dataset in data[0]:
        dataset = dataset.tolist()
        timestep.extend(dataset[0:51]) # end at 51 to ignore class attr.
        if(index == 24):
            for i in range(51):
                classattribute.append(dataset[51])
                sampleid.append(counter)
            counter+=1


    # If we reach the last Dimension...
    # Create a data frame where ->
    # column: Dimension number
    # column: Class attribute
    # column: Sample id
    # rows: timestep
    if(index == 24):
        df = pd.DataFrame({
        dimension: timestep,
        "Class attribute": classattribute,
        "Sample id": sampleid
        })
        return df    

    # Create a data frame where ->
    # column: Dimension number
    # rows: timestep
    df = pd.DataFrame({
        dimension: timestep
    })
   
    return df


# natopsfilepath: filepath to NATOPS directory
# type: 'TEST' or 'TRAIN'
def read(natopsfilepath,type):
    ''' Parse all Dimension .arff files in natopsfilepath whose type will either be train or test and concats them into one dataframe '''
    df = pd.DataFrame() 

    # Go through each file train/test in order (1,2,3...24)
    for i in range(1,25):
        for file in os.listdir(natopsfilepath):
            # Regex expression to look for a particular Dimension type: train or test
            match = re.match(rf'NATOPS(?P<Dimension>Dimension{i})_{type}.arff',file)
            if match:
                targetfilepath = os.path.join(natopsfilepath,file)
                dimension = match.group("Dimension")
                print("Scanning: " + dimension + " " + type)
                index = i
                # Format the .arff file into a dataframe
                dimension_df = format(targetfilepath,dimension,index)

                # We are looping through all the files: Dimension1, Dimension2,..etc
                # So we want to concatenate these dataframes to be right next to each other
                # essentially creating a new column for each Dimension
                df = pd.concat([df,dimension_df],axis=1)


    # Add data type
    df["Data Type"] = type
    return df

    


# Create dataframes for both test and train data
test_df = read(natopsfilepath,"TEST")
train_df = read(natopsfilepath,"TRAIN")

# Combine the test and train dataframes into one
test_train_df = pd.concat([test_df,train_df])

# Convert to csv file
test_train_df.to_csv('sampledata.csv')

# Print first 5 entries
print(test_train_df.head())
