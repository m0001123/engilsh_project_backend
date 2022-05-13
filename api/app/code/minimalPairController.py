import pymysql
from django.http import JsonResponse
import json
from eng_to_ipa import eng_to_ipa 
from similar_text import similar_text
from random import choice, sample
import re

from app.code import appAPIUtils


def minimalPairOneFinder(request):
    try:
        # 蒐集資料
        ipa = request.POST.get('ipa', '')

        # 判斷資料
        if (ipa == ''):    
            raise Exception('缺少必填參數 ipa')
   
        # 整理從資料庫得到的資料

        dataArray = appAPIUtils.minimalPairOneFinder(ipa = ipa)
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

def minimalPairTwoFinder(request):
    try:
        # 蒐集資料
        ipa1 = request.POST.get('ipa1', '')
        ipa2 = request.POST.get('ipa2', '')
        dataLimit = request.POST.get('dataLimit', '')

        # 判斷資料
        if (ipa1 == ''):    
            raise Exception('缺少必填參數 ipa1')
        if (ipa2 == ''):    
            raise Exception('缺少必填參數 ipa2')
   
        # 整理從資料庫得到的資料

        dataArray = appAPIUtils.minimalPairTwoFinder(ipa1, ipa2, dataLimit)
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

def minimalPairWordFinder(request):
    try:
        # 蒐集資料
        word1 = request.POST.get('word1', '')

        # 判斷資料
        if (word1 == ''):    
            raise Exception('缺少必填參數 word1')
   
        # 整理從資料庫得到的資料

        dataArray = appAPIUtils.minimalPairWordFinder(word1)
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

def getIPAAvailable():
    try:
        dataArray = appAPIUtils.getIPAAvailable()
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

    