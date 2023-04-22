# Python-Test


## Installation

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/address-book.git
   ```

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

   Note: You can specify a different port number using the `--port` flag in the `uvicorn` command.

## Usage

The app provides the following endpoints:

- `GET /addresses`: Retrieve all addresses in the database.
- `GET /addresses/{address_id}`: Retrieve a specific address by ID.
- `GET /addresses/nearby`: Retrieve addresses within a given distance and location coordinates.
- `POST /addresses`: Create a new address.
- `PUT /addresses/{address_id}`: Update an existing address.
- `DELETE /addresses/{address_id}`: Delete an existing address.
