# Warehouse Service

## Описание API
1. `GET /manage/health` – Swagger API;
2. `GET /api/v1/warehouse/{itemUid}` – информация о вещах на складе;
3. `POST /api/v1/warehouse` – запрос на получение вещи со склада по новому заказу;
4. `POST /api/v1/warehouse/{itemUid}/self` – запрос решения по гарантии;
5. `DELETE /api/v1/warehouse/{itemUid}` – вернуть заказ на склад.


## Логика работы
Таблица `items` содержит информацию о товарах на складе (модель, размер, количество),
`order_items` содержит связь товара на складе с заказом. Если приходит заказ (метод 2), то количество товара `items`
уменьшается и создается запись в таблице `order_items`. Если заказ отменяется, то количество `items` увеличивается,
а для `order_items` устанавливается флаг `closed`.

## Структура таблиц
```postgresql
CREATE TABLE items
(
    id              SERIAL CONSTRAINT items_pkey PRIMARY KEY,
    available_count INTEGER      NOT NULL,
    model           VARCHAR(255) NOT NULL,
    size            VARCHAR(255) NOT NULL
);

CREATE TABLE order_item
(
    id             SERIAL CONSTRAINT order_item_pkey PRIMARY KEY,
    canceled       BOOLEAN,
    order_item_uid UUID NOT NULL CONSTRAINT idx_order_item_order_item_uid UNIQUE,
    order_uid      UUID NOT NULL,
    item_id        INTEGER CONSTRAINT fk_order_item_item_id REFERENCES items
);
```