from rest_framework import serializers
from rest_extensions.validators import GeoJSONValidator
import geojson

"""
A collection of custom fields.
"""


class GeoJSONField(serializers.Field):
    """
    Serializer and deserialize GeoJSON fields
    """
    default_error_messages = {
        "parse_failed": "Failed to parse GeoJSON field: {detail_string}"
        }

    def __init__(self, geo_type=None, **kwargs):
        self.geo_type = geo_type
        super(GeoJSONField, self).__init__(**kwargs)

    def to_representation(self, obj):

        output_str = geojson.dumps(obj)

        if self.geo_type is not None and obj["type"].lower() != self.geo_type.lower():
            raise serializers.ValidationError("Expected " + self.geo_type + " type but got " + obj["type"])

        return output_str

    def to_internal_value(self, data):
        validator = GeoJSONValidator(self.geo_type)
        obj = validator(data)

        return obj
