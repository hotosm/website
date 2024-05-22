from django.db import models

from wagtail.blocks import CharBlock, StreamBlock, StructBlock, URLBlock


class ActionButtonBlock(StructBlock):
    text = CharBlock(required=True, help_text="Text to display on the button")
    link = URLBlock(required=False, blank=True, help_text="URL to link to")


class SlideBlock(StructBlock):
    header = CharBlock(required=True, help_text="Slide header")
    body = CharBlock(required=True, help_text="Slide body")
    action_button = ActionButtonBlock(required=False, help_text="Button to display on the slide")


class CarouselBlock(StreamBlock):
    slides = SlideBlock()
