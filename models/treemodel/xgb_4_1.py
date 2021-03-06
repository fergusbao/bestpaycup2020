# %%
import xgboost as xgb
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import roc_auc_score
import numpy as np
import os
import pandas as pd

# %%
base_dir = os.getcwd()
x_df = pd.read_csv(base_dir + '/dataset/dataset4/trainset/train_main.csv')
y_df = pd.read_csv(base_dir + '/dataset/raw_dataset/trainset/train_label.csv')
data_x = np.array(x_df)
data_y = np.array(y_df)

# %%
data_x = data_x[data_x[:, 0].argsort()]
data_y = data_y[data_y[:, 0].argsort()]
data_x = data_x[:, 1:].astype(float)
data_y = data_y[:, 1:].astype(float).reshape(1, -1)[0]

state = np.random.get_state()
np.random.shuffle(data_x)
np.random.set_state(state)
np.random.shuffle(data_y)

# %%
X_train, X_val, y_train, y_val = train_test_split(data_x, data_y, test_size=0.1)

# %%
train_data = xgb.DMatrix(X_train, label=y_train)
val_data = xgb.DMatrix(X_val, label=y_val)
param = {
    'silent': 0,
    'max_depth': 10,
    'n_estimators': 50,
    'learning_rate': 0.1,
    'objective': 'binary:logistic',
    'eval_metric': 'auc'
}

model = xgb.train(param, train_data, num_boost_round=100)

y_hat = model.predict(val_data)

print('auc: ', roc_auc_score(y_val, y_hat))

# %%
clf = XGBClassifier(
    learning_rate=0.1,
    n_estimators=1000,
    max_depth=5,
    min_child_weight=1,
    gamma=0,
    subsample=0.8,
    colsample_bytree=0.8,
    objective='binary:logistic',
    nthread=4,
    scale_pos_weight=1,
    seed=27,
    verbosity=1
)
clf.fit(X_train, y_train)

# %%
y_pre = clf.predict(X_val)
y_pro = clf.predict_proba(X_val)[:, 1]
print('auc: ', roc_auc_score(y_val, y_pro))