import json

from rest_framework import serializers

from .models import User
from spam.models import Spam

class UserSerializer (serializers.ModelSerializer):
  spam_report_count = serializers.SerializerMethodField()
  spam_relative_index = serializers.SerializerMethodField()

  class Meta:
    model = User
    fields = ['id', 'name', 'phone_number', 'email', 'spam_report_count', 'spam_relative_index']
  
  def get_spam_report_count (self, obj: User):
    try:
      spam: Spam = Spam.objects.get(phone_number = obj.phone_number)
    except Spam.DoesNotExist:
      return 0
    return spam.get_report_count()

  # requires optimisation and better algorithm to determine spam index
  def get_spam_relative_index (self, obj: User) -> str:
    total = 0
    spams = Spam.objects.all()
    for spam in spams:
      spam: Spam
      total += spam.get_report_count()
    return str(round(100 * self.get_spam_report_count(obj) / total, 1)) + '%'

