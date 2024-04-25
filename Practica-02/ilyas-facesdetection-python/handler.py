import base64
import cv2
import numpy as np
import requests

def handle(req):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# get the image url
    response = requests.get(req)
    image_bytes = np.frombuffer(response.content, np.uint8)
    img = cv2.imdecode(image_bytes, cv2.IMREAD_COLOR)
# change to gray
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# faces detect
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # save image
    cv2.imwrite("faces-detected.jpg", img)

    # Convert image to base64
    with open("faces-detected.jpg", "rb") as f:
        image_final = base64.b64encode(f.read()).decode("utf-8")

    # Creat  HTML 
    html_output = f'<img src="data:image/jpeg;base64,{image_final}">'
    
    return html_output


url_image = input("Entrez l'URL de l'image : ")
html_with_detected_faces = handle(url_image)
print(html_with_detected_faces)
