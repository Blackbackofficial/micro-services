# Microservices

## Состав
* [Store Service](store_service/README.md)
* [Order Service](order_service/README.md)
* [Warehouse Service](warehouse_service/README.md)
* [Warranty Service](warranty_service/README.md)

## Взаимодействие сервисов

![Mermaid](https://mermaid.ink/img/eyJjb2RlIjoiZ3JhcGggVERcbiAgQVtTdG9yZSBTZXJ2aWNlXS0tPiBCW09yZGVyIFNlcnZpY2VdXG4gIEFbU3RvcmUgU2VydmljZV0gLS0-IENbV2FyZWhvdXNlIFNlcnZpY2VdXG4gIEFbU3RvcmUgU2VydmljZV0gLS0-IERbV2FycmFudHkgU2VydmljZV1cbiAgQltPcmRlclNlcnZpY2VdIC0tPiBEW1dhcnJhbnR5IFNlcnZpY2VdXG4gIEJbT3JkZXJTZXJ2aWNlXSAtLT4gQ1tXYXJlaG91c2UgU2VydmljZV1cbiAgQ1tXYXJlaG91c2UgU2VydmljZV0gLS0-IERbV2FycmFudHkgU2VydmljZV0iLCJtZXJtYWlkIjp7InRoZW1lIjoiZGVmYXVsdCIsInRoZW1lVmFyaWFibGVzIjp7ImJhY2tncm91bmQiOiJ3aGl0ZSIsInByaW1hcnlDb2xvciI6IiNFQ0VDRkYiLCJzZWNvbmRhcnlDb2xvciI6IiNmZmZmZGUiLCJ0ZXJ0aWFyeUNvbG9yIjoiaHNsKDgwLCAxMDAlLCA5Ni4yNzQ1MDk4MDM5JSkiLCJwcmltYXJ5Qm9yZGVyQ29sb3IiOiJoc2woMjQwLCA2MCUsIDg2LjI3NDUwOTgwMzklKSIsInNlY29uZGFyeUJvcmRlckNvbG9yIjoiaHNsKDYwLCA2MCUsIDgzLjUyOTQxMTc2NDclKSIsInRlcnRpYXJ5Qm9yZGVyQ29sb3IiOiJoc2woODAsIDYwJSwgODYuMjc0NTA5ODAzOSUpIiwicHJpbWFyeVRleHRDb2xvciI6IiMxMzEzMDAiLCJzZWNvbmRhcnlUZXh0Q29sb3IiOiIjMDAwMDIxIiwidGVydGlhcnlUZXh0Q29sb3IiOiJyZ2IoOS41MDAwMDAwMDAxLCA5LjUwMDAwMDAwMDEsIDkuNTAwMDAwMDAwMSkiLCJsaW5lQ29sb3IiOiIjMzMzMzMzIiwidGV4dENvbG9yIjoiIzMzMyIsIm1haW5Ca2ciOiIjRUNFQ0ZGIiwic2Vjb25kQmtnIjoiI2ZmZmZkZSIsImJvcmRlcjEiOiIjOTM3MERCIiwiYm9yZGVyMiI6IiNhYWFhMzMiLCJhcnJvd2hlYWRDb2xvciI6IiMzMzMzMzMiLCJmb250RmFtaWx5IjoiXCJ0cmVidWNoZXQgbXNcIiwgdmVyZGFuYSwgYXJpYWwiLCJmb250U2l6ZSI6IjE2cHgiLCJsYWJlbEJhY2tncm91bmQiOiIjZThlOGU4Iiwibm9kZUJrZyI6IiNFQ0VDRkYiLCJub2RlQm9yZGVyIjoiIzkzNzBEQiIsImNsdXN0ZXJCa2ciOiIjZmZmZmRlIiwiY2x1c3RlckJvcmRlciI6IiNhYWFhMzMiLCJkZWZhdWx0TGlua0NvbG9yIjoiIzMzMzMzMyIsInRpdGxlQ29sb3IiOiIjMzMzIiwiZWRnZUxhYmVsQmFja2dyb3VuZCI6IiNlOGU4ZTgiLCJhY3RvckJvcmRlciI6ImhzbCgyNTkuNjI2MTY4MjI0MywgNTkuNzc2NTM2MzEyOCUsIDg3LjkwMTk2MDc4NDMlKSIsImFjdG9yQmtnIjoiI0VDRUNGRiIsImFjdG9yVGV4dENvbG9yIjoiYmxhY2siLCJhY3RvckxpbmVDb2xvciI6ImdyZXkiLCJzaWduYWxDb2xvciI6IiMzMzMiLCJzaWduYWxUZXh0Q29sb3IiOiIjMzMzIiwibGFiZWxCb3hCa2dDb2xvciI6IiNFQ0VDRkYiLCJsYWJlbEJveEJvcmRlckNvbG9yIjoiaHNsKDI1OS42MjYxNjgyMjQzLCA1OS43NzY1MzYzMTI4JSwgODcuOTAxOTYwNzg0MyUpIiwibGFiZWxUZXh0Q29sb3IiOiJibGFjayIsImxvb3BUZXh0Q29sb3IiOiJibGFjayIsIm5vdGVCb3JkZXJDb2xvciI6IiNhYWFhMzMiLCJub3RlQmtnQ29sb3IiOiIjZmZmNWFkIiwibm90ZVRleHRDb2xvciI6ImJsYWNrIiwiYWN0aXZhdGlvbkJvcmRlckNvbG9yIjoiIzY2NiIsImFjdGl2YXRpb25Ca2dDb2xvciI6IiNmNGY0ZjQiLCJzZXF1ZW5jZU51bWJlckNvbG9yIjoid2hpdGUiLCJzZWN0aW9uQmtnQ29sb3IiOiJyZ2JhKDEwMiwgMTAyLCAyNTUsIDAuNDkpIiwiYWx0U2VjdGlvbkJrZ0NvbG9yIjoid2hpdGUiLCJzZWN0aW9uQmtnQ29sb3IyIjoiI2ZmZjQwMCIsInRhc2tCb3JkZXJDb2xvciI6IiM1MzRmYmMiLCJ0YXNrQmtnQ29sb3IiOiIjOGE5MGRkIiwidGFza1RleHRMaWdodENvbG9yIjoid2hpdGUiLCJ0YXNrVGV4dENvbG9yIjoid2hpdGUiLCJ0YXNrVGV4dERhcmtDb2xvciI6ImJsYWNrIiwidGFza1RleHRPdXRzaWRlQ29sb3IiOiJibGFjayIsInRhc2tUZXh0Q2xpY2thYmxlQ29sb3IiOiIjMDAzMTYzIiwiYWN0aXZlVGFza0JvcmRlckNvbG9yIjoiIzUzNGZiYyIsImFjdGl2ZVRhc2tCa2dDb2xvciI6IiNiZmM3ZmYiLCJncmlkQ29sb3IiOiJsaWdodGdyZXkiLCJkb25lVGFza0JrZ0NvbG9yIjoibGlnaHRncmV5IiwiZG9uZVRhc2tCb3JkZXJDb2xvciI6ImdyZXkiLCJjcml0Qm9yZGVyQ29sb3IiOiIjZmY4ODg4IiwiY3JpdEJrZ0NvbG9yIjoicmVkIiwidG9kYXlMaW5lQ29sb3IiOiJyZWQiLCJsYWJlbENvbG9yIjoiYmxhY2siLCJlcnJvckJrZ0NvbG9yIjoiIzU1MjIyMiIsImVycm9yVGV4dENvbG9yIjoiIzU1MjIyMiIsImNsYXNzVGV4dCI6IiMxMzEzMDAiLCJmaWxsVHlwZTAiOiIjRUNFQ0ZGIiwiZmlsbFR5cGUxIjoiI2ZmZmZkZSIsImZpbGxUeXBlMiI6ImhzbCgzMDQsIDEwMCUsIDk2LjI3NDUwOTgwMzklKSIsImZpbGxUeXBlMyI6ImhzbCgxMjQsIDEwMCUsIDkzLjUyOTQxMTc2NDclKSIsImZpbGxUeXBlNCI6ImhzbCgxNzYsIDEwMCUsIDk2LjI3NDUwOTgwMzklKSIsImZpbGxUeXBlNSI6ImhzbCgtNCwgMTAwJSwgOTMuNTI5NDExNzY0NyUpIiwiZmlsbFR5cGU2IjoiaHNsKDgsIDEwMCUsIDk2LjI3NDUwOTgwMzklKSIsImZpbGxUeXBlNyI6ImhzbCgxODgsIDEwMCUsIDkzLjUyOTQxMTc2NDclKSJ9fSwidXBkYXRlRWRpdG9yIjpmYWxzZX0)

## Технологии 
1. `PostgreSQL`;
2. `Django`;
3. `DRF`;
4. `RabbitMQ`;
5. `health-check`;
6. `CI/CD`;
7. Pattern `DRY`, `Circuit Breaker`.

## Общая конфигурация

Все сервисы имеют health-чеки:
```shell script
curl https://self-service-app.herokuapp.com/manage/health
{
  "status": "Work",
    "components": {
      "db": {
      "status": "Work",
      "name": "store",
      "database": "PostgreSQL"
      },
      "ping": {
        "status": "Work"
      },
      "time": {
        "epoch": 1603933252,
        "local": "2020-10-29T01:00:52.658050+00:00",
        "offset": 0.4
      }
   }
}
```

## Отказоустойчивость системы
Реализованы механизмы, увеличивающие отказоустойчивость системы.

1. В случае недоступности части систем или внутренних ошибок сервера, возвращаем ошибку с пояснением 
   (т.е. HTTP статус 4xx или 5xx + json с пояснением).
   
2. Реализовано валидация входных данных. Если данные имеют некорректный формат возвращать 400 Bad Request.
   В основном это касается метода POST. Данные валидируются при помощи регулярных выражений.
   
3. Реализован паттерн `Circuit Breaker`. За это отвечает библиотека `circuitbreaker`. Накапливать статистику 
   (в памяти), и, если система не ответила 3 раза, то вместо запроса отдается `fallback` (предыдущая 
   ошибка со статикой). Через некоторый таймаут, выполняется запрос реальный к системе, чтобы проверить ее состояние.
   
4. На системе Store Service:
    * Для агрегирующего запроса на чтение (запрос #1 и #2) в случае недоступности одной из систем, выполняем деградацию 
      функциональности.
    * Для операции покупки и возврата (запрос #4 и #5) в случае недоступности одной из систем 
      выполняем полный откат операции.
    * Для запроса гарантии по заказу, в случае недоступности Warranty Service, возвращаем пользователю успешный 
      результат, а операцию ставим в очередь для повторного выполнения. Когда система, доступная в процессе операции, 
      будет поднята, операция должна быть выполнена. Для очереди используем `RabbitMQ`, на Heroku подключаем 
      через Add-Ons.