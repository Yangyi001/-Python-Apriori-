import pandas as pd

# 读取文件
f = pd.read_csv('sales_detail.csv', encoding='utf-8', sep='\t', header=None)

def deprive_bracket_specification(trade_name):
    # 提取商品名（中文字符），从左到右，第一个中文字符开始，第一个非中文字符结束
    # unicode编码中文的范围是4e00~9fa5
    trade_name_not_specification = list()

    start = 0

    # 左边第一个中文字符开始
    for char in trade_name:
        if not ('\u4e00' <= char <= '\u9fff'):
            start += 1
        else:
            break

    # 右边第一个非中文字符结束
    for char in trade_name[start:]:
        if '\u4e00' <= char <= '\u9fff':
            trade_name_not_specification.append(char)
        else:
            break

    return ''.join(trade_name_not_specification)

# 提取订单号列和商品名列
tip_shopname = f.loc[:,[0,5]]
tip_shopname.columns = ['tip', 'shopname']

# 去除商品的规格
tip_shopname.shopname = tip_shopname.shopname.apply(func=deprive_bracket_specification)

# 对商品名按照订单号进行分篮
grouping_by_grocery_list = []
for meb in  tip_shopname.groupby('tip'):
    grouping_by_grocery_list.append(list(meb[1].shopname))

# 导入所需要的包
from apyori import apriori

# 使用apriori包进行频繁项集及关联规则的发现。
result = apriori(grouping_by_grocery_list, min_support=0.00002, min_confidence=0.7, min_lift=10, max_length=2)

# 将结果迭代器转保存为列表
result_list = []
for meb in result:
    result_list.append(meb)

# 查看发现的频繁项集
for meb in result_list:
    print(meb.items)

# 查看对应的置信度、上升度等
for meb in result_list:
    print(meb)