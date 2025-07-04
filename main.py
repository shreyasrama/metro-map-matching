import requests
import os
import logging
from io import BytesIO
from dotenv import load_dotenv
import zipfile

import pandas as pd

import csv
import json
import folium
import polyline

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Download latest GTFS zip file
zip_headers = {
  'Cache-Control': 'no-cache',
  'Ocp-Apim-Subscription-Key': os.getenv('OCP_APIM_SUBSCRIPTION_KEY')
}

logging.info('Retrieving latest gtfs.zip from Metro')
response = requests.get(
  url=os.getenv('GTFS_ZIP_URL'),
  headers=zip_headers,
  stream=True
)

response.raise_for_status()
gtfs_zip = BytesIO(response.content)

# Unzip to gtfs/ and remove zip file
logging.info('Unzipping to gtfs/')
with zipfile.ZipFile(gtfs_zip, 'r') as zf:
    zf.extractall("gtfs")

# Read shapes.txt into dataframe
shapes_df = pd.read_csv('gtfs/shapes.txt')
grouped_shapes = shapes_df.groupby('shape_id')

# Create base map
m = folium.Map(location=[shapes_df['shape_pt_lat'].mean(), shapes_df['shape_pt_lon'].mean()], zoom_start=12)

# Add each shape as a PolyLine
logging.info('Plotting initial PolyLines')
for shape_id, group in grouped_shapes:
    points = list(zip(group['shape_pt_lat'], group['shape_pt_lon']))
    folium.PolyLine(points, color="blue", weight=2.5, opacity=1).add_to(m)

# Correcting code ---

# Open uncorrected shapes and construct JSON to use with Valhalla map matching API

# TODO: fix
# with open('gtfs/shapes.txt', newline='') as csvfile:
#     reader = csv.DictReader(csvfile)
#     points = []

#     for row in reader:
#         points.append({
#             "lat": float(row["shape_pt_lat"]),
#             "lon": float(row["shape_pt_lon"]),
#             "type": "via"
#         })
#     if points:
#         points[0]["type"] = "break"
#         points[-1]["type"] = "break"

# trace_route_json = {
#     "shape": points,
#     "costing": "auto",
#     "shape_match": "map_snap"
# }

# with open('shapes.json', "w") as f:
#     json.dump(trace_route_json, f, indent=2)

# Save map as HTML
logging.info('Saving to gtfs_corrected_shapes.html')
m.save('gtfs_corrected_shapes.html')
