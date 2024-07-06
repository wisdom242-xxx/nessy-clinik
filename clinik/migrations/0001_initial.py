# Generated by Django 5.0 on 2024-07-06 12:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id_patient', models.AutoField(primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=100)),
                ('a_consulte', models.BooleanField(default=False)),
                ('est_hospitalise', models.BooleanField(default=False)),
                ('est_examine', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Produit',
            fields=[
                ('id_produit', models.AutoField(primary_key=True, serialize=False)),
                ('designation', models.CharField(max_length=100)),
                ('quantite', models.IntegerField()),
                ('prix_unitaire', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='RapportMensuel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mois', models.CharField(max_length=7, unique=True)),
                ('patients_consultes', models.IntegerField(default=0)),
                ('patients_hospitalises', models.IntegerField(default=0)),
                ('patients_examines', models.IntegerField(default=0)),
                ('montant_ventes', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('benefice_realise', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Salle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('capacite', models.IntegerField(default=5)),
                ('occupee', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Utilisateur',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nom', models.CharField(max_length=255)),
                ('prenom', models.CharField(max_length=255)),
                ('adresse', models.CharField(max_length=255)),
                ('num_tel', models.CharField(max_length=15)),
                ('password', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Examen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinik.patient')),
            ],
        ),
        migrations.AddField(
            model_name='patient',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinik.service'),
        ),
        migrations.CreateModel(
            name='Vente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantite', models.IntegerField()),
                ('prix_unitaire', models.DecimalField(decimal_places=2, max_digits=10)),
                ('prix_de_vente', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date_vente', models.DateTimeField(auto_now_add=True)),
                ('produit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clinik.produit')),
            ],
        ),
    ]