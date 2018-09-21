from random import randint, sample, choice
from faker import Faker
from rest_framework.test import APITestCase
from movielist.models import Person, Movie
from showtimes.models import Cinema, Screening

fake = Faker()


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


class ScreeningTestCase(APITestCase):
    number_of_objects = 3
    
    def setUp(self):
        self.faker = Faker("pl_PL")

        # Fake cinema for screenings
        cinema_data = {
            "name": "{}".format(self.faker.company()),
            "city": self.faker.city()
        }
        new_cinema = Cinema.objects.create(**cinema_data)

        # Fake people for movies
        for _ in range(5):
            Person.objects.create(name=self.faker.name())

        # Fake movies for screenings
        for _ in range(self.number_of_objects):
            movie_data = {
                "title": "{} {}".format(self.faker.job(),
                                        self.faker.first_name()),
                "description": self.faker.sentence(),
                "year": int(self.faker.year()),
                "director": self._random_person().name,
            }
            people = Person.objects.all()
            actors = sample(list(people), randint(1, len(people)))
            actor_names = [a.name for a in actors]
            movie_data["actors"] = actor_names
            movie_data["director"] = self._find_person_by_name(
                movie_data["director"]
            )
            actors = movie_data["actors"]
            del movie_data["actors"]
            new_movie = Movie.objects.create(**movie_data)
            for actor in actors:
                new_movie.actors.add(self._find_person_by_name(actor))

        # Screenings
        for _ in range(self.number_of_objects):
            self._create_fake_screening()

    def _random_person(self):
        """Return a random Person object from db."""
        people = Person.objects.all()
        return people[randint(0, len(people) - 1)]

    def _find_person_by_name(self, name):
        """Return the first `Person` object that matches `name`."""
        return Person.objects.filter(name=name).first()

    def _fake_screening_data(self):
        """
        Creates fake screening dictionary.
        """
        screening_data = {
            "cinema": Cinema.objects.first().name,
            "movie": choice(Movie.objects.all()).title,
            "date": fake.date_time_this_year()
        }
        return screening_data

    def _create_fake_screening(self):
        """
        Saves the fake screening to the database.
        """
        screening_data = self._fake_screening_data()
        screening_data["movie"] = Movie.objects.get(
            title=screening_data["movie"]
        )
        screening_data["cinema"] = Cinema.objects.get(
            name=screening_data["cinema"]
        )

        new_screening = Screening.objects.create(**screening_data)

    def test_get_screening_list(self):
        response = self.client.get("/screenings/", {}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Screening.objects.count(), len(response.data))

    def test_get_screening_detail(self):
        response = self.client.get(
            f"""/screenings/{Screening.objects.first().id}/""",
            {},
            format='json'
        )
        self.assertEqual(response.status_code, 200)
        for field in ["cinema", "movie", "date"]:
            self.assertIn(field, response.data)

    def test_add_screening(self):
        """
        Tests adding a new screening using POST.

        """
        screening_count = Screening.objects.count()

        new_screening = self._fake_screening_data()
        response = self.client.post(
            "/screenings/", new_screening, format='json'
        )
        self.assertEqual(response.status_code, 201)

        self.assertEqual(Screening.objects.count(), screening_count + 1)

        # Check if db contents match the original dictionary
        for key, val in new_screening.items():
            self.assertIn(key, response.data)
            if isinstance(val, list):
                self.assertCountEqual(response.data[key], val)
            else:
                if key == "date":
                    self.assertEqual(response.data[key], val.isoformat() + "Z")
                else:
                    self.assertEqual(response.data[key], val)

    def test_delete_screening(self):
        """
        Tests removal of a screening.
        """
        screening_count = Screening.objects.count()

        last_screening = Screening.objects.last()

        response = self.client.delete(
            f"/screenings/{last_screening.id}", {}, format="json"
        )
        self.assertEqual(response.status_code, 204)
        self.assertNotEqual(screening_count, Screening.objects.count())
