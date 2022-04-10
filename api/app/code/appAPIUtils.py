import pymysql
import codecs
from eng_to_ipa import eng_to_ipa
from random import choice, sample
import difflib
import math
import random
import time



def getWordSetClassificationData():

    # 初始化SQL語法
    sqlSELECT = f'SELECT DISTINCT vocalbulary_classification_list.id, vocalbulary_classification_list.classification_name, vocalbulary_classification_list.descrip, vocalbulary_classification_list.word_count'
    sqlFROM = f'FROM vocalbulary_classification_list'
    sqlSyntax = f'{sqlSELECT} {sqlFROM};'

    # 從資料庫執行
    db = pymysql.connect(host='163.18.10.123', port=3306, user='EPuser', passwd='e507@mis', db='entries', charset='utf8mb4')
    cursor = db.cursor()
    cursor.execute(sqlSyntax)
    dbResult = cursor.fetchall()
    db.close()

    # 整理資料庫回傳資料
    response = []
    for result in dbResult:
        if (random.randint(1, 100) == 100):
            # 初始化SQL語法
            sqlUPDATE4 = f"UPDATE vocalbulary_classification_list"
            sqlSET4 = f"SET vocalbulary_classification_list.word_count = (SELECT COUNT(DISTINCT vocalbulary_classification.id) FROM vocalbulary_classification JOIN toeic10k ON toeic10k.id = vocalbulary_classification.toeic10k_id WHERE (vocalbulary_classification.ngsl30k_id != 0) AND vocalbulary_classification.classification = '{result[0]}')"
            sqlWHERE4 = f"WHERE vocalbulary_classification_list.id = '{result[0]}'"
            sqlSyntax4 = f"{sqlUPDATE4} {sqlSET4} {sqlWHERE4};"
            # 從資料庫執行
            db4 = pymysql.connect(host='163.18.10.123', port=3306, user='EPuser', passwd='e507@mis', db='entries', charset='utf8mb4')
            cursor4 = db4.cursor()
            cursor4.execute(sqlSyntax4)
            db4.commit()
            db4.close()
        data = {
            'id' : result[0],
            'title' : result[1],
            'descrip' : result[2],
            'wordCount' : result[3],
        }
        response.append(data)
        pass
    
    return response

def getSentenceTopicData():

    # 初始化SQL語法
    sqlSELECT = f'SELECT DISTINCT topiclist.class'
    sqlFROM = f'FROM topiclist'
    sqlSyntax = f'{sqlSELECT} {sqlFROM};'

    # 從資料庫執行
    db = pymysql.connect(host='163.18.10.123', port=3306, user='EPuser', passwd='e507@mis', db='entries', charset='utf8mb4')
    cursor = db.cursor()
    cursor.execute(sqlSyntax)
    dbResult = cursor.fetchall()
    db.close()

    # 整理資料庫回傳資料
    response = {}
    for result in dbResult:
        key = result[0]

        # 初始化SQL語法
        sqlSELECT2 = f'SELECT DISTINCT topiclist.id, topiclist.topicName, topiclist.descrip, topiclist.sentnceCount, topiclist.appIcon, topiclist.appStartColor, topiclist.appEndColor'
        sqlFROM2 = f'FROM topiclist'
        sqlWHERE2 = f'WHERE topiclist.class = \"{key}\"'
        sqlSyntax2 = f'{sqlSELECT2} {sqlFROM2} {sqlWHERE2};'
        # 從資料庫執行
        db2 = pymysql.connect(host='163.18.10.123', port=3306, user='EPuser', passwd='e507@mis', db='entries', charset='utf8mb4')
        cursor2 = db2.cursor()
        cursor2.execute(sqlSyntax2)
        dbResult2 = cursor2.fetchall()
        db2.close()

        titleList = []
        descripList = []
        sentnceCountList = []
        sentnceCountTotal = 0
        appIconList = []
        appStartColorList = []
        appEndColorList = []
        for result2 in dbResult2:
            titleList.append(result2[1])
            descripList.append(result2[2])
            sentnceCountList.append(result2[3])
            sentnceCountTotal = sentnceCountTotal + result2[3]
            appIconList.append(result2[4])
            appStartColorList.append(result2[5])
            appEndColorList.append(result2[6])

            if (random.randint(1, 100) == 100):
                # 初始化SQL語法
                sqlUPDATE3 = f'UPDATE topiclist'
                sqlSET3 = f'SET topiclist.sentnceCount = (SELECT COUNT(*) FROM sent WHERE sent.CompleteSentence = TRUE AND sent.Similarity >= 0.9 AND sent.sentTopic = \"{result2[0]}\")'
                sqlWHERE3 = f'WHERE topiclist.id = \"{result2[0]}\"'
                sqlSyntax3 = f'{sqlUPDATE3} {sqlSET3} {sqlWHERE3};'
                # 從資料庫執行
                db3 = pymysql.connect(host='163.18.10.123', port=3306, user='EPuser', passwd='e507@mis', db='entries', charset='utf8mb4')
                cursor3 = db3.cursor()
                cursor3.execute(sqlSyntax3)
                db3.commit()
                db3.close()

            pass
        
        titleList.insert(0, key)
        descripList.insert(0, descripList[0])
        sentnceCountList.insert(0, sentnceCountTotal)
        appIconList.insert(0, appIconList[0])
        appStartColorList.insert(0, appStartColorList[0])
        appEndColorList.insert(0, appEndColorList[0])

        data = {
            'title' : titleList,
            'descrip' : descripList,
            'sentnceCount' : sentnceCountList,
            'appIcon' : appIconList,
            'appStartColor' : appStartColorList,
            'appEndColor' : appEndColorList,
        }
        response[key] = data
        pass
    
    return response

def getWordPronunciationData(wordText):

    # 初始化SQL語法
    sqlSELECT = f'SELECT 8000wordcount.word_split'
    sqlFROM = f'FROM 8000wordcount'
    sqlWHERE = f'WHERE word = \"{wordText}\"'
    sqlSyntax = f'{sqlSELECT} {sqlFROM} {sqlWHERE};'

    # 從資料庫執行
    db = pymysql.connect(host='163.18.10.123', port=3306, user='EPuser', passwd='e507@mis', db='entries', charset='utf8mb4')
    cursor = db.cursor()
    cursor.execute(sqlSyntax)
    dbResult = cursor.fetchone() # 只取一筆
    db.close()

    # 整理回傳資料
    wordSyllable = ''
    if (dbResult and dbResult[0]):
        wordSyllable = dbResult[0].replace('¥', '・')
    response = {
        'word': wordText,
        'syllable': wordSyllable,
        'ipa': eng_to_ipa.convert(wordText, False, False),
    }
    
    return response



