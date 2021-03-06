# %%
import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.decomposition import PCA

base_dir = os.getcwd()

if __name__ == '__main__':
    pass

# %%
# 原来的需要保留的表头
old_headers_op = ['user', 'n_op', 'op_type_perc', 'op_type_std', 'op_type_n', 'op_mode_perc', 'op_mode_std',
                  'op_mode_n', 'op_device_perc', 'op_device_std', 'op_device_nan_perc', 'op_ip_perc', 'op_ip_std',
                  'op_ip_nan_perc', 'op_ip_n', 'op_net_type_perc', 'op_net_type_std', 'op_net_type_nan_perc',
                  'op_channel_perc', 'op_channel_std', 'op_channel_n', 'op_ip_3_perc', 'op_ip_3_std',
                  'op_ip_3_nan_perc', 'op_ip_3_n', 'op_ip_3_ch_freq', 'op_ip_48h_n', 'op_device_48h_n', 'op_48h_n']
old_headers_trans = ['user', 'n_trans', 'trans_platform_perc', 'trans_platform_std', 'trans_tunnel_in_perc',
                     'trans_tunnel_in_std', 'trans_tunnel_in_nan_perc', 'trans_tunnel_out_std', 'trans_amount_max',
                     'trans_amount_avg', 'trans_amount_std', 'trans_type1_0', 'trans_type1_1', 'trans_type1_2',
                     'trans_type1_3', 'trans_type1_4', 'trans_type1_perc', 'trans_type1_std', 'trans_ip_perc',
                     'trans_ip_std', 'trans_ip_nan_perc', 'trans_ip_n', 'trans_type2_perc', 'trans_type2_std',
                     'trans_ip_3_std', 'trans_ip_3_nan_perc', 'trans_ip_3_ch_freq', 'trans_amount_48h_n',
                     'trans_48h_n', 'trans_platform_48h_n', 'trans_ip_48h_n']

headers_op = ['user', 'n_op', 'op_type_perc', 'op_type_std', 'op_type_n', 'op_mode_perc', 'op_mode_std', 'op_mode_n',
              'op_device_perc', 'op_device_std', 'op_device_nan_perc', 'op_ip_perc', 'op_ip_std', 'op_ip_nan_perc',
              'op_ip_n', 'op_net_type_perc', 'op_net_type_std', 'op_net_type_nan_perc', 'op_channel_perc',
              'op_channel_std', 'op_channel_n', 'op_ip_3_perc', 'op_ip_3_std', 'op_ip_3_nan_perc', 'op_ip_3_n',
              'op_ip_3_ch_freq', 'op_ip_ch_freq', 'op_device_ch_freq', 'op_net_type_ch_freq', 'op_channel_ch_freq',
              'op_ip_48h_n', 'op_ip_3_48h_n', 'op_device_48h_n', 'op_48h_n', ]
headers_trans = ['user', 'n_trans', 'trans_platform_perc', 'trans_platform_std', 'trans_tunnel_in_perc', 'trans_tunnel_in_std',
                 'trans_tunnel_in_nan_perc', 'trans_tunnel_out_std', 'trans_amount_max', 'trans_amount_avg',
                 'trans_amount_std', 'trans_type1_0', 'trans_type1_1', 'trans_type1_2', 'trans_type1_3',
                 'trans_type1_4', 'trans_type1_perc', 'trans_type1_std', 'trans_ip_perc', 'trans_ip_std',
                 'trans_ip_nan_perc', 'trans_ip_n', 'trans_type2_perc', 'trans_type2_std', 'trans_ip_3_std',
                 'trans_ip_3_nan_perc', 'trans_ip_3_ch_freq', 'trans_ip_ch_freq', 'trans_platform_ch_freq',
                 'trans_amount_48h_n', 'trans_48h_n', 'trans_platform_48h_n', 'trans_ip_48h_n', 'trans_ip_3_48h_n']

