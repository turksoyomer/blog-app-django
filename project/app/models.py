from django.db import models

class User(models.Model):
    username = models.CharField(max_length=64, unique=True, db_index=True)

    def __str__(self):
        return '<User %r>' % self.username
    