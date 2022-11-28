
# # img2img
import torch
import requests
from PIL import Image
from io import BytesIO

from diffusers import StableDiffusionImg2ImgPipeline

# load the pipeline
device = "cuda"
# model_id =  "runwayml/stable-diffusion-v1-5" sample
model_id = "Linaqruf/anything-v3.0"


pipe = StableDiffusionImg2ImgPipeline.from_pretrained(
    model_id, torch_dtype=torch.float32
)
pipe = pipe.to(device)

# let's download an initial image
url = "https://raw.githubusercontent.com/CompVis/stable-diffusion/main/assets/stable-samples/img2img/sketch-mountains-input.jpg"

response = requests.get(url)
init_image = Image.open(BytesIO(response.content)).convert("RGB")
init_image.thumbnail((768, 768))

prompt = "A girl"

images = pipe(prompt=prompt, init_image=init_image, strength=0.75, guidance_scale=7.5).images

images[0].save("fantasy_landscape.png")