# %%
# 新的特征矩阵
train_base_df = pd.read_csv(base_dir + '/dataset/dataset2/trainset/train_base.csv')
test_base_df = pd.read_csv(base_dir + '/dataset/dataset2/testset/test_a_base.csv')
feature_train_op = pd.DataFrame(columns=headers_op)
feature_test_op = pd.DataFrame(columns=headers_op)
feature_train_trans = pd.DataFrame(columns=headers_trans)
feature_test_trans = pd.DataFrame(columns=headers_trans)
n_train = len(train_base_df)
n_test = len(test_base_df)

# 旧的特征矩阵
old_feature_train = pd.read_csv(base_dir + '/dataset/dataset2/trainset/feature_train.csv')
old_feature_test = pd.read_csv(base_dir + '/dataset/dataset2/testset/feature_test.csv')

# %%
# 将需要留下的特征搬运到新的矩阵中
for feature in old_headers_op:
    feature_train_op[feature] = old_feature_train[feature]
    feature_test_op[feature] = old_feature_test[feature]
for feature in old_headers_trans:
    feature_train_trans[feature] = old_feature_train[feature]
    feature_test_trans[feature] = old_feature_test[feature]

# %%
# 载入辅助矩阵，准备写入新特征
train_op_df = pd.read_csv(base_dir + '/dataset/dataset2/trainset/train_op.csv')
train_trans_df = pd.read_csv(base_dir + '/dataset/dataset2/trainset/train_trans.csv')
test_op_df = pd.read_csv(base_dir + '/dataset/dataset2/testset/test_a_op.csv')
test_trans_df = pd.read_csv(base_dir + '/dataset/dataset2/testset/test_a_trans.csv')


