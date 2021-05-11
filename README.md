# Inserts SQL generator

DDL: we added ON DELETE CASCADE in Employee on parent table "Department" because it makes sense that if a whole 
department is deleted, then all the employees associated with be also deleted, but not viceversa

```sql
CREATE TABLE Employee (
  empNo INT,
  fName VARCHAR(50),
  lName VARCHAR(50),
  address VARCHAR(100),
  DOB DATE,
  sex CHAR(1),
  position VARCHAR(30),
  deptNo INT,
  PRIMARY KEY (empNo)
);
CREATE TABLE Department (
  deptNo INT,
  deptName VARCHAR(50),
  mgrEmpNo INT,
  PRIMARY KEY (deptNo),
  FOREIGN KEY (mgrEmpNo) REFERENCES Employee (empNo) ON  DELETE SET NULL
);
CREATE TABLE Project (
  projNo INT,
  projName VARCHAR(50),
  deptNo INT,
  PRIMARY KEY (projNo),
  FOREIGN KEY (deptNo) REFERENCES Department (deptNo) ON  DELETE CASCADE
);
CREATE TABLE WorksOn (
  empNo INT,
  projNo INT,
  dateworked Date,
  hoursWorked Number(10,2),
  PRIMARY KEY (empNo,projNo,dateworked),
  FOREIGN KEY (EmpNo) REFERENCES Employee (EmpNo) ON DELETE SET NULL,
  FOREIGN KEY (projNo) REFERENCES Project (projNo) ON DELETE CASCADE
);

ALTER TABLE Employee
  ADD CONSTRAINT FK_Department_Employee FOREIGN KEY (deptNo)
    REFERENCES Department (deptNo)
    ON DELETE CASCADE
;
```

# Get started

## Prerequisites

- Python >= 3.7
- pip >= 20

## Installation

```
git clone https://github.com/SebasGarcia08/inserts-sql-generator
pip install -r requirements.txt
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
$ python generate_inserts.py 20 -out INSERTS.sql
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

```sql
CREATE TABLE Department (
  deptNo CHAR(9),
  deptName VARCHAR(50),
  mgrEmpNo CHAR(50),
  PRIMARY KEY (deptNo)
  );
CREATE TABLE Employee (
  empNo CHAR(9),
  fName VARCHAR(50),
  lName VARCHAR(50),
  address VARCHAR(50),
  DOB DATE,
  sex VARCHAR(6),
  position VARCHAR(30),
  deptNo CHAR(9),
  PRIMARY KEY (empNo),
  FOREIGN KEY (deptNo) REFERENCES Department (deptNo) on Delete cascade
  );
CREATE TABLE Project (
  projNo CHAR(9),
  projName VARCHAR(50),
  deptNo CHAR(9),
  PRIMARY KEY (projNo),
  FOREIGN KEY (deptNo) REFERENCES Department (deptNo) on Delete cascade
  );
CREATE TABLE WorksOn (
  empNo CHAR(9),
  projNo CHAR(9),
  dateworked Date,
  hoursWorked Number(10,2),
  PRIMARY KEY (empNo,projNo,dateworked),
  FOREIGN KEY (EmpNo) REFERENCES Employee (EmpNo) on Delete cascade,
  FOREIGN KEY (projNo) REFERENCES Project (projNo) on Delete cascade
  );
ALTER TABLE Department 
  ADD CONSTRAINT FK_Department_Employee FOREIGN KEY (mgrEmpNo) 
    REFERENCES Employee (empNo)
    on Delete cascade
  ;
```


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
