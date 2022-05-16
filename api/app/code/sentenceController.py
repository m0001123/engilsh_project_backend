import pymysql
from django.http import JsonResponse
import json
import spacy
from eng_to_ipa import eng_to_ipa
from similar_text import similar_text
from random import choice, sample
import re

from app.code import appAPIUtils


def getSentenceTopicData():
    try:
        data = appAPIUtils.getSentenceTopicData()

        # 初始化回傳值
        response = {
            'apiStatus': 'success',
            'apiMessage': 'success',
            'data': data,
        }
    except Exception as e:
        # 初始化回傳值
        response = {
            'apiStatus': 'error',
            'apiMessage': str(e),
        }

    # 將回傳值回傳
    return JsonResponse(response)


def getSentences(request):
    try:
        # 蒐集資料
        sentenceLevel = request.POST.get('sentenceLevel', '')
        sentenceTopic = request.POST.get('sentenceTopic', '')
        sentenceClass = request.POST.get('sentenceClass', '')
        aboutWord = request.POST.get('aboutWord', '')
        sentenceMinLength = request.POST.get('sentenceMinLength', '')
        sentenceMaxLength = request.POST.get('sentenceMaxLength', '')
        sentenceRanking = request.POST.get('sentenceRanking', '')
        sentenceRankingLocking = request.POST.get('sentenceRankingLocking', '')
        dataLimit = request.POST.get('dataLimit', '')

        # 判斷資料
        # if (sentenceLevel == ''):
        #    raise Exception('缺少必填參數 sentenceLevel')

        # 整理從資料庫得到的資料

        dataArray = appAPIUtils.getSentencesData(sentenceLevel=sentenceLevel, sentenceTopic=sentenceTopic, sentenceClass=sentenceClass, aboutWord=aboutWord, sentenceMinLength=sentenceMinLength,
                                                 sentenceMaxLength=sentenceMaxLength, sentenceRanking=sentenceRanking, sentenceRankingLocking=sentenceRankingLocking, dataLimit=dataLimit)
        # 初始化回傳值
        response = {
            'apiStatus': 'success',
            'apiMessage': 'success',
            'data': dataArray,
        }
    except Exception as e:
        # 初始化回傳值
        response = {
            'apiStatus': 'error',
            'apiMessage': str(e),
        }

    # 將回傳值回傳
    return JsonResponse(response)


def getSentencesByID(request):
    try:
        # 蒐集資料
        sentencesID = request.POST.get('sentencesID', '')

        # 判斷資料
        if (sentencesID == ''):
            raise Exception('缺少必填參數 sentencesID')

        # 整理從資料庫得到的資料
        dataArray = appAPIUtils.getSentencesData(sentencesID=sentencesID)
        # 初始化回傳值
        response = {
            'apiStatus': 'success',
            'apiMessage': 'success',
            'data': dataArray,
        }
    except Exception as e:
        # 初始化回傳值
        response = {
            'apiStatus': 'error',
            'apiMessage': str(e),
        }

    # 將回傳值回傳
    return JsonResponse(response)


def getPhoneticExercisesSentencesByWordSet(request):
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
        wordData = appAPIUtils.getWordLearningData(
            learningClassification=learningClassification, learningPhase=learningPhase)

        sentencesData = []
        for word in wordData:
            dataArray = appAPIUtils.getSentencesData(
                sentenceRankingLocking=word['wordRanking'], dataLimit='3')
            sentencesData = sentencesData + dataArray

        # 初始化回傳值
        response = {
            'apiStatus': 'success',
            'apiMessage': 'success',
            'data': sentencesData,
        }
    except Exception as e:
        # 初始化回傳值
        response = {
            'apiStatus': 'error',
            'apiMessage': str(e),
        }

    # 將回傳值回傳
    return JsonResponse(response)


