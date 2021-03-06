# %%
import os
import pandas as pd
import numpy as np
import threading
import time

base_dir = os.getcwd()

# %%
# 初始化表头
header = ['user', 'n_op', 'n_trans', 'op_type_0', 'op_type_1', 'op_type_2', 'op_type_3', 'op_type_4', 'op_type_5',
          'op_type_6', 'op_type_7', 'op_type_8', 'op_type_9', 'op_type_perc', 'op_type_std', 'op_type_n', 'op_mode_0',
          'op_mode_1', 'op_mode_2', 'op_mode_3', 'op_mode_4', 'op_mode_5', 'op_mode_6', 'op_mode_7', 'op_mode_8',
          'op_mode_9', 'op_mode_perc', 'op_mode_std', 'op_mode_n', 'op_device_perc', 'op_device_std',
          'op_device_nan_perc', 'op_device_n', 'op_ip_perc', 'op_ip_std', 'op_ip_nan_perc', 'op_ip_n', 'op_net_type_0',
          'op_net_type_1', 'op_net_type_2', 'op_net_type_3', 'op_net_type_perc', 'op_net_type_std',
          'op_net_type_nan_perc', 'op_channel_0', 'op_channel_1', 'op_channel_2', 'op_channel_3', 'op_channel_4',
          'op_channel_perc', 'op_channel_std', 'op_channel_n', 'op_ip_3_perc', 'op_ip_3_std', 'op_ip_3_nan_perc',
          'op_ip_3_n', 'op_ip_3_ch_freq', 'op_ip_48h_n', 'op_device_48h_n',
          'op_48h_n', 'trans_platform_0', 'trans_platform_1', 'trans_platform_2', 'trans_platform_3',
          'trans_platform_4', 'trans_platform_5', 'trans_platform_perc', 'trans_platform_std', 'trans_platform_n',
          'trans_tunnel_in_0', 'trans_tunnel_in_1', 'trans_tunnel_in_2', 'trans_tunnel_in_3', 'trans_tunnel_in_4',
          'trans_tunnel_in_5', 'trans_tunnel_in_perc', 'trans_tunnel_in_std', 'trans_tunnel_in_n',
          'trans_tunnel_in_nan_perc', 'trans_tunnel_out_0', 'trans_tunnel_out_1', 'trans_tunnel_out_2',
          'trans_tunnel_out_3', 'trans_tunnel_out_perc', 'trans_tunnel_out_std', 'trans_tunnel_n', 'trans_amount_max',
          'trans_amount_avg', 'trans_amount_std', 'trans_type1_0', 'trans_type1_1', 'trans_type1_2', 'trans_type1_3',
          'trans_type1_4', 'trans_type1_perc', 'trans_type1_std', 'trans_ip_perc', 'trans_ip_std', 'trans_ip_nan_perc',
          'trans_ip_n', 'trans_type2_0', 'trans_type2_1', 'trans_type2_2', 'trans_type2_3', 'trans_type2_4',
          'trans_type2_perc', 'trans_type2_std', 'trans_ip_3_perc', 'trans_ip_3_std', 'trans_ip_3_nan_perc',
          'trans_ip_3_n', 'trans_ip_3_ch_freq',
          'trans_amount_48h_n', 'trans_48h_n', 'trans_platform_48h_n', 'trans_ip_48h_n']

print(len(header))

# %%
feature_train = pd.DataFrame(columns=header)
feature_test_a = pd.DataFrame(columns=header)
feature_test_b = pd.DataFrame(columns=header)
train_base_df = pd.read_csv(base_dir + '/dataset/dataset2/trainset/train_base.csv')
train_op_df = pd.read_csv(base_dir + '/dataset/dataset2/trainset/train_op.csv')
train_trans_df = pd.read_csv(base_dir + '/dataset/dataset2/trainset/train_trans.csv')
test_a_base_df = pd.read_csv(base_dir + '/dataset/dataset2/testset/test_a_base.csv')
test_a_op_df = pd.read_csv(base_dir + '/dataset/dataset2/testset/test_a_op.csv')
test_a_trans_df = pd.read_csv(base_dir + '/dataset/dataset2/testset/test_a_trans.csv')
test_b_base_df = pd.read_csv(base_dir + '/dataset/dataset2/testset/test_b_base.csv')
test_b_op_df = pd.read_csv(base_dir + '/dataset/dataset2/testset/test_b_op.csv')
test_b_trans_df = pd.read_csv(base_dir + '/dataset/dataset2/testset/test_b_trans.csv')
n_train = len(train_base_df)
n_test_a = len(test_a_base_df)
n_test_b = len(test_b_base_df)