# %%
def process(n, isTrain=True):
    for i in range(n):
        if i % 1000 == 0:
            print(i)

        if isTrain:
            cur_user = feature_train_op['user'].loc[i]
            trans_user = train_trans_df[train_trans_df['user'] == cur_user]
            op_user = train_op_df[train_op_df['user'] == cur_user]
        else:
            cur_user = feature_test_op['user'].loc[i]
            trans_user = test_trans_df[test_trans_df['user'] == cur_user]
            op_user = test_op_df[test_op_df['user'] == cur_user]

        n_trans_user = len(trans_user)
        n_op_user = len(op_user)

        if n_op_user > 0:
            # 对 tm_diff 排序
            op_user.sort_values('tm_diff', inplace=True)

            # 统计各种频率
            cnt_op_ip = 0
            cnt_op_device = 0
            cnt_op_net_type = 0
            cnt_op_channel = 0
            lst_op_ip = op_user['ip'].tolist()
            lst_op_device = op_user['op_device'].tolist()
            lst_op_net_type = op_user['net_type'].tolist()
            lst_op_channel = op_user['channel'].tolist()
            pre_op_ip = lst_op_ip[0]
            pre_op_device = lst_op_device[0]
            pre_op_net_type = lst_op_net_type[0]
            pre_op_channel = lst_op_channel[0]
            for j in range(1, n_op_user):
                if pre_op_ip != lst_op_ip[j]:
                    pre_op_ip = lst_op_ip[j]
                    cnt_op_ip += 1
                if pre_op_device != lst_op_device[j]:
                    pre_op_device = lst_op_device[j]
                    cnt_op_device += 1
                if pre_op_net_type != lst_op_net_type[j]:
                    pre_op_net_type = lst_op_net_type[j]
                    cnt_op_net_type += 1
                if pre_op_channel != lst_op_channel[j]:
                    pre_op_channel = lst_op_channel[j]
                    cnt_op_channel += 1

            if isTrain:
                feature_train_op['op_ip_ch_freq'].loc[i] = cnt_op_ip
                feature_train_op['op_device_ch_freq'].loc[i] = cnt_op_device
                feature_train_op['op_net_type_ch_freq'].loc[i] = cnt_op_net_type
                feature_train_op['op_channel_ch_freq'].loc[i] = cnt_op_channel
            else:
                feature_test_op['op_ip_ch_freq'].loc[i] = cnt_op_ip
                feature_test_op['op_device_ch_freq'].loc[i] = cnt_op_device
                feature_test_op['op_net_type_ch_freq'].loc[i] = cnt_op_net_type
                feature_test_op['op_channel_ch_freq'].loc[i] = cnt_op_channel

            # 统计各种48h滑窗
            gap = 48 * 3600
            max_op_ip_48h_n = 0
            max_op_ip_3_48h_n = 0
            max_op_device_48h_n = 0
            max_op_48h_n = 0
            time_lst = op_user['tm_diff'].tolist()
            start_idx = 0
            start_time = time_lst[0]
            gap_df = op_user[(start_time <= op_user['tm_diff']) & (op_user['tm_diff'] <= start_time + gap)]
            end_idx = len(gap_df)
            pre_end_idx = 0
            while end_idx < n_op_user and start_idx < n_op_user:
                while end_idx < n_op_user-1 and time_lst[end_idx+1] - time_lst[start_idx] <= gap:
                    end_idx += 1
                if end_idx != pre_end_idx and start_idx < n_op_user and end_idx < n_op_user:
                    gap_df = op_user[(time_lst[start_idx] <= op_user['tm_diff']) &
                                     (op_user['tm_diff'] <= time_lst[end_idx])]
                    max_op_ip_48h_n = max(max_op_ip_48h_n, gap_df['ip'].nunique())
                    max_op_ip_3_48h_n = max(max_op_ip_3_48h_n, gap_df['ip_3'].nunique())
                    max_op_device_48h_n = max(max_op_device_48h_n, gap_df['op_device'].nunique())
                    max_op_48h_n = max(max_op_48h_n, len(gap_df))
                    pre_end_idx = end_idx
                start_idx += 1

            if isTrain:
                feature_train_op['op_ip_48h_n'].loc[i] = max_op_ip_48h_n
                feature_train_op['op_ip_3_48h_n'].loc[i] = max_op_ip_3_48h_n
                feature_train_op['op_device_48h_n'].loc[i] = max_op_device_48h_n
                feature_train_op['op_48h_n'].loc[i] = max_op_48h_n
            else:
                feature_test_op['op_ip_48h_n'].loc[i] = max_op_ip_48h_n
                feature_test_op['op_ip_3_48h_n'].loc[i] = max_op_ip_3_48h_n
                feature_test_op['op_device_48h_n'].loc[i] = max_op_device_48h_n
                feature_test_op['op_48h_n'].loc[i] = max_op_48h_n
        else:
            if isTrain:
                feature_train_op['op_ip_ch_freq'].loc[i] = -1
                feature_train_op['op_device_ch_freq'].loc[i] = -1
                feature_train_op['op_net_type_ch_freq'].loc[i] = -1
                feature_train_op['op_channel_ch_freq'].loc[i] = -1
                feature_train_op['op_ip_48h_n'].loc[i] = -1
                feature_train_op['op_ip_3_48h_n'].loc[i] = -1
                feature_train_op['op_device_48h_n'].loc[i] = -1
                feature_train_op['op_48h_n'].loc[i] = -1
            else:
                feature_test_op['op_ip_ch_freq'].loc[i] = -1
                feature_test_op['op_device_ch_freq'].loc[i] = -1
                feature_test_op['op_net_type_ch_freq'].loc[i] = -1
                feature_test_op['op_channel_ch_freq'].loc[i] = -1
                feature_test_op['op_ip_48h_n'].loc[i] = -1
                feature_test_op['op_ip_3_48h_n'].loc[i] = -1
                feature_test_op['op_device_48h_n'].loc[i] = -1
                feature_test_op['op_48h_n'].loc[i] = -1

        if n_trans_user > 0:
            # 对 tm_diff 排序
            trans_user.sort_values('tm_diff', inplace=True)

            # 统计各种频率
            cnt_trans_ip = 0
            cnt_trans_platform = 0
            lst_trans_ip = trans_user['ip'].tolist()
            lst_trans_platform = trans_user['platform'].tolist()
            pre_trans_ip = lst_trans_ip[0]
            pre_trans_platform = lst_trans_platform[0]
            for j in range(1, n_trans_user):
                if pre_trans_ip != lst_trans_ip[j]:
                    pre_trans_ip = lst_trans_ip[j]
                    cnt_trans_ip += 1
                if pre_trans_platform != lst_trans_platform[j]:
                    pre_trans_platform = lst_trans_platform[j]
                    cnt_trans_platform += 1

            if isTrain:
                feature_train_trans['trans_ip_ch_freq'].loc[i] = cnt_trans_ip
                feature_train_trans['trans_platform_ch_freq'].loc[i] = cnt_trans_platform
            else:
                feature_test_trans['trans_ip_ch_freq'].loc[i] = cnt_trans_ip
                feature_test_trans['trans_platform_ch_freq'].loc[i] = cnt_trans_platform

            # 统计各种48h滑窗
            gap = 48 * 3600
            max_trans_amount_48h_n = 0
            max_trans_48h_n = 0
            max_trans_platform_48h_n = 0
            max_trans_ip_48h_n = 0
            max_trans_ip_3_48h_n = 0
            time_lst = trans_user['tm_diff'].tolist()
            start_idx = 0
            start_time = time_lst[0]
            gap_df = trans_user[(start_time <= trans_user['tm_diff']) & (trans_user['tm_diff'] <= start_time + gap)]
            end_idx = len(gap_df)
            pre_end_idx = 0
            while end_idx < n_trans_user and start_idx < n_trans_user:
                while end_idx < n_trans_user-1 and time_lst[end_idx+1] - time_lst[start_idx] <= gap:
                    end_idx += 1
                if end_idx != pre_end_idx and start_idx < n_trans_user and end_idx < n_trans_user:
                    gap_df = trans_user[(time_lst[start_idx] <= trans_user['tm_diff']) &
                                        (trans_user['tm_diff'] <= time_lst[end_idx])]
                    max_trans_amount_48h_n = max(max_trans_amount_48h_n, gap_df['amount'].values.sum())
                    max_trans_48h_n = max(max_trans_48h_n, len(gap_df))
                    max_trans_platform_48h_n = max(max_trans_platform_48h_n, gap_df['platform'].nunique())
                    max_trans_ip_48h_n = max(max_trans_ip_48h_n, gap_df['ip'].nunique())
                    max_trans_ip_3_48h_n = max(max_trans_ip_3_48h_n, gap_df['ip_3'].nunique())
                    pre_end_idx = end_idx
                start_idx += 1

            if isTrain:
                feature_train_trans['trans_amount_48h_n'].loc[i] = max_trans_amount_48h_n
                feature_train_trans['trans_48h_n'].loc[i] = max_trans_48h_n
                feature_train_trans['trans_platform_48h_n'].loc[i] = max_trans_platform_48h_n
                feature_train_trans['trans_ip_48h_n'].loc[i] = max_trans_ip_48h_n
                feature_train_trans['trans_ip_3_48h_n'].loc[i] = max_trans_ip_3_48h_n
            else:
                feature_test_trans['trans_amount_48h_n'].loc[i] = max_trans_amount_48h_n
                feature_test_trans['trans_48h_n'].loc[i] = max_trans_48h_n
                feature_test_trans['trans_platform_48h_n'].loc[i] = max_trans_platform_48h_n
                feature_test_trans['trans_ip_48h_n'].loc[i] = max_trans_ip_48h_n
                feature_test_trans['trans_ip_3_48h_n'].loc[i] = max_trans_ip_3_48h_n
        else:
            if isTrain:
                feature_train_trans['trans_ip_ch_freq'].loc[i] = -1
                feature_train_trans['trans_platform_ch_freq'].loc[i] = -1
                feature_train_trans['trans_amount_48h_n'].loc[i] = -1
                feature_train_trans['trans_48h_n'].loc[i] = -1
                feature_train_trans['trans_platform_48h_n'].loc[i] = -1
                feature_train_trans['trans_ip_48h_n'].loc[i] = -1
                feature_train_trans['trans_ip_3_48h_n'].loc[i] = -1
            else:
                feature_test_trans['trans_ip_ch_freq'].loc[i] = -1
                feature_test_trans['trans_platform_ch_freq'].loc[i] = -1
                feature_test_trans['trans_amount_48h_n'].loc[i] = -1
                feature_test_trans['trans_48h_n'].loc[i] = -1
                feature_test_trans['trans_platform_48h_n'].loc[i] = -1
                feature_test_trans['trans_ip_48h_n'].loc[i] = -1
                feature_test_trans['trans_ip_3_48h_n'].loc[i] = -1


