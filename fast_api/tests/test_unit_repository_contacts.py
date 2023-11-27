from sqlalchemy.orm import Session

import unittest
from unittest.mock import MagicMock, patch

from faker import Faker

from src.database.models import User, Contact
from src.schemas import ContactBase, ContactResponse
from src.repository.contacts import (
    get_contact_by_email,
    get_contact_by_id,
    get_contacts,
    create,
    update,
)

fake = Faker()


class TestContactsRepository(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1, email="test@test.com")

    async def test_get_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter_by().all.return_value = contacts
        result = await get_contacts(self.session, self.user)
        self.assertEqual(result, contacts)

    async def test_get_contact_by_id(self):
        contact_id = 1
        user_id = self.user.id
        expected_contact = Contact(id=contact_id, user_id=user_id)

        self.session.query(Contact).filter_by(
            id=contact_id, user_id=user_id
        ).first.return_value = expected_contact

        result = await get_contact_by_id(contact_id, user_id, self.session)

        self.assertEqual(result, expected_contact)

    async def test_get_contact_by_email(self):
        user_id = self.user.id
        email = "test@example.com"
        expected_contact = Contact(email=email, user_id=user_id)
        self.session.query(Contact).filter_by(
            email=email, user_id=user_id
        ).first.return_value = expected_contact
        result = await get_contact_by_email(email, user_id, self.session)
        self.assertEqual(result, expected_contact)

    async def test_create(self):
        body = ContactBase(
            id=1,
            first_name="John",
            last_name="Mnemonick",
            email="Johnys@email.net",
            phone_number="80129992233",
            birth_date=fake.date(),
            created_at=fake.date_time_this_year(),
            updated_at=fake.date_time_this_year(),
        )

        # test свариться, що багато user_id передаю
        body_data = body.model_dump()
        body_data.pop("user_id", None)

        result = await create(body_data, self.session, self.user)
        self.assertEqual(result.first_name, body.first_name)
        self.assertTrue(hasattr(result, "id"))

    async def test_update_contact(self):
        contact_id = 1
        user_id = self.user.id
        email = "old@example.com"
        contact = Contact(id=contact_id, email=email, user_id=user_id)

        with patch(
            "src.repository.contacts.get_contact_by_id"
        ) as mock_get_contact_by_id:
            mock_get_contact_by_id.return_value = contact

            new_email = "new@example.com"
            body = ContactBase(
                id=contact_id,
                email=new_email,
                first_name="Sulan",
                last_name="Rkira",
                phone_number="646646466",
                birth_date=fake.date(),
                additional_data="",
                created_at=fake.date_time_this_year(),
                updated_at=fake.date_time_this_year(),
            )

            updated_contact = await update(contact_id, body, user_id, self.session)

            self.assertEqual(updated_contact.email, new_email)
            self.assertTrue(self.session.commit.called)