def getScoreComment(score, correctCombo):

    replyText = 'Good'
    replyEmoji = '☺️'
    if (score == 100):
        if (correctCombo > 6):
            goodCommentsArray = [
                'Exceptional',
                'Fabulous',
                'Fantastic',
                'Incredible',
                'Outstanding',
                'Phenomenal',
                'Smart',
                'Spectacular',
                'Super',
                'Terrific',
            ]
            emojiKeywordArray = [
                'winking',
            ]
        elif (3 < correctCombo <= 6):
            goodCommentsArray = [
                'Wonderful',
                'Amazing',
                'Awesome',
                'Excellent',
                'Perfect',
                'Clever',
            ]
            emojiKeywordArray = [
                'grinning',
            ]
        elif (correctCombo <= 3):
            goodCommentsArray = [
                'Beautiful',
                'Cool',
                'Fine',
                'Great',
                'Neat',
                'Nice',
                'Very Good',
            ]
            emojiKeywordArray = [
                'neutral',
            ]
    elif (score <= 99):
        goodCommentsArray = [
            'Oops',
            'Sorry',
            'Error',
            'Oopsy',
            'Whoops',
        ]
        emojiKeywordArray = [
            'cross mark',
            'anger symbol',
            'knocked-out',
            'anxious',
            'worried',
        ]

    
    replyText = choice(goodCommentsArray)
    getEmojiData = getEmojiByKeyword(emojiKeywordArray)
    if(getEmojiData):
        replyEmoji = choice(getEmojiData)['emojiDecode']



    response = {
        'score': score,
        'text': replyText,
        'emoji': replyEmoji,
    }
    
    return response

def getEmojiByKeyword(emojiKeywordArray):
    # 初始化SQL資料庫語法
    sqlSELECT = f'SELECT emojilist.id, emojilist.code, emojilist.name'
    sqlFROM = f'FROM emojilist'
    sqlWHERE = f'WHERE FALSE'
    for emojiKeyword in emojiKeywordArray:
        sqlWHERE += f' OR (emojilist.name LIKE \"%{emojiKeyword}%\")'
        pass
    sqlORDERBY = f"ORDER BY RAND()"
    sqlLIMIT = f"LIMIT 10"
    sqlSyntax = f'{sqlSELECT} {sqlFROM} {sqlWHERE} {sqlORDERBY} {sqlLIMIT};'

    # 從資料庫執行
    db = pymysql.connect(host='163.18.10.123', port=3306, user='EPuser', passwd='e507@mis', db='entries', charset='utf8mb4')
    cursor = db.cursor()
    cursor.execute(sqlSyntax)
    dbResult = cursor.fetchall()
    db.close()

    # 整理資料庫回傳資料
    responseArray = []
    for result in dbResult:
        data = {
            'emojiID' : result[0],
            'emojiCode' : result[1],
            'emojiDecode' : codecs.decode(r'\U' + result[1][2:].rjust(8, '0'), 'unicode_escape'),
            'emojiName' : result[2],
        }
        responseArray.append(data)
        pass
    
    return responseArray

def getSentencesData(sentencesID = '', sentenceLevel = '', sentenceTopic = '', sentenceClass = '', aboutWord = '', sentenceMinLength = '', sentenceMaxLength = '', sentenceRanking = '', sentenceRankingLocking = '', dataLimit = ''):

    if (dataLimit == ''):    
        dataLimit = 5

    
    dataArray = []
    similarity = 1.10
    similarityDistance = 0.10
    #raise Exception(int(len(dataArray)) < int(dataLimit))
    c = []
    while (len(dataArray) < int(dataLimit)):
        if (similarity == 0):
            break
        if (similarity > 0.80):
            #similarityDistance = similarityDistance + 0.05
            similarity = similarity - similarityDistance
        else:
            similarityDistance = 0.80
            similarity = 0

        #1.10 0.10 1.00
        #1.00 0.10 0.90
        #0.90 0.10 0.80
        
        #1.05 0.05 1.00
        #1.00 0.10 0.90
        #0.90 0.15 0.75
    
        # 初始化SQL語法
        sqlSELECT = f"SELECT sent.Id, sent.content, sent.Chinese, topiclist.topicName, topiclist.class, sent.Similarity"
        sqlFROM = f"FROM sent, topiclist"
        if(sentenceRankingLocking != ''):
            sqlFROM = f"FROM present_sentence as sent, topiclist"
        sqlWHERE = f"WHERE CompleteSentence = TRUE AND (Similarity >= {similarity} AND Similarity < {similarity + similarityDistance}) AND sent.sentTopic = topiclist.id"
        sqlORDERBY = f"ORDER BY RAND()"
        sqlLIMIT = f"LIMIT {int(dataLimit) - len(dataArray)}"

        #sqlSELECT = f"SELECT sent.Id, sent.content, sent.Chinese, topiclist.topicName, topiclist.class, sent.Similarity"
        #sqlFROM = f"FROM sent, topiclist"
        #sqlWHERE = f"WHERE CompleteSentence = TRUE AND (Similarity >= {similarity} AND Similarity < {similarity+0.05}) AND sent.sentTopic = topiclist.id AND sent.id >= (SELECT floor(RAND() * (SELECT MAX(id) FROM sent)))"
        #sqlLIMIT = f"LIMIT {int(dataLimit) - len(dataArray)}"

        if (sentencesID != ''):
            sqlWHERE = f"{sqlWHERE} AND sent.id = '{sentencesID}'"
        if (sentenceLevel != ''):
            sqlWHERE = f"{sqlWHERE} AND sent.Level = '{sentenceLevel}'"
        if (sentenceTopic != ''):
            sqlWHERE = f"{sqlWHERE} AND topiclist.topicName = '{sentenceTopic}'"
        if (sentenceClass != ''):
            sqlWHERE = f"{sqlWHERE} AND topiclist.class = '{sentenceClass}'"
        if (sentenceMinLength != ''):
            sqlWHERE = f"{sqlWHERE} AND sent.Length >= '{sentenceMinLength}'" 
        if (sentenceMaxLength != ''):
            sqlWHERE = f"{sqlWHERE} AND sent.Length <= '{sentenceMaxLength}'" 
        if (sentenceRanking != ''):
            sqlWHERE = f"{sqlWHERE} AND sent.ranking <= '{sentenceRanking}'" 
        if (sentenceRankingLocking != ''):
            sqlWHERE = f"{sqlWHERE} AND sent.ranking = '{sentenceRankingLocking}'" 
        if (aboutWord != ''):    
            #sqlINNERJOIN = f"{sqlINNERJOIN} INNER JOIN senthasword ON sent.Id = senthasword.sentId"
            #sqlWHERE = f"{sqlWHERE} AND senthasword.word = '{aboutWord}'"  
            sqlWHERE = f"{sqlWHERE}"  

        sqlSyntax = f"{sqlSELECT} {sqlFROM} {sqlWHERE} {sqlORDERBY} {sqlLIMIT};" 
        c.append(sqlSyntax)
        # 從資料庫執行
        db = pymysql.connect(host='163.18.10.123', port=3306, user='EPuser', passwd='e507@mis', db='entries', charset='utf8mb4')
        cursor = db.cursor()
        cursor.execute(sqlSyntax)
        results = cursor.fetchall()
        db.close()  
        # 整理從資料庫得到的資料
        for result in results:
            data = {
                'sentenceId' : result[0],
                'sentenceContent' : result[1],
                'sentenceIPA' : eng_to_ipa.convert(result[1], False, False),
                'sentenceChinese' : result[2],
                'sentenceTopic' : result[3],
                'sentenceClass' : result[4],
                'sentenceSimilarity' : result[5],
            }
            dataArray.append(data)
            pass
        #time.sleep(1)

    return dataArray

