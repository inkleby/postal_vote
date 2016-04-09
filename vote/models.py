# -*- coding: utf-8 -*-


from django.db import models
from tools.django_tools import EasyBulkModel,StockModelHelpers
from tools.ql import QuickList
from oscodepoint import open_codepoint
import datetime
from django.db.models import F

class Election(EasyBulkModel, StockModelHelpers):
    name = models.CharField(max_length=255, default="", blank=True)
    date = models.DateField()
    cut_off_date = models.DateField(null=True,blank=True)
    
    @classmethod
    def valid_elections(cls):
        n = datetime.datetime.now()
        return list(cls.objects.filter(date__gte=n).order_by('date'))
    
    @classmethod
    def get_time(cls,value):
        universal = False
        single_day = None
        value = int(value)
        time_range = []
        if value == 0:
            universal = True
        elif value == -1:
            range = cls.valid_elections()
            time_range = [range[0].date, range[-1].date]
        else:
            single_day = cls.objects.get(id=value).date
        
        return universal, single_day, time_range
    
    @classmethod
    def populate(cls):
        Election.objects.get_or_create(name="May Elections 2016",
                                       date= datetime.date(2016,05,05))
        Election.objects.get_or_create(name="EU Referendum (June) 2016",
                                       date= datetime.date(2016,06,23))      
        

class Council(EasyBulkModel, StockModelHelpers):
    name = models.CharField(max_length=255, default="", blank=True)
    website = models.CharField(max_length=255, default="", blank=True)
    postcode = models.CharField(max_length=9, default="", blank=True)
    lad13cd = models.CharField(max_length=13, default="", blank=True)
    address = models.TextField(default=00)
    email = models.CharField(max_length=255, default="", blank=True)
    phone = models.CharField(max_length=255, default="", blank=True)
    forms_completed = models.IntegerField(default=0)
    

    @classmethod
    def from_postcode(cls,postcode):
        """
        given a postcode - try and get the local council
        """
        def reduce(txt):
            return txt.lower().strip().replace(" ", "")
        
        r_postcode = reduce(postcode)
        
        try:
            return Postcode.objects.get(postcode=r_postcode).council
        except Postcode.DoesNotExist:
            return None
            
    def increment_count(self):
        self.forms_completed = F('forms_completed') +1
        self.save()
                
    
    @classmethod
    def populate(cls):
        """
        populate councils with ERO contact details
        source : 
        
        """
        ql = QuickList().open('resources//ERO_addresses.csv')
        
        for r in ql:
            Council(name=r["name"],
                    website = r["website"],
                    postcode = r["postcode"],
                    email=r["email"],
                    lad13cd = r["council_id"],
                    phone = r["phone"],
                    address = r["address"]
                    ).queue()
            
        Council.do_queue()
        
    

class Postcode(EasyBulkModel, StockModelHelpers):
    """
    stores reduced vesion of OS code point
     open for council and postcode connection
    """
    postcode = models.CharField(
        max_length=7, blank=True, db_index=True)  # lower and spaces removed
    council = models.ForeignKey(
        Council, null=True, blank=True, related_name="postcode_refs")

    @classmethod
    def populate(cls,delete_current=False):
        """ load postcodes through oscodepoint interfaces"""
        if delete_current:
            print "deleted {0}".format(cls.objects.all().delete())
        
        codepoint = open_codepoint('resources/codepo_gb.zip')
    
        def reduce(txt):
            return txt.lower().strip().replace(" ", "")
    
        total = codepoint.metadata['total_count']
        print "{0} total".format(total)
    
        council_lookup = {x.lad13cd: x.id for x in Council.objects.all()}
    
        for x, entry in enumerate(codepoint.entries()):
    
            try:
                council = council_lookup[entry['Admin_district_code']]
            except KeyError:
                council = None
                print "{0} doesn't exist in our councils".format(entry['Admin_district_code'])
    
            Postcode(postcode=reduce(entry['Postcode']),
                     council_id=council).queue()
                     
        Postcode.do_queue()
                     

