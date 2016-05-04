# 用于中文分词

import jieba

INPUT_NAME = "运维类职位信息.txt"


def fenci():
    """参照: https://github.com/fxsjy/jieba"""
    data = ""
    with open(INPUT_NAME, "r") as f:
        data = f.read()
    seg_list = jieba.cut(data, cut_all=False)
    result = [r for r in seg_list if r.strip() not in (
        "", " ", "、", "/", ",", ".", "@", "$",
        "，", "的", "；", ";", "nbsp", "和", "。",
        "北京", "地区", "中国", "上海", "深圳", "福利",
        "满意度", "中", "熟悉"
    )]
    return result


def show_top_n(data):
    records = dict()
    for record in data:
        if record not in records:
            records[record] = 0
        records[record] += 1
    sorted_data = sorted(records.items(),
                         key=lambda d: d[1],
                         reverse=True)
    for r in sorted_data[:200]:
        # 输出后需要手工做下过滤
        print("{kw}: {cnt}".format(kw=r[0], cnt=r[1]))


if __name__ == "__main__":
    result = fenci()
    show_top_n(result)
