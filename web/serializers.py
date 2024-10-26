from .models import *
from rest_framework import serializers
from collections import OrderedDict

class UserRegSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"

    def get_fields(self):
            new_fields = OrderedDict()
            for name, field in super().get_fields().items():
                field.required = False
                new_fields[name] = field
            return new_fields 

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username'],
            email=validated_data['email'],
            sex=validated_data['sex'],
        )
        user.set_password(validated_data['password'])  
        user.save()
        return user  