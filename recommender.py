import sys
from db_access import DatabaseAccess
from text_preprocessing import TextPreprocessing
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from fastapi import FastAPI

app = FastAPI()

# @app.post("/recomender")
class Recommender:
    def __init__(self):
        self.db_acc = DatabaseAccess()
        self.txt_prep = TextPreprocessing()
        self.table = 'recipes_cleaned'
        self.id_column = 'idRecipe'
        self.cos_sim_threshold = 0.1  #ini aku ubah 1 biar kebaca dulu buat deploy

    def recommend_recipes(self, user_ingredients):
        # read recipe ids and ingredients from database
        recipe_ids = self.db_acc.read_id(self.table)
        ingredients = self.db_acc.read_ingredients(self.table, self.id_column)
        
        # convert sql query result to list 1d (list of recipe ids and list of ingredients)
        recipe_ids_ls = self.txt_prep.sql_query_to_list(recipe_ids)
        ingredients_ls = self.txt_prep.sql_query_to_list(ingredients)
        
        # combine user ingredients and recipe ingredients
        docs = self.txt_prep.combine_query_content(user_ingredients, ingredients_ls)
        
        # calculate tf-idf and cosine similarity between user ingredients and recipe ingredients
        vectorizer = TfidfVectorizer(smooth_idf=False, norm=None)
        docs_weight = vectorizer.fit_transform(docs)
        query_weight = vectorizer.transform([user_ingredients])
        cos_sim = cosine_similarity(query_weight, docs_weight).flatten()
        
        # adjust cosine similarity score and recipe ids
        cos_sim = cos_sim[1:]
        cos_sim_dict = dict(enumerate(cos_sim))
        #return cos_sim_dict
        # return cos_sim_dict
        cos_sim_dict = {k: v for k, v in sorted(cos_sim_dict.items(), key=lambda item: item[1], reverse=True) if v > self.cos_sim_threshold}

        # set corresponding recipe ids based on cosine similarity score
        idx_for_id = list(cos_sim_dict.keys())
        recipe_ids_rank = [recipe_ids_ls[i] for i in idx_for_id]

        return recipe_ids_rank

if __name__ == "__main__":
    if len(sys.argv) == 2:
        user_input = sys.argv[1]
        recommender = Recommender()
        recommended_recipes = recommender.recommend_recipes(user_input)
        sys.stdout.write(', '.join(map(str, recommended_recipes)))
    else:
        print("Please provide user ingredients.")
        
        
recommender_instance = Recommender()


        
        