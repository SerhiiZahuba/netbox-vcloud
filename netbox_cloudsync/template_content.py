from netbox.plugins import PluginTemplateExtension
from django.urls import reverse
from django.utils.html import format_html


class CloudSyncConfigButtons(PluginTemplateExtension):
    model = 'netbox_vcloud.cloudsyncconfig'

    def buttons(self):
        obj = self.context.get('object')
        if not obj or obj._meta.label_lower != 'netbox_vcloud.cloudsyncconfig':
            return ""


        url = reverse('plugins:netbox_vcloud:run_sync_now', args=[obj.pk])
        return format_html(
            f'<a href="{url}" class="btn btn-sm btn-primary">'
            f'<i class="mdi mdi-sync"></i> Run Sync Now</a>'
        )


template_extensions = [CloudSyncConfigButtons]
