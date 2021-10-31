from django.db import models

# Create your models here.


class Landlord(models.Model):
    aadharnum = models.CharField(max_length=12, primary_key=True)
    co = models.CharField(max_length=500, null=True)
    house = models.CharField(max_length=500, null=True)
    street = models.CharField(max_length=500, null=True)
    lm = models.CharField(max_length=500, null=True)
    loc = models.CharField(max_length=500, null=True)
    vtc = models.CharField(max_length=500, null=True)
    subdist = models.CharField(max_length=500, null=True)
    dist = models.CharField(max_length=500, null=True)
    state = models.CharField(max_length=500, null=True)
    country = models.CharField(max_length=500, null=True)
    pc = models.IntegerField(null=True)
    po = models.CharField(max_length=500, null=True)
    token = models.CharField(max_length=5000, null=True)
    time = models.FloatField(null=True)

    def __str__(self):
        return str(self.aadharnum)


class Tenant(models.Model):
    aadharnum = models.CharField(max_length=12, primary_key=True)
    mod_co = models.CharField(max_length=500, null=True)
    mod_house = models.CharField(max_length=500, null=True)
    # mod_street = models.CharField(max_length=500, null=True)
    # mod_lm = models.CharField(max_length=500, null=True)
    # mod_loc = models.CharField(max_length=500, null=True)
    # mod_vtc = models.CharField(max_length=500, null=True)
    # mod_subdist = models.CharField(max_length=500, null=True)
    # mod_dist = models.CharField(max_length=500, null=True)
    # mod_state = models.CharField(max_length=500, null=True)
    # mod_country = models.CharField(max_length=500, null=True)
    # mod_pc = models.IntegerField(null=True)
    # mod_po = models.CharField(max_length=500, null=True)
    landlord = models.ForeignKey(Landlord, on_delete=models.CASCADE, null=True)

    isVerified = models.BooleanField(default=False)

    token = models.CharField(max_length=5000, null=True)
    time = models.FloatField(null=True)

    reqCode = models.CharField(max_length=4, null=True)

    def __str__(self):
        return str(self.aadharnum)
