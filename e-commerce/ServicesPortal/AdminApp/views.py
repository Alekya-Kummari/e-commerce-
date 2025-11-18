from django.shortcuts import render
import pymysql
import base64


# Create your views here.
def login(request):
    return render(request,'AdminApp/Login.html')
def AdminAction(request):
    uname=request.POST['username']
    pwd=request.POST['password']

    if uname=='Admin' and pwd =='Admin':
        return render(request,'AdminApp/AdminHome.html')
    else:
        return render(request,'AdminApp/Login.html')
def addservice(request):
    return render(request,'AdminApp/AddServices.html')
def AdminHome(request):
    return render(request,'AdminApp/AdminHome.html')

def fetch_image_blob(id):
    connection=pymysql.connect(host='localhost', user='root',password='root', database='service_portal', charset='utf8')
    with connection.cursor() as cursor:
        cursor.execute("SELECT image FROM register WHERE id=%s", [id])
        row = cursor.fetchone()
    return row[0] if row else None

def ViewCustomers(request):
    con=pymysql.connect(host='localhost', user='root',password='root', database='service_portal', charset='utf8')
    cur=con.cursor()
    table="<table><tr><th>Name</th><th>Email</th><th>Mobile</th><th>Image</th><th>Status</th></tr>"

    cur.execute("select * from register")
    data=cur.fetchall()
    for d in data:
        st=d[7]
        iid=d[0]
        image_blob = fetch_image_blob(iid)

        image_base64 = base64.b64encode(image_blob).decode('utf-8')
        if st=='waiting':
            table+="<tr><td>"+str(d[1])+"</td><td>"+str(d[2])+"</td><td>"+str(d[3])+"</td><td>"f'<img src="data:image/png;base64,{image_base64}" alt="Image" />'"</td><td><a href='/admin/accept?id="+str(d[0])+"'>Accept</a></td></tr>"
        else:
            table+="<tr><td>"+str(d[1])+"</td><td>"+str(d[2])+"</td><td>"+str(d[3])+"</td><td>"f'<img src="data:image/png;base64,{image_base64}" alt="Image" />'"</td><td>"+st+"</td></tr>"

    table+="</table>"
    context={'data':table}
    return render(request,'AdminApp/ViewAllCustomers.html', context)

def accept(request):
    iid=request.GET['id']
    con=pymysql.connect(host='localhost', user='root',password='root', database='service_portal', charset='utf8')
    cur=con.cursor()
    cur.execute("update register set status='Accepted' where id='"+iid+"'")
    con.commit()
    cur1=con.cursor()
    table="<table><tr><th>Name</th><th>Email</th><th>Mobile</th><th>Image</th><th>Status</th></tr>"

    cur1.execute("select * from register")
    data=cur1.fetchall()
    for d in data:
        st=d[7]
        iid=d[0]
        image_blob = fetch_image_blob(iid)

        image_base64 = base64.b64encode(image_blob).decode('utf-8')
        if st=='waiting':
            table+="<tr><td>"+str(d[1])+"</td><td>"+str(d[2])+"</td><td>"+str(d[3])+"</td><td>"f'<img src="data:image/png;base64,{image_base64}" alt="Image" />'"</td><td><a href='/admin/accept?id="+str(d[0])+"'>Accept</a></td></tr>"
        else:
            table+="<tr><td>"+str(d[1])+"</td><td>"+str(d[2])+"</td><td>"+str(d[3])+"</td><td>"f'<img src="data:image/png;base64,{image_base64}" alt="Image" />'"</td><td>"+st+"</td></tr>"

    table+="</table>"
    context={'data':table,'image_base64':image_base64,'msg':'Custome Accepted Successfully...!!'}
    return render(request,'AdminApp/ViewAllCustomers.html', context)

def serviceaction(request):
    servicename=request.POST['servicename']

    con=pymysql.connect(host='localhost', user='root',password='root', database='service_portal', charset='utf8')
    cur=con.cursor()
    cur.execute("select * from service where service='"+servicename+"'")
    d=cur.fetchone()
    if d is not None:
     context={'msg':'Service Name Already Exist...!!'}
     return render(request,'AdminApp/AddServices.html', context)
    else:
        cur=con.cursor()
        cur.execute("insert into service values(null,'"+servicename+"')")
        con.commit()
        context={'msg':'Service Name Added Successfully...!!'}
        return render(request,'AdminApp/AddServices.html', context)



