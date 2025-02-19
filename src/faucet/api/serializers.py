from rest_framework import serializers
from web3 import Web3

class FundRequestSerializer(serializers.Serializer):
    wallet_address = serializers.CharField(max_length=42)

    def validate_wallet_address(self, value):
        if not Web3.is_address(value):
            raise serializers.ValidationError("Invalid wallet address")
        return value
