from rest_framework import serializers

class StrictSerializerMixin(serializers.Serializer):
    def to_internal_value(self, data):
        # Vérifie les champs inattendus
        extra_fields = set(data.keys()) - set(self.fields.keys())
        if extra_fields:
            raise serializers.ValidationError(
                {field: "Ce champ n'est pas autorisé." for field in extra_fields}
            )
        return super().to_internal_value(data)

class AbstractBaseSerializer(StrictSerializerMixin,serializers.ModelSerializer):

    class Meta:
        abstract = True
