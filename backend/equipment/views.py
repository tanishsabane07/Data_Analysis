"""
API Views for Equipment Data Management.
"""

from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from .models import Dataset, EquipmentRecord
from .serializers import DatasetSerializer, DatasetDetailSerializer, UserSerializer
from .utils import parse_csv, validate_csv, calculate_summary, prepare_records
from .pdf_generator import generate_equipment_report


class CSVUploadView(APIView):
    """
    Upload a CSV file containing equipment data.
    
    POST /api/upload/
    - Parses CSV file
    - Validates columns
    - Calculates summary statistics
    - Stores dataset and records
    - Returns summary data
    """
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [AllowAny]
    
    def post(self, request):
        if 'file' not in request.FILES:
            return Response(
                {'error': 'No file provided. Please upload a CSV file.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        file = request.FILES['file']
        
        # Validate file extension
        if not file.name.endswith('.csv'):
            return Response(
                {'error': 'Invalid file type. Please upload a CSV file.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Read and parse CSV
            file_content = file.read().decode('utf-8')
            df = parse_csv(file_content)
            
            # Validate CSV structure
            is_valid, error_msg = validate_csv(df)
            if not is_valid:
                return Response(
                    {'error': error_msg},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Calculate summary statistics
            summary = calculate_summary(df)
            
            # Create dataset
            user = request.user if request.user.is_authenticated else None
            dataset = Dataset.objects.create(
                user=user,
                filename=file.name,
                total_count=summary['total_count'],
                avg_flowrate=summary['avg_flowrate'],
                avg_pressure=summary['avg_pressure'],
                avg_temperature=summary['avg_temperature'],
                type_distribution=summary['type_distribution']
            )
            
            # Create equipment records
            records = prepare_records(df, dataset)
            EquipmentRecord.objects.bulk_create(records)
            
            # Cleanup old datasets (keep only last 5)
            Dataset.cleanup_old_datasets(user=user, keep=5)
            
            # Return response
            serializer = DatasetDetailSerializer(dataset)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
            
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': f'An unexpected error occurred: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DatasetSummaryView(APIView):
    """
    Get summary statistics for a specific dataset.
    
    GET /api/summary/<id>/
    """
    permission_classes = [AllowAny]
    
    def get(self, request, pk):
        try:
            dataset = Dataset.objects.get(pk=pk)
            serializer = DatasetSerializer(dataset)
            return Response(serializer.data)
        except Dataset.DoesNotExist:
            return Response(
                {'error': 'Dataset not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class DatasetDataView(APIView):
    """
    Get all equipment records for a specific dataset.
    
    GET /api/data/<id>/
    """
    permission_classes = [AllowAny]
    
    def get(self, request, pk):
        try:
            dataset = Dataset.objects.get(pk=pk)
            serializer = DatasetDetailSerializer(dataset)
            return Response(serializer.data)
        except Dataset.DoesNotExist:
            return Response(
                {'error': 'Dataset not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class HistoryView(APIView):
    """
    Get the last 5 uploaded datasets.
    
    GET /api/history/
    """
    permission_classes = [AllowAny]
    
    def get(self, request):
        if request.user.is_authenticated:
            datasets = Dataset.objects.filter(user=request.user)[:5]
        else:
            datasets = Dataset.objects.filter(user__isnull=True)[:5]
        
        serializer = DatasetSerializer(datasets, many=True)
        return Response(serializer.data)


class DatasetDeleteView(APIView):
    """
    Delete a specific dataset and its associated records.
    
    DELETE /api/dataset/<id>/
    """
    permission_classes = [AllowAny]
    
    def delete(self, request, pk):
        try:
            dataset = Dataset.objects.get(pk=pk)
            filename = dataset.filename
            dataset.delete()
            return Response(
                {'message': f'Dataset "{filename}" deleted successfully'},
                status=status.HTTP_200_OK
            )
        except Dataset.DoesNotExist:
            return Response(
                {'error': 'Dataset not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class PDFReportView(APIView):
    """
    Generate and download PDF report for a dataset.
    
    GET /api/report/<id>/
    """
    permission_classes = [AllowAny]
    
    def get(self, request, pk):
        try:
            dataset = Dataset.objects.get(pk=pk)
            
            # Generate PDF
            pdf_buffer = generate_equipment_report(dataset)
            
            # Create response
            response = HttpResponse(pdf_buffer, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="equipment_report_{dataset.id}.pdf"'
            
            return response
            
        except Dataset.DoesNotExist:
            return Response(
                {'error': 'Dataset not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class RegisterView(APIView):
    """
    Register a new user account.
    
    POST /api/auth/register/
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'user': UserSerializer(user).data,
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    Authenticate user and return token.
    
    POST /api/auth/login/
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response(
                {'error': 'Please provide both username and password'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = authenticate(username=username, password=password)
        
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'user': UserSerializer(user).data,
                'token': token.key
            })
        
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )


class LogoutView(APIView):
    """
    Logout user by deleting their token.
    
    POST /api/auth/logout/
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response({'message': 'Successfully logged out'})
        except Exception:
            return Response({'message': 'Logged out'})
