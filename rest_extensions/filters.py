from dateutil import parser

"""
A set of classes to perform filtering on MongoEngine documents
"""


class AbstractFilter(object):
    pass


class BooleanFilter(AbstractFilter):
    def __init__(self, name, lookup_type="exact"):
        self.name = name
        self.lookup_type = lookup_type

    def to_representation(self, value):
        if value in ["True", "true"]:
            return True
        elif value in ["False", "false"]:
            return False
        else:
            raise ValueError("Invalid boolean: " + value)


class DateFilter(AbstractFilter):
    def __init__(self, name, lookup_type="exact"):
        self.name = name
        self.lookup_type = lookup_type

    def to_representation(self, value):
        return parser.parse(value, dayfirst=True)


class IntegerFilter(AbstractFilter):
    def __init__(self, name, lookup_type="exact"):
        self.name = name
        self.lookup_type = lookup_type

    def to_representation(self, value):
        return int(value)


class StringFilter(AbstractFilter):
    def __init__(self, name, lookup_type="exact"):
        self.name = name
        self.lookup_type = lookup_type

    def to_representation(self, value):
        return str(value)


class FilterSet(object):
    def __init__(self, user=None, permission=None):
        """
        Create a new object with an optional user to check permissions.
        """
        self.user = user
        self.permission = permission

    def get_fields(self):
        fields = {}
        attribute_names = dir(self)

        for attribute_name in attribute_names:
            attribute = getattr(self, attribute_name)
            if isinstance(attribute, AbstractFilter):
                fields[attribute_name] = attribute

        return fields

    def filter(self, queryset, query_params):
        """
        Given the input queryset and query_params, filter out the objects using
        the input query to return a QuerySet object. This is just a call to
        Mongoengine. If the object also has a user and permissions, then returns
        a *list* of filtered objects.
        """
        fields = self.get_fields()

        query_dict = {}
        for key, value in query_params.iteritems():
            if fields.has_key(key):
                try:
                    field = fields[key]
                    if field.lookup_type in ["gte", "lte"]:
                        query_dict[field.name + "__" + field.lookup_type] = field.to_representation(value)
                    elif field.lookup_type == "exact":
                        query_dict[field.name] = field.to_representation(value)
                    elif field.lookup_type == "contains":
                        query_dict[field.name + "__" + field.lookup_type] = field.to_representation(value)
                except (TypeError, ValueError):
                    pass

        queryset = queryset.filter(**query_dict)

        if self.user != None:
            filtered_list = []

            for item in queryset:
                if self.user.has_perm(self.permission, item):
                    filtered_list.append(item)

            return filtered_list
        else:
            return queryset
