from django.db import models
from django.utils.translation import ugettext_lazy as _
from tinymce import models as tinymce_models

class MenuItem(models.Model):
    """Model for a menu item"""
    CATEGORY_CHOICES = (
            ('soup', 'Soup'),
            ('salad', 'Salad'),
            ('appetizer', 'Appetizer'),
            ('tray', 'Tray'),
            ('breakfast', 'Breakfast'),
            ('lunch', 'Lunch'),
            ('dinner', 'Dinner'),
            ('dessert', 'Dessert'),
            ('bread', 'Bread'),
            )

    item_name = models.CharField(
            _('Item Name'),
            max_length = 200
            )

    category = models.CharField(
            _('Category'),
            max_length = 20,
            choices = CATEGORY_CHOICES
            )

    image = models.ImageField(
            _('Image'),
            default = None,
            upload_to = 'img/menu/',
            null = True,
            blank = True
            )

    description = models.TextField(
            _('Description')
            )

    price = models.DecimalField(
            _('Price'),
            max_digits = 6,
            decimal_places = 2
            )

    per_person_item = models.BooleanField(
            _('Per Person Item'),
            default = True
            )

    weekly_special = models.BooleanField(
            _('Weekly Special'),
            default = False
            )

    special_price = models.DecimalField(
            _('Special Price'),
            max_digits = 6,
            decimal_places = 2
            )

    last_modified = models.DateTimeField(
        _('Date Last Modified'),
        auto_now = True
    )

    def get_hash(self):
        return 'menu'

    def __unicode__(self):
        return self.item_name

    def get_absolute_url(self):
        return '/menu/'