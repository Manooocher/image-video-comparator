import argparse
from utils import load_image, calculate_ssim, visualize_difference, compare_videos
import os
import cv2

def compare_images(image_path_a, image_path_b, visualize=False):
    """دو تصویر را مقایسه می کند، SSIM را برمی گرداند و به صورت اختیاری تفاوت را نمایش می دهد."""
    try:
        imageA = load_image(image_path_a)
        imageB = load_image(image_path_b)
    except ValueError as e:
        print(f"Error loading images: {e}")
        return

    # اطمینان از اینکه تصاویر دارای ابعاد یکسان هستند
    if imageA.shape != imageB.shape:
        print(f"Images have different dimensions: {imageA.shape} vs {imageB.shape}. Cannot compare.")
         # تلاش برای تغییر اندازه تصویر دوم به ابعاد تصویر اول
        print(f"Resizing image B to match image A dimensions: {imageA.shape[:2]}")
        imageB = cv2.resize(imageB, (imageA.shape[1], imageA.shape[0]))
        if imageA.shape != imageB.shape: # بررسی مجدد پس از تغییر اندازه
            print("Failed to resize image B. Cannot compare.")
            return

    score, diff = calculate_ssim(imageA, imageB)

    print(f"SSIM: {score:.4f}")

    if score == 1.0:
        print("Images are identical.")
    else:
        print("Images are different.")
        if visualize:
            # ایجاد کپی برای جلوگیری از تغییر تصاویر اصلی هنگام ویژوالایز کردن
            visualize_difference(imageA.copy(), imageB.copy(), diff)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Compare two images or videos using SSIM.')
    parser.add_argument('path_a', help='Path to the first image or video file.')
    parser.add_argument('path_b', help='Path to the second image or video file.')
    parser.add_argument('--visualize', action='store_true', help='Show visual differences between images.')
    parser.add_argument('--type', choices=['image', 'video'], default=None, help='Specify the type of media (image or video). Tries to auto-detect if not specified.')
    parser.add_argument('--threshold', type=float, default=0.98, help='SSIM threshold for considering video frames as different (default: 0.98).')

    args = parser.parse_args()

    file_type = args.type

    # تلاش برای تشخیص خودکار نوع فایل اگر مشخص نشده باشد
    if file_type is None:
        _, ext_a = os.path.splitext(args.path_a)
        _, ext_b = os.path.splitext(args.path_b)
        # فرض بر این است که اگر پسوندها رایج ویدیویی باشند، نوع ویدیو است
        video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.wmv']
        if ext_a.lower() in video_extensions and ext_b.lower() in video_extensions:
            file_type = 'video'
        else:
            # در غیر این صورت، فرض بر تصویر بودن است
            file_type = 'image'
        print(f"Auto-detected file type as: {file_type}")


    if file_type == 'image':
        if not os.path.exists(args.path_a):
             print(f"Error: Image file not found at {args.path_a}")
        elif not os.path.exists(args.path_b):
             print(f"Error: Image file not found at {args.path_b}")
        else:
            compare_images(args.path_a, args.path_b, args.visualize)
    elif file_type == 'video':
        if args.visualize:
            print("Warning: Visualization is only supported for image comparison.")
        if not os.path.exists(args.path_a):
             print(f"Error: Video file not found at {args.path_a}")
        elif not os.path.exists(args.path_b):
             print(f"Error: Video file not found at {args.path_b}")
        else:
            compare_videos(args.path_a, args.path_b, args.threshold) 