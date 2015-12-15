# -*- coding: utf-8 -*-

from django.test import TestCase
from django.core.urlresolvers import reverse

from .models import About


class PersonTest(TestCase):
    """ Unit tests for About model and views """
    fixtures = ['initial_data.json']

    def create_people(self, name="A", last_name="S", email="q@q.ua",
                      jabber="-", skype="-"):
        return About.objects.create(name=name,
                                    last_name=last_name,
                                    email=email,
                                    jabber=jabber,
                                    skype=skype)

    def test_people_creation(self):
        """ Test for create person """
        a = self.create_people()
        self.assertTrue(isinstance(a, About))
        self.assertEqual(a.__str__(), a.last_name)

    def test_home_page_doesnt_contain_info(self):
        """ Test home page doesnt contain info """
        About.objects.all().delete()
        response = self.client.get(reverse('about'))
        self.assertNotContains(response, 'Name')

    def test_db_contains_two_records(self):
        """ Test db contains two records """
        About.objects.all().delete()
        self.create_people('GoodName', 'StrangeLastName')
        self.create_people()
        response = self.client.get(reverse('about'))
        self.assertContains(response, 'GoodName')

    def test_home_page_contains_cyrillic(self):
        """ Test home page contains cyrillic """
        About.objects.all().delete()
        self.create_people(u"Петя")
        response = self.client.get(reverse('about'))
        self.assertContains(response, u"Петя")

    def test_home_page_available(self):
        """ Test home page is available """
        response = self.client.get(reverse('about'))
        self.assertEquals(response.status_code, 200)

    def test_home_page_contains_info(self):
        """ Test home page contains info """
        response = self.client.get(reverse('about'))
        self.assertTrue(response.context['people'], 'Melnychuk')

    def test_home_page_use_about_template(self):
        """ Test home page uses template """
        response = self.client.get(reverse('about'))
        self.assertTemplateUsed(response, 'hello/about.html')
