from PIL import Image
import os

src_path = os.path.join("src", "pirate_icone.png")
dst_path = os.path.join("src", "pirate_icone.ico")

if os.path.exists(src_path):
    img = Image.open(src_path)
    img.save(dst_path, format='ICO', sizes=[(256, 256)])
    print(f"Converted {src_path} to {dst_path}")
else:
    print(f"Source not found: {src_path}")