# %%
# process(n_train, isTrain=True)
process(n_test, isTrain=False)

# %%
# 暂存特征
feature_train_op.to_csv(base_dir + '/dataset/dataset4/trainset/feature_train_op.csv', index=False)
feature_train_trans.to_csv(base_dir + '/dataset/dataset4/trainset/feature_train_trans.csv', index=False)
feature_test_op.to_csv(base_dir + '/dataset/dataset4/testset/feature_test_op.csv', index=False)
feature_test_trans.to_csv(base_dir + '/dataset/dataset4/testset/feature_test_trans.csv', index=False)

# %%
# 读取新特征
feature_train_op = pd.read_csv(base_dir + '/dataset/dataset4/trainset/feature_train_op.csv')
feature_train_trans = pd.read_csv(base_dir + '/dataset/dataset4/trainset/feature_train_trans.csv')
feature_test_op = pd.read_csv(base_dir + '/dataset/dataset4/testset/feature_test_op.csv')
feature_test_trans = pd.read_csv(base_dir + '/dataset/dataset4/testset/feature_test_trans.csv')

# %%
for i in range(n_train):
    if feature_train_op['n_op'].loc[i] == 0:
        feature_train_op['op_ip_ch_freq'].loc[i] = -1
        feature_train_op['op_device_ch_freq'].loc[i] = -1
        feature_train_op['op_net_type_ch_freq'].loc[i] = -1
        feature_train_op['op_channel_ch_freq'].loc[i] = -1
        feature_train_op['op_ip_48h_n'].loc[i] = -1
        feature_train_op['op_ip_3_48h_n'].loc[i] = -1
        feature_train_op['op_device_48h_n'].loc[i] = -1
        feature_train_op['op_48h_n'].loc[i] = -1
    if feature_train_trans['n_trans'].loc[i] == 0:
        feature_train_trans['trans_ip_ch_freq'].loc[i] = -1
        feature_train_trans['trans_platform_ch_freq'].loc[i] = -1
        feature_train_trans['trans_amount_48h_n'].loc[i] = -1
        feature_train_trans['trans_48h_n'].loc[i] = -1
        feature_train_trans['trans_platform_48h_n'].loc[i] = -1
        feature_train_trans['trans_ip_48h_n'].loc[i] = -1
        feature_train_trans['trans_ip_3_48h_n'].loc[i] = -1

