
from django.db import models
from datetime import datetime
from decimal import Decimal


class Loan(models.Model):
    loan_id = models.CharField(max_length=50,primary_key=True)
    investment_date = models.DateField()
    maturity_date = models.DateField()
    interest_rate = models.CharField(max_length=100)

    def daily_interest_rate(self):
        interest_rate = float(self.interest_rate.strip('%'))
        daily_interest_rate_percent= interest_rate/100
        daily_interest_rate= daily_interest_rate_percent/365

        return daily_interest_rate
    
    def daily_interest_amount(self):
        funding = self.cash_flow.filter(cash_flow_type='funding')
        invested_amount_value = 0
        for i in funding:
            invested_amount_value -= i.amount
        invested_amount = abs(invested_amount_value)
        daily_interest_rate = Decimal(self.daily_interest_rate())
        return invested_amount * daily_interest_rate
    
    def passed_days(self, reference_date):
        if self.investment_date and self.maturity_date:
            reference_date_value = datetime.strptime(reference_date, "%Y-%m-%d").date()
            return (reference_date_value - self.investment_date).days
        else:
            return 0

    
    def gross_expected_interest_amount(self,reference_date):
        
        return self.daily_interest_amount()* self.passed_days(reference_date)
    
    def gross_expected_amount(self, reference_date):
        funding = self.cash_flow.filter(cash_flow_type='funding')

        invested_amount_value = 0
        for i in funding:
            invested_amount_value -= i.amount

        invested_amount = abs(invested_amount_value)

        gross_expected_interest_amount = self.gross_expected_interest_amount(reference_date)
        gross_expected_amount = invested_amount + gross_expected_interest_amount
        return gross_expected_amount

    
    def realized_amount(self, reference_date):
        repayment_values = self.cash_flow.filter(cash_flow_date__lte=reference_date ,cash_flow_type='repayment')
        realized_amount = sum([cashflow.amount for cashflow in repayment_values])
        return realized_amount
    
    def remaining_invested_amount(self, reference_date):
        
        funding = self.cash_flow.filter(cash_flow_type='repayment')
        invested_amount_value = 0
        for i in funding:
            invested_amount_value <= i.amount
        invested_amount = abs(invested_amount_value)
        return invested_amount - self.realized_amount(reference_date)
    
    def closing_date(self):
        maturity_date = self.maturity_date
        
        if not maturity_date:
            return None

        reference_date = datetime.combine(maturity_date, datetime.min.time()).strftime('%Y-%m-%d')
        
        realized_amount = self.realized_amount(reference_date)
        gross_expected_amount = self.gross_expected_amount(reference_date)

        if realized_amount >= gross_expected_amount:
            return maturity_date
        else:
            return None
    
    
class Cash_flow(models.Model): 
    cash_flow_id = models.CharField(primary_key=True,max_length=100 )
    loan_id = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name="cash_flow")
    cash_flow_date = models.DateField()
    currency= models.CharField( max_length=50)
    cash_flow_type =models.CharField( max_length=50)
    amount = models.DecimalField(max_digits=100, decimal_places=2, default=0, null=True, blank=True)




