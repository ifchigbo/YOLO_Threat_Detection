import dash, base64, os
import numpy as np
import cv2
from dash import html, dcc, callback, Input, Output
from tfile.validator import getStaticTest, getStaticTestForFiles
from settings import IMAGES_BETWEEN_PATHS

dash.register_page(__name__)

files = os.listdir(os.getcwd() + '/' + IMAGES_BETWEEN_PATHS)
print(files)

upload_div = html.Div(
    [
        html.H2("Upload Image or Video", className="text-2xl text-white my-2 text-center"),
        html.Div(
            html.Div(
                dcc.Upload(
                    id="upload-data",
                    children=html.Div(
                        [
                            html.Div(html.Img(src='assets/images/subway_image.png', id='upload-image-icon', alt='upload image', className='mb-2')),
                            "Drag and Drop here or ",
                            html.A("Select Files", className="text-sky-800"),
                        ],
                        className="flex flex-col items-center",
                    ),
                ),
                className="p-2 border-2 border-x-zinc-700 border-dashed rounded-3xl h-full flex flex-col justify-center items-center",
            ),
            className="h-60 bg-white p-4 shadow-md rounded-3xl font-bold mb-3",
        )
    ],
    className="flex flex-col justify-center h-screen"
)

layout = html.Div(
    [
        upload_div,
        html.Div(id="output-uploaded-data"),
    ]
)

def readb64(data):
   encoded_data = data.split(',')[1]
   nparr = np.fromstring(base64.b64decode(encoded_data), np.uint8)
   img = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)
   return img

def analyze_conf_images():
    if len(files) > 0:
        for i in range(len(files)):
            getStaticTestForFiles(f'{IMAGES_BETWEEN_PATHS}{files[i]}')

# Image display callback
@callback(
    Output("output-uploaded-data", "children"),
    [Input("upload-data", "contents")],
)
def update_output(contents):
    print(contents)
    if contents is not None:
        img = readb64(contents)
        # Get Static Test
        getStaticTest(img)

        
        return html.Img(src=contents, style={"width": "50%"})
    