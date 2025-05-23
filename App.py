import cv2
import torch

model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

PATH_DATA = f'Data/vid4.mp4'  


cap = cv2.VideoCapture(PATH_DATA)  


def detect_and_track_motos(frame):
    results = model(frame)

   
    motos = results.pandas().xyxy[0][results.pandas().xyxy[0]['name'] == 'motorcycle']
    
    contador = 0
    for _, row in motos.iterrows():
        x1, y1, x2, y2 = int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax'])
        confidence = row['confidence']
        
        
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
        cv2.putText(frame, f'Moto {confidence:.2f}', (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
        
        contador += 1
    
    cv2.putText(frame, f'Total Motos: {contador}', (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    return frame

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = detect_and_track_motos(frame)

    cv2.imshow('Mottu Moto Detection', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
