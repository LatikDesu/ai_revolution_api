import uuid

import markdown
import markdown.extensions.codehilite
import markdown.extensions.fenced_code
import markdown.extensions.tables
import markdown.extensions.toc
from django.core.signing import Signer
from django.db import models
from django.urls import reverse
from django.utils.html import mark_safe
from django_cryptography.fields import encrypt
from unidecode import unidecode
from users.models import UserAccount

from .utils import generate_unique_slug


class Note(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    note_title = models.CharField(max_length=200, default='New Note')
    note_content = encrypt(models.TextField(null=True, blank=True))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=200, unique=True)
    signer = Signer(salt='notekeeper.Note')

    def get_message_as_markdown(self):
        return mark_safe(
            markdown.markdown(
                self.note_content,
                extensions=['codehilite', 'fenced_code',
                            'markdown_checklist.extension', 'tables', 'toc'],
                output_format="html5"
            )
        )

    def get_signed_hash(self):
        signed_pk = self.signer.sign(self.pk)
        return signed_pk

    def get_absolute_url(self):
        return reverse('get-shared-note', args=(self.get_signed_hash(),))

    def __str__(self):
        return self.note_title

    def save(self, *args, **kwargs):
        title = unidecode(self.note_title)
        if not self.slug:
            self.slug = generate_unique_slug(Note, title)
        elif self.slug and self.slug_exists():
            self.slug = generate_unique_slug(Note, title)

        super(Note, self).save(*args, **kwargs)

    def slug_exists(self):
        return Note.objects.filter(slug=self.slug).exclude(pk=self.pk).exists()