def getWordLearningData(learningClassification, learningPhase):

    # 初始化SQL語法
    #sqlSELECT = f"SELECT DISTINCT vocalbulary_classification.order_no, toeic10k.word, ngsl30k.id, toeic10k.wordType, toeic10k.wordLevel, vocalbulary_classification.source"
    #sqlFROM = f"FROM vocalbulary_classification"
    #sqlJOIN = f"JOIN toeic10k ON toeic10k.id = vocalbulary_classification.toeic10k_id"
    #sqlJOIN = f"{sqlJOIN} JOIN ngsl30k ON ngsl30k.word = toeic10k.word"
    #sqlWHERE = f"WHERE (vocalbulary_classification.classification = '{learningClassification}')"
    #sqlORDERBY = f"ORDER BY vocalbulary_classification.order_no ASC"
    #sqlLIMIT = f"LIMIT {(int(learningPhase) - 1) * 10}, 10"
    sqlSELECT = f"SELECT DISTINCT vocalbulary_classification.order_no, toeic10k.word, vocalbulary_classification.ngsl30k_id, toeic10k.wordType, toeic10k.wordLevel, vocalbulary_classification.source"
    sqlFROM = f"FROM vocalbulary_classification"
    sqlJOIN = f"JOIN toeic10k ON toeic10k.id = vocalbulary_classification.toeic10k_id"
    sqlWHERE = f"WHERE (vocalbulary_classification.ngsl30k_id != 0) AND vocalbulary_classification.classification = '{learningClassification}'"
    sqlORDERBY = f"ORDER BY vocalbulary_classification.order_no ASC"
    if (learningClassification == "Total"):
        sqlWHERE = f"WHERE (vocalbulary_classification.ngsl30k_id != 0)"
        sqlORDERBY = f"ORDER BY vocalbulary_classification.classification ASC, vocalbulary_classification.order_no ASC"
    sqlLIMIT = f"LIMIT {(int(learningPhase) - 1) * 10}, 10"

    sqlSyntax = f"{sqlSELECT} {sqlFROM} {sqlJOIN} {sqlWHERE} {sqlORDERBY} {sqlLIMIT};"
    
    # 從資料庫執行
    db = pymysql.connect(host='163.18.10.123', port=3306, user='EPuser', passwd='e507@mis', db='entries', charset='utf8mb4')
    cursor = db.cursor()
    cursor.execute(sqlSyntax)
    results = cursor.fetchall()
    db.close()   
    #raise Exception(sqlSyntax)
    # 整理從資料庫得到的資料
    dataArray = []
    for result in results:
        data = {
            'orderNo' : result[0],
            'word' : result[1],
            'wordRanking' : result[2],
            'wordType' : result[3],
            'wordLevel' : result[4],
            'wordIPA' : eng_to_ipa.convert(result[1], False, False),
            'wordSource' : result[5],
            'wordMeaningList' : getWordMeaningData(result[1]),
        }
        dataArray.append(data)

    return dataArray

def getWordMeaningData(word):

    # 初始化SQL語法
    sqlSELECT = f"SELECT meaninglist.pos, meaninglist.meaning"
    sqlFROM = f"FROM meaninglist"
    sqlWHERE = f"WHERE meaninglist.word = \"{word}\""

    sqlSyntax = f"{sqlSELECT} {sqlFROM} {sqlWHERE};" 
    # 從資料庫執行
    db = pymysql.connect(host='163.18.10.123', port=3306, user='EPuser', passwd='e507@mis', db='entries', charset='utf8mb4')
    cursor = db.cursor()
    cursor.execute(sqlSyntax)
    result = cursor.fetchall()
    db.close()  
    # 整理從資料庫得到的資料
    dataArray = []
    for result in result:
        data = {
            'pos' : result[0],
            'meaning' : result[1],
            'definition' : []
        }
        dataArray.append(data)

    return dataArray

def getWordDefinitionData(word, wordtype):

    # 初始化SQL語法
    sqlSELECT = f"SELECT entries.definition"
    sqlFROM = f"FROM entries"
    sqlWHERE = f"WHERE entries.word = '{word}' AND wordtype = '{wordtype}'"

    sqlSyntax = f"{sqlSELECT} {sqlFROM} {sqlWHERE};" 
    # 從資料庫執行
    db = pymysql.connect(host='163.18.10.123', port=3306, user='EPuser', passwd='e507@mis', db='entries', charset='utf8mb4')
    cursor = db.cursor()
    cursor.execute(sqlSyntax)
    result = cursor.fetchall()
    db.close()  
    # 整理從資料庫得到的資料
    dataArray = []
    for result in result:
        dataArray.append(result[0])

    return dataArray

def getQuizHistory(uuid):

    # 初始化SQL語法

    sqlSELECT = f"SELECT sentence_quiz.id, sentence_quiz.title, GROUP_CONCAT(sentence_quiz_data.sentence_id) AS 'sentence_id_array', ROUND(AVG(sentence_quiz_data.last_score), 1) AS 'last_score', sentence_quiz.created_at, sentence_quiz.updated_at"
    sqlFROM = f"FROM sentence_quiz"
    sqlINNERJOIN1 = f"INNER JOIN sentence_quiz_data ON sentence_quiz.id = sentence_quiz_data.quiz_id"
    sqlINNERJOIN2 = f"INNER JOIN uuid_data ON sentence_quiz.uuid = uuid_data.uuid"
    sqlWHERE = f"WHERE uuid_data.uuid = '{uuid}'"
    sqlGROUPBY = f"GROUP BY sentence_quiz.id"
    sqlORDERBY = f"ORDER BY sentence_quiz.updated_at DESC"
    sqlLIMIT = f"LIMIT 5"
    
    sqlSyntax = f"{sqlSELECT} {sqlFROM} {sqlINNERJOIN1} {sqlINNERJOIN2} {sqlWHERE} {sqlGROUPBY} {sqlORDERBY} {sqlLIMIT};" 

    # 從資料庫執行
    db = pymysql.connect(host='163.18.10.123', port=3306, user='EPuser', passwd='e507@mis', db='users', charset='utf8mb4')
    cursor = db.cursor()
    cursor.execute(sqlSyntax)
    result = cursor.fetchall()
    db.close()

    # 整理從資料庫得到的資料
    dataArray = []
    for result in result:
        data = {
            'quizID' : result[0],
            'quizTitle' : result[1],
            'quizSentenceIDArray' : list(map(int, result[2].replace(' ', '').split(','))),
            'quizAverageScore' : float(result[3]),
            'quizCreatedAt' : result[4],
            'quizUpdatedAt' : result[5],
        }
        dataArray.append(data)

    return dataArray

