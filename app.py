from flask import Flask, render_template, redirect, url_for, request,jsonify
import sqlite3
import datetime
import os
import random
from datetime import  timedelta
from flask import session
import webbrowser
#webbrowser.open("http://127.0.0.1:5000")

app = Flask(__name__)
app.config['DATABASE'] = 'insurancedb.db'
def get_db():
    db = sqlite3.connect(app.config['DATABASE'])
    db.row_factory = sqlite3.Row
    return db
@app.route('/')
def index():
    db = get_db()
    data = db.execute('SELECT * FROM member').fetchall()
    db.close()
    # 当用户尝试访问主页时，自动重定向到登录页面
    return redirect(url_for('login'))
app.secret_key = 'your_secret_key'
@app.route('/login')
def login():
    # 渲染登录页面
    return render_template('login.html')
@app.route('/login', methods=['POST'])
def login_post():
    username = request.form['用户名']
    password = request.form['密码']
    print(username, password)
    db = get_db()
    # Use parameterized query to prevent SQL injection
    data = db.execute('SELECT ID FROM account WHERE username = ? AND password = ?', (username, password)).fetchall()
    db.close()
    print(data)
    if data:
        ID = data[0][0]
        print(ID)
        # Store the ID in the session
        session['user_id'] = ID
        # Login successful, return a success message
        return jsonify(success=True)
    else:
        return jsonify(success=False)
@app.route('/homepage')
def homepage(): # Replace with the actual method of obtaining the user ID
    data=None
    db = get_db()
    # Use a parameterized query to prevent SQL injection
    # Replace 'your_table' with your actual table name
    query = '''
    SELECT 
    mem.name AS insured_name,po.premium,po.coverage, po.period,
    po.policy_id,po.start,
    po.payment_interval, po.duration,po.file AS policy_file,pr.pro_id,
    pr.type AS product_type,pr.pro_name AS product_name,c.company_name
FROM
    policy po
JOIN
    product pr ON po.pro_id = pr.pro_id
JOIN 
    company c ON pr.company_name = c.company_name
LEFT JOIN
    member_policy mpi ON po.policy_id = mpi.policy_id AND mpi.role = '被保人'
LEFT JOIN
    member mem ON mpi.ID = mem.ID;
        
        '''

    data = db.execute(query).fetchall()
    print(type(data[0]))
    print(data[0])
    db.close()
    # 渲染登录页面
    db = get_db()
    # Use a parameterized query to prevent SQL injection
    # Replace 'your_table' with your actual table name
    query = '''
           SELECT
    m.name,po.policy_id,cl.claim_date,
    cl.amount,pr.type AS product_type,c.company_name,pr.pro_name AS product_name
FROM
    member m
JOIN
    member_claim mc ON m.ID = mc.ID
JOIN
    claim cl ON mc.claim_id = cl.claim_id
JOIN
    policy po ON cl.policy_id = po.policy_id
JOIN
    product pr ON po.pro_id = pr.pro_id
JOIN
    company c ON pr.company_name = c.company_name;

            '''

    data1 = db.execute(query).fetchall()

    db.close()
    db = get_db()
    # Use a parameterized query to prevent SQL injection
    # Replace 'your_table' with your actual table name
    query = '''

                '''

    data2 = db.execute(query).fetchall()
    data3=[]
    for item in data2:
        print(item['policy_id'],item['pay_date'],item['start'],item['payment_interval'],item['duration'])
    for item in data2:
        # 将最近已交费日期、起始时间和当前日期转换为 datetime 对象
        last_pay_date = datetime.datetime.strptime(item['pay_date'], '%Y-%m-%d')
        start = datetime.datetime.strptime(item['start'], '%Y-%m-%d')
        current_date = datetime.datetime.now()

        # 计算下次缴费日期
        if item['payment_interval'] == '1月':
            next_pay_date = last_pay_date + datetime.timedelta(days=30)  # 假设一个月为30天
        elif item['payment_interval'] == '1年':
            next_pay_date = last_pay_date + datetime.timedelta(days=365)  # 假设一年为365天
        # 其他缴费间隔可以类似处理

        # 计算下次缴费日期与起始时间之间的总天数
        total_days = (next_pay_date - start).days

        # 将 duration 转换为总天数
        if item['duration'][-1] == '年':
            years = int(item['duration'][:-1])
            total_duration_days = years * 365
        elif item['duration'][-1] == '月':
            months = int(item['duration'][:-1])
            total_duration_days = months * 30
        # 其他 duration 单位可以类似处理

        # 检查是否超过了 duration
        if total_days <= total_duration_days:
            # 计算当前日期与下次缴费日期之间的差异
            days_until_due = (next_pay_date - current_date).days
            # 检查保单是否在七天内要缴费
            if days_until_due <= 30:
                data3.append(item)
    db.close()
    db = get_db()
    # Use a parameterized query to prevent SQL injection
    # Replace 'your_table' with your actual table name
    query = '''
                SELECT
            m.name
        FROM
            member m;

                    '''

    data0 = db.execute(query).fetchall()

    db.close()
    names = []
    for i in range(len(data0)):
        names.append({})
        names[i]['selected'] = False
        names[i]['name'] = data0[i]['name']
        names[i]['id'] = data0[i]['name']
    print(names)
    db = get_db()
    # Use a parameterized query to prevent SQL injection
    # Replace 'your_table' with your actual table name
    query = '''
                    SELECT
               pro_name
            FROM
                product;

                        '''

    data00 = db.execute(query).fetchall()

    db.close()
    pro_names = []
    for i in range(len(data00)):
        pro_names.append({})
        pro_names[i]['selected'] = False
        pro_names[i]['name'] = data00[i]['pro_name']
        pro_names[i]['id'] = data00[i]['pro_name']
    print(pro_names)
    db = get_db()
    # Use a parameterized query to prevent SQL injection
    # Replace 'your_table' with your actual table name
    query = '''
                       SELECT
                  company_name
               FROM
                   company;

                           '''

    data000 = db.execute(query).fetchall()

    db.close()
    company_names = []
    for i in range(len(data000)):
        company_names.append({})
        company_names[i]['selected'] = False
        company_names[i]['name'] = data000[i]['company_name']
        company_names[i]['id'] = data000[i]['company_name']
    print(company_names)
    return render_template('客户主界面.html',data_list=data,data_list1=data1,ID=session['user_id'],datalist=data2,names=names,pro_names=pro_names,company_names=company_names)

