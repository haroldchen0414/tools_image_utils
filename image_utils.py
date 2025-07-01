# -*- coding: utf-8 -*-
# author: haroldchen0414

import numpy as np
import string
import random
import shutil
import glob
import cv2
import os

class ImageUtils:
    def __init__(self):
        self.imageTypes = (".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", "webp")
        self.videoTypes = (".mp4", ".mov")
    
    def list_files(self, basePath, validExts=None, contains=None):
        for (rootDir, dirNames, fileNames) in os.walk(basePath):
            for fileName in fileNames:
                if contains is not None and fileName.find(contains) == -1:
                    continue

                ext = fileName[fileName.rfind("."):].lower()

                if validExts is None or ext.endswith(validExts):
                    imagePath = os.path.join(rootDir, fileName)

                    yield imagePath

    def list_images(self, basePath, contains=None):
        return self.list_files(basePath, validExts=self.imageTypes, contains=contains)

    def list_videos(self, basePath, contains=None):
        return self.list_files(basePath, validExts=self.videoTypes, contains=contains)

    def dhash(self, image_path, hashSize=8):
        gray = cv2.cvtColor(image_path, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(gray, (hashSize + 1, hashSize))

        diff = resized[:, 1:] > resized[:, :-1]

        return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])

    # 图片恢复后缀
    def fix_type(self, file_dir):
        files = list(self.list_files(file_dir))

        for file in files:
            if ".jpg" not in file and ".png" not in file:
                with open(file, "rb") as f:
                    f.seek(0, 0)
                    byte = f.read(3).hex()

                if byte.upper() == "FFD8FF":
                    os.rename(file, file + ".jpg")
                
                if byte.upper() == "89504E":
                    os.rename(file, file + ".png")
        
    # 检测删除重复的图片
    def detect_and_remove_duplicate(self, image_dir, hand_control=True):
        """
        hand_control: True的时候, 显示重复的图片, 可按d删除重复的图片
        """
        imagePaths = sorted(list(self.list_images(image_dir)))
        hashes = {}

        for imagePath in imagePaths:
            image = cv2.imdecode(np.fromfile(imagePath, dtype=np.int8), cv2.IMREAD_COLOR)

            try:
                h = self.dhash(image)
            
            except Exception as e:
                print("获取hash失败:{}, {}".format(imagePath, e))
            
            p = hashes.get(h, [])
            p.append(imagePath)
            hashes[h] = p

        for (h, hashedPaths) in hashes.items():
            if len(hashedPaths) > 1:
                montage = None

                for p in hashedPaths:
                    image = cv2.imdecode(np.fromfile(p, dtype=np.uint8), cv2.IMREAD_COLOR)
                    image = cv2.resize(image, (300, 300))

                    if montage is None:
                        montage = image
                    
                    else:
                        montage = np.hstack([montage, image])

                if hand_control:
                    cv2.imshow("Montage", montage)
                    key = cv2.waitKey(0)

                    # 手动按d删除
                    if key == ord("d"):
                        imagePaths = sorted(hashedPaths, key=lambda x:os.path.getsize(x), reverse=True)

                        for p in imagePaths[1:]:
                            os.remove(p)
            
                else:
                    imagePaths = sorted(hashedPaths, key=lambda x:os.path.getsize(x), reverse=True)

                    for p in imagePaths[1:]:
                        os.remove(p)
    
    # 重命名文件夹中的图片, 将视频移到视频文件夹
    def rename(self, image_dir, method=0, contain_video=True):
        """
        contain_video: 是否处理视频
        method: 0 重命名为xyz_1.jpg这种形式
        method: 1 重命名为1.jpg这种形式
        method: 2 重命名为00001.jpg这种形式
        """
        imagePaths = list(self.list_images(image_dir))

        if method == 0:
            randomKey = "".join(random.sample(string.ascii_lowercase, 3))

            if randomKey == os.path.basename(imagePaths[0]).split("_")[0]:
                raise Exception("随机字母跟现有命名重复, 请重新运行脚本生成其他随机字母")

            for (i, imagePath) in enumerate(imagePaths):
                imageType = os.path.basename(imagePath).split(".")[-1]
                os.rename(imagePath, os.path.join(image_dir, "{}_{}.{}".format(randomKey, i+1, imageType)))

        if method == 1:
            for (i, imagePath) in enumerate(imagePaths):
                imageType = os.path.basename(imagePath).split(".")[-1]
                os.rename(imagePath, os.path.join(image_dir, "{}.{}".format(i+1, imageType)))

        if method == 2:
            for (i, imagePath) in enumerate(imagePaths):
                imageType = os.path.basename(imagePath).split(".")[-1]
                os.rename(imagePath, os.path.join(image_dir, "{:05d}.{}".format(i+1, imageType)))

        if contain_video:
            os.makedirs(os.path.join(image_dir, "视频"), exist_ok=True)
            videoPaths = self.list_videos(image_dir)

            for videoPath in videoPaths:
                shutil.move(videoPath, os.path.join(image_dir, "视频", os.path.basename(videoPath)))

    # 增加删除文件夹图片视频大小信息[xP_yV_zMB]
    def modify_label(self, image_dir, method="add"):
        if method == "add":
            filePaths = self.list_files(image_dir)
            fileSize = 0

            fileSize += sum([os.path.getsize(filePath) for filePath in filePaths]) / 1024 / 1024
            nImages = len(list(self.list_images(image_dir)))
            nVideos = len(list(self.list_videos(image_dir)))
            label = "[{}P_{}V_{:.2f}MB]".format(nImages, nVideos, fileSize)

            os.rename(image_dir, image_dir + " " + label)
        
        if method == "delete":
            os.rename(image_dir, image_dir.split(" ")[0])

utils = ImageUtils()
#utils.detect_and_remove_duplicate("2025-05-01", hand_control=True)
#utils.fix_type("2025-05-01")
#utils.rename("2025-05-01")
#utils.modify_label("2025-05-01", method="add")