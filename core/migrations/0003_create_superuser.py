from django.db import migrations
import os # පරිසර විචල්‍යයන් (Env Variables) සඳහා

def create_superuser(apps, schema_editor):
    """
    Render.com හි පරිසර විචල්‍යයන්ගෙන් Admin ගිණුමක් සාදයි
    """
    User = apps.get_model('auth', 'User')
    
    # අපි Render.com හි ENV variables සාදනු ඇත
    username = os.environ.get('ADMIN_USER', 'admin')
    email = os.environ.get('ADMIN_EMAIL', 'admin@example.com')
    password = os.environ.get('ADMIN_PASS', 'adminpass123') # තාවකාලික මුරපදය

    # ගිණුම දැනටමත් තිබේදැයි පරීක්ෂා කිරීම
    if not User.objects.filter(username=username).exists():
        print(f"\nCreating default superuser '{username}'...")
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print("Superuser created successfully.")
    else:
        print(f"\nSuperuser '{username}' already exists.")

class Migration(migrations.Migration):
    
    # මෙතනට ඔබගේ අවසන් migration ගොනුවේ නම ඇතුළත් කරන්න
    # උදා: '0003_payment'
    dependencies = [
        ('core', '0002_payment'), 
    ]

    operations = [
        migrations.RunPython(create_superuser),
    ]