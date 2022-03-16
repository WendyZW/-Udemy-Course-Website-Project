from model.course import Course
import re, math
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from lib.helper import review_data_path, figure_save_path, course_data_path, send_request


class Review:


    def __init__(self, id=0, rating=0.0, created="", modified="", user_title="", course_id=0, crawlable_count=0):
        # your code
        # initializing

        self.id = id
        self.rating = rating
        self.created = created
        self.modified = modified
        self.user_title = user_title
        self.course_id = course_id
        self.crawlable_count = crawlable_count
        
        pass

    def __str__(self):
        # your code
        # formating print out
        res = "review id:{} | review rating:{} | created time:{} | modified time:{} | user title:{} | courseid:{}"
        
        return res.format(self.id, self.rating, self.created, self.modified, self.user_title, self.course_id)

    def clear_review_data(self):
        # your code
        # reset data
        with open(review_data_path, 'w') as csv:
            rows = ";;;".join([""] * 7)
            csv.write(rows)
        pass

    def get_reviews_by_course_id(self, course_id):
        # not impl.
        result = []
        # your code
        
        return result

    def get_reviews(self):
        # your code
        # get demo data
        with open("data/_demo_review.csv", encoding="utf-8-sig") as f:
            with open(review_data_path, 'w',encoding="utf-8-sig") as f1:
                for l in f:
                    f1.write(l)
        
        

    def get_total_number_of_reviews(self):
        # your code
        # get number of reviews
        df = pd.read_csv(review_data_path, ';;;', header = None)
        return df.shape[0]

    def get_reviews_by_page(self, page):  # each page has 20 courses
        result_review_list = []
        total_page_num = 0

        # your code
        df = pd.read_csv(review_data_path,sep=";;;", header=None) # load data
        df = df[df.isna().sum(1) < df.shape[1] - 1]
        if df.shape[0] == 0:
            return result_review_list,total_page_num  # check if has observation
        df.index = range(1, df.shape[0] + 1) 
        num_page = int(np.ceil(df.shape[0] /20))
        frm = (page -1) * 20 
        end = min(frm + 20,max(df.index ))
        tmp_df = df.iloc[frm:end,:].copy()
        res_list = []
        for j, i in tmp_df.iterrows(): #loop and create class objs
            res_list.append(Review(id= i[1], rating=i[2], created=i[3],
                                   modified=i[4], user_title=i[5],
                                   crawlable_count = i[6]))
        return res_list, num_page


    def generate_review_figure1(self): # if user title is nan, ignore that review
    
        # your code
        #using figure provided
        return "\n a graph to show the total number of (users, courses, instructors, actual reviews, crawlable reviews, subscribers)."

    def generate_review_figure2(self):  # if user title is nan, ignore that review
        # your code
        # using figure providede
        return "\n  a graph to show the number of users who published reviews"

