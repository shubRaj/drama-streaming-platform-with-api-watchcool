# Generated by Django 3.2.8 on 2021-10-27 20:27

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import webapp.models.common


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_name', models.CharField(max_length=20)),
                ('last_name', models.CharField(max_length=20)),
                ('profile', models.ImageField(blank=True, default='profiles/user.png', null=True, upload_to='profiles')),
                ('approved', models.BooleanField(default=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('country', models.CharField(blank=True, editable=False, max_length=30, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name_plural': 'Users',
                'ordering': ('-date_joined',),
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('favicon', models.ImageField(blank=True, null=True, upload_to='images')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='images')),
                ('tagline', models.CharField(blank=True, max_length=200, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('custom_header', models.TextField(blank=True, null=True)),
                ('custom_footer', models.TextField(blank=True, null=True)),
                ('themoviedb_api_key', models.CharField(blank=True, max_length=600, null=True)),
                ('recaptcha_site_key', models.CharField(max_length=40, null=True)),
                ('recaptcha_secret_key', models.CharField(max_length=40, null=True)),
                ('app_url', models.URLField(blank=True, null=True)),
                ('show_message', models.BooleanField(default=False)),
                ('message_title', models.CharField(blank=True, max_length=30, null=True)),
                ('message', models.TextField(blank=True, null=True)),
                ('movie_comment', models.BooleanField(default=False)),
                ('tv_comment', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Configuration',
            },
        ),
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('overview', models.TextField(blank=True, null=True)),
                ('episode_number', models.IntegerField()),
                ('season_number', models.IntegerField()),
                ('tmdb_episode_id', models.IntegerField()),
                ('slug', models.SlugField(blank=True, max_length=2083, null=True)),
                ('still_path', models.URLField(blank=True, null=True)),
                ('vote_average', models.IntegerField(blank=True, null=True)),
                ('views', models.IntegerField(default=0, editable=False)),
                ('air_date', models.DateField(blank=True, null=True)),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
            ],
            options={
                'ordering': ('-added_on', '-episode_number'),
            },
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('themoviedb_id', models.IntegerField(unique=True)),
                ('imdb_id', models.CharField(blank=True, max_length=13, null=True, unique=True)),
                ('original_title', models.CharField(blank=True, max_length=300, null=True)),
                ('overview', models.TextField(null=True)),
                ('backdrop_path', models.URLField(null=True)),
                ('poster_path', models.URLField(null=True)),
                ('release_date', models.DateField(blank=True, null=True)),
                ('title', models.CharField(max_length=100)),
                ('tagline', models.CharField(blank=True, max_length=200, null=True)),
                ('vote_average', models.DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=3, null=True, validators=[django.core.validators.MaxValueValidator(10)])),
                ('runtime', models.IntegerField(blank=True, null=True)),
                ('published', models.BooleanField(default=True)),
                ('trailer', models.URLField(blank=True, null=True)),
                ('slug', models.SlugField(blank=True, editable=False, max_length=300, null=True)),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
            ],
            options={
                'db_table': 'movie',
                'ordering': ('-added_on', '-release_date'),
            },
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, unique=True)),
                ('description', models.TextField()),
                ('order', models.PositiveSmallIntegerField(blank=True, null=True, unique=True)),
                ('slug', models.SlugField(blank=True, editable=False, null=True)),
            ],
            options={
                'ordering': ('order',),
            },
        ),
        migrations.CreateModel(
            name='TV',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('themoviedb_id', models.IntegerField(unique=True)),
                ('imdb_id', models.CharField(blank=True, max_length=13, null=True, unique=True)),
                ('original_title', models.CharField(blank=True, max_length=300, null=True)),
                ('overview', models.TextField(null=True)),
                ('backdrop_path', models.URLField(null=True)),
                ('poster_path', models.URLField(null=True)),
                ('release_date', models.DateField(blank=True, null=True)),
                ('title', models.CharField(max_length=100)),
                ('tagline', models.CharField(blank=True, max_length=200, null=True)),
                ('vote_average', models.DecimalField(blank=True, decimal_places=1, default=0.0, max_digits=3, null=True, validators=[django.core.validators.MaxValueValidator(10)])),
                ('runtime', models.IntegerField(blank=True, null=True)),
                ('published', models.BooleanField(default=True)),
                ('trailer', models.URLField(blank=True, null=True)),
                ('slug', models.SlugField(blank=True, editable=False, max_length=300, null=True)),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
            ],
            options={
                'verbose_name_plural': 'TV Shows',
                'db_table': 'tv',
                'ordering': ('-added_on', '-release_date'),
            },
        ),
        migrations.CreateModel(
            name='WatchMovie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(max_length=30)),
                ('url', models.URLField(max_length=2083)),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('movie', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='watch', related_query_name='has_watch', to='webapp.movie')),
            ],
            options={
                'verbose_name_plural': 'WatchMovies',
                'db_table': 'watch_movie',
            },
        ),
        migrations.CreateModel(
            name='WatchEpisode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(max_length=30)),
                ('url', models.URLField(max_length=2083)),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('episode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watch_episode', related_query_name='has_watch_episode', to='webapp.episode')),
            ],
            options={
                'verbose_name_plural': 'WatchEpisodes',
                'db_table': 'watch_episode',
            },
        ),
        migrations.CreateModel(
            name='ViewLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('viewed_on', models.DateTimeField(db_column='viewed_on', default=django.utils.timezone.now, editable=False)),
                ('movie', models.ForeignKey(blank=True, db_column='movie', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='view', related_query_name='has_view', to='webapp.movie')),
                ('tv', models.ForeignKey(blank=True, db_column='tv', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='view', related_query_name='has_view', to='webapp.tv')),
                ('user', models.ForeignKey(blank=True, db_column='user', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='view', related_query_name='has_view', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'ViewLogs',
                'db_table': 'viewlog',
                'ordering': ('-viewed_on',),
            },
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('tv', models.ManyToManyField(related_name='type', related_query_name='type', to='webapp.TV')),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('movie', models.ManyToManyField(related_name='status', related_query_name='has_status', to='webapp.Movie')),
                ('tv', models.ManyToManyField(related_name='status', related_query_name='has_status', to='webapp.TV')),
            ],
            options={
                'verbose_name_plural': 'Status',
            },
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tmdb_season_id', models.IntegerField()),
                ('season_number', models.IntegerField()),
                ('episode_count', models.IntegerField()),
                ('name', models.CharField(blank=True, max_length=30, null=True)),
                ('overview', models.TextField(blank=True, null=True)),
                ('poster_path', models.URLField(blank=True, null=True)),
                ('air_date', models.DateField(blank=True, null=True)),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('tv', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='season', related_query_name='has_season', to='webapp.tv')),
            ],
            options={
                'ordering': ('-added_on', '-season_number'),
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('rating', models.DecimalField(decimal_places=1, default=0.0, max_digits=3)),
                ('approved', models.BooleanField(default=False)),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('movie', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='review', related_query_name='has_review', to='webapp.movie')),
                ('tv', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='review', related_query_name='has_review', to='webapp.tv')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='review', related_query_name='has_review', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-added_on',),
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('p', 'Pending'), ('c', 'Cancelled'), ('s', 'Solved')], default='p', max_length=10)),
                ('option', models.CharField(choices=[('1', 'The video is not opening'), ('2', 'Subtitle has character issues'), ('3', 'Other')], default='1', max_length=50)),
                ('description', models.TextField()),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('episode', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='report', related_query_name='has_report', to='webapp.episode')),
                ('movie', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='report', related_query_name='has_report', to='webapp.movie')),
            ],
            options={
                'ordering': ('-added_on',),
            },
        ),
        migrations.CreateModel(
            name='MovieSubtitle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(max_length=2083)),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('movie', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='subtitle', related_query_name='has_subtitle', to='webapp.movie')),
            ],
            options={
                'verbose_name_plural': 'MovieSubtitles',
                'db_table': 'movie_subtitle',
            },
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('movie', models.ManyToManyField(related_name='language', related_query_name='has_language', to='webapp.Movie')),
                ('tv', models.ManyToManyField(related_name='language', related_query_name='has_language', to='webapp.TV')),
            ],
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('color', models.CharField(blank=True, default=webapp.models.common.generateRandomColor, max_length=9, null=True)),
                ('movie', models.ManyToManyField(related_name='genre', related_query_name='has_genre', to='webapp.Movie')),
                ('tv', models.ManyToManyField(related_name='genre', related_query_name='has_genre', to='webapp.TV')),
            ],
        ),
        migrations.CreateModel(
            name='EpisodeSubtitle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(max_length=2083)),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('episode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='episode_subtitle', related_query_name='has_episode_subtitle', to='webapp.episode')),
            ],
            options={
                'verbose_name_plural': 'EpisodeSubtitles',
                'db_table': 'episode_subtitle',
            },
        ),
        migrations.AddField(
            model_name='episode',
            name='season',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='episode', related_query_name='has_episode', to='webapp.season'),
        ),
        migrations.CreateModel(
            name='DownloadMovie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original_url', models.URLField(max_length=2083, null=True)),
                ('slug', models.SlugField(max_length=2083, null=True)),
                ('source', models.CharField(max_length=30, null=True)),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('movie', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='download', related_query_name='has_download', to='webapp.movie')),
            ],
            options={
                'verbose_name_plural': 'DownloadMovies',
                'db_table': 'download_movie',
            },
        ),
        migrations.CreateModel(
            name='DownloadEpisode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('original_url', models.URLField(max_length=2083, null=True)),
                ('slug', models.SlugField(max_length=2083, null=True)),
                ('source', models.CharField(max_length=30, null=True)),
                ('added_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('episode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='download_episode', related_query_name='has_download_episode', to='webapp.episode')),
            ],
            options={
                'verbose_name_plural': 'DownloadEpisodes',
                'db_table': 'download_episode',
            },
        ),
        migrations.CreateModel(
            name='Cast',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(choices=[('1', 'Female'), ('2', 'Male')], default=1, max_length=1)),
                ('name', models.CharField(max_length=100)),
                ('tmdb_cast_id', models.IntegerField()),
                ('popularity', models.DecimalField(blank=True, decimal_places=3, max_digits=6, null=True)),
                ('profile_path', models.URLField(blank=True, null=True)),
                ('slug', models.SlugField(blank=True, max_length=2083, null=True)),
                ('added_on', models.DateField(default=django.utils.timezone.now)),
                ('movie', models.ManyToManyField(related_name='cast', related_query_name='has_cast', to='webapp.Movie')),
                ('tv', models.ManyToManyField(related_name='cast', related_query_name='has_cast', to='webapp.TV')),
            ],
            options={
                'ordering': ('-popularity',),
            },
        ),
    ]