@app.route('/personal-center/<user_id>')
def personal_center(user_id):
    db = get_db()
    # Use a parameterized query to prevent SQL injection
    # Replace 'your_table' with your actual table name
    query = '''
        SELECT  mem.name,mem.ID,mem.birthday,mem.identity,mem.phone_number,mem.email,mem.address,account.username,account.password
        FROM account,member as mem
        WHERE account.ID=mem.ID AND account.ID=?
            '''

    data = db.execute(query, (user_id,)).fetchall()
    print(data)
    db.close()
    return render_template('用户信息界面.html',items=data[0])
@app.route('/information/personal-center/<user_id>')
def personal_center1(user_id):

    return redirect(url_for('personal_center', user_id=user_id))
@app.route('/information1/personal-center/<user_id>')
def personal_center0(user_id):

    return redirect(url_for('personal_center', user_id=user_id))
@app.route('/search', methods=['GET'])
def search():
    search_query = request.args.get('query', '').lower()


    db = get_db()
    # Use a parameterized query to prevent SQL injection
    # Replace 'your_table' with your actual table name
    query = '''
            SELECT 
        mem.name AS insured_name,
        po.premium,
        po.period,
        po.policy_id,
        po.start,
        po.payment_interval,
        po.duration,
        po.file AS policy_file,
        pr.type AS product_type,
        pr.pro_name AS product_name,
        c.company_name
    FROM
        policy po
    JOIN
        product pr ON po.pro_id = pr.pro_id
    JOIN 
        company c ON pr.company_name = c.company_name
    LEFT JOIN
        member_policy mpi ON po.policy_id = mpi.policy_id AND mpi.role = '被保人'
    LEFT JOIN
        member mem ON mpi.ID = mem.ID;

            '''

    data = db.execute(query).fetchall()
    print(type(data))
    print(data[0])
    db.close()
    # 渲染登录页面
    db = get_db()
    # Use a parameterized query to prevent SQL injection
    # Replace 'your_table' with your actual table name
    query = '''
               SELECT
        m.name,
        po.policy_id,
        cl.claim_date,
        cl.amount,
        pr.type AS product_type,
        c.company_name
    FROM
        member m
    JOIN
        member_claim mc ON m.ID = mc.ID
    JOIN
        claim cl ON mc.claim_id = cl.claim_id
    JOIN
        policy po ON cl.policy_id = po.policy_id
    JOIN
        product pr ON po.pro_id = pr.pro_id
    JOIN
        company c ON pr.company_name = c.company_name;

                '''
    data1 = db.execute(query).fetchall()
    db.close()

    def filter_data(data_list, search_query):
        filtered_data = []
        for item in data_list:
            # Check if the search query is in any of the fields you want to search by
            # Here, we're checking all fields in the row
            if any(search_query in str(item[column]).lower() for column in item.keys()):
                filtered_data.append(item)
        return filtered_data
    filtered_data = filter_data(data, search_query)
    filtered_data1 = filter_data(data1, search_query)

    # Pass the filtered data to the template
    return render_template('客户主界面.html',data_list=filtered_data,data_list1=filtered_data1,ID=session['user_id'])