# %%
# load encoder
op_type = pd.read_csv(base_dir + '/dataset/dataset2/encoders/enc_op_type.csv')
mp_op_type = {}
for col in op_type.columns.values:
    mp_op_type[col] = op_type[col].values

op_mode = pd.read_csv(base_dir + '/dataset/dataset2/encoders/enc_op_mode.csv')
mp_op_mode = {}
for col in op_mode.columns.values:
    mp_op_mode[col] = op_mode[col].values

net_type = pd.read_csv(base_dir + '/dataset/dataset2/encoders/enc_op_net_type.csv')
mp_net_type = {}
for col in net_type.columns.values:
    mp_net_type[col] = net_type[col].values

channel = pd.read_csv(base_dir + '/dataset/dataset2/encoders/enc_op_channel.csv')
mp_channel = {}
for col in channel.columns.values:
    mp_channel[col] = channel[col].values

platform = pd.read_csv(base_dir + '/dataset/dataset2/encoders/enc_trans_platform.csv')
mp_platform = {}
for col in platform.columns.values:
    mp_platform[col] = platform[col].values

tunnel_in = pd.read_csv(base_dir + '/dataset/dataset2/encoders/enc_trans_tunnel_in.csv')
mp_tunnel_in = {}
for col in tunnel_in.columns.values:
    mp_tunnel_in[col] = tunnel_in[col].values

tunnel_out = pd.read_csv(base_dir + '/dataset/dataset2/encoders/enc_trans_tunnel_out.csv')
mp_tunnel_out = {}
for col in tunnel_out.columns.values:
    mp_tunnel_out[col] = tunnel_out[col].values

type1 = pd.read_csv(base_dir + '/dataset/dataset2/encoders/enc_trans_type1.csv')
mp_type1 = {}
for col in type1.columns.values:
    mp_type1[col] = type1[col].values

type2 = pd.read_csv(base_dir + '/dataset/dataset2/encoders/enc_trans_type2.csv')
mp_type2 = {}
for col in type2.columns.values:
    mp_type2[col] = type2[col].values


