import cv2

if __name__ == "__main__":
    print("📸 Scanning for available camera devices...")

    for index in range(5):
        cap = cv2.VideoCapture(index)
        if cap.read()[0]:
            print(f"\n Camera at index {index} is working.")
            ret, frame = cap.read()
            if ret:
                cv2.imshow(f"Camera {index}", frame)
                cv2.waitKey(1000)
                cv2.destroyAllWindows()
        else:
            print(f"\n Camera at index {index} is not available.")
        cap.release()