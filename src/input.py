input_sql = """CREATE TABLE Employee (
      empNo CHAR(9),
      fName VARCHAR(50),
      lName VARCHAR(50),
      address VARCHAR(50),
      DOB DATE,
      sex VARCHAR(6),
      position VARCHAR(30),
      deptNo CHAR(9),
      PRIMARY KEY (empNo)
      );
    CREATE TABLE Department (
      deptNo CHAR(9),
      deptName VARCHAR(50),
      mgrEmpNo CHAR(50),
      PRIMARY KEY (deptNo),
      FOREIGN KEY (mgrEmpNo) REFERENCES Employee (empNo) on Delete cascade
      );
    CREATE TABLE Project (
      projNo CHAR(9),
      projName VARCHAR(50),
      deptNo CHAR(9),
      PRIMARY KEY (projNo),
      FOREIGN KEY (deptNo) REFERENCES Department (deptNo) on Delete cascade
      );
    CREATE TABLE WorksOn (
      worksPK CHAR(30),
      empNo CHAR(9),
      projNo CHAR(9),
      dateworked Date,
      hoursWorked Number(10,2),
      PRIMARY KEY (worksPK),
      FOREIGN KEY (EmpNo) REFERENCES Employee (EmpNo) on Delete cascade,
      FOREIGN KEY (projNo) REFERENCES Project (projNo) on Delete cascade
      );
    """

input_sql_2 = """CREATE TABLE Employee (
  empNo INT,
  fName VARCHAR(50),
  lName VARCHAR(50),
  address VARCHAR(50),
  DOB DATE,
  sex VARCHAR(6),
  position VARCHAR(30),
  deptNo INT,
  PRIMARY KEY (empNo)
);
CREATE TABLE Department (
  deptNo INT,
  deptName VARCHAR(50),
  mgrEmpNo INT,
  PRIMARY KEY (deptNo),
  FOREIGN KEY (mgrEmpNo) REFERENCES Employee (empNo)
);
CREATE TABLE Project (
  projNo INT,
  projName VARCHAR(50),
  deptNo INT,
  PRIMARY KEY (projNo),
  FOREIGN KEY (deptNo) REFERENCES Department (deptNo)
  );
CREATE TABLE WorksOn (
  empNo INT,
  projNo INT,
  dateworked Date,
  hoursWorked Number(10,2),
  PRIMARY KEY (empNo,projNo,dateworked),
  FOREIGN KEY (EmpNo) REFERENCES Employee (EmpNo),
  FOREIGN KEY (projNo) REFERENCES Project (projNo)
  );
  
ALTER TABLE Employee 
  ADD CONSTRAINT FK_Department_Employee FOREIGN KEY (deptNo) 
    REFERENCES Department (deptNo)
    ON DELETE SET NULL
  ;
  """
