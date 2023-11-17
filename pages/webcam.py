import dash, cv2 as cv
from tfile.validator import closeWebcam
from dash import html, dcc, callback, Input, Output
from dash.exceptions import PreventUpdate

dash.register_page(__name__)

layout = html.Div(
    [
        html.Div([
            html.Button('Start', className="bg-sky-500 h-10 px-6 font-semibold rounded-md text-white", id="start-webcam"),
            html.Button('Stop', className="bg-red-500 h-10 px-6 font-semibold rounded-md text-white", id="stop-webcam")
        ], className="flex justify-center space-x-3 py-3"),
        dcc.Loading(html.Div(
        ), id="display-feed"),
    ]
)

# Webcam Display Callback
@callback(
    Output('display-feed', 'children'),
    Input('start-webcam', 'n_clicks'),
    Input('stop-webcam', 'n_clicks')
)
def update_feed(start_nclick, stop_nclick):
    if start_nclick is None and stop_nclick is None:
        raise PreventUpdate
    else:
        if start_nclick:
            return html.Img(src='/webcam-feed')
        else:
            cap = cv.VideoCapture(0)
            cap.release()