import cv2
from skimage.metrics import structural_similarity as ssim
import numpy as np

def load_image(image_path):
    """تصویر را از مسیر داده شده بارگذاری می کند."""
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Image not found at path: {image_path}")
    return image

def calculate_ssim(imageA, imageB):
    """شاخص شباهت ساختاری (SSIM) بین دو تصویر را محاسبه می کند."""
    # تبدیل تصاویر به خاکستری
    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

    # محاسبه SSIM
    (score, diff) = ssim(grayA, grayB, full=True)
    diff = (diff * 255).astype("uint8")
    return score, diff

def visualize_difference(imageA, imageB, diff):
    """تفاوت بین دو تصویر را به صورت بصری نمایش می دهد."""
    # آستانه گذاری تفاوت
    thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

    # یافتن کانتورها برای مشخص کردن مناطق متفاوت
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # رسم مستطیل دور مناطق متفاوت روی هر دو تصویر
    for c in contours:
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # نمایش تصاویر
    cv2.imshow("Original", imageA)
    cv2.imshow("Modified", imageB)
    cv2.imshow("Diff", diff)
    cv2.imshow("Thresh", thresh)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def compare_videos(video_path_a, video_path_b, similarity_threshold=0.98):
    """دو ویدیو را فریم به فریم مقایسه می کند و میانگین SSIM و فریم های متفاوت را گزارش می دهد."""
    cap_a = cv2.VideoCapture(video_path_a)
    cap_b = cv2.VideoCapture(video_path_b)

    if not cap_a.isOpened():
        raise ValueError(f"Could not open video A: {video_path_a}")
    if not cap_b.isOpened():
        raise ValueError(f"Could not open video B: {video_path_b}")

    frame_count = 0
    total_ssim = 0
    different_frames = []

    while True:
        ret_a, frame_a = cap_a.read()
        ret_b, frame_b = cap_b.read()

        # اگر یکی از ویدیوها تمام شد یا هر دو تمام شدند
        if not ret_a or not ret_b:
            if ret_a != ret_b:
                print(f"Warning: Videos have different lengths. Comparison stopped at frame {frame_count}.")
            break

        # اطمینان از اینکه فریم ها دارای ابعاد یکسان هستند
        if frame_a.shape != frame_b.shape:
            print(f"Frame {frame_count}: Dimensions mismatch - Frame A: {frame_a.shape}, Frame B: {frame_b.shape}. Resizing Frame B.")
            frame_b = cv2.resize(frame_b, (frame_a.shape[1], frame_a.shape[0]))
            if frame_a.shape != frame_b.shape: # بررسی مجدد پس از تغییر اندازه
                 raise ValueError(f"Failed to resize Frame B to match Frame A dimensions at frame {frame_count}")


        score, _ = calculate_ssim(frame_a, frame_b)
        total_ssim += score
        frame_count += 1

        if score < similarity_threshold:
            different_frames.append(frame_count)
            print(f"Frame {frame_count}: Different (SSIM: {score:.4f})")
        # else:
        #     print(f"Frame {frame_count}: Identical (SSIM: {score:.4f})")

    cap_a.release()
    cap_b.release()

    if frame_count == 0:
        print("No frames were processed.")
        return 0, []

    average_ssim = total_ssim / frame_count
    print(f"\nAverage SSIM across {frame_count} frames: {average_ssim:.4f}")

    if not different_frames:
        print("Videos are identical based on the threshold.")
    else:
        print(f"Found differences in frames: {different_frames}")

    return average_ssim, different_frames 