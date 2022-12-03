import torch
from PIL import Image

import glob
import os
import argparse

from diffusers import StableDiffusionImg2ImgPipeline

IMG_DIR = "img"
IMG_DIR_CNV = "img_cnv"

def anything(prompt = "A girl", strength=0.75, guidance_scale=7.5):
  # load the pipeline
  device = "cuda"

  # model_id =  "runwayml/stable-diffusion-v1-5" sample
  model_id = "Linaqruf/anything-v3.0"

  pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
      model_id, torch_dtype=torch.float16
  )
  pipe = pipe.to(device)

  print('Number of images:', sum(os.path.isfile(os.path.join(IMG_DIR, name)) for name in os.listdir(IMG_DIR)))
  for i, f in enumerate(glob.glob(IMG_DIR + "/*")):
      file_name = os.path.split(f)[1]
      print('{0}: {1}'.format(i+1, file_name))

      init_image = Image.open(f)
      init_image.thumbnail((768, 768)) # アスペクト比を保ちながら縮小

      # init_image.save(IMG_DIR_CNV + "/" + file_name)

      images = pipe(prompt=prompt, init_image=init_image, strength=strength, guidance_scale=guidance_scale).images
      images[0].save(IMG_DIR_CNV + "/" + file_name)

  return "complete"

if __name__ == "__main__":
  #オプション引数（コマンドライン）
  parser = argparse.ArgumentParser(description='Stable Diffusion Img2Img anything-v3.0')
  parser.add_argument('-p', '--prompt', default='A girl')
  parser.add_argument('-s', '--strength', default=0.75)
  parser.add_argument('-g', '--guidance_scale', default=7.5)
  args = parser.parse_args()

  anything(args.prompt, args.strength, args.guidance_scale)