def checkSentences(request):
    try:
        # 蒐集資料
        questionText = request.POST.get('questionText', '')
        answerText = request.POST.get('answerText', '')
        correctCombo = int(request.POST.get('correctCombo', ''))

        # 判斷資料
        if (questionText == ''):
            raise Exception('缺少必填參數 questionText')
        if (answerText == ''):
            raise Exception('缺少必填參數 answerText')
        if (correctCombo == ''):
            correctCombo = 0

        # 獲取IPA文字(無標點符號)
        questionIPAText = eng_to_ipa.convert(questionText, False, False)
        answerIPAText = eng_to_ipa.convert(answerText, False, False)

        # 處理文字 移除標點符號
        replaceSymbol = [',', '.', '!', '?']
        for i in range(len(replaceSymbol)):
            questionText = questionText.replace(replaceSymbol[i], ' ')
            answerText = answerText.replace(replaceSymbol[i], ' ')
        questionText = questionText.strip()
        answerText = answerText.strip()
        # 處理文字 轉小寫
        questionText = questionText.lower()
        answerText = answerText.lower()

        # 獲取文字跟IPA文字相似度
        textSimilarity = similar_text(questionText, answerText)
        ipaTextSimilarity = similar_text(questionIPAText, answerIPAText)

        # 根據IPA相似度給予評價
        scoreComment = appAPIUtils.getScoreComment(
            ipaTextSimilarity, correctCombo)

        # 獲取有問題的單字陣列(用發音判斷)
        questionErrorWordArray = []
        answerErrorWordArray = []

        questionTextSingleWordArray = questionText.split(' ')
        questionIPATextSingleWordArray = questionIPAText.split(' ')

        answerTextSingleWordArray = answerText.split(' ')
        answerIPATextSingleWordArray = answerIPAText.split(' ')

        for i in range(len(questionIPATextSingleWordArray)):
            if not (questionIPATextSingleWordArray[i] in answerIPATextSingleWordArray):
                questionErrorWordArray.append(questionTextSingleWordArray[i])
            pass

        for i in range(len(answerIPATextSingleWordArray)):
            if not (answerIPATextSingleWordArray[i] in questionIPATextSingleWordArray):
                answerErrorWordArray.append(answerTextSingleWordArray[i])
            pass

        # 獲取問題中錯誤相關的資料
        questionError = {}
        for errorWord in questionErrorWordArray:
            ipaAboutArray = {}
            rhymesWordArray = eng_to_ipa.get_rhymes(errorWord)
            for ipaAboutWord in sample(rhymesWordArray, min(len(rhymesWordArray), 3)):
                pronunciationData = appAPIUtils.getWordPronunciationData(
                    ipaAboutWord)
                ipaAboutArray.update({ipaAboutWord: pronunciationData})
                pass
            pronunciationData = appAPIUtils.getWordPronunciationData(errorWord)
            pronunciationData.update({'ipaAbout': ipaAboutArray})
            questionError.update({errorWord: pronunciationData})
            pass

        # 獲取回答中錯誤相關的資料
        answerError = {}
        for errorWord in answerErrorWordArray:
            ipaAboutArray = {}
            rhymesWordArray = eng_to_ipa.get_rhymes(errorWord)
            for ipaAboutWord in sample(rhymesWordArray, min(len(rhymesWordArray), 3)):
                pronunciationData = appAPIUtils.getWordPronunciationData(
                    ipaAboutWord)
                ipaAboutArray.update({ipaAboutWord: pronunciationData})
                pass
            pronunciationData = appAPIUtils.getWordPronunciationData(errorWord)
            pronunciationData.update({'ipaAbout': ipaAboutArray})
            answerError.update({errorWord: pronunciationData})
            pass

        # IPA發音檢驗
        checkPronunciation = appAPIUtils.checkPronunciation(
            questionIPAText, answerIPAText)

        # 整理資料
        dataArray = {
            'questionText': questionText,
            'questionIPAText': questionIPAText,
            'answerText': answerText,
            'answerIPAText': answerIPAText,
            'textSimilarity': textSimilarity,
            'ipaTextSimilarity': ipaTextSimilarity,
            'scoreComment': scoreComment,
            'questionError': questionError,
            'answerError': answerError,
            'checkPronunciation': checkPronunciation
        }

        # 初始化回傳值
        response = {
            'apiStatus': 'success',
            'apiMessage': 'success',
            'data': dataArray,
        }
    except Exception as e:
        # 初始化回傳值
        response = {
            'apiStatus': 'error',
            'apiMessage': str(e),
        }

    # 將回傳值回傳
    return JsonResponse(response)


