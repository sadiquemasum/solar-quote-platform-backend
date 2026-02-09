from django.urls import path
from .views import QuoteCreateView, QuoteListView, PublicQuoteLookupView

urlpatterns = [
    path("quotes/", QuoteCreateView.as_view(), name="quote-create"),
    path("quotes/by-email/", PublicQuoteLookupView.as_view(), name="quotes-by-email"),
    path("dashboard/quotes/", QuoteListView.as_view(), name="dashboard-quotes"),
]

