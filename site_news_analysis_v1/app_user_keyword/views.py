from django.shortcuts import render
import pandas as pd
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
import ast
# (1) we can load data using read_csv()
# global variable
# df = pd.read_csv('dataset/news_dataset_preprocessed_for_django.csv', sep='|')

# (2) we can load data using reload_df_data() function
def load_df_data():
    # df is a global variable
    global  df
    df = pd.read_csv('app_user_keyword/dataset/ltn_category_news_hw3_processed.csv', sep='|')

# We should reload df when necessary
load_df_data() 

# hoem page
def home(request):
    return render(request, 'app_user_keyword/home.html')

# When POST is used, make this function be exempted from the csrf 
@csrf_exempt
def api_get_top_userkey(request):
    userkey = request.POST.get('userkey')  # 例如「外交部 捐贈烏克蘭」
    cate = request.POST.get('cate')
    cond = request.POST.get('cond')       # "and" / "or" / "single"
    weeks = int(request.POST.get('weeks'))
    key = userkey.split()
    global df_query
    df_query = filter_dataFrame(key, cond, cate, weeks)

    key_freq_cat, key_occurrence_cat = count_keyword(df_query, key, cond)
    key_time_freq = get_keyword_time_based_freq(df_query, key, cond)
    response = {
        'key_occurrence_cat': key_occurrence_cat,
        'key_freq_cat': key_freq_cat,
        'key_time_freq': key_time_freq,
    }
    return JsonResponse(response)

def filter_dataFrame(user_keywords, cond, cate, weeks):
    # 時間區間
    end_date = df.date.max()
    start_date = (datetime.strptime(end_date, '%Y-%m-%d').date() - timedelta(weeks=weeks)).strftime('%Y-%m-%d')
    df['tokens_v2'] = df['tokens_v2'].astype(str).fillna('')
    base_condition = (df['date'] >= start_date) & (df['date'] <= end_date)
    if cate != "全部":
        base_condition &= (df['category'] == cate)
    def get_tokens(text):
        try:
            tokens = eval(text) if isinstance(text, str) else []
            return tokens if isinstance(tokens, list) else []
        except:
            return []
    if cond == "and":
        keyword_condition = df['tokens_v2'].apply(lambda text:
            all(qk in get_tokens(text) for qk in user_keywords))
    elif cond == "or":
        keyword_condition = df['tokens_v2'].apply(lambda text:
            any(qk in get_tokens(text) for qk in user_keywords))
    elif cond == "single":
        keyword_condition = df['tokens_v2'].apply(lambda text:
            any(qk in get_tokens(text) for qk in user_keywords))  # 單獨統計時先保留符合任一的
    else:
        keyword_condition = pd.Series([True] * len(df))  # 無條件過濾
    content_valid = df['content'].apply(lambda text: isinstance(text, str))
    return df[base_condition & content_valid & keyword_condition]

news_categories = ['政治', '國際', '社會', '生活', '地方']
def count_keyword(query_df, user_keywords, cond):
    cate_occurence = {'全部': 0}
    cate_freq = {'全部': {key: 0 for key in user_keywords}}
    for cate in news_categories:
        cate_occurence[cate] = 0
        cate_freq[cate] = {key: 0 for key in user_keywords}
    for idx, row in query_df.iterrows():
        category = row.category
        tokens = eval(row.tokens_v2) if isinstance(row.tokens_v2, str) else []
        if not isinstance(tokens, list): tokens = []
        # 條件檢查
        if cond == "and" and not all(k in tokens for k in user_keywords):
            continue
        if cond == "or" and not any(k in tokens for k in user_keywords):
            continue
        cate_occurence[category] += 1
        cate_occurence['全部'] += 1
        for keyword in user_keywords:
            count = sum(1 for word in tokens if word == keyword)
            cate_freq[category][keyword] += count
            cate_freq['全部'][keyword] += count
    return cate_freq, cate_occurence

def get_keyword_time_based_freq(df_query, user_keywords, cond):
    time_data = []
    for keyword in user_keywords:
        filtered_df = df_query[df_query['tokens_v2'].apply(
            lambda text: keyword in eval(text) if isinstance(text, str) else False
        )]
        query_freq = pd.DataFrame({
            'date_index': pd.to_datetime(filtered_df.date),
            'freq': [1] * len(filtered_df)
        })
        data = query_freq.groupby(pd.Grouper(key='date_index', freq='D')).sum()
        keyword_time_data = [{'x': idx.strftime('%Y-%m-%d'), 'y': int(row.freq)} for idx, row in data.iterrows()]
        time_data.append({
            'label': keyword,
            'data': keyword_time_data
        })
    return time_data
# create your views here.
















