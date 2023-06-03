from django.http import JsonResponse
from django.shortcuts import render
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

    hasBrand = False
    hasType = False
    brand = ""
    type = ""
    words_str = words_str.strip(',')
    words_new = words_str.split(',')
    print(words_new)
    for word in words_new:
        with connection.cursor() as cursor:
            cursor.execute("select * from brand where brandname = " + word +";")
            result = cursor.fetchall()
            if len(result) > 0:
                hasBrand = True 
                brand = word[1:len(word)-1]
            cursor.execute("select * from type where typename = " + word +";")
            result = cursor.fetchall()
            if len(result) > 0:
                hasType = True 
                type = word[1:len(word)-1]
        if hasBrand and hasType:
            break 

    nullAnswer = "感谢您的使用！您查询的产品目前没有收录到我们的资料里，抱歉！\n我们中国近现代工业产品设计智能问答目前主要收录新中国建立前后到1990年代前的代表性品牌和产品，我们的产品数据库正在继续完善中，敬请期待。\n如需进一步查询，请点击"
    response = []
    if hasBrand and hasType:
        sql = "SELECT T1.id, question, answer, img, logo, pre \
                FROM questionanswer as T1  join \
                (SELECT qid, count(word) as cnt FROM wordquestion as T2 \
                WHERE word IN (" + words_str + ") GROUP BY T2.qid ORDER BY cnt DESC limit 1) as T3 where T1.id = qid;"

        print(sql)

        with connection.cursor() as cursor:
            cursor.execute(sql)
            # cursor.execute("select * from questionanswer limit 10")
            list = cursor.fetchall()
        
        print(brand)
        print(type)
        if list[0][1].find(brand) == -1 or list[0][1].find(type) == -1:
            print(list[0][1])
            response = [{"id": -1, "question":question, "answer":nullAnswer, "img":"no image", "logo": "no logo", "pre": "no pre"}]
        else:
            response = [{"id": list[0][0], "question":list[0][1], "answer":list[0][2], "img":list[0][3], "logo": list[0][4], "pre": list[0][5]}]
    else:
        response = [{"id": -1, "question":question, "answer":nullAnswer, "img":"no image", "logo": "no logo", "pre": "no pre"}]
    
    return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii":False})
