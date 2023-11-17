import dash
from dash import html
import os
from settings import NOT_ANALYZED_IMAGES_PATH

dash.register_page(__name__)

# Non-analyzed Images directory

# List of images in the non-analyzed Images directory
images = os.listdir(NOT_ANALYZED_IMAGES_PATH)

layout = html.Div(
    [
        html.H2('Not Analyzed Images', className="my-2 text-slate-50 text-2xl"),
        html.Div([
            html.Img(src=f'assets/not_analyzed_images/{image}', alt="Rifle", className="w-2/4 object-cover")
            for image in images
        ], className="flex flex-col md:flex-row md:flex-wrap lg:flex-wrap"),
        
    ],
)