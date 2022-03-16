import re, os, math, time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from lib.helper import course_data_path, figure_save_path, course_json_files_path

class Course:

    def __init__(self, category_title="", subcategory_id=-1, subcategory_title="", subcategory_description="",
                 subcategory_url="", course_id=-1, course_title="", course_url="",
                 num_of_subscribers=0, avg_rating=0.0, num_of_reviews=0):
        # your code

        ## initialiizing

        self.category_title = category_title
        self.subcategory_id =subcategory_id
        self.subcategory_title = subcategory_title
        self.subcategory_description = subcategory_description
        self.subcategory_url = subcategory_url
        self.course_id = course_id
        self.course_title = course_title
        self.course_url = course_url
        self.num_of_subscribers = num_of_subscribers
        self.avg_rating = avg_rating
        self.num_of_reviews = num_of_reviews


    def __str__(self):
        # your code
        
        # formating print out
        res = """category: {} | subcategory id:{} | subcategory:{} | \
        subcategory url:{} | course id:{} | course title:{} | course url:{} |\
        number of subscriber:{} | avg rating:{} | number of reviews:{}"""
        
        
        
        return res.format(self.category_title, self.subcategory_id, self.subcategory_title,
                         self.subcategory_url, self.course_id, self.course_title, 
                         self.course_url, self.num_of_subscribers, self.avg_rating, self.num_of_reviews)

    def clear_course_data(self):
        
        # your code
        # open a new file with empty content  but with correct columns number
        with open(course_data_path, 'w') as csv:
            rows = ";;;".join([""] * 11)
            csv.write(rows)

    def generate_page_num_list(self, page, total_pages):
        page_num_list = []
        page = int(page) # str to int

        # your code
        lower = max(1, page - 4) # from page
        upper = min(page + 4,total_pages) # end page
        if upper == total_pages: # in case end page upto total page
            lower = total_pages -8
        if lower == 1: # in case from page up to page 1
            upper = lower  +  8
        page_num_list = list(range(lower, upper + 1))
        return page_num_list

    def get_courses_by_page(self, page):  # each page has 20 courses
        page = int(page)  # str to int
        result_course_list = [] # list to store class object
        total_page_num = 0
        # your code
        df = pd.read_csv(course_data_path,sep=";;;", header=None) # load data
        df = df[df.isna().sum(1) < 9] # remove rows with empty values
        if df.shape[0] == 0:
            return result_course_list,total_page_num # if no results
            
        df.index = range(1, df.shape[0] + 1) # reset index
        num_page = int(np.ceil(df.shape[0] /20))
        frm = (page -1) * 20  # from page
        end = min(frm + 20,max(df.index )) # end page
        tmp_df = df.iloc[frm:end,:].copy() # sub set of data
        res_list = []
        for j, i in tmp_df.iterrows(): # loop and get object list
            res_list.append(Course(category_title=i[0], subcategory_id=int(i[1]),
                                                 subcategory_title= i[2], subcategory_description=i[3],
                                                  subcategory_url=i[4], course_id=int(i[5]),
                                                  course_title=i[6], course_url=i[7], num_of_subscribers=int(i[8]),
                                                  avg_rating=i[9], num_of_reviews=i[10]))
        return res_list, num_page

    def get_courses(self):
        # your code
        with open(course_data_path, 'wb') as csv:
            for root, dirs, files in os.walk(course_json_files_path[1:], topdown=False): # loop files in dictionary
                for name in files:
                    tmp = os.path.join(root, name)
                    sub = tmp.split("\\")[1].split("_")[-1]
                    with open(tmp, encoding="utf8") as f: # read files and lookup data
                        for l in f:
                            L = l.split(",")
                            ids = [i for i in L if i.find('"id"') >= 0][0].split(":")[-1].split("}")[0]
                            subcat = [i for i in L if i.find('title') >= 0][2].split(":")[-1].replace('"', '').split("}")[0]
                            desc = [i for i in L if i.find('description') >= 0][0].split(":")[-1].replace('"', '').split("}")[0]
                            suburl = [i for i in L if i.find('url') >= 0][0].split(":")[-1].replace('"', '').split("}")[0]
                            cursid = [i for i in L if i.find('"id"') >= 0][1].split(":")[-1].replace('"', '').split("}")[0]
                            cournm = [i for i in L if i.find('title') >= 0][3].split(":")[-1].replace('"', '').split("}")[0]
                            coursul = [i for i in L if i.find('url') >= 0][1].split(":")[-1].replace('"', '').split("}")[0]
                            coursnsub = [i for i in L if i.find('num_subscribers') >= 0][0].split(":")[-1].replace('"', '').split("}")[0]
                            coursrating = [i for i in L if i.find('avg_') >= 0][0].split(":")[-1].replace('"', '').split("}")[0]
                            coursnview = [i for i in L if i.find('num_reviews') >= 0][0].split(":")[-1].replace('"', '').split("}")[0]
                            rows = ";;;".join([sub,ids, subcat, desc, suburl, cursid, cournm, coursul, coursnsub, coursrating, coursnview])
                            csv.write((rows + "\n").encode("utf-8-sig")) # write csv
        

    def delete_course_info(self, temp_course_id):
        temp_course_id = str(temp_course_id)
        result = False
        # your code
        try:
            new = []
            with open(course_data_path,'r', encoding="utf8") as f: # read file
                for rows in f:
                    i = rows.split(";;;")[5]
                    if i == temp_course_id: # find observation to delete
                        rows = ""
                        result = True

                    new.append(rows) # append results
            with open(course_data_path,'wb') as f: # write new file
                for i in range(len(new)):
                    n = new[i]
                    if n != "\n":
                        f.write(n.encode("utf-8-sig"))
        except:
            result = False

            
        return result

    def get_course_by_course_id(self, temp_course_id):
        temp_course_id = str(temp_course_id)
        temp_course = None
        overall_comment = ""
        # your code
        with open(course_data_path,'r', encoding="utf8") as f: 
            for rows in f: # loop lines
                i = rows.split(";;;") # splite

                if len(i) > 1:
                    ii = i[5]

                if ii == temp_course_id: # get target observation
                    overall_comment = "General Courses"
                    ns, rating, nrw = [float(j.replace("\n", "")) for j in i[-3:]]
                
                    if ns > 10000 and rating > 4.5: # get clsss type
                        overall_comment ="Top Courses"
                    elif ns > 50000 and rating > 4 and nrw > 5000:
                        overall_comment ="Top Courses"   
                    elif ns > 10000 and rating > 3.5 and nrw > 1000:
                        overall_comment ="Top Courses"   
                    temp_course = Course(category_title=i[0], subcategory_id=int(i[1]), # create class object
                                         subcategory_title= i[2], subcategory_description=i[3],
                                          subcategory_url=i[4], course_id=int(i[5]),
                                          course_title=i[6], course_url=i[7], num_of_subscribers=int(i[8]),
                                          avg_rating=i[9], num_of_reviews=i[10])
        return temp_course, overall_comment

    def get_total_number_of_courses(self):
        df = pd.read_csv(course_data_path,sep=";;;", header=None) # load data
        df = df[df.isna().sum(1) < 9] # remove emptye observation
        
        return df.shape[0] # get nums

    def generate_course_figure1(self):
        # your code
        plt.figure()

        df = pd.read_csv(course_data_path,sep=";;;", header=None)
        df = df[df.isna().sum(1) < 9]
        df.columns = ['category_title', 'subcategory_id','subcategory_title', 
        'subcategory_description', 'subcategory_url', 'course_id',
        'course_title', 'course_url', 'num_of_subscribers','avg_rating','num_of_reviews']
        df1 = df.sort_values("num_of_subscribers",ascending =False)[['course_title','num_of_subscribers' ]] # create data frame
        # df1[df1.num]
        df11 = df1.set_index("course_title").head(15) # select data
        df11.plot.bar() # plot
        plt.title("top 15 course by num of subscribers")
        plt.tight_layout()
        plt.savefig("static/img/course_figure1.png") # save


        return "\na graph to show the top 15 courses with the most subscribers." # explain

    def generate_course_figure2(self):

        # your code
  
        df = pd.read_csv(course_data_path,sep=";;;", header=None)
        df = df[df.isna().sum(1) < 9]
        df.columns = ['category_title', 'subcategory_id','subcategory_title', 
        'subcategory_description', 'subcategory_url', 'course_id',
        'course_title', 'course_url', 'num_of_subscribers','avg_rating','num_of_reviews']
        df1 = df.sort_values("avg_rating",ascending =True)[['course_title','avg_rating' ,'num_of_reviews']]
        # df1[df1.num]
        df1 = df1[df1.num_of_reviews > 50000].copy() # get data
        del df1['num_of_reviews']
        df1 = df1.set_index("course_title").tail(15) # get subset
        df1.plot.bar() # plot
        plt.title("top 15 course by avg rating")
        plt.tight_layout()
        plt.savefig("static/img/course_figure2.png")
        

        return "\na graph to show the top 15 avg rating(ascending order) of courses that have over 50000 reviews."

    def generate_course_figure3(self):
        # your code

        df = pd.read_csv(course_data_path,sep=";;;", header=None)
        df = df[df.isna().sum(1) < 9]
        df.columns = ['category_title', 'subcategory_id','subcategory_title', 
        'subcategory_description', 'subcategory_url', 'course_id',
        'course_title', 'course_url', 'num_of_subscribers','avg_rating','num_of_reviews']

        df1 = df[df.num_of_subscribers >100]
        df2 = df1[df1.num_of_subscribers < 1000] # subset
        plt.figure()
        plt.scatter(df2.index,df2.avg_rating) # plot
        plt.title("distribution of scatter average rating")
        plt.tight_layout()
        plt.savefig("static/img/course_figure3.png")

        return "\na graph to show the all the courses avg rating distribution that has subscribers between 1000 and 100"



    def generate_course_figure4(self):
        # your code
        df = pd.read_csv(course_data_path,sep=";;;", header=None)
        df = df[df.isna().sum(1) < 9]
        df.columns = ['category_title', 'subcategory_id','subcategory_title', 
        'subcategory_description', 'subcategory_url', 'course_id',
        'course_title', 'course_url', 'num_of_subscribers','avg_rating','num_of_reviews']

        p = df.groupby("category_title")['category_title'].count().sort_values() # get data
        ep = [0 for i in range(len(p))]
        ep[-2] = 0.1 # define explode
        def absolute_value(val): # compute observation nums
            a  = np.round(val/100.*p.sum(), 0)
            return a
        plt.figure()
        p.plot(kind = 'pie', explode = ep, autopct=absolute_value) # plot
        plt.title("number of courses for all categories")
        plt.tight_layout()
        plt.savefig("static/img/course_figure4.png")
        return "\na graph to show the number of courses for all categories and sort in ascending order (pie chart, offsetting the second largest number of course with explode)"

    def generate_course_figure5(self):
        # your code
        plt.figure()
        df = pd.read_csv(course_data_path,sep=";;;", header=None)
        df = df[df.isna().sum(1) < 9]
        df.columns = ['category_title', 'subcategory_id','subcategory_title', 
        'subcategory_description', 'subcategory_url', 'course_id',
        'course_title', 'course_url', 'num_of_subscribers','avg_rating','num_of_reviews']

        p1 = df.groupby("subcategory_title")['course_id'].count().sort_values() # get data
        p1 = p1.tail(15)
        plt.figure()
        p1.plot.bar() # plot
        plt.xticks()
        plt.title("top 15 sub categories by number of courses")
        plt.tight_layout()
        plt.savefig("static/img/course_figure5.png")

        return "\na graph to show the top 15 subcategories with the most courses."


    def generate_course_figure6(self):
        # your code
        plt.figure()
        df6 = pd.read_csv(course_data_path,sep=";;;", header=None)
        df6 = df6[df6.isna().sum(1) < 9]
        df6.columns = ['category_title', 'subcategory_id','subcategory_title', 
        'subcategory_description', 'subcategory_url', 'course_id',
        'course_title', 'course_url', 'num_of_subscribers','avg_rating','num_of_reviews'] # get data

        plt.scatter(df6.index,df6.num_of_reviews) # plot
        plt.title("distribution of number of reviews")
        plt.tight_layout()
        plt.savefig("static/img/course_figure6.png")

        return "\na graph to show the distribution of courses based on the number of reviews ."


