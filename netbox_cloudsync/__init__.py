try:
    from netbox.plugins import PluginConfig
except ModuleNotFoundError:  # pragma: no cover - allows lightweight tooling/tests
    PluginConfig = None
    config = None
else:
    class CloudSyncConfig(PluginConfig):
        name = "netbox_cloudsync"
        verbose_name = "Cloud Synchronization"
        description = "Synchronize vCloud VMs into NetBox using ORM"
        version = "0.1.0"
        author = "Serhii Zahuba"
        author_email = "dev@cre.com"
        base_url = "cloudsync"
        required_settings = []
        default_settings = {}

        def ready(self):
            super().ready()
            from . import jobs, template_content

    config = CloudSyncConfig
