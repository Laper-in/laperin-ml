import time
from db_access import DatabaseAccess
from text_preprocessing import TextPreprocessing
from fastapi import FastAPI

app = FastAPI()


@app.post("/cleaning")
class IngredientsProcessor:
    def __init__(self, table_to, table_from):
        self.db_acc = DatabaseAccess()
        self.txt_prep = TextPreprocessing()
        self.table_to = table_to
        self.table_from = table_from
        self.id_column = 'id'

    def fetch_data(self):
        recipe_ids = self.db_acc.check_not_exist_id(self.table_from, self.table_to)
        recipe_ids_ls = self.txt_prep.sql_query_to_list(recipe_ids)
        recipe_ids_str = self.txt_prep.list1d_to_string(recipe_ids_ls)

        ingredients = self.db_acc.read_ingredients_by_ids(self.table_from, self.id_column, recipe_ids_str)
        ingredients_ls = self.txt_prep.sql_query_to_list(ingredients)

        return recipe_ids_ls, ingredients_ls

    def preprocess_data(self, ingredients_ls):
        clean_ingredients = self.txt_prep.remove_brackets_text_list(ingredients_ls)
        clean_ingredients = self.txt_prep.tokenize(clean_ingredients)
        clean_ingredients = self.txt_prep.remove_stopwords(clean_ingredients)
        clean_ingredients = self.txt_prep.remove_non_alpha(clean_ingredients)
        clean_ingredients = self.txt_prep.clean_doc(clean_ingredients)

        return clean_ingredients

    def insert_processed_data(self, recipe_ids_ls, clean_ingredients):
        ingredients_idx = 0
        for i in recipe_ids_ls:
            self.db_acc.insert_ingredients(i, clean_ingredients[ingredients_idx], self.table_to)
            ingredients_idx += 1

    def insert_many_processed_data(self, recipe_ids_ls, clean_ingredients):
        data = tuple(zip(recipe_ids_ls, clean_ingredients))

        self.db_acc.insert_many_ingredients(data, self.table_to)

if __name__ == "__main__":
    table_to = 'recipes_cleaned'
    table_from = 'recipes'

    # infinite loop to keep the program running
    while True:
        # create object
        ingredients_processor = IngredientsProcessor(table_to, table_from)
        # fetch data
        recipe_ids_ls, ingredients_ls = ingredients_processor.fetch_data()

        # insert data if there is any data to be inserted
        if len(recipe_ids_ls) > 0:
            # preprocess data
            clean_ingredients = ingredients_processor.preprocess_data(ingredients_ls)
            # insert data
            ingredients_processor.insert_many_processed_data(recipe_ids_ls, clean_ingredients)

        # close connection
        ingredients_processor.db_acc.close_connection()
        time.sleep(1)