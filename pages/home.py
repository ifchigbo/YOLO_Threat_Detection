import dash, os, settings
from dash import html, dcc
from dash_iconify import DashIconify


dash.register_page(__name__, path="/")

# List of Analyzed Images
analyzed_images = os.listdir(settings.ANALYZED_IMAGES_PATH)
# List of Non Analyzed Images
not_analyzed_images = os.listdir(settings.NOT_ANALYZED_IMAGES_PATH)

images_greater_70 = os.listdir(settings.IMAGES_GREATER_70_PATH)

images_between_values = os.listdir(settings.IMAGES_BETWEEN_PATHS)


report_statistics = [
    {
        "count": len(analyzed_images) + len(not_analyzed_images),
        "icon_color": "#DC143C",
        "icon": "solar:danger-triangle-bold",
        "title": "Total Reports",
        "link": "/",
    },
    {
        "count": len(not_analyzed_images),
        "icon_color": "orange",
        "icon": "solar:danger-triangle-bold",
        "title": "Non-Analyzed Reports",
        "link": "/non-analyzed-report",
    },
    {
        "count": len(analyzed_images),
        "icon_color": "green",
        "icon": "solar:danger-triangle-bold",
        "title": "Analyzed Reports",
        "link": "/analyzed-report",
    },
    {
        "count": len(images_greater_70),
        "icon_color": "#3BB9FF",
        "icon": "solar:danger-triangle-bold",
        "title": "Reports with confidence greater than 70%",
        "link": "/",
    },
    {
        "count": len(images_between_values),
        "icon_color": "#3BB9FF",
        "icon": "solar:danger-triangle-bold",
        "title": "Reports with confidence between 45 and 69%",
        "link": "/",
    },
]



layout = html.Div(
    children=[
        html.H2("Report Statistics", className="my-2 text-slate-50 text-xl"),
        html.Div(
            [
                dcc.Link(
                    html.Div(
                        [
                            html.Article(
                                [
                                    html.Div(
                                        DashIconify(
                                            icon=report["icon"],
                                            width=80,
                                            color=report["icon_color"],
                                        )
                                    ),
                                    html.Div(
                                        [
                                            html.H2(
                                                report["count"],
                                                className="font-bold text-5xl text-slate-50",
                                            ),
                                            html.Div(
                                                html.P(report["title"]),
                                                className="text-right text-slate-100",
                                            ),
                                        ],
                                        className="flex flex-col items-end space-y-2",
                                    ),
                                ],
                                className="flex flex-row justify-between",
                            )
                        ],
                        className="bg-sky-900 border-slate-700 shadow-md border-b rounded-xl p-4 pb-6 space-y-6 mb-2",
                    ),
                    href=report["link"],
                    className="w-full md:px-2 md:w-1/3 lg:w-1/3",
                )
                for report in report_statistics
            ],
            className="flex flex-col md:flex-row md:flex-wrap lg:flex-wrap",
        ),
        html.Div([
            html.H2("Report Statistics Graph", className="my-2 text-slate-50 text-xl"),
            html.Div([
                dcc.Graph(id="report-stats-graph-1", figure={'layout': {'plot_bgcolor': '#000', 'paper_bgcolor': '#000'}}),
                dcc.Graph(id="report-stats-graph-2", figure={'layout': {'plot_bgcolor': '#000', 'paper_bgcolor': '#000'}}),
            ], className="flex flex-col space-y-3")
        ])
    ]
)
