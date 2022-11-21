import os
import json
import jsonpath
from moviepy import *
from moviepy.editor import *

def bili_video(fpath):
    jsonf = os.path.join(fpath, 'entry.json')
    file = open(jsonf, 'r', encoding='utf-8')
    obj = json.loads(file.readline())
    partname = jsonpath.jsonpath(obj, '$..part')[0]
    asrc = os.path.join(fpath, '80\\audio.m4s')
    adst = os.path.join(fpath, '80\\'+partname+'.mp3')
    os.rename(asrc, adst)
    vsrc = os.path.join(fpath, '80\\video.m4s')
    vdst = os.path.join(fpath, '80\\'+partname+'.mp4')
    os.rename(vsrc, vdst)
    # 提取音轨
    audio = AudioFileClip(adst)
    # 读入视频
    video = VideoFileClip(vdst)
    # 将音轨合并到视频中
    video = video.set_audio(audio)
    # 输出
    video.write_videofile(f"{partname}.mp4")



folder = 'xxx'
path = os.path.join(os.getcwd(), folder)
files= os.listdir(path) #得到文件夹下的所有文件名称



for file in files: #遍历文件夹
    fpath = os.path.join(path, file)
    bili_video(fpath)

    
print(' OK!') #打印结果

