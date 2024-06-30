# Bar Shwatrz 313162265
# Alexndr Savitsky 316611409
import Entropy
import numpy as np
import pandas as pd
class DecisionTree:
    def __init__(self, val=None):
        self.val = val
        self.nodes = []

    def add_node(self, val):
        self.nodes.append(DecisionTree(val))

    def __repr__(self):
        return f"({self.val}): {self.nodes}"

    def __str__(self):
        return f"({self.val}): {self.nodes if len(self.nodes) > 0 else None}"

    def add_first_level(self, column, line=None):
        unique_list = column.unique().tolist()
        if line:
            self.val = (line, '->', column.name)
        else:
            self.val = (column.name)
        for i in unique_list:
            self.add_node(i)

    def build_tree(self, df, features, classification, ig_limit=None, son_label=None, son_column=None,
                   filttered_data=None, leaf_lim_precent=None):
        gain_dict = {}
        if filttered_data is not None:
            if len(set(filttered_data[classification])) == 1:
                self.add_first_level(filttered_data[classification], self.val)
                return
        if len(features) == 0:
            unique_classi, count_classi = np.unique(filttered_data[classification].tolist(), return_counts=True, axis=0)
            count_classi = count_classi.tolist()
            if len(count_classi) == 0:
                return
            max_value = max(count_classi)
            common_val = unique_classi[count_classi.index(max_value)]
            filttered_data = filttered_data.loc[df[classification] == common_val]
            self.add_first_level(filttered_data[classification], self.val)
            return
        remove_list = []
        for i in features:
            if son_label:
                temp = Entropy.information_gain(df[classification].tolist(),
                                        df[son_column].tolist(), df[i].tolist(), son_label)
            else:
                temp = Entropy.information_gain(df[classification].tolist(),
                                        df[i].tolist())
            if temp == 0.0:
                remove_list.append(i)
            elif ig_limit:
                if temp <= ig_limit:
                    remove_list.append(i)
                else:
                    gain_dict[i] = temp
            elif leaf_lim_precent:
                if filttered_data is not None:
                    if (len(filttered_data.index) / len(df.index)) * 100 <= leaf_lim_precent:
                        remove_list.append(i)
                    else:
                        gain_dict[i] = temp
                else:
                    gain_dict[i] = temp
            else:
                gain_dict[i] = temp
        for i in remove_list:  features.remove(i)
        if gain_dict:
            fin_max = max(gain_dict, key=gain_dict.get)
            features.remove(fin_max)
            self.add_first_level(df[fin_max], self.val)
        else:
            if filttered_data is not None:
                unique_classi, count_classi = np.unique(filttered_data[classification].tolist(), return_counts=True,
                                                        axis=0)
                count_classi = count_classi.tolist()
                if len(count_classi) ==0 :
                    return
                else:
                    max_value = max(count_classi)
                    common_val = unique_classi[count_classi.index(max_value)]
                    filttered_data = filttered_data.loc[df[classification] == common_val]
                    self.add_first_level(filttered_data[classification], self.val)
                    return
            else:
                self.nodes = ['ig too big']
                return
        count = 0

        for i in self.nodes:
            new_features = features.copy()
            if filttered_data is None:
                filttered_data2 = df[df[fin_max] == self.nodes[count].val]
            else:
                filttered_data2 = filttered_data[filttered_data[fin_max] == self.nodes[count].val]

            if ig_limit:
                self.nodes[count].build_tree(df=df, features=new_features, classification=classification
                                             , ig_limit=ig_limit, son_label=self.nodes[count].val, son_column=fin_max,
                                             filttered_data=filttered_data2)
            elif leaf_lim_precent:
                self.nodes[count].build_tree(df=df, features=new_features, classification=classification
                                             , son_label=self.nodes[count].val, son_column=fin_max,
                                             filttered_data=filttered_data2, leaf_lim_precent=leaf_lim_precent)
            else:
                self.nodes[count].build_tree(df=df, features=new_features, classification=classification,
                                             son_label=self.nodes[count].val, son_column=fin_max,
                                             filttered_data=filttered_data2)
            count += 1

    def compare_row_train_test(self, row, classi):
        if not self.val:
            return 0
        if type(self.val) == tuple:
            if classi == self.val[2]:
                if row[classi] == self.nodes[0].val:
                    return 1
        for i in range(len(self.nodes)):
            if type(self.val) == tuple:
                if row[self.val[2]] == self.nodes[i].val[0]:
                    return self.nodes[i].compare_row_train_test(row, classi)
            else:
                if row[self.val] == self.nodes[i].val[0]:
                    return self.nodes[i].compare_row_train_test(row, classi)

    def compare_train_test(self, df_test, classi):
        sum = 0
        for i in range(len(df_test.index)):
            temp = self.compare_row_train_test(df_test.iloc[i], classi)
            if temp:
                sum += 1
        return sum / len(df_test.index)

    def predict_row(self, row, classi):
        if type(self.val) == tuple:
            if classi == self.val[2]:
                return self.nodes[0].val
        for i in range(len(self.nodes)):
            if type(self.val) == tuple:
                if row[self.val[2]] == self.nodes[i].val[0]:
                    return self.nodes[i].predict_row(row, classi)
            else:
                if row[self.val] == self.nodes[i].val[0]:
                    return self.nodes[i].predict_row(row, classi)

    def predict(self, df_test, classi):
        y_pred = []
        for i in range(len(df_test.index)):
            a = self.predict_row(df_test.iloc[i], classi)
            y_pred.append(a)
        return y_pred




