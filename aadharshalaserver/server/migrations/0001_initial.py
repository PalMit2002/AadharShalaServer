# Generated by Django 3.2.8 on 2021-10-27 14:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Landlord',
            fields=[
                ('aadharnum', models.PositiveBigIntegerField(primary_key=True, serialize=False)),
                ('co', models.CharField(max_length=500)),
                ('house', models.CharField(max_length=500)),
                ('street', models.CharField(max_length=500)),
                ('lm', models.CharField(max_length=500)),
                ('loc', models.CharField(max_length=500)),
                ('vtc', models.CharField(max_length=500)),
                ('subdist', models.CharField(max_length=500)),
                ('dist', models.CharField(max_length=500)),
                ('state', models.CharField(max_length=500)),
                ('country', models.CharField(max_length=500)),
                ('pc', models.IntegerField()),
                ('po', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Tenant',
            fields=[
                ('aadharnum', models.PositiveBigIntegerField(primary_key=True, serialize=False)),
                ('mod_co', models.CharField(max_length=500)),
                ('mod_house', models.CharField(max_length=500)),
                ('mod_street', models.CharField(max_length=500)),
                ('mod_lm', models.CharField(max_length=500)),
                ('mod_loc', models.CharField(max_length=500)),
                ('mod_vtc', models.CharField(max_length=500)),
                ('mod_subdist', models.CharField(max_length=500)),
                ('mod_dist', models.CharField(max_length=500)),
                ('mod_state', models.CharField(max_length=500)),
                ('mod_country', models.CharField(max_length=500)),
                ('mod_pc', models.IntegerField(max_length=6)),
                ('mod_po', models.CharField(max_length=500)),
                ('request_code', models.IntegerField()),
                ('is_req_active', models.BooleanField(default=False)),
                ('landlord', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='server.landlord')),
            ],
        ),
    ]
