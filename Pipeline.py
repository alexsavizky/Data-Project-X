# Bar Shwatrz 313162265
# Alexndr Savitsky 316611409
import PickleHandler

def save(model, name):
    PickleHandler.save_model(model, f'{name}')


def clean_df_return_and_save(df, model, save_data_num):
    return PickleHandler.executePreProsesModel(df, model, save_data_num)


def excute_algorithems(clean_df, model, name):
    a = PickleHandler.excuteAlgorithems(clean_df, model)
    model['res'] = a
    save(model, name)