def getQuizDataByID(quizID, uuid):

    # 初始化SQL語法

    sqlSELECT = f"SELECT sentence_quiz_data.sentence_id, sentence_quiz_data.sentence_answer, sentence_quiz_data.last_score"
    sqlFROM = f"FROM sentence_quiz_data"
    sqlINNERJOIN1 = f"INNER JOIN sentence_quiz ON sentence_quiz_data.quiz_id = sentence_quiz.id"
    sqlINNERJOIN2 = f"INNER JOIN uuid_data ON sentence_quiz.uuid = uuid_data.uuid"
    sqlWHERE = f"WHERE sentence_quiz.id = '{quizID}' AND  uuid_data.uuid = '{uuid}'"
    
    sqlSyntax = f"{sqlSELECT} {sqlFROM} {sqlINNERJOIN1} {sqlINNERJOIN2} {sqlWHERE};" 

    # 從資料庫執行
    db = pymysql.connect(host='163.18.10.123', port=3306, user='EPuser', passwd='e507@mis', db='users', charset='utf8mb4')
    cursor = db.cursor()
    cursor.execute(sqlSyntax)
    dbResult = cursor.fetchall()
    db.close()

    # 整理回傳資料
    #quizSentenceIDArray = []
    #if (dbResult and dbResult[0]):
    #    quizSentenceIDArray = list(map(int, dbResult[0].replace(' ', '').split(',')))
    
    # 整理從資料庫得到的資料
    dataArray = []
    for result in dbResult:
        data = getSentencesData(sentencesID = result[0])
        data[0]['lastAnswer'] = result[1]
        data[0]['lastScore'] = result[2]
        dataArray.append(data[0])

    return dataArray

def saveQuizData(uuid, quizTitle, sentenceIDArray, sentenceAnswerArray, scoreArray, secondsArray):

    # 初始化SQL語法
    sqlSyntax = f"INSERT INTO uuid_data (uuid, updated_at) VALUES ('{uuid}', NOW()) ON DUPLICATE KEY UPDATE updated_at = NOW();"

    # 從資料庫執行
    db = pymysql.connect(host='163.18.10.123', port=3306, user='EPuser', passwd='e507@mis', db='users', charset='utf8mb4')
    cursor = db.cursor()
    cursor.execute(sqlSyntax)
    db.commit()
    db.close()

    # 初始化SQL語法
    sqlSyntax = f"INSERT INTO sentence_quiz (uuid, title, updated_at) VALUES ('{uuid}', '{quizTitle}', NOW());"

    # 從資料庫執行
    db = pymysql.connect(host='163.18.10.123', port=3306, user='EPuser', passwd='e507@mis', db='users', charset='utf8mb4')
    cursor = db.cursor()
    cursor.execute(sqlSyntax)
    db.commit()
    
    quizID = cursor.lastrowid

    db.close()
    
    # 初始化SQL語法
    sqlSyntax = f"INSERT INTO sentence_quiz_data (quiz_id, sentence_id, sentence_answer, last_score, spand_seconds, updated_at) VALUES ({quizID}, %s, %s, %s, %s, NOW())"
    val = []
    for i in range(len(sentenceIDArray)):
        val.append((sentenceIDArray[i], sentenceAnswerArray[i], scoreArray[i], secondsArray[i]))

    # 從資料庫執行
    db = pymysql.connect(host='163.18.10.123', port=3306, user='EPuser', passwd='e507@mis', db='users', charset='utf8mb4')
    cursor = db.cursor()
    cursor.executemany(sqlSyntax, val)
    db.commit()
    db.close()
 
    # 整理回傳資料
    #quizSentenceIDArray = []
    #if (dbResult and dbResult[0]):
    #    quizSentenceIDArray = list(map(int, dbResult[0].replace(' ', '').split(',')))
    
    # 整理從資料庫得到的資料
    dataArray = []
    #for result in dbResult:
    #    data = getSentencesData(sentencesID = result[0])
    #    data[0]['lastAnswer'] = result[1]
    #    data[0]['lastScore'] = result[2]
    #    dataArray.append(data[0])

    return quizID


def updateQuizData(uuid, quizID, sentenceIDArray, sentenceAnswerArray, scoreArray, secondsArray):

    # 初始化SQL語法
    sqlUPDATE = f"UPDATE sentence_quiz_data"
    sqlINNERJOIN1 = f"INNER JOIN sentence_quiz ON sentence_quiz_data.quiz_id = sentence_quiz.id"
    sqlINNERJOIN2 = f"INNER JOIN uuid_data ON sentence_quiz.uuid = uuid_data.uuid"
    sqlSET = f"SET sentence_quiz_data.sentence_answer = %s, sentence_quiz_data.last_score = %s, sentence_quiz_data.spand_seconds = %s, sentence_quiz.updated_at = NOW(), sentence_quiz_data.updated_at = NOW()"
    sqlWHERE = f"WHERE sentence_quiz_data.sentence_id = %s AND sentence_quiz.id = '{quizID}' AND  uuid_data.uuid = '{uuid}';"

    sqlSyntax = f"{sqlUPDATE} {sqlINNERJOIN1} {sqlINNERJOIN2} {sqlSET} {sqlWHERE};"
    
    # 初始化SQL語法
    #sqlSyntax = f"INSERT INTO sentence_quiz_data (quiz_id, sentence_id, sentence_answer, last_score, updated_at) VALUES ({quizID}, %s, %s, %s, NOW())"
    val = []
    for i in range(len(sentenceIDArray)):
        val.append((sentenceAnswerArray[i], scoreArray[i], secondsArray[i], sentenceIDArray[i]))

    # 從資料庫執行
    db = pymysql.connect(host='163.18.10.123', port=3306, user='EPuser', passwd='e507@mis', db='users', charset='utf8mb4')
    cursor = db.cursor()
    cursor.executemany(sqlSyntax, val)
    db.commit()
    db.close()
 
    # 整理回傳資料
    #quizSentenceIDArray = []
    #if (dbResult and dbResult[0]):
    #    quizSentenceIDArray = list(map(int, dbResult[0].replace(' ', '').split(',')))
    
    # 整理從資料庫得到的資料
    dataArray = []
    #for result in dbResult:
    #    data = getSentencesData(sentencesID = result[0])
    #    data[0]['lastAnswer'] = result[1]
    #    data[0]['lastScore'] = result[2]
    #    dataArray.append(data[0])

    return dataArray

