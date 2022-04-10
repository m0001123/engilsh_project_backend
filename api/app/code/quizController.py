import pymysql
from django.http import JsonResponse
import json
from eng_to_ipa import eng_to_ipa 
from similar_text import similar_text
from random import choice, sample
import re

from app.code import appAPIUtils


def getQuizHistory(request):
    try:
        # 蒐集資料
        uuid = request.POST.get('uuid', '')

        # 判斷資料
        if (uuid == ''):    
            raise Exception('缺少必填參數 uuid')
   
        # 整理從資料庫得到的資料

        dataArray = appAPIUtils.getQuizHistory(uuid = uuid)
        # 初始化回傳值
        response = {
            'apiStatus' : 'success',
			'apiMessage' : 'success',
			'data' : dataArray,
        }
    except Exception as e:
        # 初始化回傳值
        response = {
            'apiStatus' : 'error',
			'apiMessage' : str(e),
        }

    # 將回傳值回傳
    return JsonResponse(response)

    
def getQuizDataByID(request):
    try:
        # 蒐集資料
        quizID = request.POST.get('quizID', '')
        uuid = request.POST.get('uuid', '')

        # 判斷資料
        if (quizID == ''):    
            raise Exception('缺少必填參數 quizID')
        if (uuid == ''):    
            raise Exception('缺少必填參數 uuid')
   
        # 整理從資料庫得到的資料

        dataArray = appAPIUtils.getQuizDataByID(quizID = quizID, uuid = uuid)
        # 初始化回傳值
        response = {
            'apiStatus' : 'success',
			'apiMessage' : 'success',
			'data' : dataArray,
        }
    except Exception as e:
        # 初始化回傳值
        response = {
            'apiStatus' : 'error',
			'apiMessage' : str(e),
        }

    # 將回傳值回傳
    return JsonResponse(response)
    
def saveQuizData(request):
    try:
        # 蒐集資料
        uuid = request.POST.get('uuid', '')
        quizTitle = request.POST.get('quizTitle', '')
        sentenceIDArray = request.POST.get('sentenceIDArray', '')
        sentenceAnswerArray = request.POST.get('sentenceAnswerArray', '')
        scoreArray = request.POST.get('scoreArray', '')
        secondsArray = request.POST.get('secondsArray', '')

        # 判斷資料
        if (uuid == ''):    
            raise Exception('缺少必填參數 uuid')
        if (quizTitle == ''):    
            raise Exception('缺少必填參數 quizTitle')
        if (sentenceIDArray == ''):    
            raise Exception('缺少必填參數 sentenceIDArray')
        if (sentenceAnswerArray == ''):    
            raise Exception('缺少必填參數 sentenceAnswerArray')
        if (scoreArray == ''):    
            raise Exception('缺少必填參數 scoreArray')
        if (secondsArray == ''):    
            raise Exception('缺少必填參數 secondsArray')
   
        # 整理從資料庫得到的資料

        dataArray = appAPIUtils.saveQuizData(uuid, quizTitle, json.loads(sentenceIDArray), json.loads(sentenceAnswerArray), json.loads(scoreArray), json.loads(secondsArray))
        # 初始化回傳值
        response = {
            'apiStatus' : 'success',
			'apiMessage' : 'success',
			#'data' : dataArray,
        }
    except Exception as e:
        # 初始化回傳值
        response = {
            'apiStatus' : 'error',
			'apiMessage' : str(e),
        }

    # 將回傳值回傳
    return JsonResponse(response)

    
def updateQuizData(request):
    try:
        # 蒐集資料
        uuid = request.POST.get('uuid', '')
        quizID = request.POST.get('quizID', '')
        sentenceIDArray = request.POST.get('sentenceIDArray', '')
        sentenceAnswerArray = request.POST.get('sentenceAnswerArray', '')
        scoreArray = request.POST.get('scoreArray', '')
        secondsArray = request.POST.get('secondsArray', '')

        # 判斷資料
        if (uuid == ''):    
            raise Exception('缺少必填參數 uuid')
        if (quizID == ''):    
            raise Exception('缺少必填參數 quizID')
        if (sentenceIDArray == ''):    
            raise Exception('缺少必填參數 sentenceIDArray')
        if (sentenceAnswerArray == ''):    
            raise Exception('缺少必填參數 sentenceAnswerArray')
        if (scoreArray == ''):    
            raise Exception('缺少必填參數 scoreArray')
        if (secondsArray == ''):    
            raise Exception('缺少必填參數 secondsArray')
   
        # 整理從資料庫得到的資料

        dataArray = appAPIUtils.updateQuizData(uuid, quizID, json.loads(sentenceIDArray), json.loads(sentenceAnswerArray), json.loads(scoreArray), json.loads(secondsArray))
        # 初始化回傳值
        response = {
            'apiStatus' : 'success',
			'apiMessage' : 'success',
			#'data' : dataArray,
        }
    except Exception as e:
        # 初始化回傳值
        response = {
            'apiStatus' : 'error',
			'apiMessage' : str(e),
        }

    # 將回傳值回傳
    return JsonResponse(response)

    