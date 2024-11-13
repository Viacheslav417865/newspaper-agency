from django.test import TestCase
from catalog.form import RedactorCreationForm, RedactorYearsUpdateForm
from catalog.models import Redactor

class RedactorCreationFormTest(TestCase):
    def test_valid_data(self):
        form_data = {
            "username": "testuser",
            "password1": "testpassword123",
            "password2": "testpassword123",
            "years_of_experience": 5,
            "first_name": "John",
            "last_name": "Doe"
        }
        form = RedactorCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_years_of_experience(self):
        form_data = {
            "username": "testuser",
            "password1": "testpassword123",
            "password2": "testpassword123",
            "years_of_experience": 100,
            "first_name": "John",
            "last_name": "Doe",
        }
        form = RedactorCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("years_of_experience", form.errors)

    def test_password_mismatch(self):
        form_data = {
            "username": "testuser",
            "password1": "testpassword123",
            "password2": "testpassword321",  # Mismatched passwords
            "years_of_experience": 5,
            "first_name": "John",
            "last_name": "Doe"
        }
        form = RedactorCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)  # Ensure password mismatch is caught


class RedactorYearsUpdateFormTest(TestCase):
    def test_valid_data(self):
        redactor = Redactor.objects.create_user(
            username="existinguser", password="password123"
        )
        form_data = {"years_of_experience": 10}
        form = RedactorYearsUpdateForm(data=form_data, instance=redactor)
        self.assertTrue(form.is_valid())

    def test_invalid_years_of_experience(self):
        redactor = Redactor.objects.create_user(
            username="existinguser", password="password123"
        )
        form_data = {"years_of_experience": 100}  # Invalid years of experience
        form = RedactorYearsUpdateForm(data=form_data, instance=redactor)
        self.assertFalse(form.is_valid())
        self.assertIn("years_of_experience", form.errors)
