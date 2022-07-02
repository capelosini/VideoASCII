import cv2
import os
import platform
import numpy as np
from PIL import Image,ImageDraw,ImageFont
import gc
import imageio.v2 as io

def readVideo(video, w, h, totalFrames):
    frames=[]
    
    s, frame = video.read()
    count=0
    while s:
        count+=1
        percentage=round((count/totalFrames)*100)
        print(f"Loading Frame {str(count)} - {str(percentage)}%")
        s, frame = video.read()
        if s:
            resized=cv2.resize(frame, dsize=(200, 60), interpolation=cv2.INTER_CUBIC)
            frames.append(frame2ASCII(resized, w, h))
    video.release()
    return frames

def frame2ASCII(frame, w, h):
    # chars=[".", "-", "+", "#"]
    chars='.1`1^1"1,1:1;1I1l1!1i1>1<1~1+1_1-1?1]1[1}1{1)1(1|1\1/1t1f1j1r1x1n1u1v1c1z1X1Y1U1J1C1L1Q101O1Z1m1w1q1p1d1b1k1h1a1o1*1#1M1W1&181%1B1@1$'.split("1")
    char=""
    wid=1
    hei=1
    charWidth = 10
    charHeight = 18
    font = ImageFont.truetype('SourceCodePro-Medium.ttf',15)
    outputImage = Image.new('RGB',(round(w),round(h)),color=(0,0,0))
    draw = ImageDraw.Draw(outputImage)
    for line in frame:
        for pixel in line:
            b, g, r = pixel
            media=((r+g+b)/3)
            sp=127.5/len(chars)
            resul=0
            for c in chars:
                resul+=sp
                if resul >= media:
                    char=c
                    break
            # if media < 63.75:
            #     char=chars[0]
            # elif media >= 63.75 and media < 127.5:
            #     char=chars[1]
            # elif media >= 127.5 and media < 191.25:
            #     char=chars[2]
            # elif media >= 191.25:
            #     char=chars[3]
            draw.text((wid*charWidth, hei*charHeight), char, font=font,fill=(r,g,b))
            wid+=1
        hei+=1
        wid=1
    gc.collect()
    return outputImage

def clear():
    oss=platform.system()
    if oss == "Windows":
        os.system("cls")
    else:
        os.system("clear")


videoName=input("File: ")

video=cv2.VideoCapture(videoName)
width=video.get(cv2.CAP_PROP_FRAME_WIDTH )
height=video.get(cv2.CAP_PROP_FRAME_HEIGHT )
length=video.get(cv2.CAP_PROP_FRAME_COUNT)
fps=video.get(cv2.CAP_PROP_FPS)

Frames=readVideo(video, width, height, length)

print("\nRendered!")
print("\nExporting the video..")

outWriter=io.get_writer(videoName+"-OUT.mp4", format='FFMPEG', mode='I', fps=fps)

for Frame in Frames:
    framearr=np.array(Frame)
    outWriter.append_data(framearr)
    
clear()

input("\nFinished!")

