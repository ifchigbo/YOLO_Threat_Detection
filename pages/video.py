import dash
from dash import html, dcc, callback, Input, Output
import os
from dash.exceptions import PreventUpdate
from settings import VIDEOS_DIRECTORY_PATH

dash.register_page(__name__)

videos = os.listdir(VIDEOS_DIRECTORY_PATH)
print(videos)

layout = html.Div(
    [
        html.H2('Videos', className="my-2 text-slate-50 text-2xl"),
        html.Div([
            dcc.Dropdown(videos, id='video-file', className="bg-gray-50 text-gray-900")
        ]),
        html.Div(id='video-output'),
    ],
)

# Video Display Callback
@callback(
    Output('video-output', 'children'),
    Input('video-file', 'value')
)
def process_video(video_file):
    if not video_file:
        raise PreventUpdate()
    return html.Img(src=f'/video-feed/{video_file}')