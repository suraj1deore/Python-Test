# Python-Test


## Installation

1. Clone the repository:

2. Install the required dependencies:

   ```
   pip install fastapi uvicorn[standard] databases[sqlite] pydantic[dotenv]
   ```

3. Start the app:

   ```
   uvicorn app:app --reload
   ```

4. Access the Swagger documentation:

   ```
   http://localhost:8000/docs
   ```

## Usage

The app provides the following endpoints:

- `GET /addresses`: Retrieve all addresses in the database.
- `GET /addresses/{address_id}`: Retrieve a specific address by ID.
- `GET /addresses/nearby`: Retrieve addresses within a given distance and location coordinates.
- `POST /addresses`: Create a new address.
- `PUT /addresses/{address_id}`: Update an existing address.
- `DELETE /addresses/{address_id}`: Delete an existing address.
