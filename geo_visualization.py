import pandas as pd
import folium
import branca.colormap as bcm


def create_folium_colormap(data: pd.DataFrame, criterion: str, colors: list[str]) -> bcm.LinearColormap:
    """
    Create a folium linear colormap

    :param data: a pandas DataFrame object
    :param criterion: a column name of the DataFrame used for visualization. This should be a numeric value.
    :param colors: gradient colors
    """
    min_rate = data[criterion].min()
    max_rate = data[criterion].max()

    return bcm.LinearColormap(
        colors=colors,
        vmin=min_rate,
        vmax=max_rate,
        caption=criterion.replace('_', ' ')
    )


def draw_circle_marker_map(data: pd.DataFrame,
                           color_feature: str,
                           colormap: bcm.ColorMap,
                           coords: list[float],
                           marker_radius: float,
                           marker_border_color: str,
                           marker_border_width: int,
                           marker_fill_opacity: float) -> folium.Map:
    """
    :param data: a pandas DataFrame object
    :param color_feature: a column name of the DataFrame used for visualization
    :param colormap: a ColorMap object
    :param coords: coordinate values, ex [47.6062, -122.3321] for Seattle, WA
    :param marker_radius: a circle marker radius
    :param marker_border_color: a circle marker border color
    :param marker_border_width: a circle marker border width
    :param marker_fill_opacity: a circle marker fill color opacity

    :return: a complete folium.Map object
    """

    folium_map = folium.Map(location=coords, zoom_start=11)

    # Add listings to the map
    for index, row in data.iterrows():
        fill_color = colormap(row[color_feature])
        folium.CircleMarker(
            location=(row['latitude'], row['longitude']),
            radius=marker_radius,
            color=marker_border_color,
            weight=marker_border_width,
            fill=True,
            fill_color=fill_color,
            fill_opacity=marker_fill_opacity
        ).add_to(folium_map)

    # Add the colormap legend to the map
    colormap.add_to(folium_map)
    return folium_map
