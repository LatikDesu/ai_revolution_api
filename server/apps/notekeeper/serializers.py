from django.utils.text import slugify
from rest_framework import serializers

from notekeeper.models import Note


class NoteListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('id', 'note_title', 'slug')
        read_only_fields = ('id', 'note_title', 'slug')


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('id', 'user', 'note_title', 'note_content', 'slug')
        read_only_fields = ('id', 'user', 'slug')

    def create(self, validated_data):
        note_title = validated_data['note_title']
        slug = slugify(note_title)

        note = Note.objects.create(slug=slug, **validated_data)

        return note

    def update(self, instance, validated_data):
        note_title = validated_data['note_title']
        slug = slugify(note_title)

        instance.slug = slug

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
