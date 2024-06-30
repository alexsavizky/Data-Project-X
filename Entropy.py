# Bar Shwatrz 313162265
# Alexndr Savitsky 316611409
import numpy as np
import pandas as pd
def entropy(Y):
    unique, count = np.unique(Y, return_counts=True, axis=0)
    prob = count/len(Y)
    en = np.sum((-1)*prob*np.log2(prob))
    return en


def information_gain(classi, column, secound_column=None, son_label=None):
    if not son_label:
        unique_classi, count_classi = np.unique(classi, return_counts=True, axis=0)
        unique_column, count_column = np.unique(column, return_counts=True, axis=0)
        mat = [[0 for _ in range(len(count_classi))] for _ in range(len(count_column))]
        df_mat = pd.DataFrame(mat, columns=unique_classi, index=unique_column)
        for i in range(len(classi)):
            df_mat[classi[i]][column[i]] += 1
        sum2 = 0
        count = 0
        temp_array = [0] * len(count_column)
        for i in unique_column:
            for j in unique_classi:
                if df_mat[j][i] != 0:
                    result = np.where(unique_column == i)
                    prob = df_mat[j][i] / count_column[result]
                    sum2 += (-1) * prob * np.log2(prob)
            temp_array[count] = sum2[0]

            sum2 = 0
            count += 1
        for i in range(len(temp_array)):
            temp_array[i] *= count_column[i] / sum(count_column)

        return entropy(classi) - sum(temp_array)
    else:
        i = 0
        new_column, new_classi, new_secound_column = [], [], []
        while i < len(column):
            if column[i] == son_label:
                new_column.append(column[i])
                new_classi.append(classi[i])
                new_secound_column.append(secound_column[i])
            i += 1
        return conditional_entropy(new_classi, new_column) - conditional_entropy(new_classi, new_secound_column)

def joint_entropy(Y,X):
    YX = np.c_[Y,X]
    return entropy(YX)

def conditional_entropy(Y, X):
    return joint_entropy(Y, X) - entropy(X)