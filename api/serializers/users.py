from rest_framework import serializers
from django.contrib.auth import get_user_model


class EmailSerializer(serializers.Serializer):
	email = serializers.EmailField(required=True)

	def validate_email(self, email):
		if not email:
			raise serializers.ValidationError("Email cannot be empty.")

		User = get_user_model()
		try:
			user = User.objects.get(email=email)
			if not user.is_active:
				raise serializers.ValidationError("Email is not verified.")
		except User.DoesNotExist:
			pass
		return email


class CodeSerializer(serializers.Serializer):
	code = serializers.CharField(max_length=20, required=True)

	def validate_code(self, code):
		code = code.strip()
		if not code:
			raise serializers.ValidationError("Code cannot be empty.")
		if len(code) != 6: 
			raise serializers.ValidationError("Code must be 6 letters")
		if not code.isdigit():
			raise serializers.ValidationError("Code must be only numbers") 
		return code 
