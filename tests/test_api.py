import pytest


pytestmark = pytest.mark.anyio


# class TestCalculateAPI:
#     """Test /api/calculate API"""
#     # @pytest.mark.anyio
#     async def test_first_day_of_month(self, client):
#         """Testing correct output first day of month"""
#         req = {
#             "date": "01.01.2021",
#             "periods": 3,
#             "amount": 10000,
#             "rate": 6
#         }
#         resp = {
#             "01.01.2021": 10050.0,
#             "01.02.2021": 10100.25,
#             "01.03.2021": 10150.75
#         }
#         # async with AsyncClient(app=server.app, base_url="http://0.0.0.0:8000/") as ac:
#         #     response = await ac.post("/api/calculate", json=req)
#         response = await client.post("/api/calculate", json=req)
#         assert response.status_code == 200
#         assert response.json() == resp
#
#     def test_last_day_of_month(self, test_app):
#         """
#         Testing correct output of last day of month,
#         include correct output of February
#         """
#         req = {
#             "date": "31.01.2021",
#             "periods": 3,
#             "amount": 10000,
#             "rate": 6
#         }
#         resp = {
#             "31.01.2021": 10050.0,
#             "28.02.2021": 10100.25,
#             "31.03.2021": 10150.75
#         }
#         response = test_app.post("/api/calculate", json=req)
#         assert response.status_code == 200
#         assert response.json() == resp
#
#     def test_not_valid_date(self, test_app):
#         """Testing not a valid date format."""
#         req = {
#             "date": "31012021",
#             "periods": 3,
#             "amount": 10000,
#             "rate": 6
#         }
#         resp = {
#             "detail": "You should provide date in format: dd.mm.YYYY"
#         }
#         response = test_app.post("/api/calculate", json=req)
#         assert response.status_code == 400
#         assert response.json() == resp
#
#     def test_not_valid_periods(self, test_app):
#         """Testing not valid periods"""
#         req = {
#             "date": "31.01.2021",
#             "periods": 333,
#             "amount": 10000,
#             "rate": 6
#         }
#         resp = {
#             "error": 'Field [periods] - ensure this value is less than or equal to 60'
#         }
#         response = test_app.post("/api/calculate", json=req)
#         assert response.status_code == 400
#         assert response.json() == resp
#
#     def test_not_valid_amount(self, test_app):
#         """Testing not valid amount"""
#         req = {
#             "date": "31.01.2021",
#             "periods": 3,
#             "amount": 1000000000000,
#             "rate": 6
#         }
#         resp = {
#             "error": 'Field [amount] - ensure this value is less than or equal to 3000000'
#         }
#         response = test_app.post("/api/calculate", json=req)
#         assert response.status_code == 400
#         assert response.json() == resp
#
#     def test_not_valid_rate(self, test_app):
#         """Testing not valid rate"""
#         req = {
#             "date": "31.01.2021",
#             "periods": 3,
#             "amount": 10000,
#             "rate": 66
#         }
#         resp = {
#             "error": 'Field [rate] - ensure this value is less than or equal to 8.0'
#         }
#         response = test_app.post("/api/calculate", json=req)
#         assert response.status_code == 400
#         assert response.json() == resp
#
#     def test_empty_json(self, test_app):
#         """Testing if no data was provided."""
#         req = {}
#         resp = {
#             "error": 'Field [date] - field required'
#         }
#         response = test_app.post("/api/calculate", json=req)
#         assert response.status_code == 400
#         assert response.json() == resp
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
        resp = {
            "01.01.2021": 10050.0,
            "01.02.2021": 10100.25,
            "01.03.2021": 10150.75
        }
        # async with AsyncClient(app=server.app, base_url="http://0.0.0.0:8000/") as ac:
        #     response = await ac.post("/api/calculate", json=req)
        response = await client.post("/api/calculate", json=req)
        assert response.status_code == 200
        assert response.json() == resp

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
        resp = {
            "31.01.2021": 10050.0,
            "28.02.2021": 10100.25,
            "31.03.2021": 10150.75
        }
        response = await client.post("/api/calculate", json=req)
        assert response.status_code == 200
        assert response.json() == resp

    async def test_not_valid_date(self, client):
        """Testing not a valid date format."""
        req = {
            "date": "31012021",
            "periods": 3,
            "amount": 10000,
            "rate": 6
        }
        resp = {
            "detail": "You should provide date in format: dd.mm.YYYY"
        }
        response = await client.post("/api/calculate", json=req)
        assert response.status_code == 400
        assert response.json() == resp

    async def test_not_valid_periods(self, client):
        """Testing not valid periods"""
        req = {
            "date": "31.01.2021",
            "periods": 333,
            "amount": 10000,
            "rate": 6
        }
        resp = {
            "error": 'Field [periods] - ensure this value is less than or equal to 60'
        }
        response = await client.post("/api/calculate", json=req)
        assert response.status_code == 400
        assert response.json() == resp

    async def test_not_valid_amount(self, client):
        """Testing not valid amount"""
        req = {
            "date": "31.01.2021",
            "periods": 3,
            "amount": 1000000000000,
            "rate": 6
        }
        resp = {
            "error": 'Field [amount] - ensure this value is less than or equal to 3000000'
        }
        response = await client.post("/api/calculate", json=req)
        assert response.status_code == 400
        assert response.json() == resp

    async def test_not_valid_rate(self, client):
        """Testing not valid rate"""
        req = {
            "date": "31.01.2021",
            "periods": 3,
            "amount": 10000,
            "rate": 66
        }
        resp = {
            "error": 'Field [rate] - ensure this value is less than or equal to 8.0'
        }
        response = await client.post("/api/calculate", json=req)
        assert response.status_code == 400
        assert response.json() == resp

    async def test_empty_json(self, client):
        """Testing if no data was provided."""
        req = {}
        resp = {
            "error": 'Field [date] - field required'
        }
        response = await client.post("/api/calculate", json=req)
        assert response.status_code == 400
        assert response.json() == resp


class TestMortgageCRUD:

    async def test_create_bank(self, client):
        req = {
            "bank_name": "Test_bank_name",
            "term_min": 10,
            "term_max": 30,
            "rate_min": 1.8,
            "rate_max": 9.8,
            "payment_min": 1000000,
            "payment_max": 10000000
        }
        resp = {
            "id": 1,
            "bank_name": "Test_bank_name",
            "term_min": 10,
            "term_max": 30,
            "rate_min": 1.8,
            "rate_max": 9.8,
            "payment_min": 1000000,
            "payment_max": 10000000
        }
        # async with AsyncClient(app=server.app, base_url="http://test") as ac:
        #     response = await ac.post("/api/banks", json=req)
        response = await client.post("/api/banks", json=req)
        assert response.status_code == 200
        assert response.json() == resp

    async def test_get_bank(self, client):
        resp = {
            "bank_name": "VTB",
            "term_min": 10,
            "term_max": 30,
            "rate_min": 1.8,
            "rate_max": 9.8,
            "payment_min": 1000000,
            "payment_max": 10000000
        }
        # async with AsyncClient(app=server.app, base_url="http://test") as ac:
        #     response = await ac.get("/api/banks/1")
        response = await client.get("/api/banks/1")
        assert response.status_code == 200
        assert response.json() == resp
