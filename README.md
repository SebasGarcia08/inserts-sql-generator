# Inserts SQL generator


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
