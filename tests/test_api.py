class TestCalculate:

    def test_calculate_ok(self, test_app):
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
        response = test_app.post("/calculate", json=req)
        assert response.status_code == 200
        assert response.json() == resp

    def test_not_valid_date(self, test_app):
        req = {
            "date": "31012021",
            "periods": 3,
            "amount": 10000,
            "rate": 6
        }
        resp = {
            "detail": "You should provide date in format: dd.mm.YYYY"
        }
        response = test_app.post("/calculate", json=req)
        assert response.status_code == 400
        assert response.json() == resp

    def test_not_valid_periods(self, test_app):
        req = {
            "date": "31.01.2021",
            "periods": 333,
            "amount": 10000,
            "rate": 6
        }
        resp = {
            "error": 'Field [periods] - ensure this value is less than or equal to 60'
        }
        response = test_app.post("/calculate", json=req)
        assert response.status_code == 400
        assert response.json() == resp

    def test_not_valid_amount(self, test_app):
        req = {
            "date": "31.01.2021",
            "periods": 3,
            "amount": 1000000000000,
            "rate": 6
        }
        resp = {
            "error": 'Field [amount] - ensure this value is less than or equal to 3000000'
        }
        response = test_app.post("/calculate", json=req)
        assert response.status_code == 400
        assert response.json() == resp

    def test_not_valid_rate(self, test_app):
        req = {
            "date": "31.01.2021",
            "periods": 3,
            "amount": 10000,
            "rate": 66
        }
        resp = {
            "error": 'Field [rate] - ensure this value is less than or equal to 8.0'
        }
        response = test_app.post("/calculate", json=req)
        assert response.status_code == 400
        assert response.json() == resp

    def test_empty_json(self, test_app):
        req = {}
        resp = {
            "error": 'Field [date] - field required'
        }
        response = test_app.post("/calculate", json=req)
        assert response.status_code == 400
        assert response.json() == resp
