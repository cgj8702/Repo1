import huggingface_hub
import os

huggingface_hub.login(token=os.getenv("HF_TOKEN"))
