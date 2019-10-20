import os
import io
from google.cloud import vision
import pandas as pd
import folium
import sys
from random import uniform
from folium import IFrame
import base64
import time


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'spaceappsapitoken.json'

client = vision.ImageAnnotatorClient()


listeX = [39.75401758897679, 38.187901515502254, 40.24381585400583, 39.572949070312426, 38.46163096805255, 38.89499886837023, 40.63343792989501,-67.718739]

listeY = [32.15829888062895, 27.252584715607448, 27.487076520642, 30.043822207474644, 33.84322766422963, 32.94363453989796, 37.516465219892766, 45.911325]


m = folium.Map(location=[39.75401758897679,32.15829888062895],tiles="Stamen Terrain", zoom_start= 7)
feature_group = folium.FeatureGroup("Locations")



tooltip = "Click to see picture"


i=0
for lX, lY in zip(listeX, listeY):
    file_name = '%s.jpg'% i
    image_path = f'.\Images\{file_name}'

    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

    # construct an iamge instance
    image = vision.types.Image(content=content)
    response = client.label_detection(image=image)
    labels = response.label_annotations

    df = pd.DataFrame(columns=['description', 'score', 'topicality'])

    for label in labels:
        df = df.append(
            dict(
                description=label.description,
                score=label.score,
                topicality=label.topicality
            ), ignore_index=True)
        
    print(df.head(3).to_string())
    text0 = df.description[0] + " : " + str(df.score[0])
    text1 = df.description[1] + " : " + str(df.score[1])
    text2 = df.description[2] + " : " + str(df.score[2])
    temp = df.description[0]+df.description[1]+df.description[2]
    if('fire' in temp or 'Fire' in temp):
        icon1 = folium.features.CustomIcon('logo.png', icon_size=(60,45))
        feature_group.add_child(folium.Marker(location=[lX + 0.008,  lY + 0.008], tooltip='Firefighters is Coming',  icon=icon1))

    
    html = '<center><b> {} <br /> {} <br /> {} </b></center><img src="data:image/png;base64,{}">'.format
    text = './images/%s.jpg'% i
    picture1 = base64.b64encode(open(text,'rb').read()).decode()
    iframe1 = IFrame(html(text0 ,text1 ,text2 ,picture1), width=600+20, height=400+20)
    popup1 = folium.Popup(iframe1, max_width=1024,max_height=2000)
    icon1 = folium.Icon(color="red",icon='info-sign')
    feature_group.add_child(folium.Marker(location=[lX,  lY], popup=popup1, tooltip=tooltip, icon=icon1))
    i+=1
    time.sleep(1)




m.add_child(feature_group)

m.save("index.html")