def checkPronunciation(request):
    try:
        # 蒐集資料
        questionText = request.POST.get('questionText', '')
        answerText = request.POST.get('answerText', '')
        correctCombo = int(request.POST.get('correctCombo', ''))

        # 判斷資料
        if (questionText == ''):
            raise Exception('缺少必填參數 questionText')
        if (answerText == ''):
            raise Exception('缺少必填參數 answerText')
        if (correctCombo == ''):
            correctCombo = 0

        # 獲取IPA文字(無標點符號)
        questionIPAText = eng_to_ipa.convert(questionText, False, False)
        answerIPAText = eng_to_ipa.convert(answerText, False, False)

        # 處理文字 移除標點符號
        replaceSymbol = [',', '.', '!', '?']
        for i in range(len(replaceSymbol)):
            questionText = questionText.replace(replaceSymbol[i], ' ')
            answerText = answerText.replace(replaceSymbol[i], ' ')
        questionText = questionText.strip()
        answerText = answerText.strip()
        # 處理文字 轉小寫
        questionText = questionText.lower()
        answerText = answerText.lower()

        # 獲取文字跟IPA文字相似度
        textSimilarity = similar_text(questionText, answerText)
        ipaTextSimilarity = similar_text(questionIPAText, answerIPAText)

        # 根據IPA相似度給予評價
        scoreComment = appAPIUtils.getScoreComment(
            ipaTextSimilarity, correctCombo)

        # 獲取有問題的單字陣列(用發音判斷)
        questionErrorWordArray = []
        answerErrorWordArray = []

        questionTextSingleWordArray = questionText.split(' ')
        questionIPATextSingleWordArray = questionIPAText.split(' ')

        answerTextSingleWordArray = answerText.split(' ')
        answerIPATextSingleWordArray = answerIPAText.split(' ')

        for i in range(len(questionIPATextSingleWordArray)):
            if not (questionIPATextSingleWordArray[i] in answerIPATextSingleWordArray):
                questionErrorWordArray.append(questionTextSingleWordArray[i])
            pass

        for i in range(len(answerIPATextSingleWordArray)):
            if not (answerIPATextSingleWordArray[i] in questionIPATextSingleWordArray):
                answerErrorWordArray.append(answerTextSingleWordArray[i])
            pass

        # 獲取問題中錯誤相關的資料
        questionError = {}
        for errorWord in questionErrorWordArray:
            ipaAboutArray = {}
            rhymesWordArray = eng_to_ipa.get_rhymes(errorWord)
            for ipaAboutWord in sample(rhymesWordArray, min(len(rhymesWordArray), 3)):
                pronunciationData = appAPIUtils.getWordPronunciationData(
                    ipaAboutWord)
                ipaAboutArray.update({ipaAboutWord: pronunciationData})
                pass
            pronunciationData = appAPIUtils.getWordPronunciationData(errorWord)
            pronunciationData.update({'ipaAbout': ipaAboutArray})
            questionError.update({errorWord: pronunciationData})
            pass

        # 獲取回答中錯誤相關的資料
        answerError = {}
        for errorWord in answerErrorWordArray:
            ipaAboutArray = {}
            rhymesWordArray = eng_to_ipa.get_rhymes(errorWord)
            for ipaAboutWord in sample(rhymesWordArray, min(len(rhymesWordArray), 3)):
                pronunciationData = appAPIUtils.getWordPronunciationData(
                    ipaAboutWord)
                ipaAboutArray.update({ipaAboutWord: pronunciationData})
                pass
            pronunciationData = appAPIUtils.getWordPronunciationData(errorWord)
            pronunciationData.update({'ipaAbout': ipaAboutArray})
            answerError.update({errorWord: pronunciationData})
            pass

        # IPA發音檢驗
        checkPronunciation = appAPIUtils.checkPronunciation(
            questionIPAText, answerIPAText)

        # 整理資料
        dataArray = {
            'questionText': questionText,
            'questionIPAText': questionIPAText,
            'answerText': answerText,
            'answerIPAText': answerIPAText,
            'textSimilarity': textSimilarity,
            'ipaTextSimilarity': ipaTextSimilarity,
            'scoreComment': scoreComment,
            'questionError': questionError,
            'answerError': answerError,
            'checkPronunciation': checkPronunciation,
        }

        # 初始化回傳值
        response = {
            'apiStatus': 'success',
            'apiMessage': 'success',
            'data': dataArray,
        }
    except Exception as e:
        # 初始化回傳值
        response = {
            'apiStatus': 'error',
            'apiMessage': str(e),
        }

    # 將回傳值回傳
    return JsonResponse(response)


