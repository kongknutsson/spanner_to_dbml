import sys

class Entity:
    """This class represents an entity (column) in a SQL Spanner file.
    """

    def __init__(
        self, 
        name: str, 
        relations: str, 
        data_type: str, 
        is_primary_key: bool = False, 
        is_foreign_key: bool = False, 
        is_not_null: bool = False, 
        table: str = None
    ):
        self.name = name
        self.relations = relations
        self.data_type = data_type
        self.is_primary_key = is_primary_key
        self.is_foreign_key = is_foreign_key
        self.is_not_null = is_not_null
        self.table = table

    def __str__(self):
        return f"{self.table} - {self.name} {self.data_type} {self.is_primary_key} {self.is_foreign_key} {self.is_not_null}"

    def converted_to_dbml(self):
        converted_string = f"{self.name} {self.data_type}"

        if any((self.is_primary_key, self.is_foreign_key, self.is_not_null)):
            converted_string += " ["

            if self.is_not_null:
                converted_string += "not null,"

            if self.is_primary_key:
                converted_string += " pk,"

            if self.relations:
                for relation in self.relations:
                    converted_string += f" ref: > {relation[0]}.{relation[1]},"

            converted_string = converted_string[:-1] + "]"
        
        return converted_string


class Converter: 
    """This class converts a SQL Spanner file to a DBML file.
    """
    def __init__(self): 
        pass 

    def convert(self, filepath): 

        if filepath.endswith(".sql") == False:
            raise Exception("File must be a SQL file")

        with open(filepath, 'r') as f: 
            lines = f.readlines()

        entities, tables = self.create_entities_from_lines(lines)

        entities = self.add_primary_key_to_entities(entities, lines)

        entities = self.add_references_to_entities(entities, lines)

        entities = self.format_entities(tables, entities)

        self.write_to_dbml(entities, "converted.dbml")

    def write_to_dbml(self, entities, filepath = "converted.dbml", ):
        with open(filepath, 'w') as f:
            f.write(entities)

    def format_entities(self, tables, entities):
        base = ""
        
        for table in tables:
            base += f"\ntable {table} {{\n"
            for line in entities:
                if line.table == table:
                    base += f"  {line.converted_to_dbml()}\n"

            base += "}"

        return base

    def add_references_to_entities(self, entities, lines):
        current_table = ""
        for line in lines:

            if "CREATE TABLE" in line:
                current_table = line.split(" ")[2]

            if "REFERENCES" in line:
                line = line.strip().replace(",", "").replace("(", "").replace(")", "")
                entity_name = line.split(" ")[4]
                reference_entity = line.split(" ")[-1]
                reference_table = line.split(" ")[-2]

                for entity in entities:
                    if entity.name == entity_name and entity.table == current_table:
                        entity.relations.append((reference_table, reference_entity))

        return entities

    def add_primary_key_to_entities(self, entities, lines):
        current_table = ""
        for line in lines:
            if "CREATE TABLE" in line:
                current_table = line.split(" ")[2]
            if "PRIMARY KEY" in line:
                entity_name = line.split("(")[1].split(")")[0]        
                for entity in entities:
                    if entity.name == entity_name and entity.table == current_table:
                        entity.is_primary_key = True
        return entities

    def create_entities_from_lines(self, lines):
        entities = []
        tables = []
        current_table = ""
        for line in lines: 
            line = line.strip().replace(",", "")
            if line == "":
                continue
            
            # These will be filled in later. 
            if "PRIMARY KEY" in line or "CONSTRAINT" in line or "INDEX" in line:
                continue

            if "CREATE TABLE" in line:
                current_table = line.split(" ")[2]
                tables.append(current_table)
                continue
        
            entity = Entity(
                name=line.split(" ")[0],
                relations=[],
                data_type=line.split(" ")[1],
                table=current_table
            )

            if "NOT NULL" in line:
                entity.is_not_null = True

            entities.append(entity)

        return entities, tables

if __name__ == "__main__":
    converter = Converter()
    path = sys.argv[1]
    converter.convert(path)