def prop(df, x, column):
    return df[column].value_counts()[x] / df[column].value_counts().sum()

def con_prop(df,x,class_value,column_x,column_class):
    sum = 0
    for i in df.index:
        if df[column_x][i] == x and df[column_class][i] == class_value:
            sum+= 1
    return sum

def build_matrix(df,column,classi):
    unique_classi, count_classi = np.unique(df[classi].tolist(), return_counts=True, axis=0)
    unique_column, count_column = np.unique(df[column].tolist(), return_counts=True, axis=0)
    mat = [[0 for _ in range(len(count_classi))] for _ in range(len(count_column))]
    df_mat = pd.DataFrame(mat, columns=unique_classi, index=unique_column)
    for i in df_mat.columns.tolist():
        for j in df_mat.index.tolist():
            df_mat.loc[j,i] = con_prop(df,j,i,column,classi)
    #laplasian
    if 0 in df_mat.values :
        for i in df_mat.columns.tolist():
            for j in df_mat.index.tolist():
                df_mat.loc[j,i]  +=1
    for i in df_mat.columns.tolist():
        a= df_mat[i].sum()
        for j in df_mat.index.tolist():
            df_mat.loc[j,i]  /= a
    return df_mat

def build_matrix_nb(df,features,classi):
    nb_dict = {}
    for i in features:
        nb_dict[i] = build_matrix(df,i,classi)
    for i in range(len(df[classi].unique().tolist())):
        nb_dict[f'prop {df[classi].unique().tolist()[i]}']= prop(df,df[classi].unique().tolist()[i],classi)
    return nb_dict

def NB_pred_row(df,row,nb_dict,classi):
    dict_temp = {}
    class_val = df[classi].unique().tolist()
    for i in class_val:
        prop_sum=1
        for j in row:
            try:
                prop_sum *= nb_dict[j][i][row[j]]
            except KeyError:
                prop_sum *= 1

        prop_sum *= nb_dict[f'prop {i}']
        dict_temp[i] = prop_sum
    return max(dict_temp, key=dict_temp.get)

def NB_predict(nb_matrix,x_test,df_test, classi):
    y_pred = []
    for i in range(len(df_test.index)):
        temp_dict = x_test.iloc[i]
        temp_dict = temp_dict.to_dict()
        b = NB_pred_row(df_test, temp_dict,nb_matrix,classi)
        y_pred.append(b)
    return y_pred
