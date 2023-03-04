import json

from rest_framework import serializers


class ModelRunSerializer(serializers.Serializer):
    input = serializers.JSONField()

    def validate(self, data):
        if data.get("input") is None:
            raise serializers.ValidationError("Input is required")
        return data


# class ModelRunResultSerializer(serializers.Serializer):
#     task_id = serializers.CharField()
#     status = serializers.CharField()
#     result = serializers.CharField()

#     def to_representation(self, instance):
#         return {
#             "task_id": instance.task_id,
#             "status": instance.status,
#             "result": instance.result,
#         }
