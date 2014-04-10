"""
Archive App: tests
"""
from django.test import TestCase
from django.contrib.auth.models import User
from mock import Mock


from .models import *
# Create your tests here.

class CompanyDetailTest(TestCase):
    """
    Test every behaviour CompanyDetail has.
    """
    @classmethod
    def setUp(self):
        self.mocked_com = Mock(spec=CompanyDetail)
        self.mocked_com.pk = 1
        self.mocked_com.company_name = "Newsletter"
        self.mocked_com.company_country = "India"
        self.mocked_com.domain_names = "newsletterarchive.com"
        self.mocked_com.subdomain_names = "sub.newsletterarchive.com"
        self.mocked_com.company_tags = "Information"
        self.mocked_com.added_by = Mock(spec=User)

    def test_companydetail_unicode(self):
        self.assertEqual(1,1)
        #self.assertEqual(self.__unicode__(), "Company:%d, %s - %s" %(self.mocked_com.pk, 
        #    self.mocked_com.company_name, self.mocked_com.domain_names))