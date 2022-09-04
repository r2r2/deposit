# Calculate deposit 

***  

### To start project:
> docker-compose pull && docker-compose build --no-cache && docker-compose up

### To check API:
> curl -i -H "Content-Type: application/json" -d '{ "date": "31.01.2021", "periods": 3, "amount": 10000, "rate": 6 }' http://0.0.0.0:8000/calculate

### Test coverage
> pdm run coverage report -m

| Name                         |Stmts  | Miss | Cover  | Missing|
|------------------------------|-------|------|--------|------- |
| core/__init__.py             |    0  |    0 | 100%   |        |
| core/dto/__init__.py         |   0   |   0  | 100%   |        |
| core/dto/dto.py              |    6  |   0  | 100%   |        |
| core/errors/__init__.py      |    0  |   0  | 100%   |        |
| core/errors/error_handler.py |    6  |   0  | 100%   |        |
| core/errors/exceptions.py    |    8  |   0  | 100%   |        |
| core/server/__init__.py      |    0  |   0  | 100%   |        |
| core/server/api.py           |   17  |   0  | 100%   |        |
| core/server/server.py        |   20  |   1  | 95%    |25      |
| settings.py                  |    9  |   0  | 100%   |        |
| tests/__init__.py            |    0  |   0  | 100%   |        |
| tests/conftest.py            |    7  |   0  | 100%   |        |
| tests/test_api.py            |   37  |   0  | 100%   |        |
| TOTAL                        |  110  |   1  | 99%    |        |