def viewserivces(request):
    con=pymysql.connect(host='localhost', user='root',password='root', database='service_portal', charset='utf8')
    cur=con.cursor()

    cur.execute("select * from sregister")
    data=cur.fetchall()
    table="<table><tr><th>Service Name</th><th>Email</th><th>Mobile</th><th>Working Hours</th><th>Cost</th></tr>"
    for d in data:
        table+="<tr><td>"+str(d[1])+"</td><td>"+str(d[2])+"</td><td>"+str(d[7])+"</td><td>"+str(d[5])+"</td><td>Rs."+str(d[6])+"</td></tr>"
    table+="</table>"
    context={'data':table}
    return render(request,'AdminApp/ViewServices.html', context)

def AddSerivces(request):
    con=pymysql.connect(host='localhost', user='root',password='root', database='service_portal', charset='utf8')
    cur=con.cursor()
    cur.execute("select * from service")
    data=cur.fetchall()
    table=""
    for d in data:
        table+="<option value="+str(d[1])+">"+str(d[1])+"</option>"

    context={'d':table}
    return render(request,'AdminApp/AddService.html',context)



def ServiceRegAction(request):
    servicename=request.POST['servicename']
    email=request.POST['email']
    username=request.POST['username']
    password=request.POST['password']
    w_hours=request.POST['w_hours']
    cost=request.POST['cost']
    mobile=request.POST['mobile']



    con=pymysql.connect(host='localhost', user='root',password='root', database='service_portal', charset='utf8')
    cur=con.cursor()
    cur.execute("select * from sregister where service='"+servicename+"' and email='"+email+"' and mobile='"+mobile+"'")
    d=cur.fetchone()
    if d is not None:
     cur=con.cursor()
     cur.execute("select * from service ")
     data=cur.fetchall()
     table="<select class='contactus' name='servicename'>"
     for d in data:
         table+="<option value="+str(d[1])+">"+str(d[1])+"</option>"
     table+="</select>"
     context={'msg':'User Already Exist...!!','data':table}
     return render(request,'AdminApp/AddService.html',context)
    else:
        cur=con.cursor()
        cur.execute("insert into sregister values(null,'"+servicename+"','"+email+"','"+username+"','"+password+"','"+w_hours+"','"+cost+"','"+mobile+"')")
        con.commit()
        cur=con.cursor()
        cur.execute("select * from service ")
        data=cur.fetchall()
        table="<select class='contactus' name='servicename'>"
        for d in data:
            table+="<option value="+str(d[1])+">"+str(d[1])+"</option>"
        table+="</select>"
        context={'data':table,'msg':'Successfully Registered Your Details...!!'}
        return render(request,'AdminApp/AddService.html',context)

def AddProducts(request):
    return render(request,'AdminApp/AddProducts.html')

def ProductAction(request):
    if request.method == 'POST' and request.FILES['image']:
        pname=request.POST['pname']
        price=request.POST['price']
        usage=request.POST['usage']
        image=request.FILES['image'].read()


        con=pymysql.connect(host='localhost', user='root',password='root', database='service_portal', charset='utf8')
        cur=con.cursor()
        cur.execute("select * from product where pname='"+pname+"'")
        d=cur.fetchone()
        if d is not None:
            context={'msg':'Product Already Exist...!!'}
            return render(request,'AdminApp/AddProducts.html', context)
        else:
            cur=con.cursor()
            cur.execute('insert into product values(null,%s,%s,%s,%s)',(pname,price,usage,image))
            con.commit()
            context={'msg':'Successfully Product Added...!!'}
            return render(request,'AdminApp/AddProducts.html', context)

def fetch_image_blob_from_product(id):
    connection=pymysql.connect(host='localhost', user='root',password='root', database='service_portal', charset='utf8')
    with connection.cursor() as cursor:
        cursor.execute("SELECT image FROM product WHERE id=%s", [id])
        row = cursor.fetchone()
    return row[0] if row else None

