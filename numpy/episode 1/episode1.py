import numpy as np
from PIL import Image


def enhance_lunar_contrast(
    file_path: str = "luna.png", save_path: str = "luna_enhanced.png"
):
  img = Image.open(file_path).convert("L")
  data = np.array(img, dtype=float)

  min_val = np.min(data)
  max_val = np.max(data)

  print(f"Исходный диапазон яркостей: [{min_val}, {max_val}]")

  if max_val == min_val:
    enhanced_data = np.zeros_like(data, dtype=np.uint8)
  else:

    enhanced_data = (data - min_val) / (max_val - min_val) * 255
    enhanced_data = np.clip(enhanced_data, 0, 255).astype(np.uint8)

  res_img = Image.fromarray(enhanced_data)
  res_img.save(save_path)
  print(f"Улучшенное изображение сохранено в файл '{save_path}'.")

  return enhanced_data


if __name__ == "__main__":
  enhance_lunar_contrast("lunar01_raw.jpg", "luna_enhanced01.png")
  enhance_lunar_contrast("lunar02_raw.jpg", "luna_enhanced02.png")
  enhance_lunar_contrast("lunar03_raw.jpg", "luna_enhanced03.png")
  pass