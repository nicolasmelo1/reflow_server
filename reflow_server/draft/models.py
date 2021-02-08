from django.conf import settings
from django.db import models

from reflow_server.draft.managers import DraftDraftManager
from reflow_server.rich_text.managers import DraftRichTextManager
from reflow_server.data.managers import DraftDataManager


class DraftType(models.Model):
    """
    This model is a `type` so it contains required data used for this program to work. This model holds the type of the draft,
    so right now it can be only `file`, `value`. Values are just strings saved in our database. Files are stored in our storage provider.
    """
    name = models.CharField(max_length=250)
    order = models.BigIntegerField(default=1)

    class Meta:
        db_table = 'draft_type'
        ordering = ('order',)


class Draft(models.Model):
    """
    What is a draft?

    To put it in simple words a draft is something that is temporary. In our system sometimes we want to save files
    just after saving, but we don't want to store them forever, we just want to upload it after saving for performance
    reasons. That is exactly the case here.

    An easy example is when handling files:
    - The user added a new file to an attachments field while editing a formulary. When the user attach a new file we
    have 2 options: option 1 is to upload this file ONLY when the user hits save. The option 2 is to upload this file exactly
    on the moment he attach a new file.

    On option one you will not be able to edit the formulary while the upload is happening, on option 2, you can, and when you hit save
    the attachment will be long uploaded.

    Another example is on rich texts, where the user can upload a new image while he is writting. If he is writting a really long text
    with lot's of images, those images will take too much time to be uploaded, while if they are uploaded in the exact moment
    they are attached when you hit save it will be a lot less costly.

    Another non trivial example but could be a use case for this kind of funcionality: prevent users from doing poop.
    What we mean is that, we can create an history or even fallback funcionality. When the users click save while editing a formulary
    we display to them the a message if they want to fallback to how the data was before saving. If he hit this button we undo his changes
    otherwise we keep this changes.

    As you can see, there is a lot of room for use cases for temporary data in our platform. Right now we support two:
    - Files - As the name suggests they are exactly that: files. They are files we store in our storage provider.
    - values - They are strings that are not saved elsewhere, they are saved in our database directly. For Json, and other types
    of values that can be strigfied you might prefer this over files.

    I don't know if you understand but those files and values are deleted from our database after some time, they are just temporary and exists
    on a certain time.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    draft_type = models.ForeignKey('draft.DraftType', models.CASCADE, db_index=True)
    bucket = models.CharField(max_length=200, default=settings.S3_BUCKET, blank=True, null=True)
    file_draft_path = models.CharField(max_length=250, default=settings.S3_FILE_DRAFT_PATH, blank=True, null=True)
    file_url = models.CharField(max_length=1000, null=True, blank=True)
    file_size = models.BigIntegerField(default=0, blank=True, null=True)
    value = models.TextField(blank=True, null=True)
    user = models.ForeignKey('authentication.UserExtended', models.CASCADE, db_index=True, blank=True, null=True, related_name='user_drafts')
    company = models.ForeignKey('authentication.Company', models.CASCADE, db_index=True, blank=True, null=True, related_name='company_drafts')
    
    class Meta:
        db_table = 'draft'

    draft_ = DraftDraftManager()
    rich_text_ = DraftRichTextManager()
    data_ = DraftDataManager()
