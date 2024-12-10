# Generated by Django 3.0.2 on 2020-01-17 20:00

import core.models
from django.conf import settings
from django.db import migrations, models
from datetime import datetime
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=core.models.avatar_image_file_path),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('title', models.CharField(max_length=255, unique=True)),
                ('title_h1', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('content', models.TextField(blank=True, null=True)),
                ('short_name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(unique=True, max_length=150, editable=False)),
                ('sort', models.SmallIntegerField(default=0, null=True)),
                ('parent_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Category')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RunSQL(
            sql=[
                ("""INSERT INTO core_category (name, title, title_h1, short_name, slug, created_at, updated_at) 
                VALUES (%s, %s, %s, %s, %s, %s, %s);""",
                ['Programlama', 'Programlama Dilleri', 'Programlama Dilleri Hakkında', 'Programlama', 'programlama', datetime.now(), datetime.now()]),
                ("""INSERT INTO core_category (name, title, title_h1, short_name, slug, created_at, updated_at) 
                VALUES (%s, %s, %s, %s, %s, %s, %s);""",
                ['Veritabanı', 'Veritabanları', 'Veritabanları Hakkında', 'Veritabanı', 'veritabani', datetime.now(), datetime.now()]),
                ("""INSERT INTO core_category (name, title, title_h1, short_name, slug, created_at, updated_at) 
                VALUES (%s, %s, %s, %s, %s, %s, %s);""",
                ['Sistemler / Dağıtımlar', 'Sistemler ve Dağıtımlar', 'İşletim sistemleri ve dağıtımlar hakkında', 'Sistemler', 'sistemler-dagitimlar', datetime.now(), datetime.now()]),
                ("""INSERT INTO core_category (name, title, title_h1, short_name, slug, created_at, updated_at) 
                VALUES (%s, %s, %s, %s, %s, %s, %s);""",
                ['Haberler', 'Teknoloji Haberleri', 'Teknoloji haberleri hakkında', 'teknoloji', 'teknoloji-haberleri', datetime.now(), datetime.now()]),
                ("""INSERT INTO core_category (name, title, title_h1, short_name, slug, created_at, updated_at, parent_category_id) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);""",
                ['Python', 'Python Programlama Dili', 'Python Programlama Dili Hakkında', 'Python', 'python', datetime.now(), datetime.now(), '1']),
                ("""INSERT INTO core_category (name, title, title_h1, short_name, slug, created_at, updated_at, parent_category_id) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);""",
                ['Php', 'Php Programlama Dili', 'Php Programlama Dili Hakkında', 'Php', 'php', datetime.now(), datetime.now(), '1']),
                ("""INSERT INTO core_category (name, title, title_h1, short_name, slug, created_at, updated_at, parent_category_id) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);""",
                ['Go', 'Go Programlama Dili', 'Go Programlama Dili Hakkında', 'Go', 'go', datetime.now(), datetime.now(), '1']),
                ("""INSERT INTO core_Category (name, title, title_h1, short_name, slug, created_at, updated_at, parent_category_id) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);""",
                ['C#', 'C# Programlama Dili', 'C# Programlama Dili Hakkında', 'C#', 'c-sharp', datetime.now(), datetime.now(), '1']),
                ("""INSERT INTO core_category (name, title, title_h1, short_name, slug, created_at, updated_at, parent_category_id) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);""",
                ['Java Script', 'Java Script Programlama Dili', 'Java Script Programlama Frameworkleri', 'Java Script', 'javascript', datetime.now(), datetime.now(), '1']),
                ("""INSERT INTO core_category (name, title, title_h1, short_name, slug, created_at, updated_at, parent_category_id) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);""",
                ['Mobil Programlama', 'Mobil Programlama Dilleri', 'Mobil Programlama', 'Mobil Programlama', 'mobil', datetime.now(), datetime.now(), '1']),
                ("""INSERT INTO core_category (name, title, title_h1, short_name, slug, created_at, updated_at, parent_category_id) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);""",
                ['MySql / MariaDb', 'MySql ve MariaDb veritabanları', 'MySql ve MariaDb Veritabanları Hakkında', 'MySql / MariaDb', 'mysql-mariadb', datetime.now(), datetime.now(), '2']),
                ("""INSERT INTO core_category (name, title, title_h1, short_name, slug, created_at, updated_at, parent_category_id) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);""",
                ['MsSql', 'MsSql Veritabanı', 'MsSql Veritabanı Hakkında', 'MsSql', 'mssql', datetime.now(), datetime.now(), '2']), 
                ("""INSERT INTO core_category (name, title, title_h1, short_name, slug, created_at, updated_at, parent_category_id) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);""",
                ['PostgreSql', 'PostgreSql Veritabanı', 'PostgreSql Veritabanı Hakkında', 'PostgreSql', 'postgresql', datetime.now(), datetime.now(), '2']),
                ("""INSERT INTO core_category (name, title, title_h1, short_name, slug, created_at, updated_at, parent_category_id) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);""",
                ['Oracle', 'Oracle Veritabanı', 'Oracle Veritabanı Hakkında', 'Oracle', 'oracle', datetime.now(), datetime.now(), '2']),
                ("""INSERT INTO core_category (name, title, title_h1, short_name, slug, created_at, updated_at, parent_category_id) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);""",
                ['Linux', 'Linux İşletim Sistemleri', 'Debian \\ Ubuntu \\ Pardus vb', 'Linux', 'linux', datetime.now(), datetime.now(), '3']),
                 ("""INSERT INTO core_category (name, title, title_h1, short_name, slug, created_at, updated_at, parent_category_id) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);""",
                ['OS', 'MacOs ve Ios', 'MacOs ve Ios İşletim Sistemleri', 'macos', 'macos-ios', datetime.now(), datetime.now(), '3']),
                ("""INSERT INTO core_category (name, title, title_h1, short_name, slug, created_at, updated_at, parent_category_id) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);""",
                ['Windows X', 'Windows İşletim Sistemleri', 'Windows İşletim Sistemi', 'Windows', 'windows', datetime.now(), datetime.now(), '3']),
            ],
        ),
    ]
