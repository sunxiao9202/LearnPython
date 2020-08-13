import json
from time import sleep

import pymysql
import requests

db = pymysql.connect("192.168.9.223", "sunxiao", "sunxiao", "KG_MAKER")
cursor = db.cursor()


def load_data():
    sql = "select label from k12_label"
    cursor.execute(sql)
    res = list(cursor.fetchall())
    listData = []
    if res is not None:
        for i in res:
            listData.append(i[0])
    return listData


# 获取歧义关系
def getAmbiguous(entity):
    sess = requests.get('https://api.ownthink.com/kg/ambiguous?mention=' + entity)
    result = sess.text
    resDict = json.loads(result)
    return resDict


def getPropertyName(param):
    if param == 'desc':
        return '简介'
    if param == 'tag':
        return '标签'
    if param == 'avp':
        return '属性'
    if param == 'domain':
        return '领域'
    else:
        return param


# 获取实体知识
def getKnowledge(entity):
    sess = requests.get("https://api.ownthink.com/kg/knowledge?entity=" + entity)
    answer = sess.text
    answer = json.loads(answer)
    if answer['message'] == 'success':
        dataDict = answer['data']
        for key in dataDict.keys():
            if key == 'entity':
                continue
            objs = dataDict[key]
            if isinstance(objs, list):
                for content in objs:
                    if key == 'tag':
                        print("爬取到entity:" + entity + "  " + key + "  value:" + content)
                        sql = "INSERT INTO `sizhi_content`(entity,param,content) VALUES('{0}','{1}','{2}')".format(
                            entity, getPropertyName(key), content)
                        cursor.execute(sql)
                        db.commit()
                    else:
                        print("爬取到entity:" + entity + "  " + key + "   key:" + content[0] + "  value:" + content[1])
                        sql = "INSERT INTO `sizhi_content`(entity,param,property,content) VALUES('{0}','{1}','{2}','{3}')".format(
                            entity, getPropertyName(key), content[0], content[1])
                        cursor.execute(sql)
                        db.commit()
            else:
                print("爬取到entity:" + entity + "  " + key + ":" + objs)
                sql = "INSERT INTO `sizhi_content`(entity,param,content) VALUES('{0}','{1}','{2}')".format(entity,
                                                                                                           getPropertyName(
                                                                                                               key),
                                                                                                           objs)
                cursor.execute(sql)
                db.commit()


def save_ambiguous(entity, ambiguous):
    sql = "INSERT INTO `sizhi_ambiguous`(entity,ambiguous) VALUES('{0}','{1}')".format(entity,
                                                                                       ambiguous)
    cursor.execute(sql)
    db.commit()


def main():
    listData = load_data()
    if listData is not None:
        i = 0
        while i < len(listData):
            entity = listData[i]
            resDict = getAmbiguous(entity)
            if resDict['message'] == 'success':
                entitys = resDict['data']
                if entitys and len(entitys) > 0:
                    for item in entitys:
                        save_ambiguous(entity, item[0])
                        getKnowledge(item[0])
            print(str(i) + "=================")
            i = i + 1
            sleep(2)


if __name__ == '__main__':
    main()
    cursor.close()
    db.close()
