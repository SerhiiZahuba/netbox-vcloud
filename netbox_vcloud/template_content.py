from netbox.plugins import PluginTemplateExtension
from django.urls import reverse
from django.utils.html import format_html


class CloudSyncConfigButtons(PluginTemplateExtension):
    model = "netbox_vcloud.cloudsyncconfig"

    def buttons(self):
        obj = self.context.get("object")
        if (
            not obj
            or obj._meta.label_lower != "netbox_vcloud.cloudsyncconfig"
            or not getattr(obj, "pk", None)
        ):
            return ""

        url = reverse("plugins:netbox_vcloud:run_sync_now", kwargs={"pk": obj.pk})
        return format_html(
            '<a href="{}" class="btn btn-sm btn-primary">'
            '<i class="mdi mdi-sync"></i> Run Sync Now</a>',
            url,
        )


template_extensions = [CloudSyncConfigButtons]