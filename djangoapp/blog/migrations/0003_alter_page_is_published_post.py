# Generated by Django 4.2.5 on 2023-09-22 16:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_category_page_alter_tags_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='is_published',
            field=models.BooleanField(default=True, help_text='Marque essa opção para exibir a página.'),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('slug', models.SlugField(blank=True, default='', max_length=255, unique=True)),
                ('exerpt', models.CharField(max_length=100)),
                ('is_published', models.BooleanField(default=False, help_text='Marque essa opção para exibir a página.')),
                ('content', models.TextField()),
                ('cover', models.ImageField(blank=True, default='', upload_to='posts/%Y/%m')),
                ('cover_in_post_content', models.BooleanField(default=True, help_text='Exibe a imagem de capa dentro do conteúdo do post')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.category')),
            ],
            options={
                'verbose_name': 'Posts',
            },
        ),
    ]
