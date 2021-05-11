# Inserts SQL generator

DDL: we added ON DELETE CASCADE in Employee on parent table "Department" because it makes sense that if a whole 
department is deleted, then all the employees associated with be also deleted, but not viceversa

# Get started

## Prerequisites

- Python >= 3.7
- pip >= 20

## Installation

```
git clone https://github.com/SebasGarcia08/inserts-sql-generator
pip install -r requirements.txt --user
```

## Usage

```shell
$ python generate_inserts.py --help
usage: gen_specific_inserts.py [-h] [-out OUTPUT_FILE] n

Oracle SQL generator for "Modelado TP3" specific DDL.

positional arguments:
  n                     Minimum number of occurrences in each table

optional arguments:
  -h, --help            show this help message and exit
  -out OUTPUT_FILE, --output-file OUTPUT_FILE
                        Output *.sql file where to save the inserts. If not
                        specified, inserts are printed.
```

Prints in terminal:

```shell
$ python generate_inserts.py 20
```

Saves to INSERTS.sql file:

```shell
$ python generate_inserts.py 20 -out INSERTS.sql
```

# Generating generic inserts

We tried to make a program that automatically generates inserts for any DDL, this was our approach.

- Parse the SQL code and build a tree. 
- Traverse the tree and generate inserts according to types for the entities with the least number of foreign keys. 

However, we did not reach that goal. This is an example of the above:

```python
{
  "entities": {
    '<entity_name>': {
        'attributes': [
            {
                'name': '<entity_name>',
                'type': '<type>',
                'max_length': '<max_length>', # Optional  
            }, 
            ...
        ],
        'pk': [
            '<pk_attribute_name>', # Available for unique or composite pks
            ...
        ],
        'fk': [
            {
                'attribute': '<attribute_name_on_this_entity>',
                'entity': '<other_entity>',
                'field': '<attribute_name_on_other_entity>',
                'constraint_type': '<constraint_type>', # Example 'Delete'
                'constraint_mode': '<constraint_mode>', # Example 'cascade'
            },
            ...
        ]
    }
  }
}
```
