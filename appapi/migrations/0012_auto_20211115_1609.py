# Generated by Django 3.2.8 on 2021-11-15 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appapi', '0011_rename_server_choices_configuration_server_dialog_selection'),
    ]

    operations = [
        migrations.RenameField(
            model_name='configuration',
            old_name='authorization',
            new_name='ad_unit_id_appodeal_rewarded',
        ),
        migrations.RenameField(
            model_name='configuration',
            old_name='custom_banner_link',
            new_name='custom_banner_image_link',
        ),
        migrations.RemoveField(
            model_name='configuration',
            name='media_placehoder_path',
        ),
        migrations.RemoveField(
            model_name='configuration',
            name='purchase_key',
        ),
        migrations.AddField(
            model_name='configuration',
            name='ad_face_audience_native',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='configuration',
            name='ad_unit_id_facebook_native_audience',
            field=models.CharField(blank=True, max_length=191, null=True),
        ),
        migrations.AddField(
            model_name='configuration',
            name='ad_unit_id_facebook_rewarded',
            field=models.CharField(blank=True, max_length=191, null=True),
        ),
        migrations.AddField(
            model_name='configuration',
            name='ad_unit_id_native',
            field=models.CharField(blank=True, max_length=191, null=True),
        ),
        migrations.AddField(
            model_name='configuration',
            name='ad_unit_id_native_enable',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='configuration',
            name='ad_unit_id_rewarded',
            field=models.CharField(blank=True, max_length=191, null=True),
        ),
        migrations.AddField(
            model_name='configuration',
            name='applovin_banner',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='configuration',
            name='applovin_banner_unitid',
            field=models.CharField(blank=True, max_length=191, null=True),
        ),
        migrations.AddField(
            model_name='configuration',
            name='applovin_interstital_show',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='configuration',
            name='applovin_interstitial',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='configuration',
            name='applovin_interstitial_unitid',
            field=models.CharField(blank=True, max_length=191, null=True),
        ),
        migrations.AddField(
            model_name='configuration',
            name='applovin_reward_unitid',
            field=models.CharField(blank=True, max_length=191, null=True),
        ),
        migrations.AddField(
            model_name='configuration',
            name='appnext_banner',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='configuration',
            name='appnext_interstitial',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='configuration',
            name='appnext_interstitial_show',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='configuration',
            name='appnext_placementid',
            field=models.CharField(blank=True, max_length=191, null=True),
        ),
        migrations.AddField(
            model_name='configuration',
            name='appodeal_banner',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='configuration',
            name='appodeal_intersitial',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='configuration',
            name='appodeal_show_interstitial',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='configuration',
            name='aws_access_key_id',
            field=models.CharField(blank=True, max_length=191, null=True),
        ),
        migrations.AddField(
            model_name='configuration',
            name='aws_bucket',
            field=models.CharField(blank=True, max_length=191, null=True),
        ),
        migrations.AddField(
            model_name='configuration',
            name='aws_default_region',
            field=models.CharField(blank=True, max_length=191, null=True),
        ),
        migrations.AddField(
            model_name='configuration',
            name='aws_s3_storage',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='configuration',
            name='aws_secret_access_key',
            field=models.CharField(blank=True, max_length=191, null=True),
        ),
        migrations.AddField(
            model_name='configuration',
            name='default_cast_option',
            field=models.CharField(blank=True, max_length=191, null=True),
        ),
        migrations.AddField(
            model_name='configuration',
            name='default_layout_networks',
            field=models.CharField(blank=True, max_length=191, null=True),
        ),
        migrations.AddField(
            model_name='configuration',
            name='default_media_placeholder_path',
            field=models.CharField(blank=True, max_length=191, null=True),
        ),
        migrations.AddField(
            model_name='configuration',
            name='default_network',
            field=models.CharField(blank=True, max_length=191, null=True),
        ),
        migrations.AddField(
            model_name='configuration',
            name='default_network_player',
            field=models.CharField(blank=True, max_length=191, null=True),
        ),
        migrations.AddField(
            model_name='configuration',
            name='default_payment',
            field=models.CharField(blank=True, max_length=191, null=True),
        ),
        migrations.AddField(
            model_name='configuration',
            name='default_trailer_default',
            field=models.CharField(blank=True, max_length=191, null=True),
        ),
        migrations.AddField(
            model_name='configuration',
            name='email_verify',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='configuration',
            name='enable_banner_bottom',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='configuration',
            name='enable_download',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='configuration',
            name='enable_webview',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='configuration',
            name='favoriteonline',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='configuration',
            name='flag_secure',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='configuration',
            name='force_inappupdate',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='configuration',
            name='force_login',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='configuration',
            name='force_password_access',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='configuration',
            name='force_update',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='configuration',
            name='hxfile_api_key',
            field=models.CharField(blank=True, max_length=191, null=True),
        ),
        migrations.AddField(
            model_name='configuration',
            name='ironsource_app_key',
            field=models.CharField(blank=True, max_length=191, null=True),
        ),
        migrations.AddField(
            model_name='configuration',
            name='ironsource_banner',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='configuration',
            name='ironsource_banner_placement_name',
            field=models.CharField(blank=True, max_length=191, null=True),
        ),
        migrations.AddField(
            model_name='configuration',
            name='ironsource_interstitial',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='configuration',
            name='ironsource_interstitial_placement_name',
            field=models.CharField(blank=True, max_length=191, null=True),
        ),
        migrations.AddField(
            model_name='configuration',
            name='ironsource_interstitial_show',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='configuration',
            name='ironsource_reward_placement_name',
            field=models.CharField(blank=True, max_length=191, null=True),
        ),
        migrations.AddField(
            model_name='configuration',
            name='live_multi_servers',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='configuration',
            name='network',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='configuration',
            name='notification_separated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='configuration',
            name='notification_style',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='configuration',
            name='password',
            field=models.CharField(blank=True, max_length=191, null=True),
        ),
        migrations.AddField(
            model_name='configuration',
            name='paypal_amount',
            field=models.CharField(blank=True, max_length=191, null=True),
        ),
        migrations.AddField(
            model_name='configuration',
            name='paypal_client_id',
            field=models.CharField(blank=True, max_length=191, null=True),
        ),
        migrations.AddField(
            model_name='configuration',
            name='paypal_currency',
            field=models.CharField(blank=True, max_length=191, null=True),
        ),
        migrations.AddField(
            model_name='configuration',
            name='reset_password_message',
            field=models.CharField(blank=True, max_length=600, null=True),
        ),
        migrations.AddField(
            model_name='configuration',
            name='root_detection',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='configuration',
            name='separate_download',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='configuration',
            name='startapp_banner',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='configuration',
            name='startapp_id',
            field=models.CharField(blank=True, max_length=191, null=True),
        ),
        migrations.AddField(
            model_name='configuration',
            name='startapp_interstitial',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='configuration',
            name='stripe_publishable_key',
            field=models.CharField(blank=True, max_length=191, null=True),
        ),
        migrations.AddField(
            model_name='configuration',
            name='stripe_secret_key',
            field=models.CharField(blank=True, max_length=191, null=True),
        ),
        migrations.AddField(
            model_name='configuration',
            name='suggest_auth',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='configuration',
            name='unity_banner_placement_id',
            field=models.CharField(blank=True, max_length=191, null=True),
        ),
        migrations.AddField(
            model_name='configuration',
            name='unity_game_id',
            field=models.CharField(blank=True, max_length=191, null=True),
        ),
        migrations.AddField(
            model_name='configuration',
            name='unity_intersitial_placement_id',
            field=models.CharField(blank=True, max_length=191, null=True),
        ),
        migrations.AddField(
            model_name='configuration',
            name='unity_reward_placement_id',
            field=models.CharField(blank=True, max_length=191, null=True),
        ),
        migrations.AddField(
            model_name='configuration',
            name='unity_show',
            field=models.IntegerField(default=True, null=True),
        ),
        migrations.AddField(
            model_name='configuration',
            name='unityads_banner',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='configuration',
            name='unityads_interstitial',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='configuration',
            name='vpn',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='configuration',
            name='vungle_appid',
            field=models.CharField(blank=True, max_length=191, null=True),
        ),
        migrations.AddField(
            model_name='configuration',
            name='vungle_banner',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='configuration',
            name='vungle_banner_placment_name',
            field=models.CharField(blank=True, max_length=191, null=True),
        ),
        migrations.AddField(
            model_name='configuration',
            name='vungle_interstitial',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='configuration',
            name='vungle_interstitial_placement_name',
            field=models.CharField(blank=True, max_length=191, null=True),
        ),
        migrations.AddField(
            model_name='configuration',
            name='vungle_interstitial_show',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='configuration',
            name='vungle_reward_placement_name',
            field=models.CharField(blank=True, max_length=191, null=True),
        ),
        migrations.AddField(
            model_name='configuration',
            name='wach_ads_to_unlock',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='configuration',
            name='wasabi_access_key_id',
            field=models.CharField(blank=True, max_length=191, null=True),
        ),
        migrations.AddField(
            model_name='configuration',
            name='wasabi_bucket',
            field=models.CharField(blank=True, max_length=191, null=True),
        ),
        migrations.AddField(
            model_name='configuration',
            name='wasabi_default_region',
            field=models.CharField(blank=True, max_length=191, null=True),
        ),
        migrations.AddField(
            model_name='configuration',
            name='wasabi_secret_access_key',
            field=models.CharField(blank=True, max_length=191, null=True),
        ),
        migrations.AddField(
            model_name='configuration',
            name='wasabi_storage',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='configuration',
            name='webview_link',
            field=models.CharField(blank=True, max_length=191, null=True),
        ),
    ]