# Flow Shipping Co. Shipping System

## Description
This system is designed to manage the shipping of orders for Flow Shipping Co. It allows the company to:
- Get the list of available carriers.
- Get the list of orders that are waiting to be shipped.
- Assign an available carrier to ship an unshipped order.
- Mark an order as shipped.
- Get the list of orders assigned to a given carrier.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/rajat315315/flow_shipping_assignment
    ```

2. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Create the database tables:
    ```
    mysql -u root -p < astro.sql
    ```

5. Run fake_data.py to create some fake data.
    ```
    python fake_data.py
    ```

## Usage

### Raw SQL Version

Run the raw SQL version of the system:
```sh
python direct_queries.py
```

### ORM Version

Run the ORM version of the system:
```sh
python orm_solution.py
```