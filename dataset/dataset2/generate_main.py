# %%
import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.decomposition import PCA
base_dir = os.getcwd()

# %%
# 初始化表头
op_header = ['op_type_0', 'op_type_1', 'op_type_2', 'op_type_3', 'op_type_4', 'op_type_5', 'op_type_6', 'op_type_7',
             'op_type_8', 'op_type_9', 'op_type_perc', 'op_type_std', 'op_type_n', 'op_mode_0', 'op_mode_1',
             'op_mode_2', 'op_mode_3', 'op_mode_4', 'op_mode_5', 'op_mode_6', 'op_mode_7', 'op_mode_8', 'op_mode_9',
             'op_mode_perc', 'op_mode_std', 'op_mode_n', 'op_device_perc', 'op_device_std', 'op_device_nan_perc',
             'op_device_n', 'op_ip_perc', 'op_ip_std', 'op_ip_nan_perc', 'op_ip_n', 'op_net_type_0', 'op_net_type_1',
             'op_net_type_2', 'op_net_type_3', 'op_net_type_perc', 'op_net_type_std', 'op_net_type_nan_perc',
             'op_channel_0', 'op_channel_1', 'op_channel_2', 'op_channel_3', 'op_channel_4', 'op_channel_perc',
             'op_channel_std', 'op_channel_n', 'op_ip_3_perc', 'op_ip_3_std', 'op_ip_3_nan_perc', 'op_ip_3_n',
             'op_freq', 'op_ip_freq', 'op_ip_3_freq', 'op_ip_3_ch_freq', 'op_ip_48h_n', 'op_device_48h_n', 'op_48h_n']
trans_header = ['trans_platform_0', 'trans_platform_1', 'trans_platform_2', 'trans_platform_3',
                'trans_platform_4', 'trans_platform_5', 'trans_platform_perc', 'trans_platform_std', 'trans_platform_n',
                'trans_tunnel_in_0', 'trans_tunnel_in_1', 'trans_tunnel_in_2', 'trans_tunnel_in_3', 'trans_tunnel_in_4',
                'trans_tunnel_in_5', 'trans_tunnel_in_perc', 'trans_tunnel_in_std', 'trans_tunnel_in_n',
                'trans_tunnel_in_nan_perc', 'trans_tunnel_out_0', 'trans_tunnel_out_1', 'trans_tunnel_out_2',
                'trans_tunnel_out_3', 'trans_tunnel_out_perc', 'trans_tunnel_out_std', 'trans_tunnel_n',
                'trans_amount_max', 'trans_amount_avg', 'trans_amount_std', 'trans_type1_0', 'trans_type1_1',
                'trans_type1_2', 'trans_type1_3', 'trans_type1_4', 'trans_type1_perc', 'trans_type1_std',
                'trans_ip_perc', 'trans_ip_std', 'trans_ip_nan_perc', 'trans_ip_n']


# %%
feature_train_trans = pd.DataFrame(columns=trans_header)
feature_test_trans = pd.DataFrame(columns=trans_header)
feature_train_op = pd.DataFrame(columns=op_header)
feature_test_op = pd.DataFrame(columns=op_header)
train_base_df = pd.read_csv(base_dir + '/dataset/dataset2/trainset/train_base.csv')
train_op_df = pd.read_csv(base_dir + '/dataset/dataset2/trainset/train_op.csv')
train_trans_df = pd.read_csv(base_dir + '/dataset/dataset2/trainset/train_trans.csv')
test_base_df = pd.read_csv(base_dir + '/dataset/dataset2/testset/test_a_base.csv')
test_op_df = pd.read_csv(base_dir + '/dataset/dataset2/testset/test_a_op.csv')
test_trans_df = pd.read_csv(base_dir + '/dataset/dataset2/testset/test_a_trans.csv')
train_n = len(train_base_df)
test_n = len(test_base_df)

# %%
# load encoder
op_type = np.loadtxt(base_dir + '/dataset/dataset2/encoders/enc_op_type.csv', delimiter=',')
mp_op_type = {}
for i in range(op_type.shape[0]):
    mp_op_type[op_type[i, 0]] = op_type[i, 1:].tolist()

op_mode = np.loadtxt(base_dir + '/dataset/dataset2/encoders/enc_op_mode.csv', delimiter=',')
mp_op_mode = {}
for i in range(op_mode.shape[0]):
    mp_op_mode[op_mode[i, 0]] = op_mode[i, 1:].tolist()

net_type = np.loadtxt(base_dir + '/dataset/dataset2/encoders/enc_net_type.csv', delimiter=',')
mp_net_type = {}
for i in range(net_type.shape[0]):
    mp_net_type[net_type[i, 0]] = net_type[i, 1:].tolist()

channel = np.loadtxt(base_dir + '/dataset/dataset2/encoders/enc_channel.csv', delimiter=',')
mp_channel = {}
for i in range(channel.shape[0]):
    mp_channel[channel[i, 0]] = channel[i, 1:].tolist()

platform = np.loadtxt(base_dir + '/dataset/dataset2/encoders/enc_platform.csv', delimiter=',')
mp_platform = {}
for i in range(platform.shape[0]):
    mp_platform[platform[i, 0]] = platform[i, 1:].tolist()

tunnel_in = np.loadtxt(base_dir + '/dataset/dataset2/encoders/enc_tunnel_in.csv', delimiter=',')
mp_tunnel_in = {}
for i in range(tunnel_in.shape[0]):
    mp_tunnel_in[tunnel_in[i, 0]] = tunnel_in[i, 1:].tolist()

tunnel_out = np.loadtxt(base_dir + '/dataset/dataset2/encoders/enc_tunnel_out.csv', delimiter=',')
mp_tunnel_out = {}
for i in range(tunnel_out.shape[0]):
    mp_tunnel_out[tunnel_out[i, 0]] = tunnel_out[i, 1:].tolist()

type1 = np.loadtxt(base_dir + '/dataset/dataset2/encoders/enc_type1.csv', delimiter=',')
mp_type1 = {}
for i in range(type1.shape[0]):
    mp_type1[type1[i, 0]] = type1[i, 1:].tolist()

type2 = np.loadtxt(base_dir + '/dataset/dataset2/encoders/enc_type2.csv', delimiter=',')
mp_type2 = {}
for i in range(type2.shape[0]):
    mp_type2[type2[i, 0]] = type2[i, 1:].tolist()


# %%
# train set
for i in range(train_n):
    cur_user = train_base_df['user'].loc[i]
    tr_trans_user = train_trans_df[train_trans_df['user'] == cur_user]
    tr_op_user = train_op_df[train_op_df['user'] == cur_user]

    tr_trans_user_n = len(tr_trans_user)    # 该用户的trans记录条数
    tr_op_user_n = len(tr_op_user)          # 该用户的trans记录条数

    # -----------op_type----------- #
    op_type_df = pd.DataFrame(columns=['op_type_' + str(i) for i in range(10)])

