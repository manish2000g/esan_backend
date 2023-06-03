# Generated by Django 4.2 on 2023-06-02 07:29

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0007_rename_organization_name_organizer_organizer_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EliminationMode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('elimination_mode', models.CharField(choices=[('Single Elimination', 'Single Elimination'), ('Double Elimination', 'Double Elimination'), ('Battle Royale', 'Battle Royale'), ('Round Robbin', 'Round Robbin')], max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=700)),
                ('event_name', models.CharField(max_length=700, unique=True)),
                ('event_thumbnail', models.FileField(blank=True, upload_to='')),
                ('event_thumbnail_alt_description', models.CharField(blank=True, max_length=500)),
                ('event_description', ckeditor.fields.RichTextField(blank=True)),
                ('event_start_date', models.DateTimeField()),
                ('event_end_date', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('organizer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.organizer')),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_name', models.CharField(max_length=500)),
                ('game_image', models.FileField(upload_to='')),
                ('game_type', models.CharField(choices=[('PC', 'PC'), ('Mobile', 'Mobile')], default='Mobile', max_length=100)),
                ('elimination_modes', models.ManyToManyField(to='tournament.eliminationmode')),
            ],
        ),
        migrations.CreateModel(
            name='SoloGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_name', models.CharField(max_length=500)),
                ('participants', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Stage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stage_number', models.IntegerField()),
                ('no_of_participants', models.IntegerField()),
                ('no_of_groups', models.IntegerField()),
                ('stage_name', models.CharField(max_length=500)),
                ('stage_elimation_mode', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='tournament.eliminationmode')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_name', models.CharField(max_length=500)),
                ('team_image', models.FileField(upload_to='')),
                ('team_type', models.CharField(choices=[('Duo', 'Duo'), ('Squad', 'Squad')], default='Squad', max_length=500)),
                ('is_active', models.BooleanField(default=True)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournament.game')),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='manager', to=settings.AUTH_USER_MODEL)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='account.organization')),
                ('players', models.ManyToManyField(blank=True, related_name='players', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TeamGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_name', models.CharField(max_length=500)),
                ('participants', models.ManyToManyField(to='tournament.team')),
                ('stage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournament.stage')),
            ],
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('location', models.CharField(max_length=100)),
                ('tournament_name', models.CharField(max_length=700)),
                ('tournament_logo', models.FileField(blank=True, upload_to='')),
                ('tournament_banner', models.FileField(blank=True, upload_to='')),
                ('tournament_mode', models.CharField(choices=[('Online', 'Online'), ('LAN', 'LAN')], default='Online', max_length=700)),
                ('tournament_status', models.CharField(choices=[('Live', 'Live'), ('Past', 'Past'), ('Upcoming', 'Upcoming')], max_length=50)),
                ('tournament_participants', models.CharField(choices=[('Players', 'Players'), ('Teams', 'Teams')], default='Squad', max_length=700)),
                ('is_free', models.BooleanField(default=False)),
                ('tournament_fee', models.FloatField(blank=True)),
                ('maximum_no_of_participants', models.IntegerField()),
                ('tournament_description', ckeditor.fields.RichTextField(blank=True)),
                ('tournament_short_description', ckeditor.fields.RichTextField(blank=True, max_length=25)),
                ('tournament_rules', ckeditor.fields.RichTextField(blank=True)),
                ('tournament_prize_pool', ckeditor.fields.RichTextField(blank=True)),
                ('registration_opening_date', models.DateTimeField()),
                ('registration_closing_date', models.DateTimeField()),
                ('tournament_start_date', models.DateTimeField()),
                ('tournament_end_date', models.DateTimeField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_published', models.BooleanField(default=False)),
                ('is_registration_enabled', models.BooleanField(default=False)),
                ('accept_registration_automatic', models.BooleanField(default=False)),
                ('contact_email', models.CharField(blank=True, max_length=500)),
                ('discord_link', models.URLField(blank=True, max_length=500)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournament.event')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournament.game')),
                ('organizer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.organizer')),
            ],
        ),
        migrations.CreateModel(
            name='TournamentStreams',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stream_name', models.CharField(max_length=500)),
                ('url', models.URLField(max_length=500)),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournament.tournament')),
            ],
        ),
        migrations.CreateModel(
            name='TournamentSponsor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sponsor_name', models.CharField(max_length=500)),
                ('sponsorship_category', models.CharField(max_length=500)),
                ('sponsor_logo', models.FileField(upload_to='')),
                ('sponsor_link', models.URLField(max_length=500)),
                ('sponsor_banner', models.FileField(upload_to='')),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournament.tournament')),
            ],
        ),
        migrations.CreateModel(
            name='TournamentFAQ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=100)),
                ('heading', models.CharField(max_length=1000)),
                ('detail', models.TextField()),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournament.tournament')),
            ],
        ),
        migrations.CreateModel(
            name='TournamentBracket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bracket_type', models.CharField(choices=[('Winner Bracket', 'Winner Bracket'), ('Looser Bracket', 'Looser Bracket')], max_length=30)),
                ('participants', models.ManyToManyField(related_name='Team_participants', to='tournament.team')),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournament.tournament')),
            ],
        ),
        migrations.CreateModel(
            name='TeamTournamentRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registration_date', models.DateTimeField(auto_now_add=True)),
                ('registration_fee', models.FloatField()),
                ('registration_status', models.CharField(choices=[('Ongoing Review', 'Ongoing Review'), ('Verified', 'Verified'), ('Rejected', 'Rejected')], default='Ongoing Review', max_length=500)),
                ('payment_method', models.CharField(choices=[('Cash', 'Cash'), ('Bank Transfer', 'Bank Transfer'), ('Esewa', 'Esewa'), ('Other', 'Other')], default='Other', max_length=500)),
                ('current_stage', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='current_stagee', to='tournament.stage')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournament.team')),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournament.tournament')),
            ],
        ),
        migrations.CreateModel(
            name='TeamMatch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team1_points', models.FloatField()),
                ('team2_points', models.FloatField()),
                ('team1_result', models.CharField(choices=[('WIN', 'WIN'), ('LOSE', 'LOSE'), ('DRAW', 'DRAW')], max_length=500)),
                ('team2_result', models.CharField(choices=[('WIN', 'WIN'), ('LOSE', 'LOSE'), ('DRAW', 'DRAW')], max_length=500)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='tournament.teamgroup')),
                ('stage', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='tournament.stage')),
                ('team1', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='team1', to='tournament.team')),
                ('team2', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='team2', to='tournament.team')),
            ],
        ),
        migrations.AddField(
            model_name='stage',
            name='tournament',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournament.tournament'),
        ),
        migrations.CreateModel(
            name='SoloTournamentRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registration_date', models.DateTimeField(auto_now_add=True)),
                ('registration_fee', models.FloatField()),
                ('registration_status', models.CharField(choices=[('Ongoing Review', 'Ongoing Review'), ('Verified', 'Verified'), ('Rejected', 'Rejected')], default='Ongoing Review', max_length=500)),
                ('payment_method', models.CharField(choices=[('Cash', 'Cash'), ('Bank Transfer', 'Bank Transfer'), ('Esewa', 'Esewa'), ('Other', 'Other')], default='Other', max_length=500)),
                ('current_stage', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='current_stage', to='tournament.stage')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournament.tournament')),
            ],
        ),
        migrations.CreateModel(
            name='SoloMatch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player1_points', models.FloatField()),
                ('player2_points', models.FloatField()),
                ('player1_result', models.CharField(choices=[('WIN', 'WIN'), ('LOSE', 'LOSE'), ('DRAW', 'DRAW')], max_length=500)),
                ('player2_result', models.CharField(choices=[('WIN', 'WIN'), ('LOSE', 'LOSE'), ('DRAW', 'DRAW')], max_length=500)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='tournament.sologroup')),
                ('player1', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='player1', to=settings.AUTH_USER_MODEL)),
                ('player2', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='player2', to=settings.AUTH_USER_MODEL)),
                ('stage', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='tournament.stage')),
            ],
        ),
        migrations.AddField(
            model_name='sologroup',
            name='stage',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournament.stage'),
        ),
        migrations.CreateModel(
            name='EventSponsor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sponsor_name', models.CharField(max_length=500)),
                ('sponsorship_category', models.CharField(max_length=500)),
                ('sponsor_banner', models.FileField(upload_to='')),
                ('order', models.IntegerField(default=0)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournament.event')),
            ],
        ),
        migrations.CreateModel(
            name='EventNewsFeed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', ckeditor.fields.RichTextField()),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournament.event')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.organizer')),
            ],
        ),
        migrations.CreateModel(
            name='EventFAQ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=100)),
                ('heading', models.CharField(max_length=1000)),
                ('detail', models.TextField()),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tournament.event')),
            ],
        ),
    ]
