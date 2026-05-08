from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('favourites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPreference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dark_mode', models.CharField(choices=[('system', 'System Default'), ('on', 'On'), ('off', 'Off')], default='system', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'User Preference',
                'verbose_name_plural': 'User Preferences',
            },
        ),
    ]