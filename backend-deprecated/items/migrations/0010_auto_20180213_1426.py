# Generated by Django 2.0.2 on 2018-02-13 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0009_auto_20180213_1415'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='lvl',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Lvl'),
        ),
        migrations.AlterField(
            model_name='item',
            name='type',
            field=models.IntegerField(choices=[(1, 'Jednoręczne'), (2, 'Dwuręczne'), (3, 'Półtoraręczne'), (4, 'Dystansowe'), (5, 'Pomocnicze'), (6, 'Różdzki'), (7, 'Laski'), (8, 'Zbroje'), (9, 'Hełmy'), (10, 'Buty'), (11, 'Rękawice'), (12, 'Pierścienie'), (13, 'Naszyjniki'), (14, 'Tarcze'), (15, 'Neutralne'), (16, 'Konsumpcyjne'), (17, 'Złoto'), (18, 'Klucze'), (19, 'Questowe'), (20, 'Odnawialne'), (21, 'Strzały'), (22, 'Talizmany'), (23, 'Książki'), (24, 'Torby'), (25, 'Mikstury'), (26, 'Eventowe')], verbose_name='Typ'),
        ),
        migrations.AddIndex(
            model_name='item',
            index=models.Index(fields=['name'], name='items_item_name_1c746e_idx'),
        ),
    ]
