from django.db import models
from django.contrib.auth.models import User


class Dataset(models.Model):
    """
    Represents an uploaded CSV dataset with calculated summary statistics.
    Only the last 5 datasets are kept in the system.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    # Summary statistics
    total_count = models.IntegerField(default=0)
    avg_flowrate = models.FloatField(default=0.0)
    avg_pressure = models.FloatField(default=0.0)
    avg_temperature = models.FloatField(default=0.0)
    
    # Equipment type distribution stored as JSON
    type_distribution = models.JSONField(default=dict)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.filename} - {self.uploaded_at.strftime('%Y-%m-%d %H:%M')}"
    
    @classmethod
    def cleanup_old_datasets(cls, user=None, keep=5):
        """Keep only the last N datasets per user (or global if no user)."""
        if user:
            datasets = cls.objects.filter(user=user).order_by('-uploaded_at')
        else:
            datasets = cls.objects.filter(user__isnull=True).order_by('-uploaded_at')
        
        to_delete = datasets[keep:]
        for dataset in to_delete:
            dataset.delete()


class EquipmentRecord(models.Model):
    """
    Individual equipment record from a CSV upload.
    """
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='records')
    equipment_name = models.CharField(max_length=255)
    equipment_type = models.CharField(max_length=100)
    flowrate = models.FloatField()
    pressure = models.FloatField()
    temperature = models.FloatField()
    
    def __str__(self):
        return f"{self.equipment_name} ({self.equipment_type})"
