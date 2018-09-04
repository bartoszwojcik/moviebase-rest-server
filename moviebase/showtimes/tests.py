from django.test import TestCase
from random import randint, sample
from faker import Faker
from rest_framework.test import APITestCase
from showtimes.models import Cinema


# class CinemaTestCase(APITestCase):
#
#     def setUp(self):
#         self.faker = Faker("pl_PL")
#         for _ in range(3):
#             self._create_fake_cinema()
#
#     def _fake_cinema_data(self):
#         cinema_data = {
#             "name": "{}".format(self.faker.company()),
#             "city": self.faker.city()
#         }
#         movies = sample(list(people), randint(1, len(people)))  # change
#         movie_names = [a.movie for a in movies]
#         cinema_data["movies"] = movie_names
#         print(cinema_data["name"])
#         return cinema_data
#
#     def _create_fake_cinema(self):
#         cinema_data = self._fake_cinema_data()
#         cinema_data["director"] = self._find_person_by_name(cinema_data["director"])
#         actors = cinema_data["actors"]
#         del cinema_data["actors"]
#         new_cinema = Cinema.objects.create(**cinema_data)
#         for actor in actors:
#             new_movie.actors.add(self._find_person_by_name(actor))

    # def test_add_cinema(self):
        # movies_before = Movie.objects.count()
        # new_movie = self._fake_movie_data()
        # response = self.client.post("/movies/", new_movie, format='json')
        # self.assertEqual(response.status_code, 201)
        # self.assertEqual(Movie.objects.count(), movies_before + 1)
        # for key, val in new_movie.items():
        #     self.assertIn(key, response.data)
        #     if isinstance(val, list):
        #         # Compare contents regardless of their order
        #         self.assertCountEqual(response.data[key], val)
        #     else:
        #         self.assertEqual(response.data[key], val)
