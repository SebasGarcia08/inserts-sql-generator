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
        self.db_tree = dict()

    def generate_inserts(self):
        raise ValueError("Not implemented")


    @staticmethod
    def _extract_from_parentheses(s):
        return re.search('\(([^)]+)', s).group(1)

    def _process_primary_key(self, entity_name, args):
        pk_name = self._extract_from_parentheses(args[-1])
        entity_subtree = self.db_tree['entities'][entity_name]
        if 'pk' not in entity_subtree:
            entity_subtree['pk'] = []

        if ',' in pk_name:
            pks = pk_name.split(",")
            for pk in pks:
                entity_subtree['pk'].append(pk)
        else:
            entity_subtree["pk"].append(pk_name)

    def _process_foreign_key(self, table_name, args):
        if "fk" not in self.db_tree['entities'][table_name]:
            self.db_tree['entities'][table_name]["fk"] = []

        self.entity_name2num_fk[table_name] += 1

        fk_name = self._extract_from_parentheses(args[2])
        table_referenced = args[4]
        field_referenced = self._extract_from_parentheses(args[5])

        fk_subtree = {
            'attribute': fk_name,
            "entity": table_referenced,
            "field": field_referenced,
            'constraint_type': 'default',
            'constraint_mode': None,
        }

        if len(args) > 5:
            constraint_type = args[-2]
            constraint_mode = args[-1]

            fk_subtree['constraint_type'] = constraint_type
            fk_subtree['constraint_mode'] = constraint_mode

        self.db_tree['entities'][table_name]["fk"].append(fk_subtree)

    def _process_alters(self, input_sql):
        alters = input_sql.split("ALTER TABLE")[1:]
        for alter in alters:
            lines = [line.strip() for line in alter.split("\n")]
            altered_entity_raw = lines[0] # ALTER TABLE <entity>
            constraint_raw = lines[1] # ADD CONSTRAINT <constraint_name> FOREIGN KEY (attribute)
            references_raw = lines[2] # REFERENCES <referenced_entity> (referenced_attribute)
            type_mode_raw = lines[3] # on Delete cascade

            altered_entity = altered_entity_raw.split()[-1]
            attribute_fk = self._extract_from_parentheses(constraint_raw) # attribute
            referenced_entity = references_raw.split()[1]
            referenced_attribute = self._extract_from_parentheses(references_raw)
            constraint_type = type_mode_raw.split()[-2]
            constraint_mode = type_mode_raw.split()[-1]

            new_fk = {
                'attribute': attribute_fk,
                'entity': referenced_entity,
                'field': referenced_attribute,
                'constraint_type': constraint_type,
                'constraint_mode': constraint_mode,
            }

            altered_entity_subtree = self.db_tree['entities'][altered_entity]
            if 'fk' not in altered_entity_subtree:
                altered_entity_subtree['fk'] = [new_fk]
            else:
                altered_entity_subtree['fk'].append(new_fk)
            self.entity_name2num_fk[altered_entity] += 1

    def _build_db_tree(self, input_sql):
        entities = input_sql.split("CREATE TABLE")[1:]
        self.entity_name2num_fk = dict()
        self.db_tree["entities"] = dict()

        for entity in entities:
            lines = entity.split("\n")
            entity_name = re.sub(r"\(*", "", lines[0]).strip()

            self.db_tree['entities'][entity_name] = {}
            self.db_tree['entities'][entity_name]["attributes"] = {}
            self.entity_name2num_fk[entity_name] = 0

            for attribute in lines[1:]:
                args = attribute.strip().split(" ")
                if args[0].startswith("PRIMARY"):
                    self._process_primary_key(entity_name, args)

                elif args[0].startswith("FOREIGN"):
                    self._process_foreign_key(entity_name, args)

                elif args[0].isalpha():
                    entity_type = re.sub(',', '', args[1])
                    attribute_name = args[0]
                    self.db_tree['entities'][entity_name]["attributes"][attribute_name] = entity_type
        self._process_alters(input_sql)

    def __str__(self):
        return json.dumps(self.db_tree, indent=4)


if __name__ == "__main__":
    from input import input_sql_2 as inp
    db_pop = DBPopulator(inp)
    print(db_pop)
    print(db_pop.entity_name2num_fk)
    print(sorted(list(db_pop.entity_name2num_fk.values())))
