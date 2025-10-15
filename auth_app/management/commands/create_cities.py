from django.core.management import BaseCommand
import requests
from auth_app.models import Provinces , Cities


class Command(BaseCommand):
    help = "Create Provinces and Cities"
    provinces_url = "https://iranplacesapi.liara.run/api/provinces"
    cities_url = "https://iranplacesapi.liara.run/api/cities"

    def handle(self, *args, **options):
        try:
            self.stdout.write("Start extracting from api")
            provinces_response = requests.get(self.provinces_url)
            provinces_response.raise_for_status()
            provinces_data = provinces_response.json()

            for province_data in provinces_data:
                try:
                    province , created = Provinces.objects.get_or_create(
                    id = province_data["id"],
                    defaults={'name':province_data['name']}
                )
                except Provinces.DoesNotExist:
                    self.stdout.write("Province not found")
            self.stdout.write("Creating Province successfuly")

            cities_response = requests.get(self.cities_url)
            cities_response.raise_for_status()
            cities_datas = cities_response.json()

            for city_data in cities_datas:
                get_province = Provinces.objects.get(id = city_data["province_id"])
                try:
                    city , created = Cities.objects.get_or_create(
                        id = city_data["id"],
                        province = get_province,
                        defaults={'name':city_data['name']}
                    )
                except Cities.DoesNotExist:
                    self.stdout.write(f"Province with id {city_data['province_id']} not found for city {city_data['name']}")
                except Exception as e:
                    self.stdout.write(f"Error creting city {city_data['name']} : {str(e)}")
            self.stdout.write("Creating Cities successfuly")

        except requests.RequestException as e:
            self.stdout.write(f"Request Error {e}")
