from django.http import JsonResponse

import requests

def getConversationTokenAndID():
    try:
        r = requests.post(
            'http://127.0.0.1:5002/api/auth/jwt',
            json = {
                'chat_token':'d313faf5bf904bd2a27f864a5de413cf'
            },
        )
        rJASON = r.json()

        dataArray = {
            'accessToken' : rJASON['access_token'],
            'conversationID' : rJASON['conversation_id'],
        }

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

def sendMessageToConversation(request):
    try:
        # 蒐集資料
        accessToken = request.POST.get('accessToken', '')
        conversationID = request.POST.get('conversationID', '')
        message = request.POST.get('message', '')
        
        # 判斷資料
        if (accessToken == ''):
            raise Exception('缺少必填參數 accessToken')
        if (conversationID == ''):
            raise Exception('缺少必填參數 conversationID')
        if (message == ''):
            raise Exception('缺少必填參數 message')

        r = requests.post(
            f'http://127.0.0.1:5002/api/conversations/{conversationID}/messages/', 
            headers = {
                'Accept': 'application/json',
                'Content-type': 'application/json',
                'Authorization': f'Bearer {accessToken}'
            }, 
            json = {
                'message': message
            },
        )
        rJASON = r.json()

        dataArray = []
        for i in rJASON:
            if ('image' in i):
                data = {
                    'type' : 'image',
                    'value' : i['image'],
                }
            if ('text' in i):
                data = {
                    'type' : 'text',
                    'value' : i['text'],
                }


            dataArray.append(data)

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