import os

import cv2
from retinaface import RetinaFace
import aiohttp
import numpy as np
import asyncio
from io import BytesIO
from PIL import Image
async def download_image(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            
            if response.status == 200:
                return  await response.read()
            else:
                return False
async def detect_facex(imageURL, output_file, save_img):
    pass
    output_file = f'images/{output_file}.jpg'
    image_content = await download_image(imageURL)
    if image_content != False:
        img_array = np.frombuffer(image_content, np.uint8)
        image = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        resp = RetinaFace.detect_faces(image)
        if save_img:
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            for face_id, face_info in resp.items():
                facial_area = face_info['facial_area']
                x1, y1, x2, y2 = facial_area  
                cv2.rectangle(image_rgb, (x1, y1), (x2, y2), (255, 0, 32), 2)
            pil_image = Image.fromarray(image_rgb)
            pil_image.save(output_file)
        if len(resp) > 0:
            return True
        else:
            return False
    else:
        return 'URL ERROR'




    # import matplotlib.pyplot as plt
    # plt.imshow(image_rgb)
    # plt.axis('off')  
    # plt.show()




# username = 'marianandadqwd22'
# async def detect_face():
#     x = await detect_facex('https://pbs.twimg.com/profile_images/1770830343001509888/FjBXF46t.jpg', username, save_img = False)
#     print(x)


# asyncio.run(detect_face())
