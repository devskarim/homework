from django.core.mail import send_mail,EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


def send_code(user,email:str, code:str):
	subject = "Your vertifaction code" 
	html_content = render_to_string("password.html", {
        "user": user,
        "password": code
    })
	
	msg = EmailMultiAlternatives(
					subject=subject,
					body="Your verification code is included in this email.",
					from_email=f"X Security <{settings.EMAIL_HOST_USER}>",
					to=[user.email]
		)

	msg.attach_alternative(html_content, "text/html")
	msg.send()