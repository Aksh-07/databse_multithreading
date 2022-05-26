# Inserting and Fetching Data into Database using Multi-threading

## Libraries Used
#### 1. threading:
                    1.a Semaphore: To lock crucial parts of database
                    1.b get_indent: to get id of current thread

#### 2. sqlite3: 
                    Used to create and handle Databse in our project

#### 3. concurrent.futures: 
                    ThreadPoolExecutor to handle threads efficiently

#### 4. time:
                    to track total time in code execution


------------------------------------------------------------------------------------------------------------------------
## Database Structure

### Database name:  practice.db
Contains 1 table with 4 columns:
                                         
                                          my_table   

                      column1  |   column2  |  column3    |   column4
                    -----------|------------|-------------|------------
                      Integer  |   Integer  |  Integer    |  String(contain list)

________________________________________________________________________________________________________________________

## User defined Functions
1. create_table: Create a table named **my_table**
2. delete_table: Delete the table
3. insert: To insert multiple items into database
4. fetch: To fetch all the data from database
5. convert_data: To convert raw data into structured data that can be used easily with insert function

________________________________________________________________________________________________________________________

## Raw data file
We have dummy data in dataset.txt file, containing around 1470 data items in form of tuples with 4 items.
first 3 items are integers and last item is a list of integers or string

------------------------------------------------------------------------------------------------------------------------

## working of code
_Here we have 2 approaches to tackle this process_

### 1. batch_insert.py

We have a table _my_table_ in our database _practice.db_ structured in the same way as our raw data.
In this approach we are using batch insert with executemany in our insert function and there are 4 threads running
concurrently to insert data into our table.
First we read the raw data from dataset into a variable name data using open with context manager.
Then our convert_data functions changes the data type from tuple to a list and of our 4th item in list(which is also a list) 
to a string and then divide the whole raw data into 4 equal parts and store them into data_list1, data_list2, data_list3, data_list4
After that we create 4 threads using ThreadPoolExecutor with context manager.
All the threads run the same function Insert to Upload data into table, for threads to work concurrently and in sync 
with each other **Semaphores** are used with count value as 4, to allow 4 different threads to access the critical part 
of our insert function part.
Now we have created 4 different batches from raw data and can use executemany to batch insert the whole list at once,
and since 4 threads are running on this function, all the batches of data are being inserted concurrently
When all the threads are done inserting the data, fetch function is called to fetch all the data from our table in the 
database and print them on our screen along with the primary key(which is an integer) and data items
After fetching the threads are destroyed and the main thread calculate finish time and print total time taken by the 
process to execute.

TOTAL TIME TAKEN BY THE PROCESS TO EXECUTE: AROUND 0.2 SECONDS

### 2. single_insert.py
    In this approach an extra library is used ---- queue.Queue
We have a table _my_table_ in our database _practice.db_ structured in the same way as our raw data.
In this approach we are inserting single row of item from our data using execute in our insert function and there are 
4 threads running concurrently to insert data into our table.
First we read the raw data from dataset into a variable name data using open with context manager.
Then our convert_data functions changes the data type from tuple to a list and of our 4th item in list(which is also a list) 
to a string and then push the item to a Queue named as q
After that we create 4 threads using ThreadPoolExecutor with context manager.
All the threads run the same function Insert to Upload data into table, for threads to work concurrently and in sync 
with each other **Semaphores** are used with count value as 4, to allow 4 different threads to access the critical part 
of our insert function part.
Each of the 4 threads get a value in sync from q(Queue) and insert it into the table until the q is empty.
When all the threads are done inserting the data, fetch function is called to fetch all the data from our table in the 
database and print them on our screen along with the primary key(which is an integer) and data items
After fetching the threads are destroyed and the main thread calculate finish time and print total time taken by the 
process to execute.

TOTAL TIME TAKEN BY THE PROCESS TO EXECUTE: AROUND 8 SECONDS