def minimalPairFinder(ipa1, ipa2):

    sqlSELECT = f"SELECT *"
    sqlFROM = f"FROM ipa_word"
    sqlWHERE = f"WHERE (ipa_word.L_pair LIKE '/{ipa1}/' AND ipa_word.R_pair LIKE '/{ipa2}/') OR (ipa_word.L_pair LIKE '/{ipa2}/' AND ipa_word.R_pair LIKE '/{ipa1}/')"
    sqlORDERBY = f"ORDER BY RAND()"
    sqlLIMIT = f"LIMIT 3"

    sqlSyntax = f"{sqlSELECT} {sqlFROM} {sqlWHERE} {sqlORDERBY} {sqlLIMIT};"

    # 從資料庫執行
    db = pymysql.connect(host='163.18.10.123', port=3306, user='EPuser', passwd='e507@mis', db='entries', charset='utf8mb4')
    cursor = db.cursor()
    cursor.execute(sqlSyntax)
    dbResult = cursor.fetchall()
    db.close()  
    # 整理從資料庫得到的資料
    dataArray = []
    for result in dbResult:
        data = {
            'leftIPA' : result[4],
            'leftWord' : result[5],
            'rightIPA' : result[7],
            'rightWord' : result[6],
        }
        dataArray.append(data)

    return dataArray

def minimalPairOneFinder(ipa):

    sqlSELECT = f"SELECT *"
    sqlFROM = f"FROM ipa_word"
    sqlWHERE = f"WHERE ipa_word.L_pair LIKE '/{ipa}/' OR ipa_word.R_pair LIKE '/{ipa}/'"
    sqlORDERBY = f"ORDER BY RAND()"
    sqlLIMIT = f"LIMIT 3"

    sqlSyntax = f"{sqlSELECT} {sqlFROM} {sqlWHERE} {sqlORDERBY} {sqlLIMIT};"

    # 從資料庫執行
    db = pymysql.connect(host='163.18.10.123', port=3306, user='EPuser', passwd='e507@mis', db='entries', charset='utf8mb4')
    cursor = db.cursor()
    cursor.execute(sqlSyntax)
    dbResult = cursor.fetchall()
    db.close()  
    # 整理從資料庫得到的資料
    dataArray = []
    for result in dbResult:
        data = {
            'leftIPA' : result[4],
            'leftWord' : result[5],
            'rightIPA' : result[7],
            'rightWord' : result[6],
        }
        dataArray.append(data)

    return dataArray
  
def minimalPairTwoFinder(ipa1, ipa2):

    sqlSELECT = f"SELECT *"
    sqlFROM = f"FROM ipa_30k_minimal_pair"
    sqlWHERE = f"WHERE (ipa_30k_minimal_pair.L_pair LIKE '{ipa1}' AND ipa_30k_minimal_pair.R_pair LIKE '{ipa2}') OR (ipa_30k_minimal_pair.L_pair LIKE '{ipa2}' AND ipa_30k_minimal_pair.R_pair LIKE '{ipa1}')"
        #sqlWHERE = f"WHERE (ipa_word.L_pair LIKE '/{ipa1}/' AND ipa_word.R_pair LIKE '/{ipa2}/') OR (ipa_word.L_pair LIKE '/{ipa2}/' AND ipa_word.R_pair LIKE '/{ipa1}/')"
    sqlORDERBY = f"ORDER BY RAND()"
    sqlLIMIT = f"LIMIT 3"

    sqlSyntax = f"{sqlSELECT} {sqlFROM} {sqlWHERE} {sqlORDERBY} {sqlLIMIT};"

    # 從資料庫執行
    db = pymysql.connect(host='163.18.10.123', port=3306, user='EPuser', passwd='e507@mis', db='entries', charset='utf8mb4')
    cursor = db.cursor()
    cursor.execute(sqlSyntax)
    dbResult = cursor.fetchall()
    db.close()  
    # 整理從資料庫得到的資料
    dataArray = []
    for result in dbResult:
        data = {
            'leftIPA' : result[3],
            'leftWord' : result[4],
            'rightIPA' : result[6],
            'rightWord' : result[5],
        }
        dataArray.append(data)

    return dataArray
"""
def minimalPairTwoFinder(lett1, lett2):
    all_IPA = []
    ipa1 = []
    ipa2 = []
    dataArray = []

    sql = f"SELECT * from ngsl30k WHERE IPA LIKE '%{lett1}%' OR IPA LIKE '%{lett2}%';"
    db = pymysql.connect(host='163.18.10.123', port=3306, user='EPuser',
                    passwd='e507@mis', db='entries', charset='utf8mb4')

    cursor = db.cursor()
    cursor.execute(sql)
    all_data = cursor.fetchall()
    cursor.close()
    
    for i, s in enumerate(all_data):
        all_IPA.append([all_data[i][0], all_data[i][1], all_data[i][2], all_data[i][3], all_data[i][4], all_data[i][5].strip().replace("ˈ", "").replace("ˌ", "")])
    
    for i, s in enumerate(all_IPA):
        for j in range(i):
            if len(all_IPA[i][5]) == len(all_IPA[j][5]):
                if ipa_minimal_pair(all_IPA[i][5], all_IPA[j][5]) == 1:
                    ipa1.append(all_IPA[i])
                    ipa2.append(all_IPA[j])
                    
    for i, s in enumerate(ipa1):
        ipa1[i].append(different(ipa1[i][5], ipa2[i][5]))
        ipa2[i].append(different(ipa2[i][5], ipa1[i][5]))
        
    for i, s in enumerate(ipa1):
        if ipa1[i][6] == lett1 and ipa2[i][6] == lett2:
            data = {
            'leftIPA' : ipa1[i][5],
            'leftWord' : ipa1[i][2],
            'rightIPA' : ipa2[i][5],
            'rightWord' : ipa2[i][2],
            }
            dataArray.append(data)
            
    return dataArray
"""

