from typing import Tuple
from geoalchemy2.functions import ST_GeogFromText, ST_DWithin, ST_AsText, ST_Distance
from geoalchemy2.elements import WKTElement
from config import settings

def create_point_wkt(latitude: float, longitude: float) -> str:
    """Создание WKT представления точки для PostGIS"""
    return f"POINT({longitude} {latitude})"

def create_point_geography(latitude: float, longitude: float):
    """Создание Geography объекта для PostGIS"""
    return f"SRID=4326;POINT({longitude} {latitude})"

def parse_coordinates_from_wkt(wkt: str) -> Tuple[float, float]:
    """Парсинг координат из WKT строки"""
    # Формат: POINT(longitude latitude)
    coords = wkt.replace("POINT(", "").replace(")", "").split()
    longitude = float(coords[0])
    latitude = float(coords[1])
    return latitude, longitude

def validate_caspian_coordinates(latitude: float, longitude: float) -> bool:
    """Проверка что координаты находятся в регионе Каспийского моря"""
    return (
        settings.CASPIAN_MIN_LAT <= latitude <= settings.CASPIAN_MAX_LAT and
        settings.CASPIAN_MIN_LON <= longitude <= settings.CASPIAN_MAX_LON
    )

def calculate_bbox_query(min_lat: float, max_lat: float, min_lon: float, max_lon: float):
    """Создание запроса для фильтрации по bounding box"""
    bbox_wkt = f"POLYGON(({min_lon} {min_lat}, {max_lon} {min_lat}, {max_lon} {max_lat}, {min_lon} {max_lat}, {min_lon} {min_lat}))"
    return bbox_wkt