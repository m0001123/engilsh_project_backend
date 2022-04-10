import pymysql
from django.http import JsonResponse
import json
from eng_to_ipa import eng_to_ipa
from similar_text import similar_text
from random import choice, sample
import re

from app.code import appAPIUtils

def getWordSetClassificationData():
    try:
        data = appAPIUtils.getWordSetClassificationData()
       
        # 初始化回傳值
        response = {
            'apiStatus' : 'success',
			'apiMessage' : 'success',
			'data' : data,
        }
    except Exception as e:
        # 初始化回傳值
        response = {
            'apiStatus' : 'error',
			'apiMessage' : str(e),
        }

    # 將回傳值回傳
    return JsonResponse(response)

def getWordByWord(request):
    try:
        word = request.POST.get('word', '')
        db = pymysql.connect(host='mysql-server-write.alicsnet.com', port=3306,
                             user='alicsnet_data', passwd='Z.0oIoi.O)PrEZT4', db='alicsnet_data', charset='utf8mb4')
        cursor = db.cursor()
        word_lst = []
        same_words = eng_to_ipa.get_rhymes(word)
        sql_where = ''
        if same_words:
            for i in range(len(same_words)):
                sql_where += f' or (word = \"{same_words[i]}\")' if i else f'(word = \"{same_words[i]}\")'
            getWord_sql = f'select distinct word from 8000wordhasipa where {sql_where} order by RAND() limit 3'
            cursor.execute(getWord_sql)
            ErrorWordOfIpa = cursor.fetchall()
            for tmp in ErrorWordOfIpa:
                word_lst.append(tmp[0])
        db.close()
        res = {
            'apiStatus': 'success',
            'apiMessage': 'success',
            'data': {'Word_lst': word_lst},
        }
    except Exception as e:
        res = {
            'apiStatus' : 'error',
            'apiMessage': str(e),
        }
    return JsonResponse(res)


def getWordByIPA(request):
    try:
        ipa = request.POST.get('ipa_id', '')
        db = pymysql.connect(host='mysql-server-write.alicsnet.com', port=3306,
                             user='alicsnet_data', passwd='Z.0oIoi.O)PrEZT4', db='alicsnet_data', charset='utf8mb4')
        cursor = db.cursor()
        word_lst = []
        getWord_sql = f'select distinct word from 8000wordhasipa where  ipaId = {ipa} order by RAND() limit 3'
        cursor.execute(getWord_sql)
        ErrorWordOfIpa = cursor.fetchall()
        for tmp in ErrorWordOfIpa:
            word_lst.append(tmp[0])
        db.close()
        res = {
            'apiStatus': 'success',
            'apiMessage': 'success',
            'data': {'Word_lst': word_lst},
        }
    except Exception as e:
        res = {
            'apiStatus' : 'error',
            'apiMessage': str(e),
        }
    return JsonResponse(res)


# 單字集學習區
# 單字集學習區 - 獲取單字集列表
def getWordSetList(request):
    try:
        # 蒐集資料
        uid = request.POST.get('uid', '')
        learningClassification = request.POST.get('learningClassification', '')

        # 判斷資料
        if (uid == ''):    
            raise Exception('缺少必填參數 uid')
        if (learningClassification == ''):    
            raise Exception('缺少必填參數 learningClassification')
   
        # 整理從資料庫得到的資料

        data = appAPIUtils.getWordSetList(uid, learningClassification)
        
        # 初始化回傳值
        response = {
            'apiStatus' : 'success',
            'apiMessage' : 'success',
            'data' : data,
        }
    except Exception as e:
        # 初始化回傳值
        response = {
            'apiStatus' : 'error',
			'apiMessage' : str(e),
        }

    # 將回傳值回傳
    return JsonResponse(response)

# 單字集學習區 - 獲取單字集資料
def getWordLearning(request):
    try:
        # 蒐集資料
        learningClassification = request.POST.get('learningClassification', '')
        learningPhase = request.POST.get('learningPhase', '')

        # 判斷資料
        if (learningClassification == ''):    
            raise Exception('缺少必填參數 learningClassification')
        if (learningPhase == ''):    
            raise Exception('缺少必填參數 learningPhase')
   
        # 整理從資料庫得到的資料
        data = appAPIUtils.getWordLearningData(learningClassification, learningPhase)
        
        # 初始化回傳值
        response = {
            'apiStatus' : 'success',
            'apiMessage' : 'success',
            'data' : data,
        }
    except Exception as e:
        # 初始化回傳值
        response = {
            'apiStatus' : 'error',
			'apiMessage' : str(e),
        }

    # 將回傳值回傳
    return JsonResponse(response)