# 找出輸入的word對應的minimal pair
def minimalPairWordFinder(word1):

    sqlSELECT = f"SELECT *"
    sqlFROM = f"FROM ipa_30k_minimal_pair"
    sqlWHERE = f"WHERE ipa_30k_minimal_pair.L_word LIKE '{word1}' OR ipa_30k_minimal_pair.R_word LIKE '{word1}'"
    sqlORDERBY = f"ORDER BY RAND()"
    sqlLIMIT = f"LIMIT 3"

    sqlSyntax = f"{sqlSELECT} {sqlFROM} {sqlWHERE} {sqlORDERBY} {sqlLIMIT};"

    # 從資料庫執行
    db = pymysql.connect(host='163.18.10.123', port=3306, user='EPuser', passwd='e507@mis', db='entries', charset='utf8mb4')
    cursor = db.cursor()
    cursor.execute(sqlSyntax)
    dbResult = cursor.fetchall()
    db.close()  
    # 整理從資料庫得到的資料
    dataArray = []
    for result in dbResult:
        data = {
            'leftIPA' : result[3],
            'leftWord' : result[4],
            'rightIPA' : result[6],
            'rightWord' : result[5],
        }
        dataArray.append(data)

    return dataArray

# 篩選出minimal pair
def ipa_minimal_pair(a, b):
    diffletter = 0
    for i, s in enumerate(a):
        if b[i] != s:
            diffletter += 1  
    #if diffletter == 1:
    #    print(a, b)
    return diffletter

# 找出不同的地方
def different(b, a):
    for i, s in enumerate(difflib.ndiff(a, b)):   
        if s[0] == ' ': continue
        elif s[0] == '+':
            diff = s[2]
    return diff

def checkPronunciation(questionIPAText, answerIPAText):

    questionIPATextCheckedArray = []
    answerIPATextCheckedArray = []

    match = difflib.SequenceMatcher(None, questionIPAText, answerIPAText).get_matching_blocks()

    questionIPATextCheckedArray.append(questionIPAText[:match[0][0]])
    answerIPATextCheckedArray.append(answerIPAText[:match[0][1]])
    for i in range(len(match)):
        if (i>0):
            questionIPATextCheckedArray.append(questionIPAText[match[i-1][0] + match[i-1][2]:match[i][0]])
            answerIPATextCheckedArray.append(answerIPAText[match[i-1][1] + match[i-1][2]:match[i][1]])

        questionIPATextCheckedArray.append(questionIPAText[match[i][0]:match[i][0] + match[i][2]])
        answerIPATextCheckedArray.append(answerIPAText[match[i][1]:match[i][1] + match[i][2]])

    # 整理從資料庫得到的資料

    response = {
        'questionCheckedArray' : questionIPATextCheckedArray,
        'answerCheckedArray' : answerIPATextCheckedArray,
    }
    
    return response

# 文字比較
def textCompare(Text1, Text2):

    Text1Array = []
    Text2Array = []

    match = difflib.SequenceMatcher(None, Text1, Text2).get_matching_blocks()

    Text1Array.append(Text1[:match[0][0]])
    Text2Array.append(Text2[:match[0][1]])
    for i in range(len(match)):
        if (i>0):
            Text1Array.append(Text1[match[i-1][0] + match[i-1][2]:match[i][0]])
            Text2Array.append(Text2[match[i-1][1] + match[i-1][2]:match[i][1]])

        Text1Array.append(Text1[match[i][0]:match[i][0] + match[i][2]])
        Text2Array.append(Text2[match[i][1]:match[i][1] + match[i][2]])

    # 整理從資料庫得到的資料

    response = {
        'Text1Array' : Text1Array,
        'Text2Array' : Text2Array,
    }
    
    return response

# 單字與發音比較
def wordCompare(Text1, Text2):
    
    textCompare2 = textCompare(Text1, Text2)

    Text1Array = []
    Text2Array = []
    Text1IPAArray = []
    Text2IPAArray = []

    for i in range(len(textCompare2['Text1Array'])):
        if (textCompare2['Text1Array'][i] == textCompare2['Text2Array'][i]):
            Text1Array.append(textCompare2['Text1Array'][i])
            Text2Array.append(textCompare2['Text2Array'][i])
        else:
            Text1Array.append('*' + textCompare2['Text1Array'][i] + '*')
            Text2Array.append('*' + textCompare2['Text2Array'][i] + '*')

    Text1ArrayText = ''
    Text2ArrayText = ''
    for i in range(len(Text1Array)):
        Text1ArrayText += Text1Array[i]
        Text2ArrayText += Text2Array[i]
        if (Text1Array[i] == '**'):
            Text1ArrayText += ' '
        if (Text2Array[i] == '**'):
            Text2ArrayText += ' '
    
    Text1Array = Text1ArrayText.split(' ')
    Text2Array = Text2ArrayText.split(' ')
    
    for i in range(len(Text1Array)):
        Text1Array[i] = Text1Array[i].replace('*', '')
        Text1IPAArray.append(eng_to_ipa.convert(Text1Array[i], False, False))
        Text2Array[i] = Text2Array[i].replace('*', '')
        Text2IPAArray.append(eng_to_ipa.convert(Text2Array[i], False, False))

    # 整理從資料庫得到的資料

    response = {
        'Text1Array' : Text1Array,
        'Text2Array' : Text2Array,
        'Text1IPAArray' : Text1IPAArray,
        'Text2IPAArray' : Text2IPAArray,
    }
    
    return response

