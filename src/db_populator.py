from faker import Faker
import json
import re
from argparse import ArgumentParser
from pprint import pprint


class DBPopulator(object):

    def __init__(self, input_sql):
        self.fake = Faker()
        self.str_rep = None
        self._build_db_tree(input_sql)

    def generate_inserts(self):
        print(self.entity_name2num_fk)

    def _extract_from_parentheses(self, s):
        return re.search('\(([^)]+)', s).group(1)

    def _build_db_tree_attributes(self):
        pass

    def _build_db_tree(self, input_sql):
        entities = input_sql.split("CREATE TABLE")[1:]
        #pprint(entities)
        alters = input_sql.split("ALTER TABLE")[1:]
        pprint(alters)
        self.entity_name2num_fk = {}

        self.db_tree = {}
        self.db_tree["entities"] = {}

        for entity in entities:
            lines = entity.split("\n")
            table_name = re.sub(r"\(*", "", lines[0]).strip()

            self.db_tree['entities'][table_name] = {}
            self.db_tree['entities'][table_name]["attributes"] = {}
            self.entity_name2num_fk[table_name] = 0

            for attribute in lines[1:]:
                args = attribute.strip().split(" ")
                if args[0].startswith("PRIMARY"):
                    pk_name = self._extract_from_parentheses(args[-1])
                    self.db_tree['entities'][table_name]["pk"] = pk_name

                elif args[0].startswith("FOREIGN"):
                    if "fk" not in self.db_tree['entities'][table_name]:
                        self.db_tree['entities'][table_name]["fk"] = []

                    self.entity_name2num_fk[table_name] += 1

                    fk_name = self._extract_from_parentheses(args[2])
                    table_referenced = args[4]
                    field_referenced = self._extract_from_parentheses(args[5])

                    fk_subtree = {
                        fk_name: {
                            "entity": table_referenced,
                            "field": field_referenced
                        }
                    }

                    if len(args) > 5:
                        constraint_type = args[-2]
                        constraint_mode = args[-1]

                        fk_subtree[fk_name]["mode"] = {
                            'constraint_type': constraint_type,
                            'constraint_mode': constraint_mode
                        }

                    self.db_tree['entities'][table_name]["fk"].append(fk_subtree)

                elif args[0].isalpha():
                    entity_type = re.sub(',', '', args[1])
                    attribute_name = args[0]
                    self.db_tree['entities'][table_name]["attributes"][attribute_name] = entity_type

    def __str__(self):
        return json.dumps(self.db_tree, indent=4)


if __name__ == "__main__":
    from input import input_sql_2 as inp
    db_pop = DBPopulator(inp)
    print(db_pop)
    print(db_pop.entity_name2num_fk)
    sorted(list(db_pop.entity_name2num_fk.values()))
