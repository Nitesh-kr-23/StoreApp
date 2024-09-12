import mysql.connector as conn
from tabulate import tabulate 
m=conn.connect(host="localhost",user="root",passwd="",charset="utf8")
if m.is_connected():
         print("connected")
else:
         print("not connected")
cur=m.cursor()
cur.execute("create database if not exists cloth_store")
cur.execute("use cloth_store") 
cur.execute("create table if not exists product(PID int(10),PNAME char(20),BRAND char(20),CATEGORY char(20),PRICE int(10),QUANTITY int(10),SALE int(10),REMAINING int(10))")
cur.execute("create table if not exists customer(CID int(10),CNAME char(20),GENDER char(20),AGE int(10),PHONE char(10),ADDRESS char(50))")
cur.execute("create table if not exists bill(CID int(10),PID int(10),QUANTITY int(20))")


#Product Code

def product():
    while True:
        print("\t1.Insert Product Details")
        print("\t2.Display Product Details")
        print("\t3.Search Product Details")
        print("\t4.Update Product Details")
        print("\t5.Delete Product Details")
        print("\t6.Back To Main Menu")
        ch=int(input("Enter your choice"))
        if ch==1:
            insert()
        elif ch==2:
            display()
        elif ch==3:
            search()
        elif ch==4:
            update()
        elif ch==5:
            delete()
        elif ch==6:
            main()
        else:
            print("Please make an appropriate choice")
def insert():
    i=int(input("enter product id"))
    n=input("enter product name")
    b=input("enter brand name")
    c=input("enter product category")
    p=int(input("enter product price"))
    q=int(input("enter quantity"))
    s=int(input("enter sale"))
    remaining=q-s
    cur.execute("insert into product values({},'{}','{}','{}',{},{},{},{})".format(i,n,b,c,p,q,s,remaining))
    m.commit()
    print("PRODUCT RECORD SUCCESSFULLY INSERTED")
def display():
    cur.execute("Select * from product")
    c=cur.fetchall()
    t=tabulate(c,headers=['PID','PNAME','BRAND','CATEGORY','PRICE','QUANTITY','SALE','REMAINING'],tablefmt='fancy_grid')
    print(t)
def search():
    find=input("enter the column name to find the record ")
    find_value=input("enter value ")
    cur.execute("select * from product where {}='{}'".format(find,find_value))
    c=cur.fetchall()
    t=tabulate(c,headers=['PID','PNAME','BRAND','CATEGORY','PRICE','QUANTITY','SALE','REMAINING'],tablefmt='fancy_grid')
    print(t)
def update():
    mod=input("enter product id to update ")
    find=input("enter the column name whose value you want to change ")
    find_value=input("enter the value")
    cur.execute("update product set {}='{}' where PID={}".format(find,find_value,mod))
    m.commit()
    if find=='QUANTITY' or find=='SALE':
        cur.execute("update product set REMAINING=QUANTITY-SALE where PID={}".format(mod))
        m.commit()
        print("Product Record Succesfully Updated")
def delete():
    find=input("Enter product id to delete record")
    cur.execute("delete from product where PID={}".format(find))
    m.commit()



#User Code
    
def customer():
    while True:
        print("\t1.Insert Customer Details")
        print("\t2.Display Customer Details")
        print("\t3.Search Customer Details")
        print("\t4.Update Customer Details")
        print("\t5.Delete Customer Details")
        print("\t6.Back To Main Menu")
        ch=int(input("Enter your choice"))
        if ch==1:
            insertC()
        elif ch==2:
            displayC()
        elif ch==3:
            searchC()
        elif ch==4:
            updateC()
        elif ch==5:
            deleteC()
        elif ch==6:
            main()
        else:
            print("lnvalid choice entered")

def insertC():
    i=int(input("Enter Customer Id"))
    n=input("Enter Customer Name")
    g=input("Enter Customer Gender")
    a=int(input("Enter Customer Age"))
    p=input("Enter Customer Phone no.")
    ads=input("Enter Customer Address")
    cur.execute("insert into customer values({},'{}','{}',{},'{}','{}')".format(i,n,g,a,p,ads))
    m.commit()
    print("Customer Record Succesfully Inserted")
    purchase()

def displayC():
    cur.execute("Select*from customer")
    c=cur.fetchall()
    t=tabulate(c,headers=['CID','CNAME','GENDER','AGE','PHONE','ADDRESS'],tablefmt='fancy_grid')
    print(t)

def searchC():
    find=input("enter the column name to find the record ")
    find_value=input("enter the value")
    cur.execute("select*from customer where {}='{}'".format(find,find_value))
    c=cur.fetchall()
    t=tabulate(c,headers=['CID','CNAME','GENDER','AGE','PHONE','ADDRESS'],tablefmt='fancy_grid')
    print(t)

def updateC():
    mod=input("enter customer id to update ")
    find=input("enter the column name whose value you want to change ")
    find_value=input("enter value")
    cur.execute("update customer set {}='{}' where CID={}".format(find,find_value,mod))
    m.commit()
    print("Customer Record Successfully Updated")

def deleteC():
    find=input("Enter Customer id to delete record")
    cur.execute("delete from customer where CID={}".format(find))
    m.commit()

def purchase():
    c=int(input("enter customer id to purchase product"))
    ch='y'
    while ch=='y':
        p=int(input("enter product id"))
        q=int(input("enter quantity"))
        ch=input("If you want to purchase more item press y to continue")
        cur.execute("insert into bill values({},{},{})".format(c,p,q))
        m.commit()


def bill():
    e=int(input("enter customer id"))
    cur.execute("select * from customer,bill where customer.CID=bill.CID and customer.CID={}".format(e))
    j=cur.fetchall()
    r=cur.rowcount
    cur.execute("select * from product,bill where product.PID=bill.PID and CID={}".format(e))
    i=cur.fetchall()
    s=0
    print("-"*95)
    print(" "*30,"Customer Bill")
    print("-"*95)          
    print("Customer Id".ljust(25),j[0][0])
    print("Name".ljust(25),j[0][1])
    print("Gender".ljust(25),j[0][2])
    print("Age".ljust(25),j[0][3])
    print("Phone".ljust(25),j[0][4])
    print("Address".ljust(25),j[0][5])
    print("-"*40)
    for k in range(r):
        print("Product Id".ljust(25),i[k][0])
        print("Name".ljust(25),i[k][1])
        print("Brand".ljust(25),i[k][2])
        print("Category".ljust(25),i[k][3])
        print("Price".ljust(25),i[k][4])
        print("Quantity".ljust(25),i[k][10])
        print("Cost".ljust(25),i[k][4]*i[k][10])
        s=s+i[k][4]*i[k][10]
    print("-"*95)
    print("Total payable amount is: ".ljust(15),s)
    print("-"*95)
    print("THANKS FOR VISITING")
    main()

#main start

def main():
    print()
    print("*"*35,"CLOTH STORE MANAGEMENT","*"*35)
    print("l. PRODUCT DETAILS")
    print("2. CUSTOMER DETAILS")
    print("3. BILL")
    print("4. Exit")
    cs=int(input("Enter the user choice"))
    if cs==1:
        product()
    elif cs==2:
        customer()
    elif cs==3:
        bill()
        m.close()
    elif cs==4:
        exit()
    else:
        print("lnvalid choice entered ")
main()
