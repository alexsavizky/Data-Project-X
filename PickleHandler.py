# Bar Shwatrz 313162265
# Alexndr Savitsky 316611409
import pickle
import My_Classifier
import Preprocess
from sklearn.neighbors import KNeighborsClassifier
from sklearn import preprocessing
from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.cluster import KMeans
from sklearn.naive_bayes import GaussianNB
from sklearn import tree


def save_model(model_dict , save_name):
    """
    :param dict: dict
    :param save_name : str - name of the fille i want to save
    :return: -
    """
    file = open(save_name, 'wb')
    pickle.dump(model_dict, file)
    file.close()


def load_model(filename):
    """
    :param filename: the model name i want to open
    :return: dict with the model
    """
    file = open(filename, 'rb')
    model = pickle.load(file)
    file.close()
    return model


def executePreProsesModel(df, model, save_num):
    """
    :param df: raw data frame
    :param model: dict whith the pre proses info
    :param save_num: the funk will save clean data frame with the name df_name+_clean+(save_num)
    :return: clean_df
    """
    preprocess_model = model['preprocess']
    classification_column_label = model['dataframe']['class_column']

    # deafult classification column clean
    df = Preprocess.cleanMissingValuesClassificationColumn(df, classification_column_label)

    # other column clean

    discrete_columns = model['dataframe']['discrete_columns']
    continuous_columns = model['dataframe']['continuous_columns']

    if preprocess_model['features_cleaner'] == 'column':
        for i in discrete_columns:
            Preprocess.columnNullCleanerCommon(df, i)
        for i in continuous_columns:
            Preprocess.columnNullCleanerMean(df, i)
    elif preprocess_model['features_cleaner'] == 'class':
        for i in discrete_columns:
            Preprocess.classificationNullCleanerCommon(df, classification_column_label, i)
        for i in continuous_columns:
            Preprocess.classificationNullCleanerMean(df, classification_column_label, i)

    # normalize

    if preprocess_model['normalize']:
        if isinstance(preprocess_model['normalize'], list):
            for i in preprocess_model['normalize']:
                Preprocess.normalize(df, i)
        else:
            Preprocess.normalize(df, preprocess_model['normalize'])

    # Discretization

    if preprocess_model['discretization']:
        if preprocess_model['discretization'] == 'equal freq':
            for i in model['dataframe']['continuous_columns']:
                Preprocess.EqualFreqDiscretization(df,i,preprocess_model['bins'])
                model['dataframe']['continuous_columns'].remove(i)
                model['dataframe']['discrete_columns'].append(i)
        elif preprocess_model['discretization'] == 'equal width':
            for i in model['dataframe']['continuous_columns']:
                Preprocess.EqualWidthDiscretization(df,i,preprocess_model['bins'])
                model['dataframe']['continuous_columns'].remove(i)
                model['dataframe']['discrete_columns'].append(i)
        elif preprocess_model['discretization'] == 'entropy':
            for i in model['dataframe']['continuous_columns']:
                Preprocess.entropy_discretization_row(df,i,classification_column_label,preprocess_model['bins'])
                model['dataframe']['continuous_columns'].remove(i)
                model['dataframe']['discrete_columns'].append(i)

    # save new data frame
    name = model['dataframe']['name']
    df.to_csv(f'{name}{save_num}_clean.csv', index=False)
    return df


def adapt_data_sklearn_classifiers(x_train, x_test, y_train, y_test, classification_column_label):
    """
    :param x_train: x_train
    :param x_test: x_test
    :param y_train: y_train
    :param y_test: y_test
    :param classification_column_label: classification label
    :return: x_train , x_test, y_train , y_test -> only nums for the sklearn classifier
    """
    le = preprocessing.LabelEncoder()
    for i in x_train.columns.tolist():
        le.fit(x_train[i])
        x_train[i] = le.transform(x_train[i])
    le.fit(y_train[classification_column_label])
    y_train[classification_column_label] = le.transform(y_train[classification_column_label])
    for i in x_test.columns.tolist():
        le.fit(x_test[i])
        x_test[i] = le.transform(x_test[i])
    le.fit(y_test[classification_column_label])
    y_test[classification_column_label] = le.transform(y_test[classification_column_label])
    return x_train, x_test, y_train, y_test