# 單字集學習區 - 獲取單字集列表
def getWordSetList(uid, learningClassification):

    # 初始化SQL語法
    sqlSELECT = f"SELECT word_set.id, word_set.title, word_set.learning_classification, word_set.learning_phase, word_set.test_score, word_set.created_at, word_set.updated_at"
    sqlFROM = f"FROM word_set"
    sqlWHERE = f"WHERE word_set.uuid = '{uid}' AND word_set.learning_classification = '{learningClassification}'"
    sqlORDERBY = f"ORDER BY word_set.learning_phase DESC"
    
    sqlSyntax = f"{sqlSELECT} {sqlFROM} {sqlWHERE} {sqlORDERBY};" 

    # 從資料庫執行
    db = pymysql.connect(host='163.18.10.123', port=3306, user='EPuser', passwd='e507@mis', db='users', charset='utf8mb4')
    cursor = db.cursor()
    cursor.execute(sqlSyntax)
    results = cursor.fetchall()
    db.close()

    # 整理從資料庫得到的資料
    wordSetArray = []
    scoreSum = 0
    for result in results:
        # 
        wordList = []

        # 初始化SQL語法
        #sqlSELECT2 = f"SELECT DISTINCT toeic10k.word"
        #sqlFROM2 = f"FROM vocalbulary_classification"
        #sqlJOIN2 = f"JOIN toeic10k ON toeic10k.id = vocalbulary_classification.toeic10k_id"
        #sqlWHERE2 = f"WHERE (vocalbulary_classification.classification = '{result[2]}')"
        #sqlORDERBY2 = f"ORDER BY vocalbulary_classification.order_no ASC"
        #sqlLIMIT2 = f"LIMIT {(int(result[3]) - 1) * 10}, 10"

        sqlSELECT2 = f"SELECT DISTINCT vocalbulary_classification.id, toeic10k.word"
        sqlFROM2 = f"FROM vocalbulary_classification"
        sqlJOIN2 = f"JOIN toeic10k ON toeic10k.id = vocalbulary_classification.toeic10k_id"
        sqlWHERE2 = f"WHERE (vocalbulary_classification.ngsl30k_id != 0) AND vocalbulary_classification.classification = '{result[2]}'"
        sqlORDERBY2 = f"ORDER BY vocalbulary_classification.order_no ASC"
        sqlLIMIT2 = f"LIMIT {(int(result[3]) - 1) * 10}, 10"

        sqlSyntax2 = f"{sqlSELECT2} {sqlFROM2} {sqlJOIN2} {sqlWHERE2} {sqlORDERBY2} {sqlLIMIT2};"
        
        # 從資料庫執行
        db2 = pymysql.connect(host='163.18.10.123', port=3306, user='EPuser', passwd='e507@mis', db='entries', charset='utf8mb4')
        cursor2 = db2.cursor()
        cursor2.execute(sqlSyntax2)
        results2 = cursor2.fetchall()
        db2.close()
        # 整理從資料庫得到的資料
        for value in results2:
            wordList.append(value[1])
            pass

        data = {
            'wordSetID' : result[0],
            'wordSetTitle' : result[1],
            'wordSetClassification' : result[2],
            'wordSetPhase' : result[3],
            'wordSetScore' : result[4],
            'wordList' : wordList,
            'wordSetCreatedAt' : result[5],
            'wordSetUpdatedAt' : result[6],
        }
        scoreSum += result[4]
        wordSetArray.append(data)
        pass

    # 初始化SQL語法
    sqlSELECT3 = f"SELECT DISTINCT vocalbulary_classification_list.id, vocalbulary_classification_list.classification_name, vocalbulary_classification_list.descrip, vocalbulary_classification_list.word_count"
    sqlFROM3 = f"FROM vocalbulary_classification_list"
    sqlWHERE3 = f"WHERE vocalbulary_classification_list.id = '{learningClassification}'"
    sqlSyntax3 = f"{sqlSELECT3} {sqlFROM3} {sqlWHERE3};"
    # 從資料庫執行
    db3 = pymysql.connect(host='163.18.10.123', port=3306, user='EPuser', passwd='e507@mis', db='entries', charset='utf8mb4')
    cursor3 = db3.cursor()
    cursor3.execute(sqlSyntax3)
    dbResult3 = cursor3.fetchone() # 只取一筆
    db3.close()
    learningClassificationData = {
        'id' : dbResult3[0],
        'name' : dbResult3[1],
        'descrip' : dbResult3[2],
        'count' : dbResult3[3],
    }
    dataJSON = {
        'learningClassification' : learningClassificationData['id'],
        'learningClassificationName' : learningClassificationData['name'],
        'learningClassificationDescrip' : learningClassificationData['descrip'],
        'wordSetTotal' : math.ceil(int(learningClassificationData['count']) / 10),
        'averageScore' : round(scoreSum / max(1, len(wordSetArray) )),
        'wordSetArray' : wordSetArray
    }
    return dataJSON

# 單字集學習區 - 獲取下一個單字集
def addWordSet(uid, learningClassification, learningPhase):

    # 初始化SQL語法
    
    sqlSyntax = f"INSERT INTO word_set (uuid, learning_classification, learning_phase) VALUES ('{uid}', '{learningClassification}', '{learningPhase}');" 

    # 從資料庫執行
    db = pymysql.connect(host='163.18.10.123', port=3306, user='EPuser', passwd='e507@mis', db='users', charset='utf8mb4')
    cursor = db.cursor()
    cursor.execute(sqlSyntax)
    db.commit()
    db.close()

    return True



def getWordSetTotalList(index):


    # 初始化SQL語法
    sqlSELECT3 = f"SELECT COUNT(DISTINCT vocalbulary_classification.id)"
    sqlFROM3 = f"FROM vocalbulary_classification"
    sqlJOIN3 = f"JOIN toeic10k ON toeic10k.id = vocalbulary_classification.toeic10k_id"
    sqlWHERE3 = f"WHERE (vocalbulary_classification.ngsl30k_id != 0)"

    sqlSyntax3 = f"{sqlSELECT3} {sqlFROM3} {sqlJOIN3} {sqlWHERE3};"
    ## 從資料庫執行
    db3 = pymysql.connect(host='163.18.10.123', port=3306, user='EPuser', passwd='e507@mis', db='entries', charset='utf8mb4')
    cursor3 = db3.cursor()
    cursor3.execute(sqlSyntax3)
    dbResult3 = cursor3.fetchone() # 只取一筆
    db3.close()
    learningClassificationData = {
        'id' : '',
        'name' : 'Total',
        'descrip' : '',
        'count' : dbResult3[0],
    }

    wordSetArray = []
    indexDataArray = [int(index) - 1, int(index), int(index) + 1]
    scoreSum = 0
    for indexData in indexDataArray:

        if ( (1 <= indexData) and (indexData <= math.ceil(int(learningClassificationData['count']) / 10)) ):
            # 
            wordList = []

            # 初始化SQL語法
            #sqlSELECT2 = f"SELECT DISTINCT toeic10k.word"
            #sqlFROM2 = f"FROM vocalbulary_classification"
            #sqlJOIN2 = f"JOIN toeic10k ON toeic10k.id = vocalbulary_classification.toeic10k_id"
            #sqlWHERE2 = f"WHERE (vocalbulary_classification.classification = '{result[2]}')"
            #sqlORDERBY2 = f"ORDER BY vocalbulary_classification.order_no ASC"
            #sqlLIMIT2 = f"LIMIT {(int(result[3]) - 1) * 10}, 10"

            sqlSELECT2 = f"SELECT DISTINCT vocalbulary_classification.id, toeic10k.word"
            sqlFROM2 = f"FROM vocalbulary_classification"
            sqlJOIN2 = f"JOIN toeic10k ON toeic10k.id = vocalbulary_classification.toeic10k_id"
            sqlWHERE2 = f"WHERE (vocalbulary_classification.ngsl30k_id != 0)"
            sqlORDERBY2 = f"ORDER BY vocalbulary_classification.classification ASC, vocalbulary_classification.order_no ASC"
            sqlLIMIT2 = f"LIMIT {int(indexData - 1) * 10}, 10"

            sqlSyntax2 = f"{sqlSELECT2} {sqlFROM2} {sqlJOIN2} {sqlWHERE2} {sqlORDERBY2} {sqlLIMIT2};"
            
            # 從資料庫執行
            db2 = pymysql.connect(host='163.18.10.123', port=3306, user='EPuser', passwd='e507@mis', db='entries', charset='utf8mb4')
            cursor2 = db2.cursor()
            cursor2.execute(sqlSyntax2)
            results2 = cursor2.fetchall()
            db2.close()
            # 整理從資料庫得到的資料
            for value in results2:
                wordList.append(value[1])
                pass

            data = {
                'wordSetID' : 0,
                'wordSetTitle' : '',
                'wordSetClassification' : 'Total',
                'wordSetPhase' : indexData,
                'wordSetScore' : 0,
                'wordList' : wordList,
                'wordSetCreatedAt' : '',
                'wordSetUpdatedAt' : '',
            }
            scoreSum += 0
            wordSetArray.append(data)
        pass

    dataJSON = {
        'learningClassification' : learningClassificationData['id'],
        'learningClassificationName' : learningClassificationData['name'],
        'learningClassificationDescrip' : learningClassificationData['descrip'],
        'wordSetTotal' : math.ceil(int(learningClassificationData['count']) / 10),
        #'averageScore' : round(scoreSum / max(1, len(wordSetArray) )),
        'wordSetArray' : wordSetArray
    }
    return dataJSON

