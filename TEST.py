a_list = [datetime.datetime(2000,5,20),datetime.datetime(2000,5,20),datetime.datetime(2000,5,20)]
b_list = [datetime.datetime(2000,5,22),datetime.datetime(2000,5,23),datetime.datetime(2005,5,20)]
a_list_np = np.array(a_list)
b_list_np = np.array(b_list)

a_list = ["2020-01-07 22:46:06","2020-01-07 22:46:12","2020-01-07 22:46:20","2020-01-07 22:46:25","2020-01-07 22:46:58","2020-01-07 22:47:03","2020-01-07 22:47:22"
          ,"2020-01-07 22:47:27","2020-01-07 22:47:29","2020-01-07 22:47:34"]
b_list = a_list[1:]
b_list.append(a_list[-1])
a_list_np = map(string2datetime,a_list)
b_list_np = map(string2datetime,b_list)
a_list_np = np.array(a_list_np)
b_list_np = np.array(b_list_np)
result_dt = b_list_np - a_list_np
result_str = map(tinterval_string,result_dt)
print(result_str)