def excuteAlgorithems(df, model):
    # init
    discrete_columns = model['dataframe']['discrete_columns'].copy()
    classification_column_label = model['dataframe']['class_column']
    train_size = model['preprocess']['train_size']
    average = 'micro'
    algo = model['algorithm']
    result_dict = {}


    x_train, x_test, y_train, y_test = Preprocess.test_train_splite(df, classification_column_label, discrete_columns,
                                                                    train_size)
    # train test
    df_train = x_train.copy()
    df_train[classification_column_label] = y_train
    df_test = x_test.copy()
    df_test[classification_column_label] = y_test

    # ------------------------------------------------------------
    # our tree
    print(discrete_columns)
    features = discrete_columns.copy()
    if algo['my_tree']['switch']:
        my_tree_train = My_Classifier.DecisionTree()
        my_tree_test = My_Classifier.DecisionTree()
        if algo['my_tree']['ig_limit'] == 'ig':
            my_tree_train.build_tree(df_train, features , classification_column_label, algo['my_tree']['num'])
            features = discrete_columns.copy()
            my_tree_test.build_tree(df_test, features , classification_column_label, algo['my_tree']['num'])
        elif algo['my_tree']['ig_limit'] == 'samples leaf':
            my_tree_train.build_tree(df_train, features, classification_column_label,leaf_lim_precent= algo['my_tree']['num'])
            features = discrete_columns.copy()
            my_tree_test.build_tree(df_test, features, classification_column_label ,leaf_lim_precent=algo['my_tree']['num'])
        else:
            my_tree_train.build_tree(df_train, features , classification_column_label)
            features = discrete_columns.copy()
            my_tree_test.build_tree(df_test, features , classification_column_label)
        y_pred = my_tree_train.predict(df_test, classification_column_label)
        y_pred_train = my_tree_test.predict(df_train, classification_column_label)
        result_dict['my tree'] = {}
        result_dict['my tree']['train on train'] = model_score(y_test, y_pred, average)
        result_dict['my tree']['train on test'] = model_score(y_train, y_pred_train, average)

    # ------------------------------------------------------------
    # our Nb
    features = discrete_columns.copy()
    if algo['my_nb']['switch']:
        nb_matrix = My_Classifier.build_matrix_nb(df_train, features, classification_column_label)
        y_pred = My_Classifier.NB_predict(nb_matrix, x_test, df_test, classification_column_label)
        features = discrete_columns.copy()
        nb_matrix = My_Classifier.build_matrix_nb(df_test, features, classification_column_label)
        y_pred_train = My_Classifier.NB_predict(nb_matrix, x_train, df_train, classification_column_label)
        result_dict['my NB'] = {}
        result_dict['my NB']['train on train'] = model_score(y_test, y_pred, average)
        result_dict['my NB']['train on test'] = model_score(y_train, y_pred_train, average)

    # ------------------------------------
    # addapt to sklearn clasifiers
    if algo['tree']['switch'] or algo['nb']['switch'] or algo['knn']['switch'] or algo['k_means']['switch']:
        x_train, x_test, y_train, y_test = adapt_data_sklearn_classifiers(x_train, x_test, y_train, y_test,
                                                                          classification_column_label)

    # ----------------------------------------------------------------------------------------
    # sklearn NB
    if algo['nb']['switch']:
        clf_train = GaussianNB()
        clf_test = GaussianNB()
        y_pred = clf_train.fit(x_train, y_train.values.ravel()).predict(x_test)
        y_pred_train = clf_test.fit(x_test, y_test.values.ravel()).predict(x_train)
        result_dict['sklearn NB'] = {}
        result_dict['sklearn NB']['train on train'] = model_score(y_test, y_pred, average)
        result_dict['sklearn NB']['train on test'] = model_score(y_train, y_pred_train, average)

    # ------------------------------------------------------------
    # knn
    if algo['knn']['switch']:
        clf_train = KNeighborsClassifier(algo['knn']['n_neighbors'])
        clf_test = KNeighborsClassifier(algo['knn']['n_neighbors'])
        clf_train.fit(x_train, y_train.values.ravel())
        y_pred = clf_train.predict(x_test)
        clf_test.fit(x_test, y_test.values.ravel())
        y_pred_train = clf_test.predict(x_train)
        result_dict['knn'] = {}
        result_dict['knn']['train on train'] = model_score(y_test, y_pred, average)
        result_dict['knn']['train on test'] = model_score(y_train, y_pred_train, average)

    # ------------------------------------------------------------
    # sklearn tree
    if algo['tree']['switch']:
        if algo['tree']['ig_limit or min samples leaf'] == 'min samples leaf':
            clf_train = tree.DecisionTreeClassifier(min_samples_leaf=algo['tree']['num'])
            clf_test = tree.DecisionTreeClassifier(min_samples_leaf=algo['tree']['num'])
        elif algo['tree']['ig_limit or min samples leaf'] == 'ig':
            clf_train = tree.DecisionTreeClassifier(criterion='entropy', min_impurity_decrease=algo['tree']['num'])
            clf_test = tree.DecisionTreeClassifier(criterion='entropy', min_impurity_decrease=algo['tree']['num'])
        else:
            clf_train = tree.DecisionTreeClassifier()
            clf_test = tree.DecisionTreeClassifier()
        clf_train = clf_train.fit(x_train, y_train)
        y_pred = clf_train.predict(x_test)
        clf_test = clf_test.fit(x_test, y_test)
        y_pred_train = clf_test.predict(x_train)
        result_dict['sklearn tree'] = {}
        result_dict['sklearn tree']['train on train'] = model_score(y_test, y_pred, average)
        result_dict['sklearn tree']['train on test'] = model_score(y_train,y_pred_train,average)

    # ------------------------------------------------------------
    # k_means

    if algo['k_means']['switch']:
        kmeans = KMeans(n_clusters=algo['k_means']['n_clusters'])
        y_pred = k_mean_adapter(kmeans,x_train,x_test,y_train,algo['k_means']['n_clusters'],classification_column_label)
        kmeans = KMeans(n_clusters=algo['k_means']['n_clusters'])
        y_pred_train = k_mean_adapter(kmeans,x_test,x_train,y_test,algo['k_means']['n_clusters'],classification_column_label)
        result_dict['K_means'] = {}
        result_dict['K_means']['train on train'] = model_score(y_test, y_pred, average)
        result_dict['K_means']['train on test'] = model_score(y_train, y_pred_train, average)

    result_dict['majority'] = df[classification_column_label].value_counts()[df[classification_column_label].value_counts().idxmax()]/len(df[classification_column_label])
    return result_dict


