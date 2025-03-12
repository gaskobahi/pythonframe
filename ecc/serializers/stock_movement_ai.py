# serializers.py
from rest_framework import serializers

from ecc.serializers.stock_movement import StockMovementSerializer

class Stock_Movement_AiSerializer(serializers.Serializer):
    question = serializers.CharField()
    stock_table = StockMovementSerializer(many=True)