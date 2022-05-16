from http.client import REQUEST_ENTITY_TOO_LARGE
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from app.code import sentenceController, wordController, grammarController, rasaController, quizController, minimalPairController


@csrf_exempt
def sentence(request, type):
    if request.method == 'GET':
        if type == 'getSentenceTopicData':
            return sentenceController.getSentenceTopicData()
    if request.method == 'POST':
        if type == 'getSentences':
            return sentenceController.getSentences(request)
        elif type == 'getSentencesByID':
            return sentenceController.getSentencesByID(request)
        elif type == 'getPhoneticExercisesSentencesByWordSet':
            return sentenceController.getPhoneticExercisesSentencesByWordSet(request)
        elif type == 'checkSentences':
            return sentenceController.checkSentences(request)
        elif type == 'checkPronunciation':
            return sentenceController.checkPronunciation(request)
        elif type == 'checkSentences2':
            return sentenceController.checkSentences2(request)
        elif type == 'sentSegmentation':
            return sentenceController.sentSegmentation(request)


@csrf_exempt
def word(request, type):
    if request.method == 'GET':
        if type == 'getWordSetClassificationData':
            return wordController.getWordSetClassificationData()
    if request.method == 'POST':
        if type == 'getWordByWord':
            return wordController.getWordByWord(request)
        elif type == 'getWordByIPA':
            return wordController.getWordByIPA(request)
        elif type == 'getWordLearning':
            return wordController.getWordLearning(request)
        elif type == 'getWordSetList':
            return wordController.getWordSetList(request)
        elif type == 'addWordSet':
            return wordController.addWordSet(request)
        elif type == 'getWordSetTotalList':
            return wordController.getWordSetTotalList(request)
        elif type == 'getWordList':
            return wordController.getWordList(request)
        elif type == 'getWordRowIndex':
            return wordController.getWordRowIndex(request)
        elif type == 'getWordData':
            return wordController.getWordData(request)

            
@csrf_exempt
def grammar(request, type):
    if request.method == 'POST':
        if type == 'checkGrammar':
            return grammarController.checkGrammar(request)

@csrf_exempt
def quiz(request, type):
    if request.method == 'POST':
        if type == 'getQuizHistory':
            return quizController.getQuizHistory(request)
        elif type == 'getQuizDataByID':
            return quizController.getQuizDataByID(request)
        elif type == 'saveQuizData':
            return quizController.saveQuizData(request)
        elif type == 'updateQuizData':
            return quizController.updateQuizData(request)

            

@csrf_exempt
def rasa(request, type):
    if request.method == 'GET':
        if type == 'getConversationTokenAndID':
            return rasaController.getConversationTokenAndID()
    if request.method == 'POST':
        if type == 'sendMessageToConversation':
            return rasaController.sendMessageToConversation(request)

@csrf_exempt
def minimalPair(request, type):
    if request.method == 'GET':
        if type == 'getIPAAvailable':
            return minimalPairController.getIPAAvailable()
    if request.method == 'POST':
        if type == 'oneFinder':
            return minimalPairController.minimalPairOneFinder(request)
        if type == 'twoFinder':
            return minimalPairController.minimalPairTwoFinder(request)
        if type == 'wordFinder':
            return minimalPairController.minimalPairWordFinder(request)