def viewproducts(request):
    con=pymysql.connect(host='localhost', user='root',password='root', database='service_portal', charset='utf8')
    cur=con.cursor()

    cur.execute("select * from product")
    data=cur.fetchall()
    table="<table><tr><th>Product Name</th><th>Price</th><th>Product Usage</th><th>Product Image</th></tr>"
    for d in data:
        iid=d[0]
        image_blob = fetch_image_blob_from_product(iid)
        image_base64 = base64.b64encode(image_blob).decode('utf-8')
        table+="<tr><td>"+str(d[1])+"</td><td>"+str(d[2])+"</td><td>"+str(d[3])+"</td><td>"f'<img src="data:image/png;base64,{image_base64}" alt="Image" />'"</td>"
    context={'data':table}
    return render(request,'AdminApp/ViewAllProducts.html', context)

def viewbookings(request):

    con=pymysql.connect(host='localhost', user='root',password='root', database='service_portal', charset='utf8')
    cur=con.cursor()
    cur.execute("select * from product_book pb, register r,product p where pb.user_id=r.id and p.id=pb.product_id")
    data=cur.fetchall()
    table="<table><tr><th>Customer Name</th><th>Email</th><th>Mobile</th><th>Product Name</th><th>Product Price</th><th>Booked Date</th><th>Status</th></tr>"
    for d in data:
        status=d[4]
        if status=='waiting':
            table+="<tr><td>"+str(d[6])+"</td><td>"+str(d[7])+"</td><td>"+str(d[8])+"</td><td>"+str(d[13])+"</td><td>"+str(d[14])+" Rs.</td><td>"+str(d[3])+"</td><td><a href='/admin/AcceptProduct?sid="+str(d[0])+"'>Accept</a></td></tr>"
        else:
            table+="<tr><td>"+str(d[6])+"</td><td>"+str(d[7])+"</td><td>"+str(d[8])+"</td><td>"+str(d[13])+"</td><td>"+str(d[14])+" Rs.</td><td>"+str(d[3])+"</td><td>"+str(d[4])+"</td></tr>"
    table+="</table>"

    cur.execute("select * from service_book sb, register r,sregister s where sb.userid=r.id and s.id=sb.service_id")
    data=cur.fetchall()
    srtable="<table><tr><th>Customer Name</th><th>Mobile</th><th>Service Name</th><th>Mobile</th><th>Working Hours</th><th>Cost</th><th>Booked Date</th><th>Status</th></tr>"
    for d in data:
        status=d[4]
        if status=='waiting':
            srtable+="<tr><td>"+str(d[6])+"</td><td>"+str(d[8])+"</td><td>"+str(d[13])+"</td><td>"+str(d[19])+"</td><td>"+str(d[17])+"</td><td>"+str(d[18])+" Rs.</td><td>"+str(d[3])+"</td><td><a href='/admin/AcceptService?sid="+str(d[0])+"'>Accept</a></td></tr>"
        else:
            srtable+="<tr><td>"+str(d[6])+"</td><td>"+str(d[8])+"</td><td>"+str(d[13])+"</td><td>"+str(d[19])+"</td><td>"+str(d[17])+"</td><td>"+str(d[18])+" Rs.</td><td>"+str(d[3])+"</td><td>"+str(d[4])+"</td></tr>"
    srtable+="</table>"
    context={'data':table,'servicetable':srtable}
    return render(request,'AdminApp/ViewAllBookings.html', context)