# %%
def process(n, isTrain=True, isA=False):
    for i in range(n):
        if i % 1000 == 0:
            print("train - " if isTrain else "test_a - " if isA else "test_b - ", end='')
            print(i)

        if isTrain:
            cur_user = train_base_df['user'].loc[i]
            tr_trans_user = train_trans_df[train_trans_df['user'] == cur_user]  # 该用户的trans记录
            tr_op_user = train_op_df[train_op_df['user'] == cur_user]  # 该用户的op记录
        elif isA:
            cur_user = test_a_base_df['user'].loc[i]
            tr_trans_user = test_a_trans_df[test_a_trans_df['user'] == cur_user]  # 该用户的trans记录
            tr_op_user = test_a_op_df[test_a_op_df['user'] == cur_user]  # 该用户的op记录
        else:
            cur_user = test_b_base_df['user'].loc[i]
            tr_trans_user = test_b_trans_df[test_b_trans_df['user'] == cur_user]  # 该用户的trans记录
            tr_op_user = test_b_op_df[test_b_op_df['user'] == cur_user]  # 该用户的op记录

        n_tr_trans_user = len(tr_trans_user)  # 该用户的trans记录条数
        n_tr_op_user = len(tr_op_user)  # 该用户的op记录条数

        line = [cur_user, n_tr_op_user, n_tr_trans_user]  # 一行，即当前用户的所有二次特征

        if n_tr_op_user > 0:
            ### op_type
            mode_op_type = tr_op_user['op_type'].mode()[0]
            code = mp_op_type[mode_op_type]
            line.extend(code)

            line.append(sum(tr_op_user['op_type'].apply(lambda x: 1 if x == mode_op_type else 0)) / n_tr_op_user)

            s = tr_op_user['op_type'].value_counts()
            line.append(np.std(s.values))

            line.append(len(s))

            ### op_mode
            mode_op_mode = tr_op_user['op_mode'].mode()[0]
            code = mp_op_mode[mode_op_mode]
            line.extend(code)

            line.append(sum(tr_op_user['op_mode'].apply(lambda x: 1 if x == mode_op_mode else 0)) / n_tr_op_user)

            s = tr_op_user['op_mode'].value_counts()
            line.append(np.std(s.values))

            line.append(len(s))

            ### op_device
            mode_op_device = tr_op_user['op_device'].mode()[0]
            line.append(sum(tr_op_user['op_device'].apply(lambda x: 1 if x == mode_op_device else 0)) / n_tr_op_user)

            s = tr_op_user['op_device'].value_counts()
            line.append(np.std(s.values))

            # line.append(tr_op_user['op_device'].isnull().sum() / n_tr_op_user)
            line.append(sum(tr_op_user['op_device'].apply(lambda x: 1 if x == 'op_device_nan' else 0)) / n_tr_op_user)

            line.append(len(s))

            ### op_ip
            mode_op_ip = tr_op_user['ip'].mode()[0]
            line.append(sum(tr_op_user['ip'].apply(lambda x: 1 if x == mode_op_ip else 0)) / n_tr_op_user)

            s = tr_op_user['ip'].value_counts()
            line.append(np.std(s.values))

            # line.append(tr_op_user['ip'].isnull().sum() / n_tr_op_user)
            line.append(sum(tr_op_user['ip'].apply(lambda x: 1 if x == 'ip_nan' else 0)) / n_tr_op_user)

            line.append(len(s))

            ### op_net_type
            mode_op_net_type = tr_op_user['net_type'].mode()[0]
            code = mp_net_type[mode_op_net_type]
            line.extend(code)

            line.append(sum(tr_op_user['net_type'].apply(lambda x: 1 if x == mode_op_net_type else 0)) / n_tr_op_user)

            s = tr_op_user['net_type'].value_counts()
            line.append(np.std(s.values))

            # line.append(tr_op_user['net_type'].isnull().sum() / n_tr_op_user)
            line.append(sum(tr_op_user['net_type'].apply(lambda x: 1 if x == 'net_type_nan' else 0)) / n_tr_op_user)

            ### channel
            mode_op_channel = tr_op_user['channel'].mode()[0]
            code = mp_channel[mode_op_channel]
            line.extend(code)

            line.append(sum(tr_op_user['channel'].apply(lambda x: 1 if x == mode_op_channel else 0)) / n_tr_op_user)

            s = tr_op_user['channel'].value_counts()
            line.append(np.std(s.values))

            line.append(len(s))

            ### ip_3
            mode_op_ip_3 = tr_op_user['ip_3'].mode()[0]
            line.append(sum(tr_op_user['ip_3'].apply(lambda x: 1 if x == mode_op_ip_3 else 0)) / n_tr_op_user)

            s = tr_op_user['ip_3'].value_counts()
            line.append(np.std(s.values))

            # line.append(tr_op_user['ip_3'].isnull().sum() / n_tr_op_user)
            line.append(sum(tr_op_user['ip_3'].apply(lambda x: 1 if x == 'ip_3_nan' else 0)) / n_tr_op_user)

            line.append(len(s))

            ### 对tm_diff排序
            tr_op_user.sort_values('tm_diff', inplace=True)
            cnt = 0
            l = tr_op_user['ip_3'].values
            pre = l[0]
            for j in range(1, n_tr_op_user):
                if l[j] != pre:
                    pre = l[j]
                    cnt += 1
            line.append(cnt)

            ### 48h最高ip种类数量、最高的op_device种类数量、最高的op记录次数
            tr_op_tm_max = tr_op_user['tm_diff'].values.max()
            tr_op_tm_min = tr_op_user['tm_diff'].values.min()
            gap = 48 * 3600
            start = tr_op_tm_min
            end = start + gap
            max_48h_ip_n = 0
            max_48h_op_device_n = 0
            max_48h_op_n = 0
            while start <= tr_op_tm_max:
                gap_df = tr_op_user[(start <= tr_op_user['tm_diff']) & (tr_op_user['tm_diff'] < end)]
                max_48h_ip_n = max(max_48h_ip_n, gap_df['ip'].nunique())
                max_48h_op_device_n = max(max_48h_op_device_n, gap_df['op_device'].nunique())
                max_48h_op_n = max(max_48h_op_n, len(gap_df))
                start = end
                end += gap

            line.extend([max_48h_ip_n, max_48h_op_device_n, max_48h_op_n])
        else:
            line.extend([-1] * 57)

        if n_tr_trans_user > 0:
            ### platform
            mode_trans_platform = tr_trans_user['platform'].mode()[0]
            code = mp_platform[mode_trans_platform]
            line.extend(code)

            line.append(
                sum(tr_trans_user['platform'].apply(lambda x: 1 if x == mode_trans_platform else 0)) / n_tr_trans_user)

            s = tr_trans_user['platform'].value_counts()
            line.append(np.std(s.values))

            line.append(len(s))

            ### tunnel_in
            mode_trans_tunnel_in = tr_trans_user['tunnel_in'].mode()[0]
            code = mp_tunnel_in[mode_trans_tunnel_in]
            line.extend(code)

            line.append(sum(
                tr_trans_user['tunnel_in'].apply(lambda x: 1 if x == mode_trans_tunnel_in else 0)) / n_tr_trans_user)

            s = tr_trans_user['tunnel_in'].value_counts()
            line.append(np.std(s.values))

            line.append(len(s))

            # line.append(tr_trans_user['tunnel_in'].isnull().sum() / n_tr_trans_user)
            line.append(
                sum(tr_trans_user['tunnel_in'].apply(lambda x: 1 if x == 'tunnel_in_nan' else 0)) / n_tr_trans_user)

            ### tunnel_out
            mode_trans_tunnel_out = tr_trans_user['tunnel_out'].mode()[0]
            code = mp_tunnel_out[mode_trans_tunnel_out]
            line.extend(code)

            line.append(sum(
                tr_trans_user['tunnel_out'].apply(lambda x: 1 if x == mode_trans_tunnel_out else 0)) / n_tr_trans_user)

            s = tr_trans_user['tunnel_out'].value_counts()
            line.append(np.std(s.values))

            line.append(len(s))

            ### amount
            s = tr_trans_user['amount']
            line.append(s.values.max())
            line.append(s.values.mean())
            line.append(s.values.std())

            ### type1
            mode_trans_type1 = tr_trans_user['type1'].mode()[0]
            code = mp_type1[mode_trans_type1]
            line.extend(code)

            line.append(
                sum(tr_trans_user['type1'].apply(lambda x: 1 if x == mode_trans_type1 else 0)) / n_tr_trans_user)

            s = tr_trans_user['type1'].value_counts()
            line.append(np.std(s.values))

            ### trans_ip
            mode_trans_ip = tr_trans_user['ip'].mode()[0]
            line.append(sum(tr_trans_user['ip'].apply(lambda x: 1 if x == mode_trans_ip else 0)) / n_tr_trans_user)

            s = tr_trans_user['ip'].value_counts()
            line.append(np.std(s.values))

            # line.append(tr_trans_user['ip'].isnull().sum() / n_tr_trans_user)
            line.append(sum(tr_trans_user['ip'].apply(lambda x: 1 if x == 'ip_nan' else 0)) / n_tr_trans_user)

            line.append(len(s))

            ### type2
            mode_trans_type2 = tr_trans_user['type2'].mode()[0]
            code = mp_type2[mode_trans_type2]
            line.extend(code)

            line.append(
                sum(tr_trans_user['type2'].apply(lambda x: 1 if x == mode_trans_type2 else 0)) / n_tr_trans_user)

            s = tr_trans_user['type2'].value_counts()
            line.append(np.std(s.values))

            ### trans_ip_3
            mode_trans_ip_3 = tr_trans_user['ip_3'].mode()[0]
            line.append(sum(tr_trans_user['ip_3'].apply(lambda x: 1 if x == mode_trans_ip_3 else 0)) / n_tr_trans_user)

            s = tr_trans_user['ip'].value_counts()
            line.append(np.std(s.values))

            line.append(sum(tr_trans_user['ip_3'].apply(lambda x: 1 if x == 'ip_3_nan' else 0)) / n_tr_trans_user)

            line.append(len(s))

            ### 对tm_diff排序
            tr_trans_user.sort_values('tm_diff', inplace=True)
            cnt = 0
            l = tr_trans_user['ip_3'].values
            pre = l[0]
            for j in range(1, n_tr_trans_user):
                if l[j] != pre:
                    pre = l[j]
                    cnt += 1
            line.append(cnt)

            ### 48h最高amount总量、最高的trans数量、最高的platform种类数量、最高的ip种类数量
            tr_trans_tm_max = tr_trans_user['tm_diff'].values.max()
            tr_trans_tm_min = tr_trans_user['tm_diff'].values.min()
            gap = 48 * 3600
            start = tr_trans_tm_min
            end = start + gap
            max_48h_sum_amount = 0
            max_48h_trans_n = 0
            max_48h_platform_n = 0
            max_48h_ip_n = 0
            while start <= tr_trans_tm_max:
                gap_df = tr_trans_user[(start <= tr_trans_user['tm_diff']) & (tr_trans_user['tm_diff'] < end)]
                max_48h_sum_amount = max(max_48h_sum_amount, gap_df['amount'].values.sum())
                max_48h_trans_n = max(max_48h_trans_n, len(gap_df))
                max_48h_platform_n = max(max_48h_platform_n, gap_df['platform'].nunique())
                max_48h_ip_n = max(max_48h_ip_n, gap_df['ip'].nunique())
                start = end
                end += gap

            line.extend([max_48h_sum_amount, max_48h_trans_n, max_48h_platform_n, max_48h_ip_n])
        else:
            line.extend([-1] * 56)

        # print(len(line))

        ### 填入feature矩阵
        if isTrain:
            feature_train.loc[len(feature_train)] = line
        elif isA:
            feature_test_a.loc[len(feature_test_a)] = line
        else:
            feature_test_b.loc[len(feature_test_b)] = line

    # 存
    if isTrain:
        feature_train.to_csv(base_dir + '/dataset/dataset2/trainset/feature_train.csv', index=False)
    elif isA:
        feature_test_a.to_csv(base_dir + '/dataset/dataset2/testset/feature_test_a.csv', index=False)
    else:
        feature_test_b.to_csv(base_dir + '/dataset/dataset2/testset/feature_test_b.csv', index=False)


