# مقایسه گر تصویر و ویدیو با SSIM

این پروژه ابزاری خط فرمان برای مقایسه دو تصویر یا دو ویدیو با استفاده از شاخص شباهت ساختاری (SSIM) فراهم می کند.

## ویژگی ها

*   مقایسه دو تصویر و گزارش میزان شباهت SSIM.
*   نمایش بصری تفاوت های بین دو تصویر.
*   مقایسه دو ویدیو به صورت فریم به فریم و گزارش میانگین SSIM.
*   شناسایی فریم هایی در ویدیوها که زیر یک آستانه شباهت مشخص هستند.
*   تشخیص خودکار نوع فایل (تصویر یا ویدیو) بر اساس پسوند.
*   مدیریت تصاویر یا فریم های ویدیو با ابعاد متفاوت (با تلاش برای تغییر اندازه).

## نصب

1.  **کلون کردن مخزن:**
    ```bash
    git clone https://github.com/Manooocher/image-video-comparator
    cd https://github.com/Manooocher/image-video-comparator/
    ```

2.  **ایجاد محیط مجازی (اختیاری اما توصیه می شود):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **نصب وابستگی ها:**
    ```bash
    pip install -r requirements.txt
    ```

## استفاده

اسکریپت اصلی `main.py` است. شما می توانید آن را از خط فرمان اجرا کنید.

**پارامترهای اصلی:**

*   `path_a`: مسیر فایل اول (تصویر یا ویدیو).
*   `path_b`: مسیر فایل دوم (تصویر یا ویدیو).

**پارامترهای اختیاری:**

*   `--type {image,video}`: نوع فایل ها را مشخص می کند. اگر مشخص نشود، اسکریپت سعی می کند به طور خودکار تشخیص دهد.
*   `--visualize`: (فقط برای تصاویر) تفاوت های بصری بین دو تصویر را نمایش می دهد.
*   `--threshold FLOAT`: (فقط برای ویدیوها) آستانه SSIM برای در نظر گرفتن فریم های متفاوت (پیش فرض: 0.98).

### مثال ها

**مقایسه دو تصویر:**
```bash
python main.py path/to/image1.jpg path/to/image2.png
```

**مقایسه دو تصویر با نمایش تفاوت ها:**
```bash
python main.py path/to/image1.jpg path/to/image2.png --visualize
```

**مقایسه دو ویدیو:**
```bash
python main.py path/to/video1.mp4 path/to/video2.avi
```

**مقایسه دو ویدیو با آستانه SSIM متفاوت:**
```bash
python main.py path/to/video1.mp4 path/to/video2.mp4 --threshold 0.95
```

**مقایسه دو ویدیو با تعیین نوع فایل:**
```bash
python main.py path/to/file1 path/to/file2 --type video
```

## توضیحات کد

*   **`main.py`**: این فایل شامل منطق اصلی برای تجزیه آرگومان های خط فرمان و فراخوانی توابع مناسب برای مقایسه تصویر یا ویدیو است.
*   **`utils.py`**: این فایل شامل توابع کمکی است:
    *   `load_image()`: بارگذاری یک تصویر با استفاده از OpenCV.
    *   `calculate_ssim()`: محاسبه SSIM بین دو تصویر.
    *   `visualize_difference()`: نمایش تفاوت های بصری بین دو تصویر.
    *   `compare_videos()`: مقایسه فریم به فریم دو ویدیو.
*   **`requirements.txt`**: لیست کتابخانه های پایتون مورد نیاز. 
