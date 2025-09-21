import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

def convert_to_grayscale_luminosity(rgb_img):
    #L = 0.299 * R + 0.587 * G + 0.114 * B
    return np.dot(rgb_img[..., :3], [0.299, 0.587, 0.114])

def convert_to_grayscale_luminosity_HDTV(rgb_img):
    #L = 0.2126 * R + 0.7152 * G + 0.0722 * B
    return np.dot(rgb_img[..., :3], [0.2126, 0.7152, 0.0722])

def calculate_difference(img1, img2):
    return img1 - img2

def create_test_image():
    size = 300
    x = np.linspace(0, 255, size)
    y = np.linspace(0, 255, size)
    xx, yy = np.meshgrid(x, y)

    r_channel = xx.astype(np.uint8)
    g_channel = yy.astype(np.uint8)
    b_channel = np.full_like(xx, 128, dtype=np.uint8)

    return np.stack([r_channel, g_channel, b_channel], axis=-1)

image_path = input("Путь к изображению: ").strip()
try:
    img = Image.open(image_path)
    image = np.array(img)
    if image.shape[2] == 4:
        image = image[..., :3]
    print(f"Изображение загружено")
except Exception as e:
    print(f"Ошибка загрузки изображения: {e}")
    image = create_test_image()
    print("Создано тестовое изображение")

gray_luminosity = convert_to_grayscale_luminosity(image)
gray_luminosity_HDTV = convert_to_grayscale_luminosity_HDTV(image)
difference = calculate_difference(gray_luminosity, gray_luminosity_HDTV)

if difference.max() != difference.min():
    difference_normalized = (difference - difference.min()) / (difference.max() - difference.min())
else:
    difference_normalized = np.zeros_like(difference)

fig, axes = plt.subplots(2, 3, figsize=(15, 10))

axes[0, 0].imshow(image)
axes[0, 0].set_title('Исходное RGB изображение')
axes[0, 0].axis('off')

axes[0, 1].imshow(gray_luminosity, cmap='gray')
axes[0, 1].set_title('Обычный метод\n(0.299R + 0.587G + 0.114B)')
axes[0, 1].axis('off')

axes[0, 2].imshow(gray_luminosity_HDTV, cmap='gray')
axes[0, 2].set_title('HDTV метод\n(0.2126R + 0.7152G + 0.0722B)')
axes[0, 2].axis('off')

im_diff = axes[1, 0].imshow(difference_normalized, cmap='coolwarm')
axes[1, 0].set_title('Разность методов\n(Обычный - HDTV)')
axes[1, 0].axis('off')
plt.colorbar(im_diff, ax=axes[1, 0])

data1 = gray_luminosity.flatten()
data2 = gray_luminosity_HDTV.flatten()

x_min = min(data1.min(), data2.min())
x_max = max(data1.max(), data2.max())
y_max = max(np.histogram(data1, bins=50)[0].max(), 
            np.histogram(data2, bins=50)[0].max()) * 1.1

axes[1, 1].hist(data1, bins=50, color='gray', alpha=0.7, edgecolor='black')
axes[1, 1].set_title('Гистограмма: Обычный метод')
axes[1, 1].set_xlabel('Интенсивность')
axes[1, 1].set_ylabel('Частота')
axes[1, 1].set_xlim(x_min, x_max)
axes[1, 1].set_ylim(0, y_max)
axes[1, 1].grid(True, alpha=0.3)

axes[1, 2].hist(data2, bins=50, color='gray', alpha=0.7, edgecolor='black')
axes[1, 2].set_title('Гистограмма: HDTV метод')
axes[1, 2].set_xlabel('Интенсивность')
axes[1, 2].set_ylabel('Частота')
axes[1, 2].set_xlim(x_min, x_max)
axes[1, 2].set_ylim(0, y_max)
axes[1, 2].grid(True, alpha=0.3)

plt.tight_layout()
plt.subplots_adjust(wspace=0.3, hspace=0.3)

plt.show()