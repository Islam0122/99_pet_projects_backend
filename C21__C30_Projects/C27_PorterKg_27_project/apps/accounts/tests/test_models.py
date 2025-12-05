from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.accounts.models import GuestProfile, DriverProfile, Car, CarImage

User = get_user_model()


class UserModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            first_name='Test',
            last_name='User',
            password='testpass123',
            role='guest'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.full_name, 'Test User')
        self.assertTrue(self.user.check_password('testpass123'))

    def test_user_str(self):
        self.assertEqual(str(self.user), 'test@example.com')

    def test_is_guest_method(self):
        self.assertTrue(self.user.is_guest())
        self.assertFalse(self.user.is_driver())


class GuestProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='guest@example.com',
            first_name='Guest',
            last_name='User',
            password='testpass123',
            role='guest'
        )
        self.profile = GuestProfile.objects.create(
            user=self.user,
            phone_number='+996555123456'
        )

    def test_profile_creation(self):
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.phone_number, '+996555123456')

    def test_has_complete_profile(self):
        self.assertFalse(self.profile.has_complete_profile)

        from datetime import date
        self.profile.birth_date = date(1990, 1, 1)
        self.profile.save()

        self.assertTrue(self.profile.has_complete_profile)


class DriverProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='driver@example.com',
            first_name='Driver',
            last_name='User',
            password='testpass123',
            role='driver'
        )
        self.profile = DriverProfile.objects.create(
            user=self.user,
            phone_number='+996555123456',
            driver_license_number='ABC123456',
            driver_license_category='B',
            experience_years=5
        )

    def test_profile_creation(self):
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.rating, 100.0)
        self.assertEqual(self.profile.total_trips, 0)

    def test_update_rating(self):
        self.profile.total_trips = 10
        self.profile.update_rating(95.0)

        expected_rating = (100.0 * 10 + 95.0) / 11
        self.assertAlmostEqual(self.profile.rating, expected_rating, places=2)

    def test_increment_trips(self):
        initial_trips = self.profile.total_trips
        self.profile.increment_trips()
        self.assertEqual(self.profile.total_trips, initial_trips + 1)


class CarModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='driver@example.com',
            first_name='Driver',
            last_name='User',
            password='testpass123',
            role='driver'
        )
        self.driver_profile = DriverProfile.objects.create(
            user=self.user,
            phone_number='+996555123456',
            driver_license_number='ABC123456',
            driver_license_category='B'
        )
        self.car = Car.objects.create(
            driver=self.driver_profile,
            marka='Toyota',
            model='Camry',
            color='Черный',
            year=2020,
            number_plate='01ABC123'
        )

    def test_car_creation(self):
        self.assertEqual(self.car.marka, 'Toyota')
        self.assertEqual(self.car.full_name, 'Toyota Camry 2020')

    def test_car_activation(self):
        self.assertTrue(self.car.is_active)

        self.car.deactivate()
        self.assertFalse(self.car.is_active)

        self.car.activate()
        self.assertTrue(self.car.is_active)