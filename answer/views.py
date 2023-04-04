from django.http import JsonResponse
from django.shortcuts import render
from pyparsing import WordStart
from answer.models import Questionanswer
from django.db import connection
import jieba
import jieba.posseg as pseg

# Create your views here.

def answer_list(request):
    # 通过objects这个模型管理器的all()获得所有数据行，相当于SQL中的SELECT * FROM
    
    # list = Questionanswer.objects.raw("SELECT T1.id, question, answer, img " +
    #                                     "FROM questionanswer as T1  join " + 
    #                                     "(SELECT T2.id, T2.qid, count(T2.qid) as cnt FROM wordquestion as T2 " +
    #                                     "where word in ('东风', '东风牌','CA71', '型', '轿车', '小轿车', '是', '哪个', '厂家', '生产','的', '?')" + 
    #                                     "group by T2.qid limit 1) as T3 where T1.id = T3.qid")
    question = request.GET.get('question')
    words = jieba.cut_for_search(question)
    words_str = ""
    for word in words:
        if word in ['大小', '规格']:
            words_str += " '尺寸', "
        if word == '时间':
            words_str += " '时候', "
        if word == '特征':
            words_str += " '特点', "
        if word == 'BK640B':
            words_str += " 'BK640', 'B型', "
        if word == 'SH760A':
            words_str += " 'SH760', 'A型', "
        if word == '客牌':
            words_str += " '客',"
        words_str += "'" + word + "',"


    # for (word, flag) in pseg.cut(question):
    #     words_str += "'" + word + "',"

    
    words_str = words_str.strip(',')


    sql = "SELECT T1.id, question, answer, img, logo, pre \
            FROM questionanswer as T1  join \
            (SELECT qid, count(word) as cnt FROM wordquestion as T2 \
            WHERE word IN (" + words_str + ") GROUP BY T2.qid ORDER BY cnt DESC limit 1) as T3 where T1.id = qid"

    print(sql)

    with connection.cursor() as cursor:
        cursor.execute(sql)
        # cursor.execute("select * from questionanswer limit 10")
        list = cursor.fetchall()
    
    response = [{"id": list[0][0], "question":list[0][1], "answer":list[0][2], "img":list[0][3], "logo": list[0][4], "pre": list[0][5]}]
    
    return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii":False})
