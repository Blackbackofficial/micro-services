# Warehouse Service

## API Description
1. `GET /manage/health` - Swagger API;
2. `GET /api/v1/warehouse/{itemUid}` – information about items in the warehouse;
3. `POST /api/v1/warehouse` - a request to receive an item from the warehouse for a new order;
4. `POST /api/v1/warehouse/{itemUid}/warranty` – request for a warranty decision;
5. `DELETE /api/v1/warehouse/{itemUid}` – return the order to the warehouse.


## Operation logic
The `items` table contains information about the goods in stock (model, size, quantity),
`order_items` contains the relation of the item in stock to the order. If an order arrives (method 2), then the quantity of goods `items`
is decremented and an entry is created in the `order_items` table. If the order is canceled, then the number of `items` is increased,
and `order_items` is set to the `closed` flag.

## Table structure
```postgresql
CREATE TABLE items
(
    id SERIAL CONSTRAINT items_pkey PRIMARY KEY,
    available_count INTEGER NOT NULL,
    model VARCHAR(255) NOT NULL,
    VARCHAR(255) NOT NULL
);

CREATE TABLE order_item
(
    id SERIAL CONSTRAINT order_item_pkey PRIMARY KEY,
    canceled BOOLEAN,
    order_item_uid UUID NOT NULL CONSTRAINT idx_order_item_order_item_uid UNIQUE,
    order_uid UUID NOT NULL,
    item_id INTEGER CONSTRAINT fk_order_item_item_id REFERENCES items
);
```
