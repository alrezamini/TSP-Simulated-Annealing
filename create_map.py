import folium

def c_map(lst,cord,html_name):
    mp = folium.Map(location = [32.4279,53.6880],zoom_start = 5)
    for x in lst:
        folium.CircleMarker([x["lat"],x["lng"]],radius=2,color='blue',fill=True,).add_to(mp)
    folium.PolyLine(cord,color='blue').add_to(mp)
    mp.save(f"{html_name}.html")