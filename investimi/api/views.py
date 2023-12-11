from rest_framework.response import Response
from rest_framework.decorators import api_view
from investimi import setup
setup()

from rest_framework.views import APIView
from investimi.models import Loan, Cash_flow
from django.views import View
from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import os
from decimal import Decimal
from rest_framework.parsers import MultiPartParser
from datetime import datetime
from rest_framework import status



class LoadDataView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, *args, **kwargs):
        setup()

        trades_files = request.FILES.getlist('trades_files')
        cash_flows_files = request.FILES.getlist('cash_flows_files')


        if not trades_files:
            return Response({'error': 'trades_files is required.'}, status=400)


        for trades_file in trades_files:
          
            df_trades = pd.read_excel(trades_file)

       
            for index, row in df_trades.iterrows():

                investment_date = datetime.strptime(row['investment_date'], '%d/%m/%Y').strftime('%Y-%m-%d')
                maturity_date = datetime.strptime(row['maturity_date'], '%d/%m/%Y').strftime('%Y-%m-%d')
             
                loan, created = Loan.objects.get_or_create(
                    loan_id=row['loan_id'],
                    defaults={
                        'investment_date': investment_date,
                        'maturity_date': maturity_date,
                        'interest_rate': row['interest_rate']
                    }
                )

     
        if not cash_flows_files:
            return Response({'error': 'cash_flows_files is required.'}, status=400)

      
        for cash_flows_file in cash_flows_files:
       
            df_cash_flows = pd.read_excel(cash_flows_file)

            for index, row in df_cash_flows.iterrows():
        
                loan, created = Loan.objects.get_or_create(loan_id=row['loan_id'])

             
                cash_flow_date = datetime.strptime(row['cashflow_date'], '%d/%m/%Y').strftime('%Y-%m-%d')

                cashflow, created = Cash_flow.objects.get_or_create(
                    cash_flow_id=row['cashflow_id'],
                    defaults={
                        'loan_id': loan,
                        'cash_flow_date': cash_flow_date,
                        'currency': row['cashflow_currency'],
                        'cash_flow_type': row['cashflow_type'],
                        'amount': Decimal(row['amount'].replace(',', '').strip())
                    }
                )

        return Response({'message': 'Data loaded successfully.'}, status=200)


class RealizedAmountView(APIView):
    def get(self, request, loan_id, reference_date, format=None):
        try:
            loan = Loan.objects.get(loan_id=loan_id)
        except Loan.DoesNotExist:
            return Response({'error': 'Loan not found.'}, status=status.HTTP_404_NOT_FOUND)

        realized_amount = loan.realized_amount(reference_date)
        return Response({'realized_amount': realized_amount}, status=status.HTTP_200_OK)


class GrossExpectedView(APIView):
    def get(self, request, loan_id, reference_date, format=None):
        try:
            loan = Loan.objects.get(loan_id=loan_id)
        except Loan.DoesNotExist:
            return Response({'error': 'Loan not found.'}, status=status.HTTP_404_NOT_FOUND)

        gross_expected_amount = loan.gross_expected_amount(reference_date)
        return Response({'gross_expected_amount': gross_expected_amount}, status=status.HTTP_200_OK)

class RemainingInvestedView(APIView):
    def get(self, request, loan_id, reference_date, format=None):
        try:
            loan = Loan.objects.get(loan_id=loan_id)
        except Loan.DoesNotExist:
            return Response({'error': 'Loan not found.'}, status=status.HTTP_404_NOT_FOUND)

        remaining_invested_amount = loan.remaining_invested_amount(reference_date)
        return Response({'remaining_invested_amount': remaining_invested_amount}, status=status.HTTP_200_OK)


class ClosingDateView(APIView):
    def get(self, request, loan_id):
        try:
            loan = Loan.objects.get(loan_id=loan_id)
            closing_date = loan.closing_date()

            if closing_date:
                return Response({'closing_date': closing_date}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'The loan is not closed yet.'}, status=status.HTTP_200_OK)
        except Loan.DoesNotExist:
            return Response({'error': 'Loan not found.'}, status=status.HTTP_404_NOT_FOUND)
    