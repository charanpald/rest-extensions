from rest_extensions import serializers as serializers_ext
from rest_framework import serializers
import unittest

class GeoJSONFieldTestCase(unittest.TestCase):
    def test_to_representation(self):
        field = serializers_ext.GeoJSONField()

        field_data = {"type": "Polygon", "coordinates": [[[0,1],[2,3], [5,6], [0,1]]]}
        serialized_field = '{"type": "Polygon", "coordinates": [[[0, 1], [2, 3], [5, 6], [0, 1]]]}'
        self.assertEquals(field.to_representation(field_data), serialized_field)

        #Let's try a LineString
        field_data = {"type": "LineString", "coordinates": [[[0,1],[2,3], [5,6], [0,1]]]}
        field.to_representation(field_data)

        #Now let's fix the geo-type and check it validates
        field = serializers_ext.GeoJSONField(geo_type="Polygon")
        field_data = {"type": "LineString", "coordinates": [[[0,1],[2,3], [5,6], [0,1]]]}
        self.assertRaises(serializers.ValidationError, field.to_representation, field_data)

        field_data = {"type": "Polygon", "coordinates": [[[0,1],[2,3], [5,6], [0,1]]]}
        self.assertEquals(field.to_representation(field_data), serialized_field)

        #Now test the case where a polygon isn't closed - not sure we care about this
        #Also test when the type is not a valid GeoJSON type
        #field_data = {"type": "Polygon", "coordinates": [[[0,1],[2,3], [5,6], [0,2]]]}
        #print(field.to_representation(field_data))

    def test_to_internal_value(self):
        field = serializers_ext.GeoJSONField()

        field_data = {"type": "Polygon", "coordinates": [[[0,1],[2,3], [5,6], [0,1]]]}
        serialized_field = '{"type": "Polygon", "coordinates": [[[0, 1], [2, 3], [5, 6], [0, 1]]]}'

        self.assertEquals(field.to_internal_value(serialized_field), field_data)

        field_data = {"type": "Point", "coordinates": [0.5, 1.2]}
        serialized_field = '{"type": "Point", "coordinates": [0.5, 1.2]}'
        self.assertEquals(field.to_internal_value(serialized_field), field_data)

if __name__ == '__main__':
    unittest.main()