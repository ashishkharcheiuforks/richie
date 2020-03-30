# Generated by Django 2.2.11 on 2020-03-24 02:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("cms", "0022_auto_20180620_1551"),
    ]

    operations = [
        migrations.CreateModel(
            name="NestedItem",
            fields=[
                (
                    "cmsplugin_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        related_name="nesteditem_nesteditem",
                        serialize=False,
                        to="cms.CMSPlugin",
                    ),
                ),
                ("content", models.TextField(default="", verbose_name="Content")),
                (
                    "variant",
                    models.CharField(
                        blank=True,
                        choices=[
                            (None, "Default from parent template"),
                            ("accordion", "Accordion"),
                            ("list", "List"),
                        ],
                        default=None,
                        help_text="Form factor variant",
                        max_length=50,
                        null=True,
                        verbose_name="Variant",
                    ),
                ),
            ],
            options={"abstract": False,},
            bases=("cms.cmsplugin",),
        ),
    ]
