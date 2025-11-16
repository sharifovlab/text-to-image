import base64
import PySimpleGUI as psg
import openai
from PIL import Image
from io import BytesIO
import os
from dotenv import load_dotenv

# Load .env
load_dotenv()
openai.api_key = os.getenv("API_AI_KEY")


def get_user_input():
    layout = [
        [psg.Text("Please enter prompt")],
        [psg.InputText(key="-INPUT-")],
        [psg.Submit(), psg.Cancel()]
    ]

    window = psg.Window(
        "Text to Image",
        layout,
        size=(500, 150),
        element_justification="center",
        finalize=True
    )
    window.bring_to_front()

    while True:
        event, values = window.read()
        if event in (psg.WIN_CLOSED, "Cancel"):
            window.close()
            return None
        elif event == "Submit":
            prompt = values["-INPUT-"]
            window.close()
            return prompt


def call_api(prompt):
    response = openai.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024"
    )
    return base64.b64decode(response.data[0].b64_json)


def display_image(image_bytes):
    # Convert PIL to PNG data
    image = Image.open(BytesIO(image_bytes))
    bio = BytesIO()
    image.save(bio, format="PNG")
    img_data = bio.getvalue()

    # Scrollable image column so buttons never get pushed off screen
    layout = [
        [psg.Column(
            [[psg.Image(data=img_data, key="-IMG-")]],
            scrollable=True,
            vertical_scroll_only=True,
            size=(900, 600)
        )],
        [psg.Button("Save"), psg.Button("Close")]
    ]

    window = psg.Window(
        "Your Image",
        layout,
        finalize=True,
        resizable=True,
        element_justification="center"
    )

    window.bring_to_front()

    while True:
        event, values = window.read()

        if event in (psg.WIN_CLOSED, "Close"):
            break

        if event == "Save":
            filename = psg.popup_get_file(
                "Save Image As",
                save_as=True,
                file_types=(("PNG Files", "*.png"), ("All Files", "*.*")),
                default_extension=".png"
            )

            if filename:
                with open(filename, "wb") as f:
                    f.write(image_bytes)
                psg.popup("Saved Successfully!", keep_on_top=True)

    window.close()


def main():
    prompt = get_user_input()
    if prompt:
        print("Generating image...")
        image_bytes = call_api(prompt)
        display_image(image_bytes)
        print("Done.")


if __name__ == "__main__":
    main()
