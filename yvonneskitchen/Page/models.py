from django.db import models
from django.utils.translation import ugettext_lazy as _
from tinymce import models as tinymce_models

class HomePage(models.Model):
    """Model for the home page"""

    intro_statement = tinymce_models.HTMLField(
            _('Intro Statement')
            )

    food_description = tinymce_models.HTMLField(
            _('Food Description')
            )

    def get_hash(self):
        return 'home'

    ## override methods ##
    def __unicode__(self):
        return 'Home Page'

    def get_absolute_url(self):
        return '/'

    ## meta data ##
    class Meta:
        verbose_name_plural = 'Home Page Variables'