def model_score(y_test, y_pred, average):
    score_dict = {}
    try:
        score_dict['accuracy_score'] = str(accuracy_score(y_test, y_pred))
        score_dict['precision score'] = str(precision_score(y_test, y_pred, average=average))
        score_dict['confusion matrix'] = str(confusion_matrix(y_test, y_pred))
        score_dict['recall score'] = str(recall_score(y_test, y_pred, average=average))
        score_dict['F-measure'] = str(f1_score(y_test, y_pred, average=average))
    except ZeroDivisionError:
        print('Zero Division Error')
    return score_dict

def k_mean_adapter(kmeans,x_train,x_test,y_train,num_of_cluster,classification_column_label):
    kmeans = kmeans.fit(x_train)
    x_train.to_csv(f'x_train_k_means_test.csv', index=False)
    y_train_kmeans = kmeans.predict(x_train)
    k_mean_mat = []
    for i in range(num_of_cluster):
        k_mean_mat.append([0] * len(y_train[classification_column_label].unique().tolist()))
    for i in y_train.index:
        k_mean_mat[y_train_kmeans.tolist()[i]][y_train[classification_column_label][i]] += 1
    parse_lst = []
    for i in range(len(k_mean_mat)):
        max_value = max(k_mean_mat[i])
        max_index = k_mean_mat[i].index(max_value)
        parse_lst.append(max_index)
    y_kmeans = y_train_kmeans.tolist()
    for i in range(len(y_kmeans)):
        y_kmeans[i] = parse_lst[y_kmeans[i]]
    y_pred = kmeans.predict(x_test)
    for i in range(len(y_pred)):
        y_pred[i] = parse_lst[y_pred[i]]
    return y_pred