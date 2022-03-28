# Order Service

## API Description
1. `GET /manage/health` - Swagger API;
1. `POST /api/v1/orders/{userUid}` – place an order on behalf of the user;
1. `GET /api/v1/orders/{userUid}/{orderUid}` – get information on a specific user order;
1. `GET /api/v1/orders/{userUid}` – get all user orders;
1. `POST /api/v1/orders/{orderUid}/warranty` – order warranty request;
1. `DELETE /api/v1/orders/{orderUid}` – return an order.


## Operation logic
The service is responsible for working with the order, receiving the goods from the warehouse (request to Warehouse) and creating a guarantee (request to Warranty).
When requesting, the order `order` is obtained, from it we get `item_uid` and with this parameter the necessary requests to Warehouse and Warranty are performed.

## Table structure
```postgresql
CREATE TABLE orders
(
    id SERIAL CONSTRAINT orders_pkey PRIMARY KEY,
    item_uid UUID NOT NULL,
    order_date TIMESTAMP NOT NULL,
    order_uid UUID NOT NULL CONSTRAINT idx_orders_order_uid UNIQUE,
    status VARCHAR(255) NOT NULL,
    user_uid UUID NOT NULL
);
```
