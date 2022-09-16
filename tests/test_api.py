import pytest


pytestmark = pytest.mark.anyio


class TestCalculateAPI:
    """Test /api/calculate API"""
    async def test_first_day_of_month(self, client):
        """Testing correct output first day of month"""
        req = {
            "date": "01.01.2021",
            "periods": 3,
            "amount": 10000,
            "rate": 6
        }
        expected = {
            "01.01.2021": 10050.0,
            "01.02.2021": 10100.25,
            "01.03.2021": 10150.75
        }
        response = await client.post("/api/calculate", json=req)
        assert response.status_code == 200
        assert response.json() == expected

    async def test_last_day_of_month(self, client):
        """
        Testing correct output of last day of month,
        include correct output of February
        """
        req = {
            "date": "31.01.2021",
            "periods": 3,
            "amount": 10000,
            "rate": 6
        }
        expected = {
            "31.01.2021": 10050.0,
            "28.02.2021": 10100.25,
            "31.03.2021": 10150.75
        }
        response = await client.post("/api/calculate", json=req)
        assert response.status_code == 200
        assert response.json() == expected

    async def test_not_valid_date(self, client):
        """Testing not a valid date format."""
        req = {
            "date": "31012021",
            "periods": 3,
            "amount": 10000,
            "rate": 6
        }
        expected = {
            "detail": "You should provide date in format: dd.mm.YYYY"
        }
        response = await client.post("/api/calculate", json=req)
        assert response.status_code == 400
        assert response.json() == expected

    async def test_not_valid_periods(self, client):
        """Testing not valid periods"""
        req = {
            "date": "31.01.2021",
            "periods": 333,
            "amount": 10000,
            "rate": 6
        }
        expected = {
            "error": 'Field [periods] - ensure this value is less than or equal to 60'
        }
        response = await client.post("/api/calculate", json=req)
        assert response.status_code == 400
        assert response.json() == expected

    async def test_not_valid_amount(self, client):
        """Testing not valid amount"""
        req = {
            "date": "31.01.2021",
            "periods": 3,
            "amount": 1000000000000,
            "rate": 6
        }
        expected = {
            "error": 'Field [amount] - ensure this value is less than or equal to 3000000'
        }
        response = await client.post("/api/calculate", json=req)
        assert response.status_code == 400
        assert response.json() == expected

    async def test_not_valid_rate(self, client):
        """Testing not valid rate"""
        req = {
            "date": "31.01.2021",
            "periods": 3,
            "amount": 10000,
            "rate": 66
        }
        expected = {
            "error": 'Field [rate] - ensure this value is less than or equal to 8.0'
        }
        response = await client.post("/api/calculate", json=req)
        assert response.status_code == 400
        assert response.json() == expected

    async def test_empty_json(self, client):
        """Testing if no data was provided."""
        req = dict()
        expected = {
            "error": 'Field [date] - field required'
        }
        response = await client.post("/api/calculate", json=req)
        assert response.status_code == 400
        assert response.json() == expected


class TestMortgageCRUD:

    async def test_create_bank(self, client, db):
        req = {
            "bank_name": "Test_bank_name",
            "term_min": 10,
            "term_max": 30,
            "rate_min": 1.8,
            "rate_max": 9.8,
            "payment_min": 1000000,
            "payment_max": 10000000
        }
        expected = {
            "payment": None,
            "bank_name": "Test_bank_name",
            "term_min": 10,
            "term_max": 30,
            "rate_min": 1.8,
            "rate_max": 9.8,
            "payment_min": 1000000,
            "payment_max": 10000000
        }
        response = await client.post("/api/banks", json=req)
        assert response.status_code == 200
        bank_id = response.json().pop('id')
        expected.update({"id": bank_id})
        assert response.json() == expected

        response = await client.get(f"/api/banks/{bank_id}")
        assert response.status_code == 200
        expected.pop("id"), expected.pop("payment")
        assert response.json() == expected

    # async def test_get_bank(self, client, db):
    #     expected = {
    #         "bank_name": "Test_bank_name",
    #         "term_min": 10,
    #         "term_max": 30,
    #         "rate_min": 1.8,
    #         "rate_max": 9.8,
    #         "payment_min": 1000000,
    #         "payment_max": 10000000
    #     }
    #     response = await client.get("/api/banks/1")
    #     assert response.status_code == 200
    #     expected.pop("id"), expected.pop("payment")
    #     assert response.json() == expected
