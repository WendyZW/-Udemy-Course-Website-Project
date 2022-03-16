import random
from lib.helper import get_day_from_timestamp, user_data_path


class User:
    def __init__(self, new_id=-1, username="", password="", email="empty@gmail.com", register_time="xx-xx-xxxx"):
        # your code
        # initializing
        self.id = new_id
        self.name = username
        self.password = password
        self.email = email
        self.register_time = register_time
#         pass

    def __str__(self):
        # your code
        # format print out
        res = "user id: {} | username: {} | password: {} | email: {} |register_time: {}"
        return res.format(self.id, self.name, self.password,
                         self.email, self.register_time)

    def authenticate_user(self, username, password):
        result = False
        # your code
        password = self.encrypt_password(password) # get encrypt_password
        with open(user_data_path) as f: # lookup value 
            for l in f:
                itms = l.split(";;;")
                n = itms[1]
                p = itms[2]
                if n == username:
                    if p == password: # if mathced
                        result = True
                        break
        return result

    def check_username_exist(self, username):
        result = False
        # your code
        with open(user_data_path) as f: # read data and lookup if user exists
            for l in f:
                itms = l.split(";;;")
                n = itms[1]
                if n == username:
                    result = True
                    break
        return result

    def generate_unique_user_id(self): 
        new_id = "".join([str(random.randint(0, 9)) for i in range(6)]) # create userid
        
        with open(user_data_path) as f:
            for l in f:
                itms = l.split(";;;")
                d = itms[0]
                if d == new_id: # if exists
                    return self.generate_unique_user_id() # do once more
        return new_id

    def encrypt_password(self, password):
        # your code
        new_p = []
        fix = "**"
        for ch in password:
            if ch.isdigit(): # for digit terms
                n = int(ch) * 10 + 5
                n = str(int(n))
                new_p.append(fix + n + fix)
            else:
                new_p.append(fix + ch + fix) # for strings
        a =  "".join(new_p)
        
        return a

    def register_user(self, username, password, email, register_time):
        result = False
        # your code
        with open(user_data_path) as f:
            for l in f:
                itms = l.split(";;;")
                n = itms[1]
                if n == username:
                    return result # if user exists
        self.id = self.generate_unique_user_id() # creat id
        smi = ";;;"
        row = smi.join([self.id, username, 
                        self.encrypt_password(password),
                       email, self.date_conversion(register_time)]) # create rows
        with open(user_data_path, 'a') as f:  # append to data bank
            f.write(row + "\n")
            result = True
        return result

    # sample time: 1637549590753   milli seconds
    def date_conversion(self, register_time): # convert to melbourne time
        # Human Readable Time	        Seconds
        # 1 Hour	                    3600 Seconds
        # 1 Day	                        86400 Seconds
        # 1 Week	                    604800 Seconds
        # 1 Month	                    2629743 Seconds
        # 1 Year 	                    31556926 Seconds

        # test time here https://www.unixtimestamp.com/index.php

        # melbourne time is GMT+11
        
        # your code
        
        
        # compute base
        y = 31556926e3
        m = 2629743e3
        w =  604800e3
        d = 86400e3
        h = 3600e3
        ms = 60e3
        s = 1e3
        a = int(register_time)
        def get_divd(a, b):# get divd int and rest
    
            return int(a //b), a%b 
        year, mm = get_divd(a, y)
        mm, dd = get_divd(mm, m)
        dd, hh = get_divd(dd, d)
        hh, mms = get_divd(hh, h)
        mms, ss = get_divd(mms, ms)
        ss, r = get_divd(ss, s)
        
        # format string
        res = str(year +1970) + "-" +str(mm + 1)\ 
        + "-" + str(dd + 1) + " " + str(hh + 1) + ":" + str(mms) \
        +  ":"+ str(ss) + "." + str(int(r))
        
        

        return res