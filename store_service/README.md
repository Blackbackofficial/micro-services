# Store Service

## API Description
1. `GET /manage/health` - Swagger API;
1. `GET /api/v1/store/{userUid}/orders` – get a list of user orders;
1. `GET /api/v1/store/{userUid}/{orderUid}` – information on a specific order;
1. `POST /api/v1/store/{userUid}/{orderUid}/warranty` – order warranty request;
1. `POST /api/v1/store/{userUid}/purchase` – make a purchase;
1. `DELETE /api/v1/store/{userUid}/{orderUid}/refund` – return an order;


## Operation logic
The service is a kind of gateway, all requests go through it on behalf of the user.
Order information is collected from the Order Service, and then optionally from the Warehouse and Warranty Service.
The remaining methods check the user and delegate the request further to the OrderService, because all information about the order is stored there.

## Table structure
```postgresql
CREATE TABLE users
(
    id SERIAL CONSTRAINT users_pkey PRIMARY KEY,
    name VARCHAR(255) NOT NULL CONSTRAINT idx_user_name UNIQUE,
    user_uid UUID NOT NULL CONSTRAINT idx_user_user_uid UNIQUE
);
```

## Data in the database
 id | name |user_uid
--- | ---- | ---
 1 | Alex |6d2cb5a0-943c-4b96-9aa6-89eac7bdfd2b
