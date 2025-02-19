from django.db import models


class TransactionLog(models.Model):
    wallet_address = models.CharField(max_length=42)
    source_ip = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=None, null=True)
    tx_id = models.CharField(max_length=66, blank=True, null=True)
