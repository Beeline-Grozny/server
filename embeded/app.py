from flask import Flask, request, jsonify
import cv2
from nomeroff_net import filters, RectDetector, TextDetector, Detector, OCR

app = Flask(__name__)

# Инициализация Nomeroff-net
nnet = Detector()
nnet.load()

rectDetector = RectDetector()
textDetector = TextDetector()
textDetector.load("latest")

ocr = OCR()
ocr.load("latest")

@app.route('/recognize', methods=['POST'])
def recognize():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    file = request.files['image']
    image = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_COLOR)

    # Обнаружение прямоугольников
    targets = rectDetector.detect(image)

    if len(targets) == 0:
        return jsonify({"error": "No license plates detected"}), 400

    # Распознавание текста
    textArr = textDetector.detect(image, targets)

    # OCR
    ocrResult = ocr.predict(textArr)

    return jsonify({"license_plates": ocrResult})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
