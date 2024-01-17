import csv
from datetime import datetime
from dateutil.relativedelta import relativedelta
try:
    id_list=[]
    def checking():
        try:
            with open("C:\\my_file\\Contracts.csv", "r") as inp_file:
                # scape the header
                next(inp_file)
                # making an date object for the purpose of reading
                data = csv.reader(inp_file)
                for row in data:
                    id_list.append(row[0])
        except FileNotFoundError:
            print("csv file not found")
        except ValueError:
            print("invalid in ID value")
        except PermissionError:
            print("the file is already open")


    def agent(id):
        # making a list of non-working_days
        off_days = [4,5]
        # assigning the payment method to the variable  inst_m
        inst_m = {1:'ANNUAL', 4:'QUARTER', 12:'MONTHLY', 2:'HALF_ANNUAL'}
        # assigning column title or header to  the variable header
        header = ['installment_serial', 'installment date', 'installment amount', 'max grace date']
        # opening the file as read method to read the values
        with open("C:\\my_file\\Contracts.csv","r") as inp_file:
            # scape the header
            next(inp_file)
            # making an date object for the purpose of reading
            data = csv.reader(inp_file)
            # iterate over the rows of date to find the required data
            for row in data:
                if id not in id_list:
                    print('This id is not exist')
                    break
                if row[0] == id:
                    #  making the file according to the client name
                    _path = f"{row[0]}-{row[5]}-installment"
                    # creat the file
                    write_file = open(f"C:\\my_file\\{_path}.csv",'w',newline='')
                    # make the write object
                    write_obj = csv.writer(write_file)
                    # write the header to the file
                    write_obj.writerow(header)
                    # transfer the start date from slashes(1/1/2010) to minus(2010-1-1)
                    start_date_list = row[1].split('/')
                    start_date = datetime(int(start_date_list[2]),int(start_date_list[1]),int(start_date_list[0])).date()
                    # transfer the end date from slashes(1/1/2010) to minus(2010-1-1)
                    end_date_list = row[2].split('/')
                    end_date = datetime(int(end_date_list[2]),int(end_date_list[1]) ,int(end_date_list[0])).date()
                    # find the difference between the two dates
                    diff = relativedelta(end_date,start_date).years
                    add_months = 0
                    # for selecting the payment method for the dictionary inst_m
                    if row[6] == inst_m[1]:
                        diff = diff * 1
                        add_months = 12
                    elif row[6] == inst_m[2]:
                        diff = diff * 2
                        add_months = 6
                    elif row[6] == inst_m[4]:
                        diff = diff * 4
                        add_months = 3
                    elif row[6] == inst_m[12]:
                        diff = diff*12
                        add_months = 1
                    # calculating the installment amount
                    ins_amount = (int(row[3])-int(row[4])) / diff
                    # iteration for selecting date and making operation
                    for r_num in range(diff):
                        # setting the initial value for grace period to zero
                        max_grace_period = 0
                        # setting variable initial _date to use it in processing
                        initial_date = start_date
                        # incrementation for serial by one
                        installment_serial = r_num+1
                        # adding variable max_date representing maximum payment date
                        max_date = initial_date
                        # avoiding the non_working days
                        while initial_date.weekday() in off_days:
                            initial_date = initial_date + relativedelta(days=1)
                        # adding the grace period
                        while max_grace_period <= (int(row[7])-1):
                            max_date = max_date+relativedelta(days=1)
                            if max_date.weekday() not in off_days:
                                max_grace_period = max_grace_period + 1
                        # installment amount in the format of money
                        amount = f'{ins_amount:,.2f}'
                        # adding the results to list for writing
                        lst_row=[installment_serial,initial_date,amount,max_date]
                        # writing the results to the out
                        write_obj.writerow(lst_row)
                        start_date = start_date + relativedelta(months=add_months)
    # asking the user for the required agent through the id number
    agent_id = input('Enter the agent ID for processing :')
    # go to the function for checking the id
    checking()
    # calling the function through the agent id for processing
    agent(agent_id)
# exception for expected error
except FileNotFoundError:
    print("csv file not found")
except ValueError:
    print("invalid in ID value")
except PermissionError:
    print("the file is already open")

