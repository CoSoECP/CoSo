from models import PoliticalFunction

from django.test import TestCase


class PoliticalFunctionTests(TestCase):

    def test_short_description(self):
        """
        Should return a short description of the field position
        """
        position = "European Commissioner for European Commissioner for Economic" \
            + " and Monetary Affairs and the Euro|Economic and Financial Affairs, " \
            + "European Commissioner for Taxation and Customs Union, Audit and Anti-Fr"
        short_description = "European Commissioner for European Commissioner for Economic" \
            + " and Monetary Affairs and the Euro|Ec..."
        political_function = PoliticalFunction(position=position)
        self.assertEquals(political_function.short_description, short_description)