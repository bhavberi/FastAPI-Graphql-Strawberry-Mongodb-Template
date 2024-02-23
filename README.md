# FastAPI Strawberry-graphql MongoDB Integrated Template/Boilerplate Code 🚀
## ⚖️ ![GitHub License](https://img.shields.io/github/license/bhavberi/FastAPI-Graphql-Strawberry-Mongodb-Template?label=License&style=plastic&logo=Github)

Template repository for a Service using ***FastAPI + Strawberry-Graphql + MongoDB***.

_Contains example code  for various variations of queries, mutations, types and models, for further reference and easy coding..._  
Check out `Sample` entities, for reference.

----
## How to use 📝
1. Click the green `Use this template` button on the top right to create a new repository in the personal account for the service.
2. Clone the newly created repository to make changes and push.
3. Copy .env file (Make changes in it as required):
```
cp .example.env .env
```
4. Build and spin up all services:
```
docker compose up --build -d
```
5. Check out 
```
localhost:80
```
6. To stop, press `Ctrl + C`

## Example Requests

```bash
# Create document
curl -X 'POST' \
  'http://localhost:80/graphql' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"query": "mutation{sampleMutationOne(sampleInput: {attribute2: \"hi\", email: \"me@gmail.com\", name: \"test\"}) {name}}"}'

# Get documents
curl -X 'POST' \
  'http://localhost:80/graphql' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{"query": "query{sampleQueryTwo{attribute1, name}}"}'
```

----
This code was referred from the template code (Private Repository in [Clubs-Council-IIITH Organisation](https://github.com/Clubs-Council-IIITH)) by 
[@bhavberi](https://github.com/bhavberi), 
[@ek234](https://github.com/ek234) and 
[@v15hv4](https://github.com/v15hv4).

----
![GitHub Code size in bytes](https://img.shields.io/github/languages/code-size/bhavberi/FastAPI-Graphql-Strawberry-Mongodb-Template?color=yellow&label=Code%20Size&style=plastic)
<!-- ![GitHub Repo size](https://img.shields.io/github/repo-size/bhavberi/FastAPI-Graphql-Strawberry-Mongodb-Template?color=orange&label=Repository%20Size) -->

