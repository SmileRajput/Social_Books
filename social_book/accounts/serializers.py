from rest_framework import serializers
from .models import UploadedFiles


class UploadedFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFiles
        fields = ['id', 'file', 'title', 'description', 'visibility', 'cost', 'year_published', 'uploaded_at'] # noqa
