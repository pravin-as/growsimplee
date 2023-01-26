from django.http import JsonResponse
from .algorithm import master
from .serializers import ProductSerializer
from rest_framework import mixins, generics, status, response
from .models import Product

# Create your views here.

def home(request):
    a = master()
    return JsonResponse({"a" : a})

class ProductView(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def post(self, request):
        serializer = self.get_serializer(data = request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            return response.Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)