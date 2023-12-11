from rest_framework import serializers
from investimi.models import Loan, Cash_flow

class LoanSerializer(serializers.ModelSerializer):

    class Meta:
        model = Loan
        fields = "__all__"


class CashFlowSerializer(serializers.ModelSerializer):

    cash_flow = LoanSerializer

    class Meta:
        model = Cash_flow
        fields = "__all__"

        