for i in range(n_test):
    if feature_test_op['n_op'].loc[i] == 0:
        feature_test_op['op_ip_ch_freq'].loc[i] = -1
        feature_test_op['op_device_ch_freq'].loc[i] = -1
        feature_test_op['op_net_type_ch_freq'].loc[i] = -1
        feature_test_op['op_channel_ch_freq'].loc[i] = -1
        feature_test_op['op_ip_48h_n'].loc[i] = -1
        feature_test_op['op_ip_3_48h_n'].loc[i] = -1
        feature_test_op['op_device_48h_n'].loc[i] = -1
        feature_test_op['op_48h_n'].loc[i] = -1
    if feature_test_trans['n_trans'].loc[i] == 0:
        feature_test_trans['trans_ip_ch_freq'].loc[i] = -1
        feature_test_trans['trans_platform_ch_freq'].loc[i] = -1
        feature_test_trans['trans_amount_48h_n'].loc[i] = -1
        feature_test_trans['trans_48h_n'].loc[i] = -1
        feature_test_trans['trans_platform_48h_n'].loc[i] = -1
        feature_test_trans['trans_ip_48h_n'].loc[i] = -1
        feature_test_trans['trans_ip_3_48h_n'].loc[i] = -1

order = feature_train_op.columns.tolist()
feature_train_op = feature_train_op[order[-1] + order[:-1]]
order = feature_train_trans.columns.tolist()
feature_train_trans = feature_train_trans[order[-1] + order[:-1]]
order = feature_test_op.columns.tolist()
feature_test_op = feature_test_op[order[-1] + order[:-1]]
order = feature_test_trans.columns.tolist()
feature_test_trans = feature_test_trans[order[-1] + order[:-1]]

