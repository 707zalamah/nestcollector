"""
Module containing the OSMElements class, which is used to parse OSM elements from the Overpass API.
"""

from shapely.geometry import MultiPolygon, Polygon
from typing import List, Mapping, Optional


class Node:
    """
    Represents an OSM node.

    Attributes:
        type (str): The type of the element.
        id (int): The ID of the element.
        lat (float): The latitude of the node.
        lon (float): The longitude of the node.
        tags (Optional[dict]): The tags of the element.
    """

    def __init__(self, type: str, id: int, lat: float, lon: float, tags: Optional[dict] = None) -> None:
        """
        Initializes the Node class.

        Args:
            type (str): The type of the element.
            id (int): The ID of the element.
            lat (float): The latitude of the node.
            lon (float): The longitude of the node.
            tags (Optional[dict]): The tags of the element.
        """
        self.type = type
        self.id = id
        self.lat = lat
        self.lon = lon
        self.tags = tags

    def __eq__(self, other: 'Node') -> bool:
        """
        Checks if two nodes are equal, by comparing their IDs.

        Args:
            other (Node): The other node.
        
        Returns:
            bool: True if the nodes are equal, False otherwise.
        """
        return isinstance(other, Node) and self.id == other.id

    def __str__(self) -> str:
        """
        Returns a string representation of the node.

        Returns:
            str: The string representation of the node.
        """
        return f'Node(id={self.id}, lat={self.lat}, lon={self.lon}, tags={self.tags})'


class Way:
    """
    Represents an OSM way.

    Attributes:
        type (str): The type of the element.
        id (int): The ID of the element.
        nodes (List[int]): The nodes of the way.
        tags (Optional[dict]): The tags of the element.
        name (Optional[str]): The name of the way.
        polygon (Optional[Polygon]): The polygon of the way.
    """

    def __init__(self, type: str, id: int, nodes: List[int], tags: Optional[dict] = None) -> None:
        """
        Initializes the Way class.

        Args:
            type (str): The type of the element.
            id (int): The ID of the element.
            nodes (List[int]): The nodes of the way.
            tags (Optional[dict]): The tags of the element.
        """
        self.type = type
        self.id = id
        self.nodes = nodes
        self.tags = tags
        self.name = tags['name'] if tags and 'name' in tags else None
        self.polygon = None

    def build_polygon(self, nodes: Mapping[int, Node]) -> Polygon:
        """
        Builds a polygon from the way's nodes.

        Args:
            nodes (Mapping[int, Node]): The nodes of the way.

        Returns:
            Polygon: The polygon of the way.
        """
        polygon = Polygon([(nodes[node].lat, nodes[node].lon) for node in self.nodes])
        return polygon

    def __eq__(self, other: 'Way') -> bool:
        """
        Checks if two ways are equal, by comparing their IDs.

        Args:
            other (Way): The other way.

        Returns:
            bool: True if the ways are equal, False otherwise.
        """
        return isinstance(other, Way) and self.id == other.id

    def __str__(self) -> str:
        """
        Returns a string representation of the way.

        Returns:
            str: The string representation of the way.
        """
        return f'Way(id={self.id}, nodes={self.nodes}, tags={self.tags})'


class Relation:
    """
    Represents an OSM relation.

    Attributes:
        type (str): The type of the element.
        id (int): The ID of the element.
        members (List[dict]): The members of the relation.
        tags (Optional[dict]): The tags of the element.
        name (Optional[str]): The name of the relation.
        multipolygon (Optional[MultiPolygon]): The multipolygon of the relation.
    """

    def __init__(self, type: str, id: int, members: List[dict], tags: Optional[dict] = None) -> None:
        """
        Initializes the Relation class.

        Args:
            type (str): The type of the element.
            id (int): The ID of the element.
            members (List[dict]): The members of the relation.
            tags (Optional[dict]): The tags of the element.
        """
        self.type = type
        self.id = id
        self.members = members
        self.tags = tags
        self.name = tags['name'] if tags and 'name' in tags else None
        self.multipolygon = None

    def build_multipolygon(self, ways: Mapping[int, Way]) -> MultiPolygon:
        """
        Builds a multipolygon from the relation's ways.

        Args:
            ways (Mapping[int, Way]): The ways of the relation.

        Returns:
            MultiPolygon: The multipolygon of the relation.
        """
        polygons = []
        for member in self.members:
            if member['type'] == 'way':
                way = ways[member['ref']]
                if way.polygon is None:
                    way.polygon = way.build_polygon(ways)
                polygons.append(way.polygon)
        multipolygon = MultiPolygon(polygons)
        return multipolygon

    def __eq__(self, other: 'Relation') -> bool:
        """
        Checks if two relations are equal, by comparing their IDs.

        Args:
            other (Relation): The other relation.
        """
        return isinstance(other, Relation) and self.id == other.id

    def __str__(self) -> str:
        """
        Returns a string representation of the relation.

        Returns:
            str: The string representation of the relation.
        """
        return f'Relation(id={self.id}, members={self.members}, tags={self.tags})'