@app.route('/get_names/', methods=['GET'])
def get_names():
    db = get_db()
    # Use a parameterized query to prevent SQL injection
    # Replace 'your_table' with your actual table name
    query = '''
            SELECT
        m.name
    FROM
        member m;

                '''

    data = db.execute(query).fetchall()

    db.close()
    data1=[]
    for i in range(len(data)):
        data1.append({})
        data1[i]['selected']=False
        data1[i]['name']=data[i]['name']
        data1[i]['id']=data[i]['name']
    print(data1)
    return jsonify(data1)
@app.route('/remind/<policy_id>')
def insurance_notice(policy_id):
    db = get_db()
    # Use a parameterized query to prevent SQL injection
    query = '''
        SELECT 
    p.policy_id,
    p.start,
    p.period,
    p.coverage,
    p.premium,
    p.payment_interval,
    p.duration,
    payment.pay_date,
    mem.name
FROM 
    policy p,payment
    LEFT JOIN member_policy mpi ON p.policy_id = mpi.policy_id AND mpi.role = '被保人'
    LEFT JOIN member mem ON mpi.ID = mem.ID
WHERE
    payment.policy_id = p.policy_id AND 
    p.policy_id = ?;

                        '''

    data = db.execute(query,(policy_id,)).fetchall()
    db.close()
    return render_template('通知界面.html',item=data[0])

def random_date(start, end):
    return start + timedelta(minutes=random.randint(0, int((end - start).total_seconds() / 60)))
@app.route('/get_data', methods=['GET'])
def get_data():
    db = get_db()
    query = '''
        SELECT * FROM all_payments
        WHERE days_until_due < 31
        '''
    # 使用 cursor 执行查询并获取结果
    cursor = db.cursor()
    cursor.execute(query)
    data3 = cursor.fetchall()

    # 检查 data3 是否为空
    if not data3:
        # 如果为空，获取 all_payments 视图中的前三条记录
        query = '''
            SELECT * FROM all_payments
            LIMIT 3
            '''
        cursor.execute(query)
        data3 = cursor.fetchall()

    # 关闭 cursor
    cursor.close()
    data=[]

    for k in range(len(data3)):
        data.append({})
        data[k]['title']='保单号为'+data3[k]['policy_id']+'的保单即将到期，请及时缴费'
        data[k]['href']='/remind/'+data3[k]['policy_id']

        data[k]['date']=data3[k]['next_pay_date']
    return jsonify(data)