def checkSentences2(request):
    try:
        # 蒐集資料
        questionText = request.POST.get('questionText', '')
        answerText = request.POST.get('answerText', '')
        correctCombo = int(request.POST.get('correctCombo', ''))

        # 判斷資料
        if (questionText == ''):
            raise Exception('缺少必填參數 questionText')
        if (answerText == ''):
            raise Exception('缺少必填參數 answerText')
        if (correctCombo == ''):
            correctCombo = 0

        # 獲取IPA文字(無標點符號)
        questionIPAText = eng_to_ipa.convert(questionText, False, False)
        answerIPAText = eng_to_ipa.convert(answerText, False, False)

        # 處理文字 移除標點符號
        replaceSymbol = [',', '.', '!', '?']
        for i in range(len(replaceSymbol)):
            questionText = questionText.replace(replaceSymbol[i], ' ')
            answerText = answerText.replace(replaceSymbol[i], ' ')
        questionText = questionText.strip()
        answerText = answerText.strip()
        # 處理文字 轉小寫
        questionText = questionText.lower()
        answerText = answerText.lower()

        # 獲取文字跟IPA文字相似度
        textSimilarity = similar_text(questionText, answerText)
        ipaTextSimilarity = similar_text(questionIPAText, answerIPAText)

        # 根據IPA相似度給予評價
        scoreComment = appAPIUtils.getScoreComment(
            ipaTextSimilarity, correctCombo)

        # 單字與發音檢驗
        wordCompare = appAPIUtils.wordCompare(questionText, answerText),

        # IPA音節檢驗
        pronunciationCompare = appAPIUtils.textCompare(
            questionIPAText, answerIPAText)

        # 整理資料
        dataArray = {
            'questionText': questionText,
            'questionIPAText': questionIPAText,
            'answerText': answerText,
            'answerIPAText': answerIPAText,
            'textSimilarity': textSimilarity,
            'ipaTextSimilarity': ipaTextSimilarity,
            'scoreComment': scoreComment,
            'wordCompare': appAPIUtils.wordCompare(questionText, answerText),
            'pronunciationCompare': pronunciationCompare,
        }

        # 初始化回傳值
        response = {
            'apiStatus': 'success',
            'apiMessage': 'success',
            'data': dataArray,
        }
    except Exception as e:
        # 初始化回傳值
        response = {
            'apiStatus': 'error',
            'apiMessage': str(e),
        }

    # 將回傳值回傳
    return JsonResponse(response)


def sentSegmentation(request):
    try:
        article = request.POST.get('article', '')
        # 判斷資料
        if (article == ''):
            raise Exception('缺少必填參數 article')

        nlp = spacy.load('en_core_web_sm')
        result_sent = []
        doc = nlp(article)

        for sent in doc.sents:
            result = str(sent)
            result_sent.append(result)

        response = {
            'apiStatus': 'success',
            'apiMessage': 'success',
            'data': result_sent,
        }

    except Exception as e:
        # 初始化回傳值
        response = {
            'apiStatus': 'error',
            'apiMessage': str(e),
        }

    return JsonResponse(response)
def getSentenceIPA(request):
    try:
        sentenceList = request.POST.get('sentenceList')
        if(sentenceList==""):
            raise Exception('缺少必填參數 sentenceList')
        try:
            sentenceList_eval = eval(sentenceList)
            if(type(sentenceList_eval)!=type([])):
                raise Exception("輸入格式必須是List")
        except Exception as e:
            raise Exception('輸入格式必須是List')
        sentenceList_eval = eval (sentenceList)
        ipaList = []
        for i in sentenceList_eval:
            ipaList.append(eng_to_ipa.convert(i,False,False))
        
        response =  {
            'apiStatus' : 'success',
            'apiMessage' : 'success',
            'data':ipaList
            }
        
    except Exception as e:
        response = {
            'apiStatus' : 'error',
            'apiMessage' : str(e),
        }
    
    return JsonResponse(response)
    
