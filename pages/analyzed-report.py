import dash
from dash import html
import os
from settings import ANALYZED_IMAGES_PATH

dash.register_page(__name__)

# List of the Images in the analyzed directory
images = os.listdir(ANALYZED_IMAGES_PATH)

layout = html.Div(
    [
        html.H2('Analyzed Images', className="my-2 text-slate-50 text-2xl"),
        html.Div([
            html.Img(src=f'assets/analyzed_images/{image}', alt="Rifle", className="w-2/4 object-cover")
            for image in images
        ], className="flex flex-col md:flex-row md:flex-wrap lg:flex-wrap"),
    ],
)