@app.route('/information/<policy_id>')
def policy_information(policy_id):
    db = get_db()
    # Use a parameterized query to prevent SQL injection
    # Replace 'your_table' with your actual table name
    query = '''
          SELECT 
    po.policy_id,po.start,po.period,po.coverage,po.premium,ph.name AS policy_holder_name,po.file,
    ph.phone_number AS policy_holder_phone_number,ph.ID AS policy_holder_ID,mem.name AS insured_name,mem.ID AS insured_ID,
    mem.phone_number AS insured_phone,
    group_concat(DISTINCT bn.name || ' (身份证号: ' || bn.ID|| ', 联系电话: ' || bn.phone_number  || ')') AS beneficiary_details,
    po.payment_interval,po.duration,po.file AS policy_file,pr.pro_name AS product_name,
    pr.type AS product_type,pr.introduction AS product_intro,c.company_name
FROM
    policy po
JOIN
    product pr ON po.pro_id = pr.pro_id
JOIN 
    company c ON pr.company_name = c.company_name
LEFT JOIN
    member_policy mph ON po.policy_id = mph.policy_id AND mph.role = '投保人'
LEFT JOIN
    member ph ON mph.ID = ph.ID
LEFT JOIN
    member_policy mpi ON po.policy_id = mpi.policy_id AND mpi.role = '被保人'
LEFT JOIN
    member mem ON mpi.ID = mem.ID
LEFT JOIN
    member_policy mpb ON po.policy_id = mpb.policy_id AND mpb.role = '受益人'
LEFT JOIN
    member bn ON mpb.ID = bn.ID
WHERE 
    po.policy_id = ?
GROUP BY 
    po.policy_id,po.premium,po.period,po.start,po.payment_interval,po.duration,po.file,
    pr.type,c.company_name,ph.name,mem.name

            '''

    data = db.execute(query, (policy_id,)).fetchall()

    db.close()
    db = get_db()
    # Use a parameterized query to prevent SQL injection
    # Replace 'your_table' with your actual table name
    query = '''
    SELECT mem.name,pay.pay_date,pay.bank_account,po.premium
    FROM payment as pay,member as mem,policy as po 
    WHERE pay.ID=mem.ID AND pay.policy_id=po.policy_id AND po.policy_id=?
        
                '''

    data1 = db.execute(query, (policy_id,)).fetchall()

    db.close()
    db = get_db()
    # Use a parameterized query to prevent SQL injection
    # Replace 'your_table' with your actual table name
    query = '''
        SELECT mem.name,claim.claim_date,claim.amount
        FROM claim ,member as mem ,member_claim as mc
        WHERE mc.ID=mem.ID AND claim.claim_id=mc.claim_id AND claim.policy_id=?

                    '''

    data2 = db.execute(query, (policy_id,)).fetchall()

    db.close()
    # 渲染登录页面
    return render_template('电子保单详情页.html',item=data[0],data_list1=data1,data_list2=data2,ID=session['user_id'])


@app.route('/information1/<pro_name>')
def product_information(pro_name):
    db = get_db()
    # Use a parameterized query to prevent SQL injection
    # Replace 'your_table' with your actual table name
    query = '''
          select  product.pro_id,product.pro_name,product.introduction,product.type,company.company_name,
          company.com_address,company.com_phone_num
          FROM product,company
          WHERE product.company_name=company.company_name AND product.pro_name=?

            '''

    data = db.execute(query, (pro_name,)).fetchall()

    db.close()

    # 渲染登录页面
    return render_template('保险产品详情页.html', item=data[0],ID=session['user_id'])
@app.route('/update_field', methods=['POST'])
def update_field():
    field = request.form.get('field')
    value = request.form.get('value')
    print(field, value)

    db = get_db()
    # 更新member表中feild字段的值
    db.execute(f'UPDATE member SET {field} = ? WHERE ID = ?', (value, session['user_id']))
    db.commit()
    db.close()
    if field =='ID':
        session['user_id']=value
    return jsonify({'message': '更新成功！'})
