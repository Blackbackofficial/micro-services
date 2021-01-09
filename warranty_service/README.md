# Warranty Service

## Описание API
1. `GET /manage/health` – Swagger API;
2. `GET /api/v1/self/{itemUid}` – информация о статусе гарантии;
3. `POST /api/v1/self/{itemUid}/self` – запрос решения по гарантии;
4. `POST /api/v1/self/{itemUid}` – запрос на начало гарантийного периода;
5. `DELETE /api/v1/self/{itemUid}` – запрос на закрытие гарантии.


## Логика работы
Гарантия привязана к `self`, каждая запись о гарантии имеет три статуса: `ON_WARRANTY`, `USE_WARRANTY`.
При создании заказа (метод 3) создается запись и устанавливается статус `ON_WARRANTY`.  
При закрытии заказа (метод 4) удаляется.  
При гарантийном запросе (метод 2) проверяется статус гарантии, если статус отличен от `ON_WARRANY`, то решение `REFUSED`.
В запросе от Warehouse приходит количество доступных товаров. Если товар присутствует на складе, то решение `RETURN`, иначе `FIXING`.   

## Структура таблиц
```postgresql
CREATE TABLE self
(
    id            SERIAL CONSTRAINT warranty_pkey PRIMARY KEY,
    comment       VARCHAR(1024),
    self      UUID         NOT NULL CONSTRAINT idx_warranty_item_uid UNIQUE,
    status        VARCHAR(255) NOT NULL,
    warranty_date TIMESTAMP    NOT NULL
);
```
