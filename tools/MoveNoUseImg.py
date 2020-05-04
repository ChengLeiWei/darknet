# coding = uft-8
# coco_label.py解析coco2014数据集的instances_train2014.json和instances_val2014.json会出现
# 解析获得的labels文件夹下文件数量与对应JPEGImages文件夹下文件数量不一致（标签文件数量少于图片数量）
# 原因是COCO2014数据集中有的图片本身没有标签，因此这些没标签的图片不需要与label文件对应的继续存
# 放在JPEGImages文件夹下，所以该.py文件将没有对应上的图片文件移动至如下新建的文件夹，以获得适用于
# ultralytics版本的yolov3项目的数据集。
# 首先，在train2014和val2014文件夹下分别创建train2014_nouseImages和val2014_nouseImages文件夹
# 然后，判断原JPEGImages文件夹中的图片名字是否在labels文件夹中，如果不存在就将其移动至对
# 应的新建文件夹中（如train2014_nouseImages文件夹下）

import os, shutil
from tqdm import *


def checkJpgXml(jpeg_dir, labels_dir):
    """
    dir1 是图片所在文件夹
    dir2 是标注文件所在文件夹
    """
    subsettype = 'train2014'
    nousefile_path = './cocodata/%s/%s_nouseImages' % (subsettype, subsettype)
    if not os.path.exists(nousefile_path):
        os.makedirs(nousefile_path)
    pBar = tqdm(total=len(os.listdir(jpeg_dir)))
    cnt = 0
    for file in os.listdir(jpeg_dir):
        pBar.update(1)
        f_name, f_ext = file.split(".")
        if not os.path.exists(os.path.join(labels_dir, f_name + ".txt")):
            print(f_name)
            cnt += 1
            OrigionalNoUseFilePath = os.path.join(jpeg_dir, file)
            NewNoUseFilePath = os.path.join(nousefile_path, file)
            shutil.move(OrigionalNoUseFilePath, NewNoUseFilePath)

    if cnt > 0:
        print("有%d个文件不符合要求,已全部移至%s。" % (cnt, nousefile_path))
    else:
        print("所有图片和对应的xml文件都是一一对应的。")


dataType = 'train2014'
dir1 = r"./cocodata/%s/JPEGImages" % (dataType)
dir2 = r"./cocodata/%s/labels" % (dataType)
checkJpgXml(dir1, dir2)
