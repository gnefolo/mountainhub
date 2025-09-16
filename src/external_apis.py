"""
Wrapper services for external APIs.

This module defines service classes that encapsulate calls to third‑party
APIs such as Open‑Meteo, Overpass (OpenStreetMap) and others. Each service
provides a clean method for retrieving or transforming data in a format
convenient for the application.
"""

import requests
from typing import Any, Dict, Optional


class WeatherService:
    """
    Service for interacting with the Open‑Meteo Weather API.
    """

    def __init__(self) -> None:
        self.base_url = "https://api.open-meteo.com/v1/forecast"

    def get_weather(self, latitude: float, longitude: float, timezone: str = "auto") -> Optional[Dict[str, Any]]:
        """Get current weather and forecast for a specific location."""
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "timezone": timezone,
            "current": (
                "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,rain,"
                "showers,snowfall,weather_code,cloud_cover,pressure_msl,surface_pressure,"
                "wind_speed_10m,wind_direction_10m,wind_gusts_10m"
            ),
            "hourly": (
                "temperature_2m,relative_humidity_2m,dew_point_2m,apparent_temperature,"
                "precipitation_probability,precipitation,rain,showers,snowfall,snow_depth,"
                "weather_code,pressure_msl,surface_pressure,cloud_cover,cloud_cover_low,"
                "cloud_cover_mid,cloud_cover_high,visibility,wind_speed_10m,wind_direction_10m,"
                "wind_gusts_10m"
            ),
            "daily": (
                "weather_code,temperature_2m_max,temperature_2m_min,apparent_temperature_max,"
                "apparent_temperature_min,sunrise,sunset,precipitation_sum,rain_sum,showers_sum,"
                "snowfall_sum,precipitation_hours,precipitation_probability_max,wind_speed_10m_max,"
                "wind_gusts_10m_max,wind_direction_10m_dominant"
            ),
            "forecast_days": 7,
        }
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as exc:  # pragma: no cover
            print(f"Error fetching weather data: {exc}")
            return None


class TrailService:
    """
    Service for interacting with the OpenStreetMap/Overpass API to get trail data.
    """

    def __init__(self) -> None:
        self.base_url = "https://overpass-api.de/api/interpreter"

    def get_trails_in_area(self, south: float, west: float, north: float, east: float) -> Optional[Dict[str, Any]]:
        """Get hiking trails in a bounding box area."""
        overpass_query = f"""
        [out:json][timeout:25];
        (
          way["highway"="path"]["sac_scale"]({south},{west},{north},{east});
          way["highway"="footway"]["sac_scale"]({south},{west},{north},{east});
          way["highway"="track"]["foot"="yes"]({south},{west},{north},{east});
          way["highway"="path"]["trail_visibility"]({south},{west},{north},{east});
          relation["route"="hiking"]({south},{west},{north},{east});
        );
        out body;
        >;
        out skel qt;
        """
        try:
            response = requests.post(self.base_url, data={"data": overpass_query})
            response.raise_for_status()
            return self._convert_to_geojson(response.json())
        except requests.exceptions.RequestException as exc:  # pragma: no cover
            print(f"Error fetching trail data: {exc}")
            return None

    def get_trail_by_id(self, osm_id: int, osm_type: str = "way") -> Optional[Dict[str, Any]]:
        """Get a specific trail by its OSM ID."""
        overpass_query = f"""
        [out:json][timeout:25];
        {osm_type}(id:{osm_id});
        out body;
        >;
        out skel qt;
        """
        try:
            response = requests.post(self.base_url, data={"data": overpass_query})
            response.raise_for_status()
            return self._convert_to_geojson(response.json())
        except requests.exceptions.RequestException as exc:  # pragma: no cover
            print(f"Error fetching trail data: {exc}")
            return None

    def _convert_to_geojson(self, osm_data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert OSM data to GeoJSON format (simplified)."""
        features = []
        nodes = {node["id"]: node for node in osm_data.get("elements", []) if node.get("type") == "node"}
        for element in osm_data.get("elements", []):
            if element.get("type") == "way" and "nodes" in element:
                coordinates = []
                for node_id in element["nodes"]:
                    if node_id in nodes:
                        coordinates.append([nodes[node_id]["lon"], nodes[node_id]["lat"]])
                if coordinates:
                    properties = element.get("tags", {})
                    properties["id"] = element["id"]
                    properties["type"] = "way"
                    feature = {
                        "type": "Feature",
                        "geometry": {"type": "LineString", "coordinates": coordinates},
                        "properties": properties,
                    }
                    features.append(feature)
        return {"type": "FeatureCollection", "features": features}


class RefugeService:
    """
    Service for interacting with the Overpass API to get mountain refuge data.
    """

    def __init__(self) -> None:
        self.base_url = "https://overpass-api.de/api/interpreter"

    def get_refuges_in_area(self, south: float, west: float, north: float, east: float) -> Optional[Dict[str, Any]]:
        """Get mountain refuges and huts in a bounding box area."""
        overpass_query = f"""
        [out:json][timeout:25];
        (
          node["tourism"="alpine_hut"]({south},{west},{north},{east});
          node["tourism"="wilderness_hut"]({south},{west},{north},{east});
          node["tourism"="hostel"]["mountain"="yes"]({south},{west},{north},{east});
          node["amenity"="shelter"]["shelter_type"="basic_hut"]({south},{west},{north},{east});
        );
        out body;
        """
        try:
            response = requests.post(self.base_url, data={"data": overpass_query})
            response.raise_for_status()
            return self._convert_to_geojson(response.json())
        except requests.exceptions.RequestException as exc:  # pragma: no cover
            print(f"Error fetching refuge data: {exc}")
            return None

    def _convert_to_geojson(self, osm_data: Dict[str, Any]) -> Dict[str, Any]:
        """Convert OSM data to GeoJSON format for refuge nodes."""
        features = []
        for element in osm_data.get("elements", []):
            if element.get("type") == "node":
                properties = element.get("tags", {}).copy()
                properties["id"] = element["id"]
                properties["type"] = "node"
                feature = {
                    "type": "Feature",
                    "geometry": {"type": "Point", "coordinates": [element["lon"], element["lat"]]},
                    "properties": properties,
                }
                features.append(feature)
        return {"type": "FeatureCollection", "features": features}