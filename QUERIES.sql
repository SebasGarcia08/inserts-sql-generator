SELECT * FROM Employee;

SELECT * FROM Employee WHERE sex='F';

SELECT Employee.fName, Employee.lName, Employee.address
FROM Employee,Department WHERE Employee.empNo=Department.mgrEmpNo;

SELECT fName, lName, address
FROM Employee WHERE deptNo=1;

SELECT Employee.* FROM Employee,WorksOn
WHERE WorksOn.projNo=1
AND WorksOn.empNo=Employee.empNo;

SELECT Employee.fName, Employee.lName, Employee.address FROM Employee,Department
WHERE Employee.empNo=Department.deptNo
AND (Employee.sex='M'
AND ((EXTRACT(YEAR FROM SYSDATE)-EXTRACT(YEAR FROM Employee.DOB))>=62)
OR (Employee.sex='F'
AND (EXTRACT(YEAR FROM SYSDATE)-EXTRACT(YEAR FROM Employee.DOB))>=57));

SELECT Employee.fName, Employee.lName, Employee.address
FROM Employee,Department
WHERE Employee.deptNo=(SELECT deptNo FROM Department WHERE mgrEmpNo='4')
AND Employee.empNo<>'4' AND Department.deptNo=(SELECT deptNo FROM Department WHERE mgrEmpNo='4');
