from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

# It's recommended to configure your API key at the beginning of your script
# genai.configure(api_key="YOUR_API_KEY")

client = genai.Client()

try:
    woman_image = Image.open(
        'C:/Users/carly/Pictures/Camera Roll/Various Profile Pics/craiyon_190620_Create_an_image_that_looks_like_a_selfie_taken_from_an_iPhone__There_should_be_no_clear_subject_or_s.png'
    )
    logo_image = Image.open(
        'C:/Users/carly/Pictures/Camera Roll/Various Profile Pics/craiyon_190441_Create_an_image_that_looks_like_a_selfie_taken_from_an_iPhone__There_should_be_no_clear_subject_or_s.png'
    )

    text_input = """Using the 2 images provided, create a similar image with the same young woman. 
    Ensure the young woman's face and features remain unchanged. 
    The original prompt used is as follows: Create an image that looks like a selfie taken from an iPhone. There should be no clear subject or specific composition. Just a casual snapshot of a young woman who looks around 18 in the photo with a White/Florida/Miami look attractive woman with blonde hair and brown eyed. She is in her bedroom, there is a closet door closed and her bedroom decorations and light purple lighting in the dark room and her unmade cute bed with stuffed animals. Aspect of the ratio of the photo should be 9:16 but not look AI generated but rather look as though it was taken to send to someone/selfie. she has her tongue out.
    """

    # Generate an image from a text prompt and images
    response = client.models.generate_content(
        model="gemini-2.5-flash-image",
        contents=[text_input, woman_image, logo_image],
        # The config parameter is optional and can be removed if you don't need to specify thinking_budget
        # config=types.GenerateContentConfig(
        #     thinking_config=types.ThinkingConfig(thinking_budget=0)
        # ),
    )

    # Extract and save the generated image
    if (
        response.candidates
        and response.candidates[0].content
        and response.candidates[0].content.parts
    ):
        image_parts = [
            part.inline_data.data
            for part in response.candidates[0].content.parts
            if part.inline_data and part.inline_data.data is not None
        ]

        if image_parts:
            image_bytes = image_parts[0]  # now guaranteed not None
            image = Image.open(BytesIO(image_bytes))
            image.save('generated_image.png')
            image.show()
        else:
            print("No image data found in the response.")
            # It's helpful to print the response to understand why an image wasn't generated
            print(response)


except FileNotFoundError as e:
    print(f"Error: {e}. Please check the file paths for your images.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