# %%
process(n_train, isTrain=True)
process(n_test_a, isTrain=False, isA=True)
process(n_test_b, isTrain=False, isA=False)

# %%
# 多线程
def process_threaded(n_train, n_test_a, n_test_b):

    def process1():
        process(n_train, isTrain=True)

    def process2():
        process(n_test_a, isTrain=False, isA=True)

    def process3():
        process(n_test_b, isTrain=False, isA=False)

    t1 = threading.Thread(target=process1)
    t1.start()
    t2 = threading.Thread(target=process2)
    t2.start()
    t3 = threading.Thread(target=process3)
    t3.start()

# %%
process_threaded(n_train, n_test_a, n_test_b)

# %%
# 并入主矩阵
### 以下l六行可以不跑
feature_train = pd.read_csv(base_dir + '/dataset/dataset2/trainset/feature_train.csv')
feature_test_a = pd.read_csv(base_dir + '/dataset/dataset2/testset/feature_test_a.csv')
feature_test_b = pd.read_csv(base_dir + '/dataset/dataset2/testset/feature_test_b.csv')
train_base_df = pd.read_csv(base_dir + '/dataset/dataset2/trainset/train_base.csv')
test_a_base_df = pd.read_csv(base_dir + '/dataset/dataset2/testset/test_a_base.csv')
test_b_base_df = pd.read_csv(base_dir + '/dataset/dataset2/testset/test_b_base.csv')

