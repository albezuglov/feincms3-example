from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
from django.utils.html import format_html, mark_safe

from content_editor.contents import contents_for_mptt_item
from content_editor.renderer import PluginRenderer

from .models import Page, RichText, Image


renderer = PluginRenderer()
renderer.register(
    RichText,
    lambda plugin: mark_safe(plugin.text),
)
renderer.register(
    Image,
    lambda plugin: format_html(
        '<figure><img src="{}" alt=""/><figcaption>{}</figcaption></figure>',
        plugin.image.url,
        plugin.caption,
    ),
)


def page_detail(request, path=None):
    page = get_object_or_404(
        Page.objects.active(),
        path='/{}/'.format(path) if path else '/',
    )
    page.activate_language(request)
    contents = contents_for_mptt_item(page, [RichText, Image])
    return render(request, page.template.template_name, {
        'page': page,
        'content': {
            region.key: renderer.render(contents[region.key])
            for region in page.regions
        },
    })