feature_train_op.to_csv(base_dir + '/dataset/dataset4/trainset/feature_train_op.csv', index=False)
feature_train_trans.to_csv(base_dir + '/dataset/dataset4/trainset/feature_train_trans.csv', index=False)
feature_test_op.to_csv(base_dir + '/dataset/dataset4/testset/feature_test_op.csv', index=False)
feature_test_trans.to_csv(base_dir + '/dataset/dataset4/testset/feature_test_trans.csv', index=False)


# %%
# 删除省份数据
train_base_df = train_base_df.drop(labels=[str(x) for x in range(31)], axis=1)
test_base_df = test_base_df.drop(labels=[str(x) for x in range(31)], axis=1)

# 删除city_20 - city_49
train_base_df = train_base_df.drop(labels=['city_' + str(x) for x in range(20, 50)], axis=1)
test_base_df = test_base_df.drop(labels=['city_' + str(x) for x in range(20, 50)], axis=1)

# %%
# 对city进行降维，降到20
raw_train_base_df = pd.read_csv(base_dir + '/dataset/raw_dataset/trainset/train_base.csv')
raw_test_base_df = pd.read_csv(base_dir + '/dataset/raw_dataset/testset/test_a_base.csv')
city = pd.concat([raw_train_base_df['city'], raw_test_base_df['city']])
values_ct_org = city.unique().tolist()
values_ct = np.array(values_ct_org).reshape(len(values_ct_org), -1)
enc = OneHotEncoder()
enc.fit(values_ct)
onehot = enc.transform(values_ct).toarray()

pca = PCA(n_components=20)
pca.fit(onehot)
result = pca.transform(onehot)
mp = dict(zip(values_ct_org, [code for code in result]))

# 保存encoder
pd.DataFrame.from_dict(data=mp, orient='columns')\
    .to_csv(base_dir + '/dataset/dataset4/encoders/enc_city.csv', index=False)

for i in range(len(raw_train_base_df)):
    if i % 1000 == 0:
        print(i)
    code = mp[raw_train_base_df['city'].loc[i]]
    train_base_df.loc[i, ['city_' + str(x) for x in range(20)]] = code

for i in range(len(raw_test_base_df)):
    if i % 1000 == 0:
        print(i)
    code = mp[raw_test_base_df['city'].loc[i]]
    test_base_df.loc[i, ['city_' + str(x) for x in range(20)]] = code

# %%
# save
feature_train_op = feature_train_op.drop(labels='user', axis=1)
feature_train_trans = feature_train_trans.drop(labels='user', axis=1)
feature_test_op = feature_test_op.drop(labels='user', axis=1)
feature_test_trans = feature_test_trans.drop(labels='user', axis=1)
train_main = train_base_df.join(feature_train_op).join(feature_train_trans)
test_main = test_base_df.join(feature_test_op).join(feature_test_trans)
train_main.to_csv(base_dir + '/dataset/dataset4/trainset/train_main.csv', index=False)
test_main.to_csv(base_dir + '/dataset/dataset4/testset/test_a_main.csv', index=False)


# %%
# trytrywater
temp = pd.read_csv(r'C:\Users\RickyLi\Desktop\main_dataset.csv')
print(temp['维度'].tolist())