feature_train = feature_train.drop(labels='user', axis=1)
feature_test_a = feature_test_a.drop(labels='user', axis=1)
feature_test_b = feature_test_b.drop(labels='user', axis=1)

train_base_df = train_base_df.join(feature_train)
test_a_base_df = test_a_base_df.join(feature_test_a)
test_b_base_df = test_b_base_df.join(feature_test_b)

train_base_df.to_csv(base_dir + '/dataset/dataset2/trainset/train_main.csv', index=False)
test_a_base_df.to_csv(base_dir + '/dataset/dataset2/testset/test_a_main.csv', index=False)
test_b_base_df.to_csv(base_dir + '/dataset/dataset2/testset/test_b_main.csv', index=False)

# %%
# #######################以下为试水专用########################### #

feature_train = pd.read_csv(base_dir + '/dataset/dataset2/trainset/feature_train.csv')
feature_test = pd.read_csv(base_dir + '/dataset/dataset2/testset/feature_test.csv')

feature_train = feature_train.drop(labels=['op_freq', 'op_ip_freq', 'op_ip_3_freq', 'trans_freq', 'trans_amount_freq',
                                           'trans_ip_freq', 'trans_ip_3_freq'], axis=1)
feature_test = feature_test.drop(labels=['op_freq', 'op_ip_freq', 'op_ip_3_freq', 'trans_freq', 'trans_amount_freq',
                                         'trans_ip_freq', 'trans_ip_3_freq'], axis=1)