###期中報告!!!!
# def api_get_top_userkey(request):
#     # (1) get keywords, category, condition, and weeks passed from frontend
#     userkey = request.POST.get('userkey')
#     cate = request.POST.get('cate')
#     weeks = int(request.POST.get('weeks'))
#     key = userkey.split()
    
#     # (2) make df_query global, so it can be used by other functions
#     global  df_query 

#     # (3) filter dataframe
#     df_query = filter_dataFrame(key, cate,weeks)
#     #print(len(df_query))

#     # (4) get frequency data
#     key_freq_cat, key_occurrence_cat = count_keyword(df_query, key)
#     print(key_occurrence_cat)
    
#     # (5) get line chart data
#     # key_time_freq = [
#     # '{"x": "2019-03-07", "y": 2}',
#     # '{"x": "2019-03-08", "y": 2}',
#     # '{"x": "2019-03-09", "y": 13}']
#     key_time_freq = get_keyword_time_based_freq(df_query,key)
#     print(key_time_freq )

#     # (6) response all data to frontend home page
#     response = {
#     'key_occurrence_cat': key_occurrence_cat,
#     'key_freq_cat': key_freq_cat,
#     'key_time_freq': key_time_freq, }

#     return JsonResponse(response)
# def filter_dataFrame(user_keywords, cate, weeks):
#     # end date: the date of the latest record of news
#     end_date = df.date.max()

#     # start date
#     start_date = (datetime.strptime(end_date, '%Y-%m-%d').date() - timedelta(weeks=weeks)).strftime('%Y-%m-%d')
#     df['tokens_v2'] = df['tokens_v2'].astype(str).fillna('')

#     # 条件过滤
#     base_condition = (df['date'] >= start_date) & (df['date'] <= end_date)

#     if cate != "全部":
#         base_condition &= (df['category'] == cate)

#     # 直接使用 'or' 逻辑来检查关键字是否出现在文本中
#     keyword_condition = df['tokens_v2'].apply(lambda text: any(qk in text for qk in user_keywords))

#     # 处理 `content` 列中的 NaN 或非字符串数据
#     condition = base_condition & df['content'].apply(lambda text: isinstance(text, str) and not isinstance(text, float))

#     # 返回过滤后的数据框
#     return df[condition & keyword_condition]
# def count_keyword(query_df, user_keywords):
#     cate_occurence = {'全部': 0}  # 确保 '全部' 在初始化时已经存在
#     cate_freq = {'全部': {key: 0 for key in user_keywords}}  # 每个关键字有单独的计数器

#     for cate in news_categories:
#         cate_occurence[cate] = 0
#         cate_freq[cate] = {key: 0 for key in user_keywords}  # 每个类别也有单独的计数器

#     for idx, row in query_df.iterrows():
#         category = row.category
#         if category not in cate_occurence:
#             cate_occurence[category] = 0
#         if category not in cate_freq:
#             cate_freq[category] = {key: 0 for key in user_keywords}

#         # 计算新闻数量
#         cate_occurence[category] += 1
#         cate_occurence['全部'] += 1

#         # 确保 'tokens_v2' 是字符串并且可解析为 list
#         try:
#             tokens = eval(row.tokens_v2) if isinstance(row.tokens_v2, str) else row.tokens_v2
#             if not isinstance(tokens, list):
#                 tokens = []
#         except Exception as e:
#             print(f"解析 tokens_v2 出错: {e}")
#             tokens = []

#         # 计算每个关键词的出现次数
#         for keyword in user_keywords:
#             freq = sum(1 for word in tokens if word == keyword)
#             cate_freq[category][keyword] += freq
#             cate_freq['全部'][keyword] += freq  # 确保 "全部" 是已初始化的 key

#     return cate_freq, cate_occurence

# def get_keyword_time_based_freq(df_query, user_keywords):
#     time_data = []
    
#     for keyword in user_keywords:
#         # 过滤出特定关键字的数据
#         keyword_data = df_query[df_query['tokens_v2'].apply(lambda tokens: keyword in tokens)]
        
#         # 按日期进行统计
#         date_samples = keyword_data.date
#         query_freq = pd.DataFrame({'date_index': pd.to_datetime(date_samples), 'freq': [1 for _ in range(len(keyword_data))]})
#         data = query_freq.groupby(pd.Grouper(key='date_index', freq='D')).sum()

#         keyword_time_data = []
#         for i, idx in enumerate(data.index):
#             row = {'x': idx.strftime('%Y-%m-%d'), 'y': int(data.iloc[i].freq)}
#             keyword_time_data.append(row)

#         time_data.append({
#             'label': keyword,  # 为每个关键字指定标签
#             'data': keyword_time_data
#         })

#     return time_data
# print("app_user_keyword was loaded!")