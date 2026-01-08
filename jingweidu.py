import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import threading
from PIL import Image



def saveImg(index, jingdu_all, weidu_all, newPath, filePath):
    jingdu = jingdu_all[index : index+10]
    weidu = weidu_all[index : index+10]
    
    jingdu = np.diag(jingdu+weidu)
    # print(jingdu.shape)
    jingdu[0,2] = jingdu[1,1]
    jingdu[2,0] = jingdu[1,1]
    jingdu[0,4] = jingdu[2,2]
    jingdu[1,3] = jingdu[2,2]
    jingdu[3,1] = jingdu[2,2]
    jingdu[4,0] = jingdu[2,2]
    jingdu[0,6] = jingdu[3,3]
    jingdu[1,5] = jingdu[3,3]
    jingdu[2,4] = jingdu[3,3]
    jingdu[4,2] = jingdu[3,3]
    jingdu[5,1] = jingdu[3,3]
    jingdu[6,0] = jingdu[3,3]
    jingdu[0,8] = jingdu[4,4]
    jingdu[1,7] = jingdu[4,4]
    jingdu[2,6] = jingdu[4,4]
    jingdu[3,5] = jingdu[4,4]
    jingdu[5,3] = jingdu[4,4]
    jingdu[6,2] = jingdu[4,4]
    jingdu[7,1] = jingdu[4,4]
    jingdu[8,0] = jingdu[4,4]
    jingdu[1,9] = jingdu[5,5]
    jingdu[2,8] = jingdu[5,5]
    jingdu[3,7] = jingdu[5,5]
    jingdu[4,6] = jingdu[5,5]
    jingdu[6,4] = jingdu[5,5]
    jingdu[7,3] = jingdu[5,5]
    jingdu[8,2] = jingdu[5,5]
    jingdu[9,1] = jingdu[5,5]
    jingdu[3,9] = jingdu[6,6]
    jingdu[4,8] = jingdu[6,6]
    jingdu[5,7] = jingdu[6,6]
    jingdu[7,5] = jingdu[6,6]
    jingdu[8,4] = jingdu[6,6]
    jingdu[9,3] = jingdu[6,6]
    jingdu[5,9] = jingdu[7,7]
    jingdu[6,8] = jingdu[7,7]
    jingdu[8,6] = jingdu[7,7]
    jingdu[9,5] = jingdu[7,7]
    jingdu[7,9] = jingdu[8,8]
    jingdu[9,7] = jingdu[8,8]
    
    jingdu  = (jingdu * 255).astype(np.uint8)

    # 设置每个方块的边长
    newSideLengthEachBlock = 3
    img = Image.new('L', (10*newSideLengthEachBlock, 10*newSideLengthEachBlock), color=0)
    
    for i in range(10):
        for j in range(10):
            for ik in range(0, newSideLengthEachBlock):
                for jk in range(0, newSideLengthEachBlock):
                    img.putpixel((newSideLengthEachBlock*i+ik, newSideLengthEachBlock*j+jk), int(jingdu[i][j]))

    # #保存图片为png格式
    img.save(os.path.join(newPath, filePath, "{}_{}.png".format(typeName, str(index))))
    print("{}_{}.png".format(typeName, index),"successed")

typeName = "neg"
colName = {"pos":{"lon":"TrackPositionLongitude", "lat":"TrackPositionLatitude"}, "neg":{"lon":"lon", "lat":"lat"}}

originPath = os.path.join(r"C:\Users\Luokey\Desktop\data_prepare", typeName)
newPath = os.path.join(r"C:\Users\Luokey\Desktop\data_prepare", "generateImg_"+typeName)

if not os.path.exists(newPath):
    os.makedirs(newPath)

root = os.listdir(originPath)

import time 
start = time.time()

for filePath in root:
    data = pd.read_csv(os.path.join(originPath, filePath))
    filePath = filePath.split(".")[0]
    print("filePath", filePath)
    if not os.path.exists(os.path.join(newPath, filePath)):
        os.makedirs(os.path.join(newPath, filePath))
    jingdu_all,weidu_all = data[colName[typeName]["lat"]],data[colName[typeName]["lat"]]

    # jingdu_all = jingdu_all + weidu_all
    jingdu_all = (jingdu_all - jingdu_all.min())/(jingdu_all.max() - jingdu_all.min())
    weidu_all = (weidu_all - weidu_all.min())/(weidu_all.max() - weidu_all.min())

    print("len(jingdu_all)", len(jingdu_all))
    # threads = []
    for i in range(0, (len(jingdu_all))-10):
        saveImg(i, jingdu_all, weidu_all, newPath, filePath)
    break


endtime = time.time()
print("time", endtime-start)

