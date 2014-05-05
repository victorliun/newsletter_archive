from ajax_select import LookupChannel
from .models import CompanyDetail

class CompanyLookup(LookupChannel):
    model = CompanyDetail
    def get_query(self,q,request):
        return CompanyDetail.objects.filter(company_name__icontains=q).order_by('company_name')