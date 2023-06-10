import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
import numpy as np
from collections import Counter
# import pyocr
from PIL import Image
from ultralytics import YOLO
import cv2
import pytesseract
from konlpy.tag import Okt
from typing import List
from lexrankr import LexRank
from transformers import pipeline
import re
import googletrans
from urllib.request import urlopen
import json
import urllib.request

class OktTokenizer:
    okt: Okt = Okt()

    def __call__(self, text: str) -> List[str]:
        tokens: List[str] = self.okt.pos(text, norm=True, stem=True, join=True)
        return tokens

class Model():
    def __init__(self):
        self.info = ""
        self.summary = ""
        self.error = ""
        self.labels = {
            0: '사람',
            1: '자전거',
            2: '자동차',
            3: '오토바이',
            4: '비행기',
            5: '버스',
            6: '기차',
            7: '트럭',
            8: '보트',
            9: '신호등',
            10: '소화전',
            11: '정지표시판',
            12: '주차미터기',
            13: '벤치',
            14: '새',
            15: '고양이',
            16: '강아지',
            17: '말',
            18: '양',
            19: '소',
            20: '코끼리',
            21: '곰',
            22: '얼룩말',
            23: '기린',
            24: '배낭',
            25: '우산',
            26: '핸드백',
            27: '넥타이',
            28: '여행가방',
            29: '원반장난감',
            30: '스키',
            31: '스노보드',
            32: '공',
            33: '연',
            34: '야구방망이',
            35: '야구글러브',
            36: '스케이트보드',
            37: '서프보드',
            38: '테니스라켓',
            39: '병',
            40: '와인잔',
            41: '컵',
            42: '포크',
            43: '나이프',
            44: '숟가락',
            45: '그릇',
            46: '바나나',
            47: '사과',
            48: '샌드위치',
            49: '오렌지',
            50: '브로콜리',
            51: '당근',
            52: '핫도그',
            53: '피자',
            54: '도넛',
            55: '케이크',
            56: '의자',
            57: '소파',
            58: '화분',
            59: '침대',
            60: '식탁',
            61: '변기',
            62: '텔레비전',
            63: '노트북',
            64: '마우스',
            65: '리모컨',
            66: '키보드',
            67: '핸드폰',
            68: '전자레인지',
            69: '오븐',
            70: '토스터기',
            71: '싱크대',
            72: '냉장고',
            73: '책',
            74: '시계',
            75: '꽃병',
            76: '가위',
            77: '곰인형',
            78: '헤어드라이어',
            79: '칫솔'
        }

    def modeling(self, mode, path_dlocal, path_ulocal):
        # image open
        Image.MAX_IMAGE_PIXELS=None
        try:
            img = Image.open(path_dlocal)
        except:
            self.error = 'please check url of image'
            return

        try:
            if mode == "0":
                img = self.object(img)

            elif mode == "1":
                img = self.ocr_v2(path_dlocal)
                self.summarize()
        except:
            self.error='Exception occured while running'

        print("== self.info ====")
        print(self.info)

        print("== self.summarize ====")
        print(self.summary)

        print("== self.error ====")
        print(self.error)

        # store model image
        cv2.imwrite(path_ulocal, img)

        return self.info, self.summary, self.error

    # def translateGoogle(self, inStr):
    #     translator = googletrans.Translator()
    #
    #     outStr = translator.translate(inStr, dest='ko', src='en')
    #
    #     return outStr.text

    # def translatePapago(self, inStr):
    #     # translate eng to kor through Papago API
    #     client_id = "7cyuDLUY3kSNzmFs_i88"  # 개발자센터에서 발급받은 Client ID 값
    #     client_secret = "NMYcZYMSNp"  # 개발자센터에서 발급받은 Client Secret 값
    #     encText = urllib.parse.quote(inStr)
    #     data = "source=en&target=ko&text=" + encText
    #     url = "https://openapi.naver.com/v1/papago/n2mt"
    #     request = urllib.request.Request(url)
    #     request.add_header("X-Naver-Client-Id", client_id)
    #     request.add_header("X-Naver-Client-Secret", client_secret)
    #     response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    #     rescode = response.getcode()
    #
    #     if (rescode == 200):
    #         response_body = response.read()
    #         result = response_body.decode('utf-8')
    #         d = json.loads(result)
    #         eng_to_kor = d['message']['result']['translatedText']
    #
    #     else:
    #         eng_to_kor = "error code: " + rescode
    #
    #     return eng_to_kor
    #
    def object(self, img):
        model = YOLO("yolov8n.pt")

        obj_results = model(img, device="mps")
        obj_result = obj_results[0]

        img = np.asarray(img)
        bboxes = np.array(obj_result.boxes.xyxy.cpu(), dtype="int")

        for bbox in bboxes:
            (x, y, x2, y2) = bbox
            cv2.rectangle(img, (x, y), (x2, y2), (0, 0, 225), 2)

        classes = np.array(obj_result.boxes.cls.cpu(), dtype="int")
        class_list = []

        for i in range(len(classes)):
            class_list.append(self.labels[classes[i]])

        result = ""
        for key, value in dict(Counter(class_list)).items():
            result += str(key) + str(value) + ' '

        self.info = result.strip()

        return img

    def ocr_v2(self, img_path):
        import pytesseract
        import urllib.request
        import cv2
        import numpy as np
        import imutils

        import re
        import requests
        # req = urllib.request.urlopen(img_url)
        # arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
        # img = cv2.imdecode(arr, -1)
        img=cv2.imread(img_path)

        # convert image to grayscale
        image = imutils.resize(img, width=500)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5,), 0)
        edged = cv2.Canny(blurred, 75, 200)

        # resize & denoise image
        denoised = cv2.fastNlMeansDenoising(gray, h=10, searchWindowSize=21, templateWindowSize=7)
        res, thresh = cv2.threshold(denoised, 196, 255, cv2.THRESH_BINARY)

        # thresh[260:2090]=~thresh[260:2090]
        result = np.hstack((gray, thresh))
        # cv2.imshow(result)
        #
        # cv2.imshow(image)
        # cv2.imshow(gray)
        # cv2.imshow(blurred)
        # cv2.imshow(edged)

        # text=[]
        # #
        # text.append(str(pytesseract.image_to_string(image, lang='kor+eng')))
        # text.append(str(pytesseract.image_to_string(edged, lang='kor+eng')))
        # text.append(str(pytesseract.image_to_string(gray, lang='kor+eng')))
        # text.append(str(pytesseract.image_to_string(blurred, lang='kor+eng')))
        # text.append(str(pytesseract.image_to_string(result, lang='kor+eng')))
        # print(pytesseract.image_to_boxes(image))
        # result=''
        # for i in range(5):
        #     result+='text'+str(i)+'\n'
        #     result+=text[i]
        self.info = str(pytesseract.image_to_string(gray, lang='kor+eng'))
        # self.info=result
        return gray
    def summarize_kor(self):
        # 1. init using Okt tokenizer
        mytokenizer: OktTokenizer = OktTokenizer()
        lexrank: LexRank = LexRank(mytokenizer)
        text = self.info
        # 2. summarize (like, pre-computation)
        lexrank.summarize(text)

        summerization = []

        # 3. probe (like, query-time)
        summaries: List[str] = lexrank.probe()
        for summary in summaries:
            summerization.append(summary)

        return summerization

    def summarize_eng(self):
        # Load the summarization pipeline with the desired model
        summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

        # Use the pipeline to generate the summary
        summary_dump = summarizer(self.info, max_length=150, min_length=30, do_sample=False)

        # Print the summarized text
        summary = (summary_dump[0]['summary_text'])

        return summary

    def summarize(self):
        # Determine language of text
        lang = "en" if re.match(r"^[A-Za-z0-9\s\.,\?]+$", self.info) else "ko"

        # Summarize English text
        if lang == "en":
            summary = self.summarize_eng()
        # Summarize Korean text
        else:
            summary = self.summarize_kor()
            summary = ' '.join(summary)

        self.summary = summary

