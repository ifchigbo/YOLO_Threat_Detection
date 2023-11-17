import dash
from flask import Flask, Response
from dash import Dash, html, dcc, callback, Output, Input
from dash_iconify import DashIconify
from tfile.validator import getWebCamCap
from tfile.getCameraFeed import getRecordedVideoFeed

server = Flask(__name__)
print(dash.page_registry.values())
app = Dash(server=server, url_base_pathname='/', use_pages=True, external_scripts=["https://cdn.tailwindcss.com"])

app.scripts.config.serve_locally = True

app.layout = html.Div(
    [
        html.Header(
            html.Div(
                html.Nav(
                    [
                        # Weapons Application Icon with hidden menu button
                        # Menu hamburger button active with mobile view
                        html.Ul(
                            [
                                html.Li(dcc.Link("WA", href="/"), className="text-white font-bold"),
                                html.Li(
                                    children=DashIconify(
                                        icon="ci:hamburger-md",
                                        width=30,
                                        color="#FFFFFF",
                                        id="ham-close-button"
                                    ),
                                    id="menu-button",
                                    className="md:hidden lg:hidden"
                                ),
                            ],
                            className="flex flex-row justify-between md:basis-1/2 lg:basis-1/2",
                        ),
                        # Webcam Icon on Nav bar at the center of the page
                        html.Ul(html.Li(dcc.Link(DashIconify(
                                        icon="ri:webcam-line",
                                        width=30,
                                        color="#FFFFFF",
                                        id="webcam-button"
                                    ), href="/webcam"), className="text-white font-bold"),),
                        # Home, upload and video links on the right side of the Nav bar
                        html.Ul(
                            [
                                html.Li(
                                    dcc.Link(
                                        f"{page['name']}",
                                        href=page["relative_path"],
                                    ),
                                    className="my-2 md:text-white lg:text-white"
                                )
                                # All dash pages are housed in the pages folder
                                # Can be accessed with dash.page_registry.values()
                                for page in dash.page_registry.values() if page['name'].lower() in ['home', 'upload', 'video']
                            ],
                            className="hidden",
                            id="menu-list"
                        ),
                    ],
                    className="w-full flex flex-col md:flex-row md:justify-between lg:flex-row md:items-center lg:items-center",
                ),
                className="container px-4 mx-auto",
            ),
            className="bg-sky-900 min-h-16 shadow-sm sticky top-0 py-2 z-10",
        ),
        # Main container used by all the pages
        html.Main(
            [
                dash.page_container,
            ],
            className="container mx-auto px-4",
        ),
    ],
    className="flex flex-col w-full max-w-full min-h-screen bg-sky-950 text-white box-border",
)

# Open and Close Hamburger Menu Callback
@callback(
    Output('menu-list', 'className'),
    Output('ham-close-button', 'icon'),
    Input('menu-button', 'n_clicks')
)
def update_menu(n_click):
    click = "hidden md:flex lg:flex md:basis-1/2 lg:basis-1/2 md:justify-end lg:justify-end md:space-x-4 lg:space-x-4"
    close_child = "ci:hamburger-md",
    if n_click and n_click % 2 != 0:
        close_child = "jam:close",
        click = "grid gap-y-3 justify-items-end text-white"
    return click, close_child[0]

# Webcam Feed
@server.route('/webcam-feed')
def layout():
    return Response(getWebCamCap(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Video feed with the name of the video <video> as input
@server.route('/video-feed/<video>', methods=['GET'])
def layout_video(video):
    return Response(getRecordedVideoFeed(video), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run_server(debug=True, port=3000)


# Ending the main.py process