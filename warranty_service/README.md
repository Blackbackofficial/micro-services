# Warranty Service

## API Description
1. `GET /manage/health` - Swagger API;
2. `GET /api/v1/warranty/{itemUid}` – information about the warranty status;
3. `POST /api/v1/warranty/{itemUid}/warranty` – request for a warranty decision;
4. `POST /api/v1/warranty/{itemUid}` – request to start the warranty period;
5. `DELETE /api/v1/warranty/{itemUid}` – request to close the warranty.


## Operation logic
Warranty is bound to `item_uid`, each warranty entry has three statuses: `ON_WARRANTY`, `USE_WARRANTY`.
When an order is created (method 3), an entry is created and the status is set to `ON_WARRANTY`.
When the order is closed (method 4) is deleted.
When requesting a guarantee (method 2), the status of the guarantee is checked, if the status is other than `ON_WARRANY`, then the decision is `REFUSED`.
The request from Warehouse comes with the number of available items. If the product is in stock, then the decision is `RETURN`, otherwise `FIXING`.

## Table structure
```postgresql
CREATE TABLE warranty
(
    id SERIAL CONSTRAINT warranty_pkey PRIMARY KEY,
    comment VARCHAR(1024),
    item_uid UUID NOT NULL CONSTRAINT idx_warranty_item_uid UNIQUE,
    status VARCHAR(255) NOT NULL,
    warranty_date TIMESTAMP NOT NULL
);
```