@app.route('/update_field_policy', methods=['POST'])
def update_field_policy():
    field = request.form.get('field')
    value = request.form.get('value')

    if field =='pro_name':
        print(field, value)
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT pro_id FROM product WHERE pro_name = ?", (value,))

            product = cursor.fetchone()
            if product:
                print(product['pro_id'])
                cursor.execute("UPDATE policy SET pro_id = ? WHERE policy_id = ?",
                               (product['pro_id'], session['policy_id']))
                conn.commit()
                return jsonify({'message': '更新成功！'})
            else:
                return jsonify({'message': '更新失败！'}), 400
    elif field == 'policy_holder_name' or field == 'insured_name':
        print(field, value)
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT ID FROM member WHERE name = ?", (value,))

            member = cursor.fetchone()
            if member:
                cursor.execute("UPDATE member_policy SET ID = ? WHERE policy_id = ?",
                               (member['ID'], session['policy_id']))
                conn.commit()
                return jsonify({'message': '更新成功！'})
            else:
                return jsonify({'message': '更新失败！'}), 400
    elif field == 'beneficiary_name':
        print(field, value)
        names = value.replace('，', ',').replace('；', ';').replace('、', ',').replace('；', ',').replace(';', ',').split(',')
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM member_policy WHERE policy_id = ? AND role = '受益人'",
                           (session['policy_id'],))
            for name in names:
                print(name.strip())
                if name.strip() != '':
                    print(name.strip())
                    cursor.execute("SELECT ID FROM member WHERE name = ?", (name.strip(),))

                member = cursor.fetchone()
                if member:
                    print(member['ID'],session['policy_id'])
                    cursor.execute("INSERT INTO member_policy (ID,policy_id,  role) VALUES (?, ?, ?)",
                                   (member['ID'],session['policy_id'], '受益人'))
                    conn.commit()
            return jsonify({'message': '更新成功！'})
    else:
        db = get_db()
        # 更新member表中feild字段的值
        db.execute(f'UPDATE policy SET {field} = ? WHERE policy_id = ?', (value, session['policy_id']))
        db.commit()
        db.close()
        if field =='policy_id':
            session['policy_id']=value
        return jsonify({'message': '更新成功！'})
@app.route('/change/<policy_id>')
def policy_change(policy_id):
    session['policy_id']=policy_id
    db = get_db()
    # Use a parameterized query to prevent SQL injection
    # Replace 'your_table' with your actual table name
    query = '''
      SELECT 
    po.policy_id,
    po.start,
    po.period,
    po.coverage,
    po.premium,
    po.payment_interval,
    po.duration,
    ph.name AS policy_holder_name,
    ph.phone_number AS policy_holder_phone_number,
    ph.ID AS policy_holder_ID,
    mem.name AS insured_name,
    mem.ID AS insured_ID,
    mem.phone_number AS insured_phone,
    group_concat(DISTINCT bn.name ) AS name3,
    po.payment_interval,
    po.duration,
    po.file AS policy_file,
    pr.pro_name AS product_name,
    pr.type AS product_type,
    pr.introduction AS product_intro,
    c.company_name
FROM
    policy po
JOIN
    product pr ON po.pro_id = pr.pro_id
JOIN 
    company c ON pr.company_name = c.company_name
LEFT JOIN
    member_policy mph ON po.policy_id = mph.policy_id AND mph.role = '投保人'
LEFT JOIN
    member ph ON mph.ID = ph.ID
LEFT JOIN
    member_policy mpi ON po.policy_id = mpi.policy_id AND mpi.role = '被保人'
LEFT JOIN
    member mem ON mpi.ID = mem.ID
LEFT JOIN
    member_policy mpb ON po.policy_id = mpb.policy_id AND mpb.role = '受益人'
LEFT JOIN
    member bn ON mpb.ID = bn.ID
WHERE 
    po.policy_id = ?
GROUP BY 
    po.policy_id,
    po.premium,
    po.period,
    po.start,
    po.payment_interval,
    po.duration,
    po.file,
    pr.type,
    c.company_name,
    ph.name,
    mem.name
            '''

    data = db.execute(query, (policy_id,)).fetchall()

    db.close()

    return render_template('修改保单内容界面.html', item=data[0])
