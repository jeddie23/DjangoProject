# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Questionanswer(models.Model):
    question = models.CharField(max_length=1000, blank=True, null=True)
    answer = models.CharField(max_length=1000, blank=True, null=True)
    img = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'questionanswer'


class Wordquestion(models.Model):
    word = models.CharField(max_length=1000, blank=True, null=True)
    qid = models.ForeignKey(Questionanswer, models.DO_NOTHING, db_column='qid', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'wordquestion'