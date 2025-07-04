# Brief

- Download Christchurch's GTFS feed
- Snap bus shapes to OSM roads
    - Keyword is 'map matching'
    - Use a local Valhalla instance
- Aim to have an accurate and reproducible output
    - Output should be a new GTFS feed with improved shapes
        - Shapes: paths the public transport vehicles are scheduled to follow
            - Encoded in the `shapes.txt` file in GTFS 