@app.route('/change1/<pro_name>')
def product_change(pro_name):
    session['pro_name']=pro_name
    db = get_db()
    # Use a parameterized query to prevent SQL injection
    # Replace 'your_table' with your actual table name
    query = '''
      select  product.pro_id,product.pro_name,product.introduction,product.type,company.company_name,company.com_address,company.com_phone_num
          FROM product,company
          WHERE product.company_name=company.company_name AND product.pro_name=?
            '''

    data = db.execute(query, (pro_name,)).fetchall()

    db.close()

    return render_template('修改产品内容界面.html', item=data[0])
@app.route('/update_field_product', methods=['POST'])
def update_field_prodcut():
    field = request.form.get('field')
    value = request.form.get('value')
    db = get_db()
    # 更新member表中feild字段的值
    db.execute(f'UPDATE product SET {field} = ? WHERE pro_name = ?', (value, session['pro_name']))
    db.commit()
    db.close()
    if field == 'pro_name':
        session['pro_name'] = value
    return jsonify({'message': '更新成功！'})
@app.route('/homepage', methods=['POST'])
def home():
    if request.method == 'POST':
        print(1111111111)
        inuser_name = request.form.get('insured_name')
        print("被保人", inuser_name)
        beneficiary_name = request.form.getlist('beneficiary_name')
        print("受益人", beneficiary_name)
        # 从表单中提取数据
        policy_id = request.form.get('policy_id')
        period=request.form.get('period')
        coverage=request.form.get('coverage')
        premium=request.form.get('premium')
        print(premium)
        payment_interval=request.form.get('payment_interval')
        duration=request.form.get('duration')
        start=request.form.get('start')
        pro_name = request.form.get('pro_name')
        claim_id = request.form.get('claim_id')
        claim_name=request.form.get('claim_name')
        amount=request.form.get('amount')
        claim_date=request.form.get('claim_date')
        pro_id=request.form.get('pro_id')
        type=request.form.get('type')
        introduction=request.form.get('introduction')
        company_name=request.form.get('company_name')
        pay_id=request.form.get('pay_id')
        pay_date=request.form.get('pay_date')
        bank_account=request.form.get('bank_account')
        com_phone_num=request.form.get('com_phone_num')
        com_address=request.form.get('com_address')
        pay_name=request.form.get('pay_name')
        if coverage  :
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT pro_id FROM product WHERE pro_name = ?", (pro_name,))

                product = cursor.fetchone()
                if product:
                    cursor.execute(
                        "INSERT INTO policy (policy_id, pro_id, start, period, coverage, premium, payment_interval, duration, file) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        (policy_id, product['pro_id'], start, period, coverage, premium, payment_interval, duration, policy_id+'pdf'))
                    conn.commit()

            inuser_name = request.form.get('insured_name')
            print("被保人",inuser_name)
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT ID FROM member WHERE name = ?", (inuser_name,))

                member = cursor.fetchone()

                if member:
                    print(member['ID'], policy_id, '被保人')
                    cursor.execute("INSERT INTO member_policy (ID,policy_id,role) VALUES (?, ?, ?)",
                                   (member['ID'], policy_id, '被保人'))
            policy_holder_name = request.form.get('policy_holder_name')
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT ID FROM member WHERE name = ?", (policy_holder_name,))

                member = cursor.fetchone()

                if member:
                    print(len(member))
                    cursor.execute("INSERT INTO member_policy (ID,policy_id,role) VALUES (?, ?, ?)",
                                   (member['ID'], policy_id, '投报人'))

            with get_db() as conn:
                cursor = conn.cursor()
                for name in beneficiary_name:
                    if name.strip() != '':
                        cursor.execute("SELECT ID FROM member WHERE name = ?", (name.strip(),))

                    member = cursor.fetchone()
                    if member:
                        cursor.execute("INSERT INTO member_policy (ID,policy_id,  role) VALUES (?, ?, ?)",
                                       (member['ID'], policy_id, '受益人'))
        elif claim_id:
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT ID FROM member WHERE name = ?", (claim_name,))

                member = cursor.fetchone()

                if member:
                    cursor.execute("INSERT INTO member_claim (ID,claim_id) VALUES (?, ?)",
                                   (member['ID'], claim_id))
                cursor.execute("INSERT INTO claim (claim_id,policy_id,claim_date,amount) VALUES (?, ?, ?, ?)",
                               (claim_id, policy_id, claim_date, amount))
                conn.commit()
        elif pro_id:
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO product (pro_id,pro_name,type,introduction,company_name) VALUES (?, ?, ?, ?, ?)",
                               (pro_id, pro_name, type, introduction,company_name))
                conn.commit()
        elif bank_account:
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT ID FROM member WHERE name = ?", (pay_name,))

                member = cursor.fetchone()
                if member:
                    cursor.execute(
                    "INSERT INTO payment (pay_id,ID,policy_id,pay_date,bank_account) VALUES (?, ?, ?, ?, ?)",
                    (pay_id, member['ID'],policy_id, pay_date, bank_account))
                conn.commit()
        elif com_phone_num:
            with get_db() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO company (company_name,com_address,com_phone_num) VALUES (?, ?, ?)",
                    (company_name, com_address, com_phone_num))
                conn.commit()
        return redirect(url_for('homepage'))