feature_train.to_csv(base_dir + '/dataset/dataset2/trainset/feature_train.csv', index=False)
feature_test.to_csv(base_dir + '/dataset/dataset2/testset/feature_test.csv', index=False)

# %%
feature_train = pd.read_csv(base_dir + '/dataset/dataset2/trainset/feature_train.csv')
feature_test = pd.read_csv(base_dir + '/dataset/dataset2/testset/feature_test.csv')
train_base_df = pd.read_csv(base_dir + '/dataset/dataset2/trainset/train_base.csv')
train_op_df = pd.read_csv(base_dir + '/dataset/dataset2/trainset/train_op.csv')
train_trans_df = pd.read_csv(base_dir + '/dataset/dataset2/trainset/train_trans.csv')
test_base_df = pd.read_csv(base_dir + '/dataset/dataset2/testset/test_a_base.csv')
test_op_df = pd.read_csv(base_dir + '/dataset/dataset2/testset/test_a_op.csv')
test_trans_df = pd.read_csv(base_dir + '/dataset/dataset2/testset/test_a_trans.csv')
n_train = len(train_base_df)
n_test = len(test_base_df)

for i in range(n_train):
    if i % 1000 == 0:
        print(i)

    cur_user = train_base_df['user'].loc[i]
    tr_trans_user = train_trans_df[train_trans_df['user'] == cur_user]  # 该用户的trans记录
    tr_op_user = train_op_df[train_op_df['user'] == cur_user]  # 该用户的op记录
    n_tr_trans_user = len(tr_trans_user)  # 该用户的trans记录条数
    n_tr_op_user = len(tr_op_user)  # 该用户的op记录条数

    if n_tr_op_user > 0:
        feature_train['op_device_nan_perc'].loc[i] = sum(
            tr_op_user['op_device'].apply(lambda x: 1 if x == 'op_device_nan' else 0)) / n_tr_op_user
        feature_train['op_net_type_nan_perc'].loc[i] = sum(
            tr_op_user['net_type'].apply(lambda x: 1 if x == 'net_type_nan' else 0)) / n_tr_op_user
    if n_tr_trans_user > 0:
        feature_train['trans_tunnel_in_nan_perc'].loc[i] = sum(
            tr_trans_user['tunnel_in'].apply(lambda x: 1 if x == 'tunnel_in_nan' else 0)) / n_tr_trans_user

for i in range(n_test):
    if i % 1000 == 0:
        print(i)

    cur_user = test_base_df['user'].loc[i]
    tr_trans_user = test_trans_df[test_trans_df['user'] == cur_user]  # 该用户的trans记录
    tr_op_user = test_op_df[test_op_df['user'] == cur_user]  # 该用户的op记录
    n_tr_trans_user = len(tr_trans_user)  # 该用户的trans记录条数
    n_tr_op_user = len(tr_op_user)  # 该用户的op记录条数

    if n_tr_op_user > 0:
        feature_test['op_device_nan_perc'].loc[i] = sum(
            tr_op_user['op_device'].apply(lambda x: 1 if x == 'op_device_nan' else 0)) / n_tr_op_user
        feature_test['op_net_type_nan_perc'].loc[i] = sum(
            tr_op_user['net_type'].apply(lambda x: 1 if x == 'net_type_nan' else 0)) / n_tr_op_user
    if n_tr_trans_user > 0:
        feature_test['trans_tunnel_in_nan_perc'].loc[i] = sum(
            tr_trans_user['tunnel_in'].apply(lambda x: 1 if x == 'tunnel_in_nan' else 0)) / n_tr_trans_user

