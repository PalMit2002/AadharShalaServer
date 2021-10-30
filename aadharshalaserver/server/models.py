from django.db import models

# Create your models here.


class Landlord(models.Model):
    aadharnum = models.PositiveBigIntegerField(primary_key=True)
    co = models.CharField(max_length=500)
    house = models.CharField(max_length=500)
    street = models.CharField(max_length=500)
    lm = models.CharField(max_length=500)
    loc = models.CharField(max_length=500)
    vtc = models.CharField(max_length=500)
    subdist = models.CharField(max_length=500)
    dist = models.CharField(max_length=500)
    state = models.CharField(max_length=500)
    country = models.CharField(max_length=500)
    pc = models.IntegerField()
    po = models.CharField(max_length=500)

    def __str__(self):
        return str(self.aadharnum)


class Tenant(models.Model):
    aadharnum = models.PositiveBigIntegerField(primary_key=True)
    mod_co = models.CharField(max_length=500)
    mod_house = models.CharField(max_length=500)
    mod_street = models.CharField(max_length=500)
    mod_lm = models.CharField(max_length=500)
    mod_loc = models.CharField(max_length=500)
    mod_vtc = models.CharField(max_length=500)
    mod_subdist = models.CharField(max_length=500)
    mod_dist = models.CharField(max_length=500)
    mod_state = models.CharField(max_length=500)
    mod_country = models.CharField(max_length=500)
    mod_pc = models.IntegerField()
    mod_po = models.CharField(max_length=500)
    landlord = models.ForeignKey(Landlord, on_delete=models.CASCADE)
    request_code = models.IntegerField()
    is_req_active = models.BooleanField(default=False)

    def __str__(self):
        return str(self.aadharnum)