# 單字集學習區 - 獲取下一個單字集
def addWordSet(request):
    try:
        # 蒐集資料
        uid = request.POST.get('uid', '')
        learningClassification = request.POST.get('learningClassification', '')

        # 判斷資料
        if (uid == ''):    
            raise Exception('缺少必填參數 uid')
        if (learningClassification == ''):    
            raise Exception('缺少必填參數 learningClassification')



        data = appAPIUtils.getWordSetList(uid, learningClassification)
        
        if ( len(data['wordSetArray']) >= data['wordSetTotal']):    
            raise Exception('已超出本單字集上限')
        #if ( (data['averageScore'] <= 60) and (len(data['wordSetArray']) >= 5) ):    
        #    raise Exception('平均分數過低，再練習一下吧')

        
        if not (appAPIUtils.addWordSet(uid, learningClassification, (len(data['wordSetArray']) + 1 ))):
            raise Exception('新增單字集時發生錯誤')

        # 初始化回傳值
        response = {
            'apiStatus' : 'success',
            'apiMessage' : 'success',
        }
    except Exception as e:
        # 初始化回傳值
        response = {
            'apiStatus' : 'error',
			'apiMessage' : str(e),
        }

    # 將回傳值回傳
    return JsonResponse(response)

def getWordSetTotalList(request):
    try:
        # 蒐集資料
        index = request.POST.get('index', '')

        # 判斷資料
        if (index == ''):    
            raise Exception('缺少必填參數 index')
   
        # 整理從資料庫得到的資料

        data = appAPIUtils.getWordSetTotalList(index)
        
        # 初始化回傳值
        response = {
            'apiStatus' : 'success',
            'apiMessage' : 'success',
            'data' : data,
        }
    except Exception as e:
        # 初始化回傳值
        response = {
            'apiStatus' : 'error',
			'apiMessage' : str(e),
        }

    # 將回傳值回傳
    return JsonResponse(response)
    
def getWordList(request):
    try:
        # 蒐集資料
        index = request.POST.get('index', '')
        dataLimit = request.POST.get('dataLimit', '')

        # 判斷資料
        if (index == ''):    
            raise Exception('缺少必填參數 index')
   
        # 整理從資料庫得到的資料

        data = appAPIUtils.getWordList(index, dataLimit)
        
        # 初始化回傳值
        response = {
            'apiStatus' : 'success',
            'apiMessage' : 'success',
            'data' : data,
        }
    except Exception as e:
        # 初始化回傳值
        response = {
            'apiStatus' : 'error',
			'apiMessage' : str(e),
        }

    # 將回傳值回傳
    return JsonResponse(response)
    
def getWordRowIndex(request):
    try:
        # 蒐集資料
        word = request.POST.get('word', '')

        # 判斷資料
        if (word == ''):    
            raise Exception('缺少必填參數 word')
   
        # 整理從資料庫得到的資料

        data = appAPIUtils.getWordRowIndex(word)
        
        # 初始化回傳值
        response = {
            'apiStatus' : 'success',
            'apiMessage' : 'success',
            'data' : data,
        }
    except Exception as e:
        # 初始化回傳值
        response = {
            'apiStatus' : 'error',
			'apiMessage' : str(e),
        }

    # 將回傳值回傳
    return JsonResponse(response)
    
def getWordData(request):
    try:
        # 蒐集資料
        word = request.POST.get('word', '')

        # 判斷資料
        if (word == ''):    
            raise Exception('缺少必填參數 word')
   
        # 整理從資料庫得到的資料

        data = appAPIUtils.getWordData(word)
        
        # 初始化回傳值
        response = {
            'apiStatus' : 'success',
            'apiMessage' : 'success',
            'data' : data,
        }
    except Exception as e:
        # 初始化回傳值
        response = {
            'apiStatus' : 'error',
			'apiMessage' : str(e),
        }

    # 將回傳值回傳
    return JsonResponse(response)