import cv2

files=files[7]

cap = cv2.VideoCapture(files)
length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

def onChange(trackbarValue):
    cap.set(cv2.CAP_PROP_POS_FRAMES,trackbarValue)
    err,img = cap.read()
    cv2.imshow("mywindow", img)
    pass

cv2.namedWindow('mywindow')
cv2.createTrackbar( 'start', 'mywindow', 0, length, onChange )
cv2.createTrackbar( 'end'  , 'mywindow', 1000, length, onChange )

onChange(0)
cv2.waitKey()

start = cv2.getTrackbarPos('start','mywindow')
end   = cv2.getTrackbarPos('end','mywindow')
if start >= end:
    raise Exception("start must be less than end")

cap.set(cv2.CAP_PROP_POS_FRAMES,start)
while cap.isOpened():
    err,img = cap.read()
    if cap.get(cv2.CAP_PROP_POS_FRAMES) >= end:
        break
    cv2.imshow("mywindow", img)
    k = cv2.waitKey(10) & 0xff
    if k==27:
        break