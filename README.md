# metro-map-matching

A mini-project to explore [Valhalla](https://valhalla.github.io/valhalla/) and its [map matching APIs](https://valhalla.github.io/valhalla/api/map-matching/api-reference/) in order to correct Christchurch Metro's static GTFS shapes.

The static GTFS shapes were likely derived from existing GPS route data and often do not adhere directly to roads, which map matching (or [Snap to Roads](https://developers.google.com/maps/documentation/roads/snap)) aims to solve. In the example below, the blue line is the existing shape, and the red line is the map matched shape:

![Example of map matching, blue line is the existing shape, red line is map matched shape](example.png)

This code could be extended with minimal effort to work with other transport organisations' GTFS feeds.

## Brief

A rough outline of the project:

- Download Christchurch's GTFS feed
- Snap bus shapes to OSM roads
    - Use a local Valhalla instance
- Aim to have an accurate and reproducible output
    - Output should be a new GTFS feed with improved shapes
        - Shapes: paths the public transport vehicles are scheduled to follow
            - Encoded in the `shapes.txt` file in GTFS
        - Reproduce a gtfs.zip

## Running the project

This project has several prerequisites:

- `.env` file with the following environment variables set:
    ```
    OCP_APIM_SUBSCRIPTION_KEY=<Christchurch Metro API key>
    GTFS_ZIP_URL=<URL for the GTFS zip file>
    VALHALLA_URL=<instance of Valhalla>
    ```

- A running [Valhalla](https://valhalla.github.io/valhalla/) server. For small, test queries the public instance can be used: https://valhalla1.openstreetmap.de/trace_attributes but you may be subject to rate limiting with larger or repeated queries. The easiest way to self-host Valhalla is to use Docker and follow the instructions here: https://github.com/nilsnolde/docker-valhalla.
