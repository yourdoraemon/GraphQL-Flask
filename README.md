# GraphQL Python Flask Application

This is a simple Python Flask application that uses GraphQL with the Graphene library. It provides a single query, `people`, which returns a list of Person objects. Each Person has an `email`, `name`, and `address`. The Address object has `number`, `street`, `city`, and `state`.

The mock data is stored in `data.json` file, when the application starts, it will load the data into the SQLite

## How to Run
1. Create a virtual environment

```bash
python3 -m venv env
source env/bin/activate 
```

2. Install the required Python libraries:

```bash
pip install -r requirements.txt
```

3. To start the application, simply run the script with Python:

```bash
python app.py
```

The application will start a web server at http://localhost:8080. You can visit http://localhost:8080/graphql to access the GraphiQL interface and make GraphQL queries.

Example query to get all people:

```graphql
{
  people {
    email
    name
    address {
      number
      street
      city
      state
    }
  }
}
```