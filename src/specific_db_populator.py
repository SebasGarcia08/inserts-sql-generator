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
        self._generate_departments()
        self._update_employees()
        self._generate_projects()
        self._generate_works_on()
        if self.output_file is None:
            for s in self.statements:
                print(s)
        else:
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
                'DOB': f"TO_DATE('{self.faker.date_of_birth(minimum_age=25, maximum_age=100)}', 'YYYY-MM-DD')",
                'sex': f"'{sex}'",
                'position': f"'{str(i)}_position'",
            }
            keys = ','.join(list(field2val.keys()))
            values = ','.join(list(field2val.values()))
            self.statements.append(f"INSERT INTO Employee ({keys}) VALUES ({values});")
            self.employees.add(str(i))
        self.statements.append("\n")

    def _generate_departments(self):
        for i in range(1, (self.n // 2) + 1):
            self.statements.append(f"INSERT INTO Department (deptNo, deptName, mgrEmpNo) VALUES ({i},'department_{i}',{i});")
            self.departments.add(str(i))
        self.statements.append("\n")

    def _update_employees(self):
        updates = []
        for i in range(1, (self.n // 2)+1):
            updates.append(f"UPDATE Employee SET deptNo = {i} WHERE empNo = {i};")
        for i in range((self.n // 2)+1, self.n+1):
            depto = random.choice(list(self.departments))
            updates.append(f"UPDATE Employee SET deptNo = {depto} WHERE empNo = {i};")
        random.shuffle(updates)
        self.statements += updates
        self.statements.append("\n")

    def _generate_projects(self):
        for i in range(1, (self.n // 2) + 1):
            self.statements.append(f"INSERT INTO Project (projNo, projName, deptNo) "
                                   f"VALUES ({i}, '{self.faker.bs()}', {i});")
        self.statements.append("\n")

    def _generate_works_on(self):
        for emp_no in range(1, self.n+1):
            num_records = random.randint(0, 5)
            for _ in range(num_records):
                proj_no = random.choice(list(self.departments))
                date = f"TO_DATE('{self.faker.date_between()}','YYYY-MM-DD')"
                self.statements.append(f"INSERT INTO WorksOn(empNo, projNo, dateworked, hoursWorked) "
                                       f"VALUES ({emp_no},{proj_no},{date},{random.randint(1,10)});")
        self.statements.append("\n")


if __name__ == "__main__":
    dbpop = SpecificDBPopulator(number_occurrences=2+20, output_file="../INSERTS.sql")
    dbpop.generate_inserts();

