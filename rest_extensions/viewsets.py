from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_extensions.utils import get_model_object


class ReadOnlyModelViewSet(ViewSet):
    """
    The viewset for a read-only model. Must specify model_class and serializer_class, and can supply any other
    properties allowable for ViewSets.
    """

    def get_queryset(self):
        if hasattr(self, "order_key"):
            return self.model_class.objects.order_by(self.order_key)
        else:
            return self.model_class.objects.all()

    def list(self, request, format=None):
        instances = self.get_queryset()
        try:
            serializer = self.list_serializer_class(instances, many=True)
        except:
            serializer = self.serializer_class(instances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk, format=None):
        instance = get_model_object(self.model_class, pk)
        serializer = self.serializer_class(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ModelViewSet(ReadOnlyModelViewSet):
    """
    The viewset for a writable model. Must specify model_class and serializer_class, and can supply any other
    properties allowable for ViewSets.
    """

    def create(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk, format=None):
        instance = get_model_object(self.model_class, pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, pk, format=None):
        instance = get_model_object(self.model_class, pk)
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.fields["name"].read_only = True

        if serializer.is_valid():
            instance = serializer.save()
            instance.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)
