# OPEN_EYES-BACKEND

This repository guides you through the Backend part of "**Open Eyes**".

---

## Overview

The following shows the overall structure of Open Eyes.

When the client uploads the data that it wants to process with Firebase, it performs a function suitable for the data, either Object Detection or OCR + Summarization, and processes the information that the user wants.

<img width="1148" alt="image" src="https://github.com/GachonAI20/OPEN_EYES-BACKEND/assets/88086519/24953051-9480-4e81-92a7-ec820e961da2">

---

## Tech 1: OCR

Tesseract is an open source optical character recognition (OCR) platform.
Used Tesseract v5 model and went through the process of resizing the input image and changing it to gray to improve recognition performance.

<br/>
The overall flow of OCR and summarization is as follows.
<br/>
After importing the image using the path of the image stored in Firebase, OCR is performed using tesseractv5 through image preprocessing.
<br/>
After performing OCR, the extracted text is summarized and the result information is stored in Firebase again to deliver the information to the user.

<img width="1153" alt="image" src="https://github.com/GachonAI20/OPEN_EYES-BACKEND/assets/88086519/e8c1d17d-7351-43a6-9f60-ff41e6fe9096">

<br/><br/>

The results of OCR are as follows. After performing OCR on the input image, the information is stored as the info of the output result.
<br/>
Thereafter, information including the corresponding result of the summarization is stored in the Firebase so that the user can obtain the information.

| Input Image | Output Result |
|------|---------------|
| ![그림2-1](https://github.com/GachonAI20/OPEN_EYES-BACKEND/assets/88086519/f34fc418-eb9f-45ce-aeb3-0b71875f7fe6) | <img width="542" alt="그림2-2" src="https://github.com/GachonAI20/OPEN_EYES-BACKEND/assets/88086519/7341361c-ddab-4fd0-a649-028452a932ab"> |


---

## Tech 2: Summarization

The objective of this documentation is to provide an overview of a Python-based code that performs document summarization for both Korean and English texts.


- English Summarization:
For English text summarization, the code uses the transformers library along with the pipeline module.

- Korean Summarization:
  For Korean text summarization, the code utilizes the lexrankr library (https://github.com/theeluwin/lexrankr) with the Korean tokenizer, Okt, from konlpy.

<br/>
The overall flow of Summarization is as follows.
<br/>
When text information is extracted from an image through OCR, it first classifies which language the text is composed of, English or Korean.
<br/>
In the case of English text, it is summarized using transformer. In the case of Korean text, tokenization is performed using KoNLP's OKt tokenizer, and then summarized using a factor model.
<br/>
In this way, after performing a summary process suitable for each language, the results are stored in Firebase and the corresponding information is delivered to the user.

<img width="1192" alt="image" src="https://github.com/GachonAI20/OPEN_EYES-BACKEND/assets/88086519/243d378c-47eb-4dbd-9f6a-9589584d856f">

<br/><br/>

The results of the English summary and the Korean summary are as follows.
<br/>
After performing the summarization as follows, the information is stored in the summary part of the Output Result discussed above.
<br/>
Through this process, the results of OCR and Summarization are stored in Firebase so that the user can obtain information.

- English Summarization

| Input Text | Output Text  |
|----------------------------|---------------------------|
| South Korea, officially known as the Republic of Korea, is a country located in East Asia. With a rich history spanning back thousands of years, it has witnesse d the rise and fall of various dynasties. The Korean Peninsula's geographical loc ation has fostered close interactions with neighboring countries, particularly China, influencing its culture and traditions. Korean cuisine is renowned world wide, with dishes like kimchi, bulgogi, and bibimbap gaining international popularity. South Korea has also made a significant impact through its entertainment industry, known as the Korean Wave or Hallyu, which includes K-pop music, K-dramas, and Korean films. With its unique blend of tradition and modernity, South Korea continues to captivate global audiences with its vibrant culture and technological advancements. | South Korea, officially known as the Republic of Korea, is a country located in East Asia. The Korean Peninsula's geographical location has fostered close interactions with neighboring countries, particularly China, influencing its culture and traditions. |

- Korean Summarization

| Input Text                                                                                                                                                                                                                                                                                                                                 | Output Text  |
|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------|
| 한국은 동아시아에 위치한 반도 국가로, 역사적으로는 고려와 조선 등 다양한 왕조를 거쳐왔습니다. 지리적 특성으로 인해 주변 국가들과의 교류가 활발했으며, 중국의 문화와 영향을 많이 받았습니다. 한글은 15세기에 창제된 한 국어의 고유한 문자 체계로, 현대 한국어의 표기에 사용되고 있습니다. 한국은 특히 음식 문화로 유명하여, 김치, 불 고기, 비빔밥, 떡볶이 등 다양한 음식을 즐기며 특색 있는 맛과 조화로운 조리법으로 인정받고 있습니다. 한국은 또 한 한류 문화인 K-pop과 드라마를 통해 글로벌한 인기를 얻고 있으며, 한국의 음악, 연기, 패션 등이 전 세계적으로 사랑받고 있습니다. | 한국은 또한 한류 문화인 K-pop과 드라마를 통해 글로벌한 인기를 얻고 있으며, 한국의 음악, 연기, 패션 등이 전 세계적으로 사랑받고 있습니다. |

---

## Tech 3: Object Detection

In this project, object detection was implemented using YOLOv8. It accurately identifies various objects in a given image and provides that information to the user.

<br/>
The overall flow of Object Detection is as follows.
<br/>
After importing the image using the path of the image stored in the firebase, object detection is performed using the YOLOv8-based model.
<br/>
Thereafter, the detection result image and information are stored again in the Firebase and the corresponding information is delivered to the user.

<img width="996" alt="image" src="https://github.com/GachonAI20/OPEN_EYES-BACKEND/assets/88086519/56cf66db-77f2-4160-a196-6f5e41072548">

<br/><br/>

The YOLOv8 model, known to be relatively fast, was used. Based on the YOLOv8 model, the model was trained to increase object recognition performance in real life.

<img width="909" alt="image" src="https://github.com/GachonAI20/OPEN_EYES-BACKEND/assets/88086519/9b95f04c-fe69-42b6-a31c-c64640a46f29">

<br/><br/>

The results of Object Detection are as follows.
<br/>
After object recognition is performed on the input image, the output image and output result information are stored in the Firebase.
<br/>
Thereafter, the info portion of the same Output Result is delivered to the user so that the user can obtain information.

| Input Image | Output Image | Output Result |
|-------------|--------------|---------------|
| <img width="191" alt="그림1-1" src="https://github.com/GachonAI20/OPEN_EYES-BACKEND/assets/88086519/579c6576-6e74-4ca7-9f0a-c4b5060bc2a0"> | <img width="191" alt="그림1-2" src="https://github.com/GachonAI20/OPEN_EYES-BACKEND/assets/88086519/a8a2bd6d-65bc-4ca4-9d62-87555e437b0b"> | <img width="315" alt="그림1-3" src="https://github.com/GachonAI20/OPEN_EYES-BACKEND/assets/88086519/d03a8761-64a8-4669-9461-712ef611765a"> |

---

## Used Libraries

The libraries required for the code are stored in _requirements.txt_.
<br/>
You can use the file to install and run the library required for the backend code.
