from django.conf.urls import re_path, include

from reflow_server.core.decorators import validate_billing
from reflow_server.rich_text.views import RichTextImageView

urlpatterns = [
    re_path(r'^(?P<company_id>(\w+(\.)?(-)?(_)?)+)/(?P<page_id>\d+)/', include([
        re_path(r'^(?P<block_uuid>([a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}))/', include([
            re_path(r'^file/image/(?P<file_name>.+)/$', validate_billing(RichTextImageView.as_view()), name='rich_text_block_image_view')
        ]))
    ]))
] 