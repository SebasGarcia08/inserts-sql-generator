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