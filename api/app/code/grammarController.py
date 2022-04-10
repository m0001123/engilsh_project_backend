import language_tool_python
tool = language_tool_python.LanguageTool('en-US')

from django.http import JsonResponse


def checkGrammar(request):
    try:
        # 蒐集資料
        sentenceText = request.POST.get('sentenceText', '')
        
        # 判斷資料
        if (sentenceText == ''):    
            raise Exception('缺少必填參數 sentenceText')

        sentenceTextOriginal = sentenceText
        sentenceTextChecked = tool.correct(sentenceText)
        
        sentenceTextOriginalArray = []
        sentenceTextCheckedArray = []

        matches = tool.check(sentenceText)
        if matches:
            sentenceTextOriginalArray.append(sentenceText[:matches[0].offset])
            sentenceTextCheckedArray.append(sentenceText[:matches[0].offset])
            for i in range(len(matches)):
                if (i>0):
                    sentenceTextOriginalArray.append(sentenceText[matches[i-1].errorLength + matches[i-1].offset:matches[i].offset])
                    sentenceTextCheckedArray.append(sentenceText[matches[i-1].errorLength + matches[i-1].offset:matches[i].offset])
                sentenceTextOriginalArray.append(sentenceText[matches[i].offset:matches[i].errorLength + matches[i].offset])
                sentenceTextCheckedArray.append(matches[i].replacements[0])

            sentenceTextOriginalArray.append(sentenceText[matches[-1].errorLength + matches[-1].offset:])
            sentenceTextCheckedArray.append(sentenceText[matches[-1].errorLength + matches[-1].offset:])
        else:
            sentenceTextOriginalArray.append(sentenceText)
            sentenceTextCheckedArray.append(sentenceText)
        
        # 整理資料
        dataArray = {
            'sentenceTextOriginal' : sentenceTextOriginal,
            'sentenceTextChecked' : sentenceTextChecked,
            'sentenceTextOriginalArray' : sentenceTextOriginalArray,
            'sentenceTextCheckedArray' : sentenceTextCheckedArray,
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