# Generated by Django 5.1.4 on 2025-01-13 23:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_rename_user_favouriteartist_user_id_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="favouriteartist",
            old_name="user_id",
            new_name="user",
        ),
        migrations.RenameField(
            model_name="favouritetrack",
            old_name="user_id",
            new_name="user",
        ),
        migrations.AlterUniqueTogether(
            name="favouriteartist",
            unique_together={("user", "artist_id")},
        ),
        migrations.AlterUniqueTogether(
            name="favouritetrack",
            unique_together={("user", "track_id")},
        ),
    ]
