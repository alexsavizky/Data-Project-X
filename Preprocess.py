# Bar Shwatrz 313162265
# Alexndr Savitsky 316611409
import pandas as pd
import numpy as np
from sklearn.preprocessing import minmax_scale
from sklearn.model_selection import train_test_split
import math

import Entropy


def cleanMissingValuesClassificationColumn(df, classification_column_label):
    df = df.dropna(subset=[classification_column_label])
    df = df.reset_index(drop=True)
    return df

def classificationNullCleanerCommon(df,classification_column,column):
    if df[column].isnull().sum()!= 0:
        class_unique_list = df[classification_column].unique().tolist()
        if None in class_unique_list or np.nan in class_unique_list:
            class_unique_list.remove(None)
        df2 = pd.DataFrame()
        for i in df[column].unique().tolist():
            df2[i] = [0] * len(class_unique_list)
        df2.index = class_unique_list
        for i in range(df[column].size):
            if df[column][i] and df[classification_column][i]:
                df2[df[column][i]][df[classification_column][i]] += 1
        maxValueIndexObj = df2.idxmax(axis=1)
        for i in range(df[column].size):
            if df[column][i] is np.nan or df[column][i] is None:
                    df.loc[i,column] = maxValueIndexObj[df[classification_column][i]]
    return df

def classificationNullCleanerMean(df,classification_column,column):
    if df[column].isnull().sum()!= 0:
        temp_df = df.loc[:,[classification_column, column]]
        temp_df = temp_df.groupby([classification_column]).mean()
        for i in range(df[column].size):
            if math.isnan(df[column][i]) or df[column][i] is np.nan or df[column][i] is None:
                df.loc[i,column] = temp_df[column][df[classification_column][i]]
    return df

def columnNullCleanerCommon(df,column):
    if df[column].isnull().sum()!= 0:
        for i in range(len(df[column])):
            if df[column][i] is np.nan or df[column][i] is None:
                a = df[column].mode()[0]
                df.loc[i,column] = a
    return df


def columnNullCleanerMean(df,column):
    if df[column].isnull().sum()!= 0:
        continuous_cleaner(df,column)
        for i in range(len(df[column])):
            try:
                temp_val = float(df[column][i])
                if math.isnan(temp_val):
                    df.loc[i,column] = df[column].mean()
            except TypeError:
                if temp_val is np.nan or temp_val is None:
                    df.loc[i,column] = df[column].mean()
    return df

#do to
def continuous_cleaner(df,column):
    i=0

    for i in range(len(df[column])):
        try:
            temp_val = float(df[column][i])
        except ValueError:
            df.loc[i,column]= None

def normalize(df,colunm_label):
    arr = df[colunm_label].tolist()
    df[colunm_label] = minmax_scale(arr)
    return df

def test_train_splite(df,classification_column,features,train_size):
    x = df.loc[:, features]
    y = df.loc[:, [classification_column]]
    x_train,x_test,y_train,y_test = train_test_split(x, y, random_state=11, train_size = train_size)
    x_train = x_train.reset_index(drop=True)
    y_train = y_train.reset_index(drop=True)
    x_test = x_test.reset_index(drop=True)
    y_test = y_test.reset_index(drop=True)
    return x_train,x_test,y_train,y_test


def EqualFreqDiscretization(df, col, bins):
    ncol = df[col].sort_values()
    ncol = ncol.reset_index(drop=True)
    num_per_bin = math.floor(len(ncol) / bins)
    left = len(ncol) - (num_per_bin * bins)  # if len(ncol)/bins is not int
    binned_lst = []
    for b in range(0, bins):
        lst = []
        for i in range((b * num_per_bin), ((b + 1) * num_per_bin)):
            if i >= len(ncol): break
            lst.append(ncol[i])
        binned_lst.append(lst)
    if left > 0:  # if some data is missing add it to the last bin
        for i in range(0, left):
            binned_lst[bins - 1].append(ncol[(num_per_bin * bins) + i])

    for i in range(0, len(df[col])):
        x = 0
        for l in binned_lst:
            if df[col][i].tolist() in l:
                df.loc[i, col] =x
                break
            x += 1

def EqualWidthDiscretization(df, col, bins):
    ncol = df[col].sort_values()
    ncol = ncol.reset_index(drop=True)
    w = (max(ncol)-min(ncol))/bins
    binned_lst = []
    for b in range(0, bins):
        lst = []
        for i in ncol:
            if i >= (min(ncol) + (b * w)) and i < (min(ncol) + ((b + 1) * w)):
                lst.append(i)
        binned_lst.append(lst)
    for i in range(0, len(df[col])):
        x = 0
        for l in binned_lst:
            if df[col][i].tolist() in l:
                df.loc[i, col] = x
                break
            x += 1
def find_bin(val,split_lst):
    if val <= split_lst[0]:
        return 0
    count =1
    for j in range(1,len(split_lst)):
        print(j)
        if val > split_lst[j-1] and  val <= split_lst[j]:
            return count
        count+=1
    return count
def entropy_discretization_row(df, column , calssi,bines):
    bines = bines-1
    temp_df = df.copy()
    temp_df =temp_df.sort_values(by = column)
    hole_entrophy = Entropy.entropy(temp_df[calssi].tolist())
    splits = len(temp_df[calssi].index) -1
    val_dict = {}
    for i in range(splits):
        split_val = (temp_df[column][i+1] + temp_df[column][i])/2
        under =temp_df.loc[temp_df[column] <= split_val]
        above =temp_df.loc[temp_df[column] > split_val]
        under_entropy = Entropy.entropy(under[calssi].tolist())
        above_entropy = Entropy.entropy(above[calssi].tolist())
        num_of_rows = splits+1
        val_dict[split_val] = hole_entrophy-(under_entropy*(len(under.index) / num_of_rows) + above_entropy*(len(above.index)/num_of_rows))
    max_lst =[]
    for i in range(bines):
        max_key = max(val_dict, key=val_dict.get)
        max_lst.append(max_key)
        del val_dict[max_key]
    max_lst.sort()
    print(max_lst)
    for i in df[column].index:
        df.loc[i,column] =find_bin(df[column][i],max_lst)