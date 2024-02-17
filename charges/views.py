from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import SellerSerializer, CostumerSerializer, \
    SellRequestSerializer, SellerIncreaseSerializer, DeleteSellerSerializer, DeleteCostumerSerializer
from .models import Seller, Costumer, Transaction, TransactionLog, RegistrationLog, DeletionLog, InnerCharge
from rest_framework import status
from django.utils import timezone
from django.db import transaction
from django.db.models import F


@api_view(['GET'])
def list_costumers(request):
    costumers = Costumer.objects.all()
    serializer = CostumerSerializer(costumers, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def list_sellers(request):
    sellers = Seller.objects.all()
    serializer = SellerSerializer(sellers, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@transaction.atomic
def add_costumer(request):
    serializer = CostumerSerializer(data=request.data)
    if serializer.is_valid():

        costumer = serializer.save()
        # Add appropriate log for this new costumer
        current_time = timezone.now()
        new_log = f"***Creation***\nPhone Number : {costumer.phone_number}\nInitial Credit : {costumer.credit}\n" \
                  f"Registering Time : {current_time}\n\n"
        costumer.logs += new_log

        RegistrationLog.objects.create(
            log_type="Costumer Registration",
            costumer=costumer,
            credit=costumer.credit,
            date=current_time
        )

        costumer.save()

        return Response(serializer.data, status.HTTP_201_CREATED)
    else:
        errors = serializer.errors
        if 'phone_number' in errors:
            error_message = errors['phone_number'][0]
            return Response({'Message': error_message}, status.HTTP_400_BAD_REQUEST)
        elif 'credit' in errors:
            error_message = errors['credit'][0]
            return Response({'Message': error_message}, status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@transaction.atomic
def add_seller(request):
    serializer = SellerSerializer(data=request.data)
    if serializer.is_valid():
        seller = serializer.save()

        # Add appropriate log for this new costumer
        current_time = timezone.now()

        new_log = f"***Creation***\nUsername : {seller.username}\nInitial Credit : {seller.credit}\n" \
                  f"Registering Time : {current_time}\n\n"
        seller.logs += new_log

        RegistrationLog.objects.create(
            log_type="Seller Registration",
            seller=seller,
            credit=seller.credit,
            date=current_time
        )

        seller.save()

        message = "Successfully creation!"
        return Response({'Message': message}, status.HTTP_201_CREATED)
    else:
        errors = serializer.errors
        if 'username' in errors:
            error_message = errors['username'][0]
            return Response({'Message': error_message}, status.HTTP_400_BAD_REQUEST)
        elif 'credit' in errors:
            error_message = errors['credit'][0]
            return Response({'Message': error_message}, status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@transaction.atomic
def charge_seller(request):
    serializer = SellerIncreaseSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.data.get("username")
        amount = float(serializer.data.get("amount"))

        try:

            # seller = Seller.objects.get(username=username)
            seller = Seller.objects.select_for_update().get(username=username)
            if amount < 0:
                message = "The amount shouldn't be negative!"
                return Response({'Message': message}, status.HTTP_400_BAD_REQUEST)
            else:
                seller.credit = str(float(seller.credit) + amount)
                # seller.credit = F('credit') + amount
                current_time = timezone.now()
                # Add appropriate log
                new_log = f"***Charging***\nSeller: {seller.username}\nAmount Increased : {amount}\n" \
                          f"New Credit : {seller.credit}\nDate : {current_time}\n\n"
                seller.logs += new_log

                TransactionLog.objects.create(
                    log_type="Seller Increase",
                    seller=seller,
                    amount=amount,
                    date=current_time
                )

                InnerCharge.objects.create(
                    seller=seller,
                    amount=amount,
                    date=current_time,
                )

                seller.save()
                message = "The credit increased!"
                return Response({'Message': message}, status.HTTP_200_OK)
        except Seller.DoesNotExist:
            message = "No seller with such username!"
            return Response({'Message': message}, status.HTTP_400_BAD_REQUEST)
    else:
        message = "Wrong request format!"
        return Response({'Message': message}, status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@transaction.atomic
def transaction(request):
    serializer = SellRequestSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.data.get("username")
        phone_number = serializer.data.get("phone_number")
        amount = float(serializer.data.get("amount"))

        try:
            # seller = Seller.objects.get(username=username)
            seller = Seller.objects.select_for_update().get(username=username)
        except Seller.DoesNotExist:
            message = "No seller with such username!"
            return Response({'Message': message}, status.HTTP_400_BAD_REQUEST)

        try:
            # costumer = Costumer.objects.get(phone_number=phone_number)
            costumer = Costumer.objects.select_for_update().get(phone_number=phone_number)
        except Costumer.DoesNotExist:
            message = "No costumer with such phone number!"
            return Response({'Message': message}, status.HTTP_400_BAD_REQUEST)

        if amount < 0:
            message = "The amount you want to transact shouldn't be negative!"
            return Response({'Message': message}, status.HTTP_400_BAD_REQUEST)

        if float(seller.credit) - amount < 0:
            message = "The seller's credit is not enough to charge!"
            return Response({'Message': message}, status.HTTP_400_BAD_REQUEST)
        else:
            seller.credit = str(float(seller.credit) - amount)
            costumer.credit = str(float(costumer.credit) + amount)
            # seller.credit = F('credit') - amount
            # costumer.credit = F('credit') + amount

            current_time = timezone.now()

            # Add appropriate log
            new_log = f"***Transaction***\nSender : {seller.username}\nReceiver : {costumer.phone_number}\n" \
                      f"Amount Of Transaction : {amount}\nDate : {current_time}\n\n"
            seller.logs += new_log
            costumer.logs += new_log

            seller.save()
            costumer.save()

            Transaction.objects.create(
                seller=seller,
                costumer=costumer,
                amount=amount,
                date=current_time
            )

            TransactionLog.objects.create(
                log_type="Transaction",
                seller=seller,
                costumer=costumer,
                amount=amount,
                date=current_time
            )

            message = "The charge has been done successfully!"
            return Response({'Message': message}, status.HTTP_200_OK)

    else:
        message = "Wrong request format!"
        return Response({'Message': message}, status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def delete_seller(request):
    serializer = DeleteSellerSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.data.get('username')
        try:
            seller = Seller.objects.get(username=username)
            seller.delete()

            DeletionLog.objects.create(
                log_type="Seller Deletion",
                seller=seller,
                date=timezone.now()
            )

            message = "Seller has been deleted!"
            return Response({'Message': message}, status.HTTP_200_OK)
        except Seller.DoesNotExist:
            message = "No seller with such username!"
            return Response({'Message': message}, status.HTTP_404_NOT_FOUND)

    else:
        message = "Wrong request format!"
        return Response({'Message': message}, status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def delete_costumer(request):
    serializer = DeleteCostumerSerializer(data=request.data)
    if serializer.is_valid():
        phone_number = serializer.data.get('phone_number')
        try:
            costumer = Costumer.objects.get(phone_number=phone_number)
            costumer.delete()

            DeletionLog.objects.create(
                log_type="Costumer Deletion",
                seller=costumer,
                date=timezone.now()
            )

            message = "Costumer has been deleted!"
            return Response({'Message': message}, status.HTTP_200_OK)
        except Seller.DoesNotExist:
            message = "No costumer with such phone number!"
            return Response({'Message': message}, status.HTTP_404_NOT_FOUND)

    else:
        message = "Wrong request format!"
        return Response({'Message': message}, status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def seller_details(request, username):
    try:
        seller = Seller.objects.get(username=username)
        return Response({'Details': seller.logs}, status.HTTP_200_OK)
    except Seller.DoesNotExist:
        message = "No seller with such username!"
        return Response({'Message': message}, status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def costumer_details(request, phone_number):
    try:
        costumer = Costumer.objects.get(phone_number=phone_number)
        return Response({'Details': costumer.logs}, status.HTTP_200_OK)
    except Costumer.DoesNotExist:
        message = "No costumer with such phone number!"
        return Response({'Message': message}, status.HTTP_404_NOT_FOUND)
