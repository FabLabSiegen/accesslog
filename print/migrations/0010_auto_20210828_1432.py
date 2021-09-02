# Generated by Django 3.2.4 on 2021-08-28 12:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('print', '0009_auto_20210828_1431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignedusers',
            name='Machine',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='print.machine'),
        ),
        migrations.AlterField(
            model_name='assignedusers',
            name='User',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='print.fablabuser'),
        ),
        migrations.AlterField(
            model_name='printjob',
            name='GCode',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='print.gcode'),
        ),
        migrations.AlterField(
            model_name='printjob',
            name='Machine',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='print.machine'),
        ),
        migrations.AlterField(
            model_name='printjob',
            name='User',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='print.fablabuser'),
        ),
        migrations.AlterField(
            model_name='printmediafile',
            name='PrintJob',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='print.printjob'),
        ),
        migrations.AlterField(
            model_name='printtemperaturehistory',
            name='PrintJob',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='print.printjob'),
        ),
        migrations.AlterField(
            model_name='rating',
            name='PrintJob',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='print.printjob'),
        ),
        migrations.AlterField(
            model_name='rating',
            name='User',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='print.fablabuser'),
        ),
        migrations.AlterField(
            model_name='slicingconfigs',
            name='ConfigLocation',
            field=models.FilePathField(),
        ),
        migrations.AlterField(
            model_name='slicingconfigs',
            name='GCode',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='print.gcode'),
        ),
    ]
