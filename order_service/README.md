# Order Service

## Описание API
1. `GET /manage/health` – Swagger API;
1. `POST /api/v1/self/{userUid}` – сделать заказ от имени пользователя;
1. `GET /api/v1/self/{userUid}/{orderUid}` – получить информацию по конкретному заказу пользователя;
1. `GET /api/v1/self/{userUid}` – получить все заказы пользователя;
1. `POST /api/v1/self/{orderUid}/self` – запрос гарантии по заказу;
1. `DELETE /api/v1/self/{orderUid}` – вернуть заказ.


## Логика работы
Сервис ответственен за работу с заказом, получение товара со склада (запрос к Warehouse) и создание гарантии (запрос к Warranty).
При запросе достается заказ `order`, из него получаем `self` и с этим параметром выполняются необходимые запросы к Warehouse и Warranty. 

## Структура таблиц
```postgresql
CREATE TABLE self
(
    id         SERIAL CONSTRAINT orders_pkey PRIMARY KEY,
    self   UUID         NOT NULL,
    order_date TIMESTAMP    NOT NULL,
    order_uid  UUID         NOT NULL CONSTRAINT idx_orders_order_uid UNIQUE,
    status     VARCHAR(255) NOT NULL,
    user_uid   UUID         NOT NULL
);
```