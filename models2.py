from mongoengine import connect
# -*- coding: utf-8 -*-
from datetime import datetime

from mongoengine import DateTimeField
from mongoengine import Document
from mongoengine import IntField
from mongoengine import StringField
from mongoengine import URLField
from mongoengine import connect
from mongoengine import ListField

__author__ = "jenny"

# 连接 mongodb，无需事先创建数据库
connect('lagou3', host='localhost', port=27017)

class Post(Document):
    """
    文章信息
    """
    companyFullName = StringField()  # 公司名称
    city = StringField()  # 所在城市
    jobNature = StringField()  # 职位类型
    positionName = StringField()  # 岗位名称
    salary = StringField()  # 薪水
    positionAdvantage = StringField()  # 优势描述
    workYear = StringField()  # 工作年限
    financeStage = StringField()  # 公司融资情况
    district = StringField() # 公司区域
    education = StringField() # 教育程度
    companySize = StringField() # 公司规模
    companyLabelList = ListField()
    skillLables = ListField()
    positionId = IntField(default=0)
    secondType = StringField()
    firstType = StringField()
    thirdType = StringField()
    # read_num = IntField(default=0)  # 阅读数
    # like_num = IntField(default=0)  # 点赞数
    # comment_num = IntField(default=0)  # 评论数
    # reward_num = IntField(default=0)  # 赞赏数
    # author = StringField()  # 作者

    createTime = DateTimeField()  # 数据生成时间
    # u_date = DateTimeField(default=datetime.now)  # 最后更新时间
