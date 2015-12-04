import geojson
import re
from mongoengine.errors import ValidationError
from rest_framework import serializers


def validate_id(value):
    """
    Restrict ids/names to alphanumeric characters plus minus and underscore
    """
    valid = re.match('^[A-Za-z0-9_\-]+$', value)
    if not valid:
        raise serializers.ValidationError("Can only be composed of hyphen (-), underscore (_) and alphanumeric characters.")
    return value


def validate_non_empty_list(value):
    """
    Make sure a list is non-empty
    """
    if len(value) == 0:
        raise serializers.ValidationError("Value cannot be empty list.")
    else:
        return value


def validate_non_zero(value):
    """
    Check a numerical value is non-zero
    """
    if value == 0:
        raise serializers.ValidationError("Value cannot be zero.")
    else:
        return value


class ModelValidator(object):
    def __init__(self, model_class):
        self.model_class = model_class

    def __call__(self, value):
        try:
            self.model_class.objects.get(name=value)
        except (self.model_class.DoesNotExist, ValidationError):
            raise serializers.ValidationError("A valid identifier is required.")
        return value


class GeoJSONValidator(object):
    def __init__(self, geo_type):
        self.geo_type = geo_type

    def __call__(self, value):
        try:
            # Sometimes value is a dict, and sometimes a string
            if type(value) != dict:
                json_dict = geojson.loads(str(value))
            else:
                json_dict = value
        except Exception as e:
            raise serializers.ValidationError('Invalid GeoJSON field: ' + str(e))

        if "type" not in json_dict.keys():
            raise serializers.ValidationError("Missing type field")
        if "coordinates" not in json_dict.keys():
            raise serializers.ValidationError("Missing coordinates field")

        if self.geo_type is not None and json_dict["type"].lower() != self.geo_type.lower():
            raise serializers.ValidationError("Expected " + self.geo_type + " type but got " + json_dict["type"])

        coordinates = json_dict["coordinates"][0]
        if json_dict["type"].lower() == "polygon" and coordinates[0] != coordinates[-1]:
            raise serializers.ValidationError("Coordinates must start and end at the same point.")

        return json_dict