@app.route('/deletepolicy/<policy_id>')
def deletepolicy(policy_id):
    db = get_db()  # 假设这个函数返回一个数据库连接对象
    # 使用参数化查询来防止SQL注入
    query = 'DELETE FROM policy WHERE policy_id = ?;'
    # 使用数据库连接对象执行查询
    cursor = db.cursor()
    cursor.execute(query, (policy_id,))  # 注意这里的参数是一个元组
    db.commit()  # 提交事务，确保更改生效
    db.close()
    return redirect(url_for('homepage'))


from flask import redirect, url_for, flash


@app.route('/deleteproduct/<pro_id>')
def deleteproduct(pro_id):
    db = get_db()  # 假设这个函数返回一个数据库连接对象
    # 检查product表中是否存在指定的pro_id
    check_query = 'SELECT 1 FROM product WHERE pro_id = ? LIMIT 1;'
    cursor = db.cursor()
    cursor.execute(check_query, (pro_id,))
    exists = cursor.fetchone()

    if not exists:
        # 如果存在pro_id，执行删除操作
        delete_query = 'DELETE FROM product WHERE pro_id = ?;'
        cursor.execute(delete_query, (pro_id,))
        db.commit()  # 提交事务，确保更改生效
    else:
        # 如果不存在pro_id，返回删除失败的消息
        flash('产品ID不存在，删除失败！')
        return redirect(url_for('homepage'))

    # 关闭游标和数据库连接
    cursor.close()
    db.close()

    # 重定向到主页
    return redirect(url_for('homepage'))

@app.route('/updatepdf/<policy_id>')
def updatepdf(policy_id):
    session['filename']=policy_id+'.pdf'
    return render_template('上传pdf.html', policy_id=policy_id)
@app.route('/upload', methods=['POST'])
def uppdf():
    files = request.files.getlist('files')  # 获取多个文件
    for file in files:
        print(file)
        print(type(file))
        # 先检查static/pdf文件夹下是否存在session['filename']文件，如果存在则删除
        if os.path.exists(f'static/pdf/{session["filename"]}'):
            os.remove(f'static/pdf/{session["filename"]}')
        # 保存文件
        file.save(f'static/pdf/{session["filename"]}')
    return render_template('上传pdf.html')
if __name__ == '__main__':
    app.run(debug=True, threaded=True)
