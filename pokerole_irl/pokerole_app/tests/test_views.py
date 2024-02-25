from django.test import TestCase, Client
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model

from ..models.ability_models import Ability
from ..models.move_models import Move
from ..models.pokedex_models import Pokedex, PokedexEntry
from ..models.species_models import PokemonSpecies

bulbasaur = PokemonSpecies(
    number=1,
    dex_id="0001",
    name="Bulbasaur",
    height=1,
    weight=1,
    description="Bulbasaur is a real cutie.",
    base_strength=1,
    base_dexterity=1,
    base_vitality=1,
    base_special=1,
    base_insight=1,
    base_hp=1,
    max_strength=2,
    max_dexterity=2,
    max_vitality=2,
    max_special=2,
    max_insight=2,
    image_name="bulba.png"
)


class AbilityListViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.path = reverse_lazy("abilities")

    def test_view_as_regular_user(self):
        """A regular user should be allowed access to the view."""
        user = get_user_model().objects.create(username='test_user')
        self.client.force_login(user)

        response = self.client.get(self.path)

        expected_response = 200

        self.assertEqual(response.status_code, expected_response)

    def test_view_as_anonymous_user(self):
        """An anonymous user should be allowed access to the view."""
        response = self.client.get(self.path)

        expected_response = 200

        self.assertEqual(response.status_code, expected_response)


class AbilityDetailViewTests(TestCase):

    def setUp(self):
        ability = Ability.objects.create(name='test_ability',
                                         effect='test', description='test')
        self.client = Client()
        self.path = reverse_lazy("ability", args=[ability.pk])

    def test_view_as_regular_user(self):
        """A regular user should be allowed access to the view."""
        user = get_user_model().objects.create(username='test_user')
        self.client.force_login(user)

        response = self.client.get(self.path)

        expected_response = 200

        self.assertEqual(response.status_code, expected_response)

    def test_view_as_anonymous_user(self):
        """An anonymous user should be allowed access to the view."""
        response = self.client.get(self.path)

        expected_response = 200

        self.assertEqual(response.status_code, expected_response)


class MainPageViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.path = reverse_lazy("index")

    def test_view_as_regular_user(self):
        """A regular user should be allowed access to the view."""
        user = get_user_model().objects.create(username='test_user')
        self.client.force_login(user)

        response = self.client.get(self.path)

        expected_response = 200

        self.assertEqual(response.status_code, expected_response)

    def test_view_as_anonymous_user(self):
        """An anonymous user should be redirected to the login page."""
        response = self.client.get(self.path)

        expected_response = 302

        self.assertEqual(response.status_code, expected_response)


class MoveListViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.path = reverse_lazy("moves")

    def test_view_as_regular_user(self):
        """A regular user should be allowed access to the view."""
        user = get_user_model().objects.create(username='test_user')
        self.client.force_login(user)

        response = self.client.get(self.path)

        expected_response = 200

        self.assertEqual(response.status_code, expected_response)

    def test_view_as_anonymous_user(self):
        """An anonymous user should be allowed access to the view."""
        response = self.client.get(self.path)

        expected_response = 200

        self.assertEqual(response.status_code, expected_response)


class MoveDetailViewTests(TestCase):

    def setUp(self):
        move = Move.objects.create(name='test_move')
        self.client = Client()
        self.path = reverse_lazy("move", args=[move.pk])

    def test_view_as_regular_user(self):
        """A regular user should be allowed access to the view."""
        user = get_user_model().objects.create(username='test_user')
        self.client.force_login(user)

        response = self.client.get(self.path)

        expected_response = 200

        self.assertEqual(response.status_code, expected_response)

    def test_view_as_anonymous_user(self):
        """An anonymous user should be allowed access to the view."""
        response = self.client.get(self.path)

        expected_response = 200

        self.assertEqual(response.status_code, expected_response)


class PokedexListViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.path = reverse_lazy("pokedex_list")

    def test_view_as_regular_user(self):
        """A regular user should be allowed access to the view."""
        user = get_user_model().objects.create(username='test_user')
        self.client.force_login(user)

        response = self.client.get(self.path)

        expected_response = 200

        self.assertEqual(response.status_code, expected_response)

    def test_view_as_anonymous_user(self):
        """An anonymous user should be redirected to the login page."""
        response = self.client.get(self.path)

        expected_response = 302

        self.assertEqual(response.status_code, expected_response)


class PokedexCreateViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.path = reverse_lazy("pokedex_add")

    def test_create_as_regular_user(self):
        """A regular user should be allowed access to the view."""
        user = get_user_model().objects.create(username='test_user')
        self.client.force_login(user)

        response = self.client.get(self.path)

        expected_response = 200

        self.assertEqual(response.status_code, expected_response)

    def test_create_as_anonymous_user(self):
        """An anonymous user should be redirected to the login page."""
        response = self.client.get(self.path)

        expected_response = 302

        self.assertEqual(response.status_code, expected_response)


class PokedexUpdateViewTests(TestCase):

    def setUp(self):
        self.pokedex = Pokedex.objects.create(name='super cool pokedex')
        self.client = Client()

    def test_edit_own_pokedex_as_regular_user(self):
        """A user should be allowed to edit their own pokedex."""
        # Log in
        user = get_user_model().objects.create(username='test_user')
        self.client.force_login(user)
        # Create own pokedex
        own_pokedex = Pokedex.objects.create(name='test_pokedex', owner=user)
        path = reverse_lazy("pokedex_edit", args=[own_pokedex.pk])

        response = self.client.get(path)

        expected_response = 200

        self.assertEqual(response.status_code, expected_response)

    def test_edit_other_users_pokedex_as_regular_user(self):
        """A user should not be allowed to edit someone else's pokedex."""
        # Log in
        user = get_user_model().objects.create(username='test_user')
        self.client.force_login(user)
        # Create other user's pokedex
        other_user = get_user_model().objects.create(username='other_user')
        other_pokedex = Pokedex.objects.create(
            name='test_pokedex', owner=other_user)
        path = reverse_lazy("pokedex_edit", args=[other_pokedex.pk])

        response = self.client.get(path)

        expected_response = 403

        self.assertEqual(response.status_code, expected_response)

    def test_edit_public_pokedex_as_regular_user(self):
        """A user should not be allowed to edit a public pokedex."""
        # Log in
        user = get_user_model().objects.create(username='test_user')
        self.client.force_login(user)
        # Create public pokedex
        public_pokedex = Pokedex.objects.create(
            name='test_pokedex', owner=None)
        path = reverse_lazy("pokedex_edit", args=[public_pokedex.pk])

        response = self.client.get(path)

        expected_response = 403

        self.assertEqual(response.status_code, expected_response)

    def test_edit_as_anonymous_user(self):
        """An anonymous user should be redirected to the login page."""
        path = reverse_lazy("pokedex_edit", args=[self.pokedex.pk])
        response = self.client.get(path)

        expected_response = 302

        self.assertEqual(response.status_code, expected_response)


class PokedexDeleteViewTests(TestCase):

    def setUp(self):
        self.pokedex = Pokedex.objects.create(name='super cool pokedex')
        self.client = Client()

    def test_delete_own_pokedex_as_regular_user(self):
        """A user should be allowed to edit their own pokedex."""
        # Log in
        user = get_user_model().objects.create(username='test_user')
        self.client.force_login(user)
        # Create own pokedex
        own_pokedex = Pokedex.objects.create(name='test_pokedex', owner=user)
        path = reverse_lazy("pokedex_delete", args=[own_pokedex.pk])

        response = self.client.post(path)

        expected_response = 302

        self.assertEqual(response.status_code, expected_response)

    def test_delete_other_users_pokedex_as_regular_user(self):
        """A user should not be allowed to edit someone else's pokedex."""
        # Log in
        user = get_user_model().objects.create(username='test_user')
        self.client.force_login(user)
        # Create other user's pokedex
        other_user = get_user_model().objects.create(username='other_user')
        other_pokedex = Pokedex.objects.create(
            name='test_pokedex', owner=other_user)
        path = reverse_lazy("pokedex_delete", args=[other_pokedex.pk])

        response = self.client.post(path)

        expected_response = 403

        self.assertEqual(response.status_code, expected_response)

    def test_delete_public_pokedex_as_regular_user(self):
        """A user should not be allowed to edit a public pokedex."""
        # Log in
        user = get_user_model().objects.create(username='test_user')
        self.client.force_login(user)
        # Create public pokedex
        public_pokedex = Pokedex.objects.create(
            name='test_pokedex', owner=None)
        path = reverse_lazy("pokedex_delete", args=[public_pokedex.pk])

        response = self.client.post(path)

        expected_response = 403

        self.assertEqual(response.status_code, expected_response)

    def test_delete_as_anonymous_user(self):
        """An anonymous user should be redirected to the login page."""
        path = reverse_lazy("pokedex_delete", args=[self.pokedex.pk])
        response = self.client.post(path)

        expected_response = 302

        self.assertEqual(response.status_code, expected_response)


class PokedexEntryListViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.pokedex = Pokedex.objects.create(name='super cool pokedex')

    def test_view_own_pokedex_as_regular_user(self):
        """A regular user should be allowed access their own pokedex."""
        # Log In
        user = get_user_model().objects.create(username='test_user')
        self.client.force_login(user)
        # Create own pokedex
        own_pokedex = Pokedex.objects.create(name='test_pokedex', owner=user)
        path = reverse_lazy("pokedex_entries", args=[own_pokedex.pk])

        response = self.client.get(path)

        expected_response = 200

        self.assertEqual(response.status_code, expected_response)

    def test_view_other_users_pokedex_as_regular_user(self):
        """Regular user should have access to other users' pokedexes."""
        # Log In
        user = get_user_model().objects.create(username='test_user')
        self.client.force_login(user)
        # Create other user's pokedex
        other_user = get_user_model().objects.create(username='other_user')
        other_pokedex = Pokedex.objects.create(
            name='test_pokedex', owner=other_user)
        path = reverse_lazy("pokedex_entries", args=[other_pokedex.pk])

        response = self.client.get(path)

        expected_response = 200

        self.assertEqual(response.status_code, expected_response)

    def test_view_public_pokedex_as_regular_user(self):
        """Regular users should have access to public pokedexes."""
        # Log In
        user = get_user_model().objects.create(username='test_user')
        self.client.force_login(user)
        # Create other user's pokedex
        public_pokedex = Pokedex.objects.create(
            name='test_pokedex', owner=None)
        path = reverse_lazy("pokedex_entries", args=[public_pokedex.pk])

        response = self.client.get(path)

        expected_response = 200

        self.assertEqual(response.status_code, expected_response)

    def test_view_as_anonymous_user(self):
        """An anonymous user should be redirected to the login page."""
        path = reverse_lazy("pokedex_entries", args=[self.pokedex.pk])
        response = self.client.get(path)

        expected_response = 302

        self.assertEqual(response.status_code, expected_response)


class PokedexEntryDetailViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        bulbasaur.save()
        self.bulbasaur = PokemonSpecies.objects.get(number=1)
        self.pokedex = Pokedex.objects.create(name='super cool pokedex')
        self.entry = PokedexEntry.objects.create(
            species=self.bulbasaur, pokedex=self.pokedex, number=1)

    def test_view_own_pokedex_entry_as_regular_user(self):
        """A regular user should be allowed access their own pokedex entries."""
        # Log In
        user = get_user_model().objects.create(username='test_user')
        self.client.force_login(user)
        # Create own pokedex entry
        own_pokedex = Pokedex.objects.create(name='test_pokedex', owner=user)
        own_entry = PokedexEntry.objects.create(
            species=self.bulbasaur, pokedex=own_pokedex, number=1)
        path = reverse_lazy("pokedex_entry", args=[
                            own_pokedex.pk, own_entry.pk])

        response = self.client.get(path)

        expected_response = 200

        self.assertEqual(response.status_code, expected_response)

    def test_view_other_users_pokedex_entry_as_regular_user(self):
        """Regular user should have access to other users' pokedex entries."""
        # Log In
        user = get_user_model().objects.create(username='test_user')
        self.client.force_login(user)
        # Create other user's pokedex
        other_user = get_user_model().objects.create(username='other_user')
        other_pokedex = Pokedex.objects.create(
            name='test_pokedex', owner=other_user)
        other_entry = PokedexEntry.objects.create(
            species=self.bulbasaur, pokedex=other_pokedex, number=1)
        path = reverse_lazy("pokedex_entry", args=[
                            other_pokedex.pk, other_entry.pk])

        response = self.client.get(path)

        expected_response = 200

        self.assertEqual(response.status_code, expected_response)

    def test_view_public_pokedex_entry_as_regular_user(self):
        """Regular users should have access to public pokedex entries."""
        # Log In
        user = get_user_model().objects.create(username='test_user')
        self.client.force_login(user)
        # Create other user's pokedex
        public_pokedex = Pokedex.objects.create(
            name='test_pokedex', owner=None)
        public_entry = PokedexEntry.objects.create(
            species=self.bulbasaur, pokedex=public_pokedex, number=1)
        path = reverse_lazy("pokedex_entry", args=[
                            public_pokedex.pk, public_entry.pk])

        response = self.client.get(path)

        expected_response = 200

        self.assertEqual(response.status_code, expected_response)

    def test_view_as_anonymous_user(self):
        """An anonymous user should be redirected to the login page."""
        path = reverse_lazy("pokedex_entry", args=[
                            self.pokedex.pk, self.entry.pk])
        response = self.client.get(path)

        expected_response = 302

        self.assertEqual(response.status_code, expected_response)


class PokedexEntryCreateViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.pokedex = Pokedex.objects.create(name='super cool pokedex')

    def test_add_entry_own_pokedex_as_regular_user(self):
        """A regular user should be allowed to create entries in their own pokedex."""
        # Log In
        user = get_user_model().objects.create(username='test_user')
        self.client.force_login(user)
        # Create own pokedex
        own_pokedex = Pokedex.objects.create(name='test_pokedex', owner=user)
        path = reverse_lazy("pokedex_entry_add", args=[own_pokedex.pk])

        response = self.client.get(path)

        expected_response = 200

        self.assertEqual(response.status_code, expected_response)

    def test_add_entry_other_users_pokedex_as_regular_user(self):
        """Regular user should not be allowed to create entries in other users' pokedexes."""
        # Log In
        user = get_user_model().objects.create(username='test_user')
        self.client.force_login(user)
        # Create other user's pokedex
        other_user = get_user_model().objects.create(username='other_user')
        other_pokedex = Pokedex.objects.create(
            name='test_pokedex', owner=other_user)
        path = reverse_lazy("pokedex_entry_add", args=[other_pokedex.pk])

        response = self.client.get(path)

        expected_response = 403

        self.assertEqual(response.status_code, expected_response)

    def test_add_entry_public_pokedex_as_regular_user(self):
        """Regular users should not be allowed to create entries in public pokedexes."""
        # Log In
        user = get_user_model().objects.create(username='test_user')
        self.client.force_login(user)
        # Create other user's pokedex
        public_pokedex = Pokedex.objects.create(
            name='test_pokedex', owner=None)
        path = reverse_lazy("pokedex_entry_add", args=[public_pokedex.pk])

        response = self.client.get(path)

        expected_response = 403

        self.assertEqual(response.status_code, expected_response)

    def test_add_entry_public_pokedex_as_superuser(self):
        """Superusers should be allowed to create entries in public pokedexes."""
        # Log In
        user = get_user_model().objects.create(username='test_user')
        user.is_superuser = True
        user.save()
        self.client.force_login(user)
        # Create other user's pokedex
        public_pokedex = Pokedex.objects.create(
            name='test_pokedex', owner=None)
        path = reverse_lazy("pokedex_entry_add", args=[public_pokedex.pk])

        response = self.client.get(path)

        expected_response = 200

        self.assertEqual(response.status_code, expected_response)

    def test_view_as_anonymous_user(self):
        """An anonymous user should be redirected to the login page."""
        path = reverse_lazy("pokedex_entries", args=[self.pokedex.pk])
        response = self.client.get(path)

        expected_response = 302

        self.assertEqual(response.status_code, expected_response)


class PokedexEntryUpdateViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        bulbasaur.save()
        self.bulbasaur = PokemonSpecies.objects.get(number=1)
        self.pokedex = Pokedex.objects.create(name='super cool pokedex')
        self.entry = PokedexEntry.objects.create(
            species=self.bulbasaur, pokedex=self.pokedex, number=1)
        self.path = reverse_lazy("pokedex_entry_edit", args=[
                                 self.pokedex.pk, self.entry.pk])

    def test_add_entry_own_pokedex_as_regular_user(self):
        """A regular user should be allowed to edit entries in their own pokedex."""
        # Log In
        user = get_user_model().objects.create(username='test_user')
        self.client.force_login(user)
        # Create own pokedex
        self.pokedex.owner = user
        self.pokedex.save()

        response = self.client.get(self.path)

        expected_response = 200

        self.assertEqual(response.status_code, expected_response)

    def test_add_entry_other_users_pokedex_as_regular_user(self):
        """Regular user should not be allowed to edit entries in other users' pokedexes."""
        # Log In
        user = get_user_model().objects.create(username='test_user')
        self.client.force_login(user)
        # Create other user's pokedex
        other_user = get_user_model().objects.create(username='other_user')
        self.pokedex.owner = other_user
        self.pokedex.save()

        response = self.client.get(self.path)

        expected_response = 403

        self.assertEqual(response.status_code, expected_response)

    def test_add_entry_public_pokedex_as_regular_user(self):
        """Regular users should not be allowed to edit entries in public pokedexes."""
        user = get_user_model().objects.create(username='test_user')
        self.client.force_login(user)

        response = self.client.get(self.path)

        expected_response = 403

        self.assertEqual(response.status_code, expected_response)

    def test_add_entry_public_pokedex_as_superuser(self):
        """Superusers should be allowed to edit entries in public pokedexes."""
        user = get_user_model().objects.create(username='test_user')
        user.is_superuser = True
        user.save()
        self.client.force_login(user)

        response = self.client.get(self.path)

        expected_response = 200

        self.assertEqual(response.status_code, expected_response)

    def test_view_as_anonymous_user(self):
        """An anonymous user should be redirected to the login page."""
        path = reverse_lazy("pokedex_entries", args=[self.pokedex.pk])
        response = self.client.get(path)

        expected_response = 302

        self.assertEqual(response.status_code, expected_response)


class PokedexEntryDeleteViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        bulbasaur.save()
        self.bulbasaur = PokemonSpecies.objects.get(number=1)
        self.pokedex = Pokedex.objects.create(name='super cool pokedex')
        self.entry = PokedexEntry.objects.create(
            species=self.bulbasaur, pokedex=self.pokedex, number=1)
        self.path = reverse_lazy("pokedex_entry_delete", args=[
                                 self.pokedex.pk, self.entry.pk])

    def test_delete_entry_own_pokedex_as_regular_user(self):
        """A regular user should be allowed to delete entries in their own pokedex."""
        # Log In
        user = get_user_model().objects.create(username='test_user')
        self.client.force_login(user)
        # Create own pokedex
        self.pokedex.owner = user
        self.pokedex.save()

        response = self.client.get(self.path)

        expected_response = 200

        self.assertEqual(response.status_code, expected_response)

    def test_delete_entry_other_users_pokedex_as_regular_user(self):
        """Regular user should not be allowed to delete entries in other users' pokedexes."""
        # Log In
        user = get_user_model().objects.create(username='test_user')
        self.client.force_login(user)
        # Create other user's pokedex
        other_user = get_user_model().objects.create(username='other_user')
        self.pokedex.owner = other_user
        self.pokedex.save()

        response = self.client.get(self.path)

        expected_response = 403

        self.assertEqual(response.status_code, expected_response)

    def test_delete_entry_public_pokedex_as_regular_user(self):
        """Regular users should not be allowed to delete entries in public pokedexes."""
        user = get_user_model().objects.create(username='test_user')
        self.client.force_login(user)

        response = self.client.get(self.path)

        expected_response = 403

        self.assertEqual(response.status_code, expected_response)

    def test_delete_entry_public_pokedex_as_superuser(self):
        """Superusers should be allowed to delete entries in public pokedexes."""
        user = get_user_model().objects.create(username='test_user')
        user.is_superuser = True
        user.save()
        self.client.force_login(user)

        response = self.client.get(self.path)

        expected_response = 200

        self.assertEqual(response.status_code, expected_response)

    def test_view_as_anonymous_user(self):
        """An anonymous user should be redirected to the login page."""
        path = reverse_lazy("pokedex_entries", args=[self.pokedex.pk])
        response = self.client.get(path)

        expected_response = 302

        self.assertEqual(response.status_code, expected_response)
