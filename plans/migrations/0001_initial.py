# Generated by Django 4.2.9 on 2024-04-07 20:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, null=True)),
                ('plan_type', models.CharField(choices=[('free', 'Free'), ('basic', 'Basic'), ('standard', 'Standard'), ('pro', 'Pro')], default='free', max_length=30)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
            ],
        ),
        migrations.CreateModel(
            name='UserPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_plan', to='plans.plan')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_plan', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscription_period', models.CharField(choices=[('1', '1 Month'), ('2', '2 Months'), ('3', '3 Months'), ('4', '4 Months'), ('5', '5 Months'), ('6', '6 Months'), ('7', '7 Months'), ('8', '8 Months'), ('9', '9 Months'), ('10', '10 Months'), ('11', '11 Months'), ('12', '12 Months')], default='1', max_length=24, verbose_name='Subscription Period')),
                ('start_date', models.DateField(blank=True, db_index=True, default=None, null=True, verbose_name='Start Date')),
                ('end_date', models.DateField(blank=True, db_index=True, default=None, null=True, verbose_name='End Date')),
                ('fee_status', models.CharField(choices=[('pending', 'Pending'), ('paid', 'Paid')], default='pending', max_length=24, verbose_name='Fee Status')),
                ('amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=12)),
                ('active', models.BooleanField(default=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user_plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscription', to='plans.userplan')),
            ],
        ),
    ]
