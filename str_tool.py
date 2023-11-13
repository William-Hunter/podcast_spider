#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import time
import json
import shutil
import traceback



##返回True代表过滤掉
def filter(title,channel):
    if 'has' in channel and channel['has']:#如果包含条件
        for hasRule in channel['has']:
            if hasRule in title:
                print("↑↑↑有我想要的")
                return False    ##不过滤
        print("↑↑↑没有我想要的")
        return True ##过滤掉

    elif 'ban' in channel and channel['ban']:#如果包含屏蔽内容
        for banRule in channel['ban']:
            if banRule in title:
                print("↑↑↑有我不想要的")
                return True
        print("↑↑↑没有我不想要的")
        return False

    return False    #默认不过滤




