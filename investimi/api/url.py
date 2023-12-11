from django.urls import path
from investimi.api.views import RealizedAmountView, GrossExpectedView, RemainingInvestedView, LoadDataView, ClosingDateView

urlpatterns = [
    path('upload/', LoadDataView.as_view(), name='upload-files'),
    path('loan/realized-amount/<str:loan_id>/<str:reference_date>/', RealizedAmountView.as_view(), name='realized-amount'),
    path('loan/gross-expected/<str:loan_id>/<str:reference_date>/', GrossExpectedView.as_view(), name='gross-expected'),
    path('loan/remaining-invested/<str:loan_id>/<str:reference_date>/', RemainingInvestedView.as_view(), name='remaining-invested'),
    path('loan/closing-date/<str:loan_id>/', ClosingDateView.as_view(), name='closing-date'),
]