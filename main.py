from face_detector import detect_face
import asyncio
import random
from aiomultiprocess import Pool
import time
from asyncio.exceptions import TimeoutError
from colorama import Fore, init
import requests
import json
import aiohttp
import random
import json
import time
import sys
import os

init()
PU = []

with open('users.txt', 'r', encoding='utf-8', errors='ignore') as f:
    x = 0
    for line in f:
        x += 1
        y = line.strip()
        PU.append(f'{x}:{y}')

def data_base():
    with open('config.json', 'r', encoding='utf-8') as config:
        data = json.load(config)
        return data


async def main(chunk):
    try:
        data = chunk.split(':')
        if len(data) == 6:
            counter, username , followers, following , profile_images, URL = data
            URL_IMAGE = f'{profile_images}:{URL}'
            data_save = f'{username}:{followers}:{following}:{URL_IMAGE}'
            face_tetect = await detect_face(imageURL=URL_IMAGE, output_file=username, save_img=False)
            if face_tetect and str(face_tetect) != 'URL ERROR':
                with open('result/face_DETECTED.txt', 'a', encoding='utf-8') as f:
                    if data_save not in open('result/face_DETECTED.txt', 'r', encoding='utf-8').read():
                        f.write(data_save + '\n')
                print(f'{Fore.MAGENTA}[ {Fore.WHITE}{counter}{Fore.MAGENTA} ] [ {Fore.RED}{username}{Fore.MAGENTA} ] [ FOLLOWERS: {Fore.RED}{followers}{Fore.MAGENTA} ] [ FACE DETECT: {Fore.RED}{face_tetect} {Fore.MAGENTA} ] ')
            else:
                if str(face_tetect) == 'URL ERROR':
                    print(f'{Fore.MAGENTA}[ {Fore.WHITE}{counter}{Fore.MAGENTA} ] [ {Fore.RED}{username}{Fore.MAGENTA} ] [ FOLLOWERS: {Fore.RED}{followers}{Fore.MAGENTA} ] [ FACE DETECT: {Fore.RED}URL IMAGE ERROR{Fore.MAGENTA} ] ')
                    with open('result/url_error.txt', 'a', encoding='utf-8') as f:
                        if data_save not in open('result/url_error.txt', 'r', encoding='utf-8').read():
                            f.write(data_save + '\n')
                else:
                    with open('result/face_NOT_detetect.txt', 'a', encoding='utf-8') as f:
                        if data_save not in open('result/face_NOT_detetect.txt', 'r', encoding='utf-8').read():
                            f.write(data_save + '\n')
                    print(f'{Fore.MAGENTA}[ {Fore.WHITE}{counter}{Fore.MAGENTA} ] [ {Fore.GREEN}{username}{Fore.MAGENTA} ] [ FOLLOWERS: {Fore.GREEN}{followers}{Fore.MAGENTA} ] [ FACE DETECT: {Fore.GREEN}{face_tetect} {Fore.MAGENTA} ] ')
    
    except Exception as e:
                print(f'{Fore.MAGENTA}[ {Fore.RED}{data_save}{Fore.MAGENTA} ] [ {Fore.RED}{e}{Fore.MAGENTA} ] ')


async def x():
        thread = data_base()['THREAD']
        count =1
        n = int(thread)
        final = [PU[i * n:(i + 1) * n] for i in range((len(PU) + n - 1) // n )]
        for x in final:
            count+=1
            async with Pool() as pool:
                async for result in pool.map(main,x):
                    continue 

if __name__ == '__main__':
    try:
        asyncio.run(x())
    except Exception as e:
        print(e)