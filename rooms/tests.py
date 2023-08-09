from rest_framework.test import APITestCase
from .models import Amenity


class TestAmenities(APITestCase):
    name = "Amenity Name"
    description = "Amenity Description"
    url = "/api/v1/rooms/amenities/"

    def setUp(self):
        Amenity.objects.create(
            name=self.name,
            description=self.description,
        )

    def test_get(self):
        response = self.client.get(self.url)
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertIsInstance(data[0], dict)
        self.assertEqual(len(data[0]), 2)
        self.assertEqual(data[0]["name"], self.name)
        self.assertEqual(data[0]["description"], self.description)

    def test_post(self):
        # Valid POST
        new_amenity_name = "New Amenity Name"
        new_amenity_description = "New Amenity Description"

        response = self.client.post(
            self.url,
            data={
                "name": new_amenity_name,
                "description": new_amenity_description,
            },
        )
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["name"], new_amenity_name)
        self.assertEqual(data["description"], new_amenity_description)

        # Invalid POST: "name" field has no more than 50 characters
        response = self.client.post(
            self.url,
            data={
                "name": "123456789012345678901234567890123456789012345678901",
                "description": new_amenity_description,
            },
        )
        data = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertIn("name", data)

        # Invalid POST: "description" field has no more than 100 characters
        response = self.client.post(
            self.url,
            data={
                "name": new_amenity_name,
                "description": "12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901",
            },
        )
        data = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertIn("description", data)

        # Invalid POST: "name" field is required
        response = self.client.post(self.url)
        data = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertIn("name", data)


class TestAmenityDetail(APITestCase):
    name = "Amenity Name"
    description = "Amenity Description"
    url = "/api/v1/rooms/amenities/1"

    def setUp(self):
        Amenity.objects.create(
            name=self.name,
            description=self.description,
        )

    def test_get_object(self):
        # Invalid PK
        response = self.client.get("/api/v1/rooms/amenities/2")

        self.assertEqual(response.status_code, 404)

    def test_get(self):
        response = self.client.get(self.url)
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["name"], self.name)
        self.assertEqual(data["description"], self.description)

    def test_put(self):
        # Valid PUT
        updated_amenity_name = "Updated Amenity Name"
        updated_amenity_description = "Updated Amenity Description"

        response = self.client.put(
            self.url,
            data={
                "name": updated_amenity_name,
                "description": updated_amenity_description,
            },
        )
        data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["name"], updated_amenity_name)
        self.assertEqual(data["description"], updated_amenity_description)

        # Invalid PUT: "name" field has no more than 50 characters
        response = self.client.put(
            self.url,
            data={
                "name": "123456789012345678901234567890123456789012345678901",
                "description": updated_amenity_description,
            },
        )
        data = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertIn("name", data)

        # Invalid PUT: "description" field has no more than 100 characters
        response = self.client.put(
            self.url,
            data={
                "name": updated_amenity_name,
                "description": "12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901",
            },
        )
        data = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertIn("description", data)

        # Invalid PUT: "name" field is required
        response = self.client.put(self.url)
        data = response.json()

        self.assertEqual(response.status_code, 400)
        self.assertIn("name", data)

    def test_delete(self):
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, 204)
