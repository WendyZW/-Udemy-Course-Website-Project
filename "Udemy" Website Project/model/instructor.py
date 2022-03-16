import os, re, math
import numpy as np
import pandas as pd
from model.course import Course
import matplotlib.pyplot as plt
from lib.helper import course_data_path, instructor_data_path, figure_save_path, course_json_files_path


class Instructor:

    def __init__(self, id=-1, display_name="", job_title="", image_100x100="", 
                 course_id=0):
         # your code
         # initalizing
        self.id = id
        self.display_name = display_name
        self.job_title = job_title
        self.image_100x100 = image_100x100
        self.course_id = course_id
        

    def __str__(self):
        # your code
        # for human read print out
        res = "instructor id:{} | {} | {} | {}"
            
        
        return res.format(self.id, self.display_name, self.job_title, self.image_100x100)

    def clear_instructor_data(self):
         # your code
         # reset data
        with open(instructor_data_path, 'w') as csv:
            rows = ";;;".join([""] * 5)
            csv.write(rows)

    def get_instructors(self):
        # your code
        
        with open(instructor_data_path, 'wb') as csv: # open files to save result
          # your code
            p = '"visible_instructors(.*?)image_125_H"' # regex pattern
            removes = ['"', '{', "}", '[', ']'] # unuseful chars
            def get_chars(x): # clean strings
                for i in removes:
                    x = x.replace(i, '')
                return x
            def get_row(li): # get dictionary of key as requried term and v is value

                items = li.split(',"')
                items = [get_chars(i) for i in items]
                tmp_d = {}
                for i in items:
                    ss = i.split(":")
                    k = ss[0]
                    v = "".join(ss[1:])
                    tmp_d[k] = v.replace("https", "https:")
                return tmp_d
            def get_list(ids, d): # format string to save
                res = [ids]
                for k in ['id', 'display_name', 'job_title', 'image_100x100']:
                    if k in d.keys():
                        res.append(d[k])
                    else:
                        res.append('')
                return ";;;".join(res)
            for root, dirs, files in os.walk(course_json_files_path[1:], topdown=False): # loop dirs
                for name in files:
                    tmp = os.path.join(root, name)
                    with open(tmp, encoding="utf-8-sig") as f:
                        for l in f:
                            L = l.split(",")
                            cursid = [i for i in L if i.find('"id"') >= 0][1].split(":")[-1].replace('"', '').split("}")[0] # course id
                            L = re.findall(p,l)
                            for li in L:
                                dc =get_row(li)
                                rows = get_list(cursid, dc) # rows to write
                                csv.write((rows + "\n").encode("utf-8-sig")) # save

    def get_total_number_of_unique_instructors(self):
        total_num_instructors = 20
        # your code
        df = pd.read_csv(instructor_data_path,header=None, sep =';;;') # load data
        total_num_instructors = df[df.columns[1]].nunique() # get unique instructor
        return total_num_instructors

    def find_courses_by_instructor_id(self, instructor_id):
        result = []
        # your code
        df = pd.read_csv(course_data_path,sep=";;;", header=None) # course file
        df = df[df.isna().sum(1) < 9]
        df.columns = ['category_title', 'subcategory_id','subcategory_title', 
        'subcategory_description', 'subcategory_url', 'course_id',
        'course_title', 'course_url', 'num_of_subscribers','avg_rating','num_of_reviews']

        dfins = pd.read_csv(instructor_data_path, sep=';;;', header=None) # instructor fil
        columns = ["_"] * dfins.shape[1]
        columns[1] = 'ids'
        columns[0] = 'cid'
        dfins.columns = columns
        tmp_rows = dfins[dfins.ids == instructor_id]
        tmp_rows['cid'] = tmp_rows['cid'].apply(lambda x: int(str(x).replace("\ufeff", '')))
        tmp_cours = df[df.course_id.isin(tmp_rows.cid.unique())].head(20).copy() # get course of this instructor

        for j, i in tmp_cours.iterrows(): # loop and create class object
            temp_course = Course(category_title=i[0], subcategory_id=int(i[1]),
                                                     subcategory_title= i[2], subcategory_description=i[3],
                                                      subcategory_url=i[4], course_id=int(i[5]),
                                                      course_title=i[6], course_url=i[7], num_of_subscribers=int(i[8]),
                                                      avg_rating=i[9], num_of_reviews=i[10])
            result.append(temp_course)
        return result, tmp_cours.shape[0]

    def get_instructors_by_page(self, page):  # each page has 20 courses

        result_instructor_list = [] # list to store class obj
        total_page_num = 0
        # your code
        result_course_list = []
        total_page_num = 0
        # your code
        df = pd.read_csv(instructor_data_path,sep=";;;", header=None)
        df = df[df.isna().sum(1) < 4]
        if df.shape[0] == 0: # in case no data 
            return result_instructor_list,total_page_num 
        df.index = range(1, df.shape[0] + 1)
        num_page = int(np.ceil(df.shape[0] /20))
        frm = (page -1) * 20 
        end = min(frm + 20,max(df.index ))
        tmp_df = df.iloc[frm:end,:].copy()
        res_list = []
        for j, i in tmp_df.iterrows(): # loop and create obj
            try:

                res_list.append(Instructor(id=int(i[1]), display_name=i[2], job_title= i[3], image_100x100=i[4], # some id is na.
                                                course_id=i[0]))
            except:
                res_list.append(Instructor(id=i[1], display_name=i[2], job_title= i[3], image_100x100=i[4], #na id
                                                course_id=i[0]))
                pass
        return res_list, num_page


    def generate_instructor_figure1(self):
        # your code
        df = pd.read_csv(instructor_data_path, ';;;', header = None)
        tmpp = df[df[1].isna() == False].groupby(df.columns[1])[[1]].count() # create data
        tmpp.index = [int(i) for i in tmpp.index]
        tmpp.index.name = 'instructor_id'
        plt.figure()
        tmpp.sort_values(1,ascending = False).head(10).plot.barh() # plot
        plt.title("top instructor by number of courses")
        plt.tight_layout()
        plt.savefig('static/img/instructor_figure1')
        return "\n a graph that shows the top 10 instructors who teach the most courses"

