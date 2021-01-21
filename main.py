import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns
import os

from tqdm import tqdm
import gc
import random
import lightgbm as lgb
import re
from sklearn.metrics import *
from sklearn.model_selection import KFold
import warnings
warnings.filterwarnings(action='ignore')

from util import f_pr_auc



def main(sub_name,submit=False,model='lgbm'):
    ## data load 
    PATH = "data/"
    train_err  = pd.read_csv(PATH+'train_err_data.csv')
    train_quality  = pd.read_csv(PATH+'train_quality_data.csv')
    train_problem  = pd.read_csv(PATH+'train_problem_data.csv')
    test_err  = pd.read_csv(PATH+'test_err_data.csv')
    test_quality  = pd.read_csv(PATH+'test_quality_data.csv')


    ## FE
    
    train_x
    train_y
    test_x

    ## modeling
    if train:
        models     = []
        recalls    = []
        precisions = []
        auc_scores   = []
        threshold = 0.5
        # 파라미터 설정
        params =      {
                        'boosting_type' : 'gbdt',
                        'objective'     : 'binary',
                        'metric'        : 'auc',
                        'seed': 1015
                        }
        #-------------------------------------------------------------------------------------
        # 5 Kfold cross validation
        k_fold = KFold(n_splits=5, shuffle=True, random_state=42)
        for train_idx, val_idx in k_fold.split(train_x):

            # split train, validation set
            X = train_x[train_idx]
            y = train_y[train_idx]
            valid_x = train_x[val_idx]
            valid_y = train_y[val_idx]
            
            if model = 'lgb'
                d_train= lgb.Dataset(X, y)
                d_val  = lgb.Dataset(valid_x, valid_y)           
                #run traning
                model = lgb.train(
                                    params,
                                    train_set       = d_train,
                                    num_boost_round = 1000,
                                    valid_sets      = d_val,
                                    feval           = f_pr_auc,
                                    verbose_eval    = 20, 
                                    early_stopping_rounds = 50
                                )
                # cal valid prediction
                valid_prob = model.predict(valid_x)
                valid_pred = np.where(valid_prob > threshold, 1, 0)
                
                # cal scores
                recall    = recall_score(    valid_y, valid_pred)
                precision = precision_score( valid_y, valid_pred)
                auc_score = roc_auc_score(   valid_y, valid_prob)

                # append scores
                models.append(model)
                recalls.append(recall)
                precisions.append(precision)
                auc_scores.append(auc_score)
                print('==========================================================')

        print(np.mean(auc_scores))


    if submit:
        # predict
        pred_y_lst = []
        for model in models:
            pred_y = model.predict(test_x)
            pred_y_lst.append(pred_y.reshape(-1,1))
        pred_ensemble = np.mean(pred_y_lst, axis = 0)

        # submit
        sample_submission = pd.read_csv(PATH+'sample_submission.csv')
        sample_submission['problem'] = pred_ensemble.reshape(-1)
        os.mkdir("./submission")
        sample_submission.to_csv(f"submission/{sub_name}.csv", index = False)