import random, string
from django.db.models.signals import post_save
from django.dispatch import receiver 
from api.models import User, UserConfirmation

def generate_pin(size=6 , chars=string.digits):
	return ''.join(random.choice(chars) for _ in range(size)) 

@receiver(post_save, sender=User)
def create_user(sender, instane, created, **kwargs): 
	if created: 
		code = generate_pin()
		UserConfirmation.objects.create(
			user = sender, 
			code = code 
		)