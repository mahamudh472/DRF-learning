To build a solid foundation with Django REST Framework (DRF), here's a structured module to guide you through your learning journey. This will cover the basics and gradually introduce more advanced topics. Follow this module step-by-step, and you’ll have a good grasp of DRF by the end.

---

## **Module 1: Getting Started with Django REST Framework**

### **1.1. Setup Django and Django REST Framework**
- **Goal**: Install Django and Django REST Framework (DRF) and configure your project to use DRF.

**Tasks:**
- Install Django and DRF using `pip`:
  ```bash
  pip install django djangorestframework
  ```
- Create a Django project and a new app:
  ```bash
  django-admin startproject myproject
  cd myproject
  python manage.py startapp myapp
  ```
- Add `'rest_framework'` to `INSTALLED_APPS` in `settings.py`.

### **1.2. Creating a Simple API**
- **Goal**: Learn the basics of creating an API endpoint.

**Tasks:**
- Create a model in `myapp/models.py`:
  ```python
  from django.db import models

  class Book(models.Model):
      title = models.CharField(max_length=100)
      author = models.CharField(max_length=100)
      published_date = models.DateField()
      price = models.DecimalField(max_digits=5, decimal_places=2)
  ```
- Run `python manage.py makemigrations` and `python manage.py migrate` to create the database table.
- Create a **serializer** in `myapp/serializers.py`:
  ```python
  from rest_framework import serializers
  from .models import Book

  class BookSerializer(serializers.ModelSerializer):
      class Meta:
          model = Book
          fields = ['id', 'title', 'author', 'published_date', 'price']
  ```
- Create a **view** to handle GET and POST requests in `myapp/views.py`:
  ```python
  from rest_framework.views import APIView
  from rest_framework.response import Response
  from rest_framework import status
  from .models import Book
  from .serializers import BookSerializer

  class BookList(APIView):
      def get(self, request):
          books = Book.objects.all()
          serializer = BookSerializer(books, many=True)
          return Response(serializer.data)

      def post(self, request):
          serializer = BookSerializer(data=request.data)
          if serializer.is_valid():
              serializer.save()
              return Response(serializer.data, status=status.HTTP_201_CREATED)
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  ```
- Configure URLs in `myapp/urls.py`:
  ```python
  from django.urls import path
  from .views import BookList

  urlpatterns = [
      path('books/', BookList.as_view(), name='book-list'),
  ]
  ```
- Include the app’s URLs in the project’s `urls.py`:
  ```python
  from django.urls import path, include

  urlpatterns = [
      path('api/', include('myapp.urls')),
  ]
  ```
- Test the API by running the development server:
  ```bash
  python manage.py runserver
  ```
- Use Postman or Curl to test the API. For example, get all books:
  ```bash
  curl http://127.0.0.1:8000/api/books/
  ```

### **1.3. Using ViewSets and Routers**
- **Goal**: Learn how to simplify views using `ViewSet` and DRF's `DefaultRouter`.

**Tasks:**
- Update `views.py` to use a `ModelViewSet`:
  ```python
  from rest_framework import viewsets
  from .models import Book
  from .serializers import BookSerializer

  class BookViewSet(viewsets.ModelViewSet):
      queryset = Book.objects.all()
      serializer_class = BookSerializer
  ```
- Update `urls.py` to use `DefaultRouter`:
  ```python
  from rest_framework.routers import DefaultRouter
  from .views import BookViewSet

  router = DefaultRouter()
  router.register(r'books', BookViewSet)

  urlpatterns = router.urls
  ```
- Test the new endpoints using the same `/api/books/` route.

### **1.4. Authentication and Permissions**
- **Goal**: Implement basic authentication and permission handling.

**Tasks:**
- In `settings.py`, set up default permissions and authentication:
  ```python
  REST_FRAMEWORK = {
      'DEFAULT_PERMISSION_CLASSES': [
          'rest_framework.permissions.IsAuthenticated',
      ],
  }
  ```
- Add login functionality to the API by enabling Django’s built-in login:
  ```python
  urlpatterns = [
      path('api/', include('myapp.urls')),
      path('api-auth/', include('rest_framework.urls')),
  ]
  ```
- Add user authentication and permissions in `views.py`:
  ```python
  from rest_framework.permissions import IsAuthenticated

  class BookViewSet(viewsets.ModelViewSet):
      queryset = Book.objects.all()
      serializer_class = BookSerializer
      permission_classes = [IsAuthenticated]
  ```
- Test the authenticated API by logging in via `/api-auth/login/`.

### **1.5. Basic Token Authentication**
- **Goal**: Learn how to implement token-based authentication using `SimpleJWT`.

**Tasks:**
- Install `djangorestframework-simplejwt`:
  ```bash
  pip install djangorestframework-simplejwt
  ```
- Update `settings.py` to include JWT authentication:
  ```python
  REST_FRAMEWORK = {
      'DEFAULT_AUTHENTICATION_CLASSES': [
          'rest_framework_simplejwt.authentication.JWTAuthentication',
      ],
  }
  ```
- Update `urls.py` to include the token routes:
  ```python
  from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

  urlpatterns = [
      path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
      path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
  ]
  ```
- Test by obtaining a token via POST to `/api/token/` and use it in subsequent requests.

---

## **Module 2: Intermediate Topics**

### **2.1. Pagination, Filtering, and Ordering**
- **Goal**: Add pagination and filtering options to your API.

**Tasks:**
- Enable pagination in `settings.py`:
  ```python
  REST_FRAMEWORK = {
      'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
      'PAGE_SIZE': 10,
  }
  ```
- Use Django filters for filtering and ordering:
  ```bash
  pip install django-filter
  ```
- Add filter backends to the `settings.py`:
  ```python
  REST_FRAMEWORK = {
      'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
  }
  ```
- Update your `views.py`:
  ```python
  from django_filters.rest_framework import DjangoFilterBackend
  from rest_framework import filters

  class BookViewSet(viewsets.ModelViewSet):
      queryset = Book.objects.all()
      serializer_class = BookSerializer
      filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
      filterset_fields = ['author', 'published_date']
      ordering_fields = ['title', 'price']
  ```

---

## **Module 3: Advanced Topics**

### **3.1. Custom Permissions**
- **Goal**: Create custom permission classes to protect your API.

**Tasks:**
- Define a custom permission in `myapp/permissions.py`:
  ```python
  from rest_framework import permissions

  class IsAdminOrReadOnly(permissions.BasePermission):
      def has_permission(self, request, view):
          if request.method in permissions.SAFE_METHODS:
              return True
          return request.user and request.user.is_staff
  ```
- Use this permission in your `views.py`:
  ```python
  from .permissions import IsAdminOrReadOnly

  class BookViewSet(viewsets.ModelViewSet):
      queryset = Book.objects.all()
      serializer_class = BookSerializer
      permission_classes = [IsAdminOrReadOnly]
  ```

### **3.2. Custom Throttling**
- **Goal**: Implement rate-limiting to control the number of API requests.

**Tasks:**
- Define custom throttling in `settings.py`:
  ```python
  REST_FRAMEWORK = {
      'DEFAULT_THROTTLE_CLASSES': [
          'rest_framework.throttling.UserRateThrottle',
      ],
      'DEFAULT_THROTTLE_RATES': {
          'user': '5/minute',
      },
  }
  ```

---

Following this module step-by-step will help you build a strong foundation in Django REST Framework. Let me know if you need further clarifications or want to dive deeper into any particular topic!