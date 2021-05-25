import flask

from bokeh.embed import json_item
from bokeh.models import HoverTool
from bokeh.models.tools import LassoSelectTool
from umap import UMAP as UMAPBase
from umap.plot import interactive

def get_hovertool():
    return HoverTool(
        tooltips=f"""
        <div>
            <div>
                <img
                    src="{flask.request.host_url}/file/image/@file" height="128" alt="@name" width="128"
                    style="float: left; margin: 0px 15px 15px 0px;"
                    border="2"
                ></img>
            </div>
            <div>
                <span style="font-size: 10px; font-weight: bold;">@name</span>
                <span style="font-size: 10px; color: #966;">[$index]</span>
            </div>
            <div>
                <span style="font-size: 9px; color: #966;">(@x, @y)</span>
            </div>
            <div>
                <span style="font-size: 9px; color: #966;">@file</span>
            </div>
            <div>
                <span style="font-size: 9px; color: #966;">Identity: @class</span>
            </div>
            <div>
                <span style="font-size: 9px; color: #966;">Probability: @probability</span>
            </div>
            <div>
                <span style="font-size: 9px; color: #966;">Outlier: @outlier</span>
            </div>
        </div>
        """
    )

class UMAP:
    def visualise(self, data):
        mapper = UMAPBase()
        mapper.embedding_ = data[["x", "y"]].values
        p = interactive(mapper, labels = data["class"], hover_data = data, point_size = 5, interactive_text_search = False)
        del p.tools[len(p.tools)-1]
        p.add_tools(get_hovertool())
        p.add_tools(LassoSelectTool())
        p_json = json_item(p)
        return p_json
        