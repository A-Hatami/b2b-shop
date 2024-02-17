from django.contrib import admin
from .models import Seller, Costumer, Transaction, TransactionLog, RegistrationLog, InnerCharge

admin.site.register(Seller)
admin.site.register(Costumer)
admin.site.register(Transaction)
admin.site.register(TransactionLog)
admin.site.register(RegistrationLog)
admin.site.register(InnerCharge)
