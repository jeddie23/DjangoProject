from django.http import JsonResponse
from django.shortcuts import render
from answer.models import Questionanswer
from django.db import connection
import jieba

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
        words_str += "'" + word + "',"
    words_str = words_str.strip(',')
    print(words_str)

    sql = "SELECT T1.id, question, answer, img \
            FROM questionanswer as T1  join \
            (SELECT qid, count(qid) as cnt FROM wordquestion as T2 \
            where word in (" + words_str + ") group by T2.qid limit 1) as T3 where T1.id = qid"
    print(sql)
    with connection.cursor() as cursor:
        cursor.execute(sql)
        # cursor.execute("select * from questionanswer limit 10")
        list = cursor.fetchall()
    
    response = [{"id": list[0][0], "question":list[0][1], "answer":list[0][2], "img":list[0][3]}]
    
    return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii":False})
