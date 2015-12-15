# -*- coding: utf-8 -*-
import json

from django.test import TestCase
from django.core.urlresolvers import reverse

from .models import About, AllRequest


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


class AllRequestTest(TestCase):
    """ Unit tests for Request model and views"""
    def test_last_request_page_available(self):
        """ Test last request page available """
        response = self.client.get(reverse('request_list'))
        self.assertEquals(response.status_code, 200)

    def test_request_works(self):
        """ Test requests """
        AllRequest.objects.all().delete()
        self.client.get(reverse('about'))
        self.assertEqual(AllRequest.objects.count(), 1)
        self.assertEqual(AllRequest.objects.get(pk=1).__str__(), "Request - 1")

    def test_last_request_page_contains_info(self):
        """ Test last request page available """
        response = self.client.get(reverse('request_list'))
        self.assertTrue('<h2>Last 10 Requests</h2>' in response.content)

    def test_last_request_page_use_request_template(self):
        """ Test last request use template """
        response = self.client.get(reverse('request_list'))
        self.assertTemplateUsed(response, 'hello/request.html')

    def test_request_date_page_order(self):
        """ Test request page order """
        AllRequest.objects.all().delete()
        self.client.get(reverse('about'))
        response = self.client.get(reverse('request_list'))
        self.assertEqual(response.context['requests'][0].path, '/request/')
        self.assertEqual(response.context['requests'][1].path, '/')

    def test_last_request_ajax_list_json(self):
        """ Test json """
        self.client.get(reverse('request_list'))
        response = self.client.get(reverse('ajax_list'))
        readable_json = json.loads(response.content)
        self.assertEqual(readable_json[0]["req_path"], '/request/')
