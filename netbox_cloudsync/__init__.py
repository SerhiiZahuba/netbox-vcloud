try:
    from netbox.plugins import PluginConfig
except ModuleNotFoundError:  # pragma: no cover - allows lightweight tooling/tests
    PluginConfig = None
    config = None
else:
    class CloudSyncConfig(PluginConfig):
        name = "netbox_vcloud"
        verbose_name = "NetBox vCloud"
        description = "Synchronize vCloud VMs into NetBox using ORM"
        version = "0.2.0"
        author = "Serhii Zahuba"
        author_email = "dev@cre.com"
        base_url = "vcloud"
        required_settings = []
        default_settings = {}

        def ready(self):
            super().ready()
            from . import jobs, template_content

    config = CloudSyncConfig
