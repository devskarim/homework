from rest_framework import serializers 

class EmailSerializer(serializers.Serializer): 
	email = serializers.EmailField(required=True)

class CodeSerializer(serializers.Serializer): 
	code = serializers.CharField(max_length = 20,required=True)