def AcceptProduct(request):
    sid=request.GET['sid']

    con=pymysql.connect(host='localhost', user='root',password='root', database='service_portal', charset='utf8')
    cur=con.cursor()
    cur.execute("update product_book set status='Accepted' where id='"+sid+"'")
    cur=con.cursor()
    con.commit()
    cur=con.cursor()
    cur.execute("select * from product_book pb, register r,product p where pb.user_id=r.id and p.id=pb.product_id")
    data=cur.fetchall()
    table="<table><tr><th>Customer Name</th><th>Email</th><th>Mobile</th><th>Product Name</th><th>Product Price</th><th>Booked Date</th><th>Status</th></tr>"
    for d in data:
        status=d[4]
        if status=='waiting':
            table+="<tr><td>"+str(d[6])+"</td><td>"+str(d[7])+"</td><td>"+str(d[8])+"</td><td>"+str(d[13])+"</td><td>"+str(d[14])+" Rs.</td><td>"+str(d[3])+"</td><td><a href='/admin/AcceptProduct?sid="+str(d[0])+"'>Accept</a></td></tr>"
        else:
            table+="<tr><td>"+str(d[6])+"</td><td>"+str(d[7])+"</td><td>"+str(d[8])+"</td><td>"+str(d[13])+"</td><td>"+str(d[14])+" Rs.</td><td>"+str(d[3])+"</td><td>"+str(d[4])+"</td></tr>"
    table+="</table>"

    cur.execute("select * from service_book sb, register r,sregister s where sb.userid=r.id and s.id=sb.service_id")
    data=cur.fetchall()
    srtable="<table><tr><th>Customer Name</th><th>Mobile</th><th>Service Name</th><th>Mobile</th><th>Working Hours</th><th>Cost</th><th>Booked Date</th><th>Status</th></tr>"
    for d in data:
        status=d[4]
        if status=='waiting':
            srtable+="<tr><td>"+str(d[6])+"</td><td>"+str(d[8])+"</td><td>"+str(d[13])+"</td><td>"+str(d[19])+"</td><td>"+str(d[17])+"</td><td>"+str(d[18])+" Rs.</td><td>"+str(d[3])+"</td><td><a href='/admin/AcceptService?sid="+str(d[0])+"'>Accept</a></td></tr>"
        else:
            srtable+="<tr><td>"+str(d[6])+"</td><td>"+str(d[8])+"</td><td>"+str(d[13])+"</td><td>"+str(d[19])+"</td><td>"+str(d[17])+"</td><td>"+str(d[18])+" Rs.</td><td>"+str(d[3])+"</td><td>"+str(d[4])+"</td></tr>"
    srtable+="</table>"
    context={'data':table,'servicetable':srtable,'msg':'Successfully Accepted Request...!!'}
    return render(request,'AdminApp/ViewAllBookings.html', context)





def AcceptService(request):
    sid=request.GET['sid']
    con=pymysql.connect(host='localhost', user='root',password='root', database='service_portal', charset='utf8')
    cur=con.cursor()
    cur.execute("update service_book set status='Accepted' where id='"+sid+"'")
    cur=con.cursor()
    con.commit()

    ##Reading Product Booking Data
    cur.execute("select * from product_book pb, register r,product p where pb.user_id=r.id and p.id=pb.product_id")
    data=cur.fetchall()
    table="<table><tr><th>Customer Name</th><th>Email</th><th>Mobile</th><th>Product Name</th><th>Product Price</th><th>Booked Date</th><th>Status</th></tr>"
    for d in data:
        status=d[4]
        if status=='waiting':
            table+="<tr><td>"+str(d[6])+"</td><td>"+str(d[7])+"</td><td>"+str(d[8])+"</td><td>"+str(d[13])+"</td><td>"+str(d[14])+" Rs.</td><td>"+str(d[3])+"</td><td><a href='/admin/AcceptProduct?sid="+str(d[0])+"'>Accept</a></td></tr>"
        else:
            table+="<tr><td>"+str(d[6])+"</td><td>"+str(d[7])+"</td><td>"+str(d[8])+"</td><td>"+str(d[13])+"</td><td>"+str(d[14])+" Rs.</td><td>"+str(d[3])+"</td><td>"+str(d[4])+"</td></tr>"
    table+="</table>"


    ##Reading Service Booking Data
    cur.execute("select * from service_book sb, register r,sregister s where sb.userid=r.id and s.id=sb.service_id")
    data=cur.fetchall()
    srtable="<table><tr><th>Customer Name</th><th>Mobile</th><th>Service Name</th><th>Mobile</th><th>Working Hours</th><th>Cost</th><th>Booked Date</th><th>Status</th></tr>"
    for d in data:
        status=d[4]
        if status=='waiting':
            srtable+="<tr><td>"+str(d[6])+"</td><td>"+str(d[8])+"</td><td>"+str(d[13])+"</td><td>"+str(d[19])+"</td><td>"+str(d[17])+"</td><td>"+str(d[18])+" Rs.</td><td>"+str(d[3])+"</td><td><a href='/admin/AcceptService?sid="+str(d[0])+"'>Accept</a></td></tr>"
        else:
            srtable+="<tr><td>"+str(d[6])+"</td><td>"+str(d[8])+"</td><td>"+str(d[13])+"</td><td>"+str(d[19])+"</td><td>"+str(d[17])+"</td><td>"+str(d[18])+" Rs.</td><td>"+str(d[3])+"</td><td>"+str(d[4])+"</td></tr>"
    srtable+="</table>"
    context={'data':table,'servicetable':table,'msg':'Successfully Accepted Request...!!'}
    return render(request,'AdminApp/ViewAllBookings.html', context)
