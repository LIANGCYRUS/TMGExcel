import pandas as pd

# 读取 alipay.csv 文件，使用 gbk 编码
df_alipay = pd.read_csv('raw/alipay.csv', encoding='gbk', dtype={'Partner_transaction_id': str})
df_alipay_rows = df_alipay.shape[0]-1
print(df_alipay_rows)

# 读取 order.xlsx 文件，指定要读取的 sheet 名称
df_order = pd.read_excel('raw/order.xlsx', sheet_name='Sheet1', usecols=['订单编号', '确认收货时间'], dtype={'订单编号': str})
df_order_rows = df_order.shape[0]-1
print(df_order_rows)


# 合并两个数据集
df_merged = pd.merge(df_alipay, df_order, left_on='Partner_transaction_id', right_on='订单编号', how='left')

# 将“确认收货时间”列中的 0 值替换为空格，将缺失的值替换为“请手动确认”
df_merged['确认收货时间'] = df_merged['确认收货时间'].fillna('')
df_merged.loc[df_merged['订单编号'].isna(), '确认收货时间'] = '请手动确认'

# 新增“退款类型”列
df_merged.loc[df_merged['Amount'] == df_merged['Refund'], '退款类型'] = '售前全额退款'

df_merged_rows = df_merged.shape[0]-1
print(df_merged_rows)

df_merged.to_excel('jieguo.xlsx',index=False)
print('成功导出文件')