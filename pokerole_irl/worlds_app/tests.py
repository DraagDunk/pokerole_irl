from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from .models import World, Character

ash = get_user_model()(username="ash")
misty = get_user_model()(username="misty")
brock = get_user_model()(username="brock")

kanto = World(name="Kanto")
johto = World(name="Johto")

blue = Character(first_name="Blue", last_name="", owner=ash, world=kanto)
red = Character(first_name="Red", last_name="", owner=ash, world=kanto)
green = Character(first_name="Green", last_name="", owner=ash, world=kanto)
gold = Character(first_name="Gold", last_name="", owner=ash, world=johto)
silver = Character(first_name="Silver", last_name="", owner=ash, world=johto)


class WorldListViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        ash.save()
        misty.save()
        brock.save()
        kanto.save()
        johto.save()
        kanto.members.add(ash)
        kanto.members.add(misty)
        johto.members.add(ash)
        self.path = reverse_lazy("world-list")

    def test_view_as_regular_user(self):
        """A regular user should be able to see worlds they are a member of in the list."""
        self.client.force_login(ash)
        ash_response = self.client.get(self.path)
        self.client.force_login(misty)
        misty_response = self.client.get(self.path)
        self.client.force_login(brock)
        brock_response = self.client.get(self.path)

        ash_expected_response = 200
        misty_expected_response = 200
        brock_expected_response = 200

        self.assertEqual(ash_response.status_code, ash_expected_response)
        self.assertEqual(misty_response.status_code, misty_expected_response)
        self.assertEqual(brock_response.status_code, brock_expected_response)

        self.assertEqual(ash_response.context.get("object_list").count(), 2)
        self.assertEqual(misty_response.context.get("object_list").count(), 1)
        self.assertEqual(brock_response.context.get("object_list").count(), 0)

    def test_view_as_anonymous_user(self):
        """An anonymous user should be redirected to the login page."""
        response = self.client.get(self.path)

        expected_response = 302

        self.assertEqual(response.status_code, expected_response)


class WorldViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        ash.save()
        kanto.save()
        johto.save()
        kanto.members.add(ash)
        blue.save()
        red.save()
        green.save()

    def test_view_as_regular_user_member(self):
        """A member of the world should be able to access the world view."""
        self.client.force_login(ash)
        response = self.client.get(reverse_lazy("world", args=[kanto.slug]))

        expected_response = 200

        self.assertEqual(response.status_code, expected_response)
        self.assertEqual(response.context.get("character_list").count(), 3)

    def test_view_as_regular_user_nonmember(self):
        """A user, who is not a member of the world should not be allowed to access the view."""
        self.client.force_login(ash)
        response = self.client.get(reverse_lazy("world", args=[johto.slug]))

        expected_response = 404

        self.assertEqual(response.status_code, expected_response)

    def test_view_as_anonymous_user(self):
        """An anonymous user should be redirected to the login page."""
        path = reverse_lazy("world", args=[kanto.slug])
        response = self.client.get(path)

        expected_response = 302

        self.assertEqual(response.status_code, expected_response)


class CharacterViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        ash.save()
        kanto.save()
        johto.save()
        kanto.members.add(ash)
        blue.save()
        gold.save()

    def test_view_as_regular_user_member(self):
        """A member of the world should be able to access the character view."""
        self.client.force_login(ash)
        response = self.client.get(reverse_lazy(
            "character", args=[kanto.slug, blue.slug]))

        expected_response = 200

        self.assertEqual(response.status_code, expected_response)

    def test_view_as_regular_user_nonmember(self):
        """A user, who is not a member of the world should not be allowed to access the view."""
        self.client.force_login(ash)
        response = self.client.get(reverse_lazy(
            "character", args=[johto.slug, gold.slug]))

        expected_response = 404

        self.assertEqual(response.status_code, expected_response)

    def test_view_own_character_in_wrong_world(self):
        """Trying to access own character through the wrong world should return a 404 status code."""
        self.client.force_login(ash)
        # Blue is a real character -- but he belongs to the Kanto world, not Johto!
        response = self.client.get(reverse_lazy(
            "character", args=[johto.slug, blue.slug]))

        expected_response = 404

        self.assertEqual(response.status_code, expected_response)

    def test_view_character_in_own_wrong_world(self):
        """Trying to access character through the owned wrong world should return a 404 status code."""
        self.client.force_login(ash)
        # Gold is a real character -- but he belongs to the Johto world, not Kanto!
        response = self.client.get(reverse_lazy(
            "character", args=[kanto.slug, gold.slug]))

        expected_response = 404

        self.assertEqual(response.status_code, expected_response)

    def test_view_as_anonymous_user(self):
        """An anonymous user should be redirected to the login page."""
        path = reverse_lazy("character", args=[kanto.slug, blue.slug])
        response = self.client.get(path)

        expected_response = 302

        self.assertEqual(response.status_code, expected_response)


class CharacterCreateViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        ash.save()
        kanto.save()
        johto.save()
        kanto.members.add(ash)

    def test_view_as_regular_user_member(self):
        """A member of the world should be able to create a new character."""
        self.client.force_login(ash)
        response = self.client.get(reverse_lazy(
            "character-create", args=[kanto.slug]))

        expected_response = 200

        self.assertEqual(response.status_code, expected_response)

    def test_view_as_regular_user_nonmember(self):
        """A user, who is not a member of the world should not be allowed to create a new character."""
        self.client.force_login(ash)
        response = self.client.get(reverse_lazy(
            "character-create", args=[johto.slug]))

        expected_response = 404

        self.assertEqual(response.status_code, expected_response)

    def test_view_as_anonymous_user(self):
        """An anonymous user should be redirected to the login page."""
        path = reverse_lazy("character-create", args=[kanto.slug])
        response = self.client.get(path)

        expected_response = 302

        self.assertEqual(response.status_code, expected_response)
