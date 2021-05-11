from faker import Faker
import random


class SpecificDBPopulator(object):

    def __init__(self, number_occurrences, output_file):
        Faker.seed(666)
        random.seed(666)

        self.faker = Faker('en_US')
        self.employees = set()
        self.departments = set()
        self.projects = set()
        self.works_on = set()
        self.n = number_occurrences
        self.output_file = output_file
        self.statements = []

    def generate_inserts(self):
        self._generate_employees()
        self.statements.append("\n")
        self._generate_departments()
        self.statements.append("\n")
        self._update_employees()
        self.statements.append("\n")
        self._generate_works_on()
        self.statements.append("\n")
        with open(self.output_file, 'w') as f:
            for s in self.statements:
                f.write(s + "\n")

    def _generate_employees(self):

        for i in range(1,self.n+1):
            sex = random.choice(["M", "F"])
            field2val = {
                'empNo': str(i),
                'fName': f"'{self.faker.first_name_female() if sex == 'F' else self.faker.first_name_male()}'",
                'lName': f"'{self.faker.last_name()}'",
                'address': f"'{self.faker.address()}'",
                'DOB': f"TO_DATE('{self.faker.date()}', 'YYYY-MM-DD')",
                'sex': f"'{sex}'",
                'position': f"'{str(i)}_position'",
                'deptNo': "NULL"
            }
            keys = ','.join(list(field2val.keys()))
            values = ','.join(list(field2val.values()))
            self.statements.append(f"INSERT INTO Employee ({keys}) VALUES ({values});")
            self.employees.add(str(i))

    def _generate_departments(self):
        for i in range(1, (self.n // 2) + 1):
            self.statements.append(f"INSERT INTO Department (deptNo, deptName, mgrEmpNo) VALUES ({i},'department_{i}',{i});")

    def _update_employees(self):
        updates = []
        for i in range(1, self.n+1):
            updates.append(f"UPDATE Employee SET deptoNo = {i} WHERE empNo = {i};")
        random.shuffle(updates)
        self.statements += updates

    def _generate_projects(self):
        for i in range(1, (self.n // 2) + 1):
            self.statements.append(f"INSERT INTO Project (projNo, projName, deptNo) "
                                   f"VALUES ({i}, {self.faker.bs()}, {i});")

    def _generate_works_on(self):
        for i in range(1, self.n+1):
            date = f"TO_DATE('{self.faker.date_between()}','YYYY-MM-DD')"
            self.statements.append(f"INSERT INTO WorksOn(empNo, projNo, dateworked, hoursWorked) "
                                   f"VALUES ({i},{i},{date},{random.randint(1,10)});")


if __name__ == "__main__":
    dbpop = SpecificDBPopulator(number_occurrences=40, output_file="../INSERTS.sql")
    dbpop.generate_inserts();

