"""
Question 1: By default are django signals executed synchronously or asynchronously? 
Please support your answer with a code snippet that conclusively proves your stance. 
The code does not need to be elegant and production ready, we just need to understand your logic.
"""

import time
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def slow_signal_handler(sender, instance, **kwargs):
    print("Signal handler started")
    time.sleep(5)  # Simulate a delay
    print("Signal handler finished")

# Create a user instance
user = User.objects.create(username="test_user")
print("User creation completed")

"""
Question 2: Do django signals run in the same thread as the caller? 
Please support your answer with a code snippet that conclusively proves your stance.
The code does not need to be elegant and production ready, we just need to understand your logic.
""" 
import threading
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def check_thread(sender, instance, **kwargs):
    print(f"Signal running in thread: {threading.current_thread().name}")

print(f"Main thread: {threading.current_thread().name}")
user = User.objects.create(username="test_user")

"""
Question 3: By default do django signals run in the same database transaction as the caller?
Please support your answer with a code snippet that conclusively proves your stance.
The code does not need to be elegant and production ready, we just need to understand your logic.
"""

from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def check_transaction(sender, instance, **kwargs):
    print(f"Inside signal: Transaction active? {transaction.get_connection().in_atomic_block}")

def create_user_with_transaction():
    with transaction.atomic():
        print(f"Before user creation: Transaction active? {transaction.get_connection().in_atomic_block}")
        user = User.objects.create(username="test_user")
        print(f"After user creation: Transaction active? {transaction.get_connection().in_atomic_block}")

create_user_with_transaction()
