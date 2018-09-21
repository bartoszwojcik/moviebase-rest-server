from django.test import TestCase
from random import randint, sample
from faker import Faker
from rest_framework.test import APITestCase
from showtimes.models import Cinema


class CinemaTestCase(APITestCase):

    def setUp(self):
        self.faker = Faker("pl_PL")
        for _ in range(3):
            self._create_fake_cinema()

    def _fake_cinema_data(self):
        """
        Creates fake cinema dictionary.
        """
        cinema_data = {
            "name": "{}".format(self.faker.company()),
            "city": self.faker.city()
        }
        return cinema_data

    def _create_fake_cinema(self):
        """
        Saves the fake cinema to the database.
        """
        cinema_data = self._fake_cinema_data()
        new_cinema = Cinema.objects.create(**cinema_data)

    def test_get_cinema_list(self):
        response = self.client.get("/cinemas/", {}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Cinema.objects.count(), len(response.data))

    def test_get_cinema_detail(self):
        response = self.client.get(
            f"""/cinemas/{Cinema.objects.first().id}/""", {}, format='json'
        )
        self.assertEqual(response.status_code, 200)
        for field in ["name", "city", "movies"]:
            self.assertIn(field, response.data)

    def test_add_cinema(self):
        """
        Tests adding a new cinema using POST.
        """
        cinema_count = Cinema.objects.count()

        new_cinema = self._fake_cinema_data()
        response = self.client.post("/cinemas/", new_cinema, format='json')
        self.assertEqual(response.status_code, 201)

        self.assertEqual(Cinema.objects.count(), cinema_count + 1)

        # Check if db contents match the original dictionary
        for key, val in new_cinema.items():
            self.assertIn(key, response.data)
            if isinstance(val, list):
                self.assertCountEqual(response.data[key], val)
            else:
                self.assertEqual(response.data[key], val)

    def test_update_cinema(self):
        """
        Tests updating a cinema in DB.
        """
        response = self.client.get(
            f"""/cinemas/{Cinema.objects.first().id}/""", {}, format='json'
        )

        cinema_data = response.data
        cinema_data["name"] = "Test New Name"
        cinema_data["city"] = "Test New City"

        # Save the updated data
        response = self.client.patch(
            f"""/cinemas/{Cinema.objects.first().id}/""",
            cinema_data,
            format='json'
        )
        self.assertEqual(response.status_code, 200)

        # Verify the updated data
        cinema_obj = Cinema.objects.first()
        self.assertEqual(cinema_obj.name, cinema_data["name"])
        self.assertEqual(cinema_obj.city, cinema_data["city"])

    def test_delete_cinema(self):
        """
        Tests removal of a cinema.
        """
        cinema_count = Cinema.objects.count()

        last_cinema = Cinema.objects.last()

        response = self.client.delete(
            f"/cinemas/{last_cinema.id}", {}, format="json"
        )
        self.assertEqual(response.status_code, 204)
        self.assertNotEqual(cinema_count, Cinema.objects.count())
