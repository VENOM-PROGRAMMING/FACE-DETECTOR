import os
import matplotlib.pyplot as plt
import cv2
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
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


async def detect_face(imageURL, output_file, save_img):
    
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
    # plt.imshow(image_rgb)
    # plt.axis('off')  
    # plt.show()




# username = 'marianandadqwd22'
# async def detect_face():
#     x = await detect_face('https://i0.wp.com/basketball.wales/wp-content/uploads/2021/02/38013941_1711524018902634_7417673816026906624_o.jpg?w=750&ssl=1', username, save_img = True)
#     print(x)


# asyncio.run(run_mainx())
