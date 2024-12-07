import cv2
from datetime import datetime


def capture_image(camera_index=0, save_path="images/"):
    cap = cv2.VideoCapture(camera_index)
    ret, frame = cap.read()
    if ret:
        file_path = f"{save_path}reaction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        cv2.imwrite(file_path, frame)
    cap.release()
    return file_path


def analyze_color(image_path):
    """
    Extract the predominant color from an image and return its hex code.
    """
    image = cv2.imread(image_path)
    average_color_per_row = image.mean(axis=0)
    average_color = average_color_per_row.mean(axis=0)
    hex_color = "#{:02x}{:02x}{:02x}".format(int(average_color[2]), int(average_color[1]), int(average_color[0]))
    return hex_color
