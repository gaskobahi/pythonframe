# Generated by Django 5.1.4 on 2025-02-18 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ecc',
            fields=[
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('accounting_date', models.DateField()),
                ('lot_number', models.CharField(max_length=250)),
                ('type_ecriture', models.CharField(max_length=250)),
                ('type_document', models.CharField(max_length=250)),
                ('document_number', models.CharField(max_length=250)),
                ('article_number', models.CharField(max_length=250)),
                ('variant_code', models.CharField(max_length=250)),
                ('description', models.TextField(blank=True)),
                ('package_number', models.CharField(max_length=250)),
                ('store_code', models.CharField(max_length=250)),
                ('unit_code', models.CharField(max_length=250)),
                ('created_by', models.CharField(max_length=250)),
                ('quantity', models.CharField(max_length=250)),
                ('quantity_in_sac', models.CharField(max_length=250)),
                ('quantity_invoiced', models.CharField(max_length=250)),
                ('remaining_quantity', models.CharField(max_length=250)),
                ('quantity_reserved', models.CharField(max_length=250)),
                ('lettering_writing', models.CharField(max_length=250)),
                ('sales_amount_actual', models.CharField(max_length=250)),
                ('total_cost_actual', models.CharField(max_length=250)),
                ('total_cost_not_included', models.CharField(max_length=250)),
                ('is_open', models.CharField(max_length=250)),
                ('order_type', models.CharField(max_length=250)),
                ('created_at', models.DateField()),
                ('sequence_number', models.CharField(max_length=250)),
                ('kor_by_reception', models.CharField(max_length=250)),
                ('kor_input', models.CharField(max_length=250)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Temp_Ecc',
            fields=[
                ('accounting_date', models.DateField()),
                ('lot_number', models.CharField(max_length=250)),
                ('type_ecriture', models.CharField(max_length=250)),
                ('type_document', models.CharField(max_length=250)),
                ('document_number', models.CharField(max_length=250)),
                ('article_number', models.CharField(max_length=250)),
                ('variant_code', models.CharField(max_length=250)),
                ('description', models.TextField(blank=True)),
                ('package_number', models.CharField(max_length=250)),
                ('store_code', models.CharField(max_length=250)),
                ('unit_code', models.CharField(max_length=250)),
                ('created_by', models.CharField(max_length=250)),
                ('quantity', models.CharField(max_length=250)),
                ('quantity_in_sac', models.CharField(max_length=250)),
                ('quantity_invoiced', models.CharField(max_length=250)),
                ('remaining_quantity', models.CharField(max_length=250)),
                ('quantity_reserved', models.CharField(max_length=250)),
                ('lettering_writing', models.CharField(max_length=250)),
                ('sales_amount_actual', models.CharField(max_length=250)),
                ('total_cost_actual', models.CharField(max_length=250)),
                ('total_cost_not_included', models.CharField(max_length=250)),
                ('is_open', models.CharField(max_length=250)),
                ('order_type', models.CharField(max_length=250)),
                ('created_at', models.DateField()),
                ('sequence_number', models.BigIntegerField(primary_key=True, serialize=False)),
                ('kor_by_reception', models.CharField(max_length=250)),
                ('kor_input', models.CharField(max_length=250)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