def getWordList(index, dataLimit = ''):
    
    if (dataLimit == ''):    
        dataLimit = 10

    sqlSELECT = f"SELECT DISTINCT ROW_NUMBER() OVER() AS row_index, vocalbulary_classification_list.classification_name, vocalbulary_classification.order_no, toeic10k.word, vocalbulary_classification.ngsl30k_id, toeic10k.wordType, toeic10k.wordLevel, vocalbulary_classification.source"
    sqlFROM = f"FROM vocalbulary_classification"
    sqlJOIN = f"JOIN toeic10k ON toeic10k.id = vocalbulary_classification.toeic10k_id"
    sqlJOIN = f"{sqlJOIN} JOIN vocalbulary_classification_list ON vocalbulary_classification_list.id = vocalbulary_classification.classification"
    sqlWHERE = f"WHERE (vocalbulary_classification.ngsl30k_id != 0)"
    sqlORDERBY = f"ORDER BY vocalbulary_classification.classification ASC, vocalbulary_classification.order_no ASC"
    sqlLIMIT = f"LIMIT {(int(index) - 1)}, {dataLimit}"

    sqlSyntax = f"{sqlSELECT} {sqlFROM} {sqlJOIN} {sqlWHERE} {sqlORDERBY} {sqlLIMIT};"
    
    # 從資料庫執行
    db = pymysql.connect(host='163.18.10.123', port=3306, user='EPuser', passwd='e507@mis', db='entries', charset='utf8mb4')
    cursor = db.cursor()
    cursor.execute(sqlSyntax)
    results = cursor.fetchall()
    db.close()   
    #raise Exception(sqlSyntax)
    # 整理從資料庫得到的資料
    dataArray = []
    for result in results:
        data = {
            'index' : result[0],
            'classificationName' : result[1],
            'orderNo' : result[2],
            'word' : result[3],
            'wordRanking' : result[4],
            'wordType' : result[5],
            'wordLevel' : result[6],
            'wordIPA' : eng_to_ipa.convert(result[3], False, False),
            'wordSource' : result[7],
            'wordMeaningList' : getWordMeaningData(result[3]),
        }
        dataArray.append(data)

    return dataArray

def getWordRowIndex(word):

    sqlSELECT = f"SELECT *"
    sqlFROM = "FROM (SELECT DISTINCT ROW_NUMBER() OVER() AS row_index, vocalbulary_classification_list.classification_name, vocalbulary_classification.order_no, toeic10k.word, vocalbulary_classification.ngsl30k_id, toeic10k.wordType, toeic10k.wordLevel, vocalbulary_classification.source  FROM vocalbulary_classification JOIN toeic10k ON toeic10k.id = vocalbulary_classification.toeic10k_id JOIN vocalbulary_classification_list ON vocalbulary_classification_list.id = vocalbulary_classification.classification WHERE (vocalbulary_classification.ngsl30k_id != 0) ORDER BY vocalbulary_classification.classification ASC, vocalbulary_classification.order_no ASC) AS A"
    sqlWHERE = f"WHERE (A.word = '{word}')"

    sqlSyntax = f"{sqlSELECT} {sqlFROM} {sqlWHERE};"
    
    # 從資料庫執行
    db = pymysql.connect(host='163.18.10.123', port=3306, user='EPuser', passwd='e507@mis', db='entries', charset='utf8mb4')
    cursor = db.cursor()
    cursor.execute(sqlSyntax)
    dbResult = cursor.fetchone() # 只取一筆
    db.close()

    # 整理回傳資料
    wordSyllable = ''
    
    if (not dbResult):
        raise Exception('查無資料')
    response = {
        'index': dbResult[0],
    }
    
    return response



def getWordData(word):

    sqlSELECT = f"SELECT *"
    sqlFROM = "FROM (SELECT DISTINCT ROW_NUMBER() OVER() AS row_index, vocalbulary_classification_list.classification_name, vocalbulary_classification.order_no, toeic10k.word, vocalbulary_classification.ngsl30k_id, toeic10k.wordType, toeic10k.wordLevel, vocalbulary_classification.source  FROM vocalbulary_classification JOIN toeic10k ON toeic10k.id = vocalbulary_classification.toeic10k_id JOIN vocalbulary_classification_list ON vocalbulary_classification_list.id = vocalbulary_classification.classification WHERE (vocalbulary_classification.ngsl30k_id != 0) ORDER BY vocalbulary_classification.classification ASC, vocalbulary_classification.order_no ASC) AS A"
    sqlWHERE = f"WHERE (A.word = '{word}')"

    sqlSyntax = f"{sqlSELECT} {sqlFROM} {sqlWHERE};"
    
    # 從資料庫執行
    db = pymysql.connect(host='163.18.10.123', port=3306, user='EPuser', passwd='e507@mis', db='entries', charset='utf8mb4')
    cursor = db.cursor()
    cursor.execute(sqlSyntax)
    dbResult = cursor.fetchone() # 只取一筆
    db.close()

    # 整理回傳資料
    wordSyllable = ''
    
    if (not dbResult):
        raise Exception('查無資料')
    response = {
        'index' : dbResult[0],
        'classificationName' : dbResult[1],
        'orderNo' : dbResult[2],
        'word' : dbResult[3],
        'wordRanking' : dbResult[4],
        'wordType' : dbResult[5],
        'wordLevel' : dbResult[6],
        'wordIPA' : eng_to_ipa.convert(dbResult[3], False, False),
        'wordSource' : dbResult[7],
        'wordMeaningList' : getWordMeaningData(dbResult[3]),
    }
    
    return response
