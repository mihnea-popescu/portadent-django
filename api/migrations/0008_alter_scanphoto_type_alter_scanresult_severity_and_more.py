# Generated by Django 4.2.16 on 2024-10-30 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0007_alter_scan_source_alter_scan_status_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="scanphoto",
            name="type",
            field=models.CharField(
                choices=[
                    ("RIGHT", "RIGHT"),
                    ("LEFT", "LEFT"),
                    ("FRONT", "FRONT"),
                    ("LOWER", "LOWER"),
                    ("UPPER", "UPPER"),
                ],
                default="FRONT",
                max_length=50,
            ),
        ),
        migrations.AlterField(
            model_name="scanresult",
            name="severity",
            field=models.CharField(
                choices=[("high", "HIGH"), ("medium", "MEDIUM"), ("low", "LOW")],
                default="low",
                max_length=50,
            ),
        ),
        migrations.AlterField(
            model_name="scanresult",
            name="tooth_type",
            field=models.CharField(
                choices=[
                    ("1", "TOOTH_1"),
                    ("2", "TOOTH_2"),
                    ("3", "TOOTH_3"),
                    ("4", "TOOTH_4"),
                    ("5", "TOOTH_5"),
                    ("6", "TOOTH_6"),
                    ("7", "TOOTH_7"),
                    ("8", "TOOTH_8"),
                    ("9", "TOOTH_9"),
                    ("10", "TOOTH_10"),
                    ("11", "TOOTH_11"),
                    ("12", "TOOTH_12"),
                    ("13", "TOOTH_13"),
                    ("14", "TOOTH_14"),
                    ("15", "TOOTH_15"),
                    ("16", "TOOTH_16"),
                    ("17", "TOOTH_17"),
                    ("18", "TOOTH_18"),
                    ("19", "TOOTH_19"),
                    ("20", "TOOTH_20"),
                    ("21", "TOOTH_21"),
                    ("22", "TOOTH_22"),
                    ("23", "TOOTH_23"),
                    ("24", "TOOTH_24"),
                    ("25", "TOOTH_25"),
                    ("26", "TOOTH_26"),
                    ("27", "TOOTH_27"),
                    ("28", "TOOTH_28"),
                    ("29", "TOOTH_29"),
                    ("30", "TOOTH_30"),
                    ("31", "TOOTH_31"),
                    ("32", "TOOTH_32"),
                    ("GUM_UPPER_LEFT_OUTSIDE", "GUM_UPPER_LEFT_OUTSIDE"),
                    ("GUM_UPPER_FRONT_OUTSIDE", "GUM_UPPER_FRONT_OUTSIDE"),
                    ("GUM_UPPER_RIGHT_OUTSIDE", "GUM_UPPER_RIGHT_OUTSIDE"),
                    ("GUM_LOWER_LEFT_OUTSIDE", "GUM_LOWER_LEFT_OUTSIDE"),
                    ("GUM_LOWER_FRONT_OUTSIDE", "GUM_LOWER_FRONT_OUTSIDE"),
                    ("GUM_LOWER_RIGHT_OUTSIDE", "GUM_LOWER_RIGHT_OUTSIDE"),
                    ("ROOF", "ROOF"),
                    ("TONGUE", "TONGUE"),
                ],
                default="1",
                max_length=50,
            ),
        ),
    ]