feature_train.to_csv(base_dir + '/dataset/dataset2/trainset/feature_train.csv', index=False)
feature_test.to_csv(base_dir + '/dataset/dataset2/testset/feature_test.csv', index=False)

# %%
feature_train = pd.read_csv(base_dir + '/dataset/dataset2/trainset/feature_train.csv')

for i in range(len(feature_train)):
    if i % 1000 == 0:
        print(i)
    if feature_train['n_op'].loc[i] == 0:
        feature_train.loc[i, ('op_type_0', 'op_type_1', 'op_type_2', 'op_type_3', 'op_type_4', 'op_type_5',
                              'op_type_6', 'op_type_7', 'op_type_8', 'op_type_9', 'op_type_perc', 'op_type_std',
                              'op_type_n', 'op_mode_0',
                              'op_mode_1', 'op_mode_2', 'op_mode_3', 'op_mode_4', 'op_mode_5', 'op_mode_6', 'op_mode_7',
                              'op_mode_8',
                              'op_mode_9', 'op_mode_perc', 'op_mode_std', 'op_mode_n', 'op_device_perc',
                              'op_device_std',
                              'op_device_nan_perc', 'op_device_n', 'op_ip_perc', 'op_ip_std', 'op_ip_nan_perc',
                              'op_ip_n', 'op_net_type_0',
                              'op_net_type_1', 'op_net_type_2', 'op_net_type_3', 'op_net_type_perc', 'op_net_type_std',
                              'op_net_type_nan_perc', 'op_channel_0', 'op_channel_1', 'op_channel_2', 'op_channel_3',
                              'op_channel_4',
                              'op_channel_perc', 'op_channel_std', 'op_channel_n', 'op_ip_3_perc', 'op_ip_3_std',
                              'op_ip_3_nan_perc',
                              'op_ip_3_n', 'op_ip_3_ch_freq', 'op_ip_48h_n', 'op_device_48h_n',
                              'op_48h_n')] = -1
    if feature_train['n_trans'].loc[i] == 0:
        feature_train.loc[i, ('trans_platform_0', 'trans_platform_1', 'trans_platform_2', 'trans_platform_3',
                              'trans_platform_4', 'trans_platform_5', 'trans_platform_perc', 'trans_platform_std',
                              'trans_platform_n',
                              'trans_tunnel_in_0', 'trans_tunnel_in_1', 'trans_tunnel_in_2', 'trans_tunnel_in_3',
                              'trans_tunnel_in_4',
                              'trans_tunnel_in_5', 'trans_tunnel_in_perc', 'trans_tunnel_in_std', 'trans_tunnel_in_n',
                              'trans_tunnel_in_nan_perc', 'trans_tunnel_out_0', 'trans_tunnel_out_1',
                              'trans_tunnel_out_2',
                              'trans_tunnel_out_3', 'trans_tunnel_out_perc', 'trans_tunnel_out_std', 'trans_tunnel_n',
                              'trans_amount_max',
                              'trans_amount_avg', 'trans_amount_std', 'trans_type1_0', 'trans_type1_1', 'trans_type1_2',
                              'trans_type1_3',
                              'trans_type1_4', 'trans_type1_perc', 'trans_type1_std', 'trans_ip_perc', 'trans_ip_std',
                              'trans_ip_nan_perc',
                              'trans_ip_n', 'trans_type2_0', 'trans_type2_1', 'trans_type2_2', 'trans_type2_3',
                              'trans_type2_4',
                              'trans_type2_perc', 'trans_type2_std', 'trans_ip_3_perc', 'trans_ip_3_std',
                              'trans_ip_3_nan_perc',
                              'trans_ip_3_n', 'trans_ip_3_ch_freq',
                              'trans_amount_48h_n', 'trans_48h_n', 'trans_platform_48h_n', 'trans_ip_48h_n')] = -1

feature_train.to_csv(base_dir + '/dataset/dataset2/trainset/feature_train.csv', index=False)

# %%
feature_train = pd.read_csv(base_dir + '/dataset/dataset2/trainset/feature_train.csv')
train_base_df = pd.read_csv(base_dir + '/dataset/dataset2/trainset/train_base.csv')

feature_train = feature_train.drop(labels='user', axis=1)

train_base_df = train_base_df.join(feature_train)

train_base_df.to_csv(base_dir + '/dataset/dataset2/trainset/train_main.csv', index=False)
