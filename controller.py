from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, login_user

from app import app, db
from models import LogPassContainer, PlansAndReports


@app.route('/create_logins', methods=['POST'])
def create_logins():
    login = request.form.get('login')
    password = request.form.get('password')
    logpass = LogPassContainer(login=login, password=password)
    db.session.add(logpass)
    db.session.commit()
    return redirect(url_for('manager'))


@app.route('/db')
def database():
    data = [{"project": "Mantera", 'week': 1, "day": 1,
             "plan_fact": "Plan", 'spendings': 'Экскаваторы', "sum_of_spendings": 5000}
                ]
    for i in data:
        line = PlansAndReports(project=i["project"], week=i["week"], day=i["day"], plan_fact=i["plan_fact"],
                               spendings=i["spendings"], sum_of_spendings=i["sum_of_spendings"])
        db.session.add(line)

    db.session.commit()
    for i in PlansAndReports.query.all():
        print(i.id, i.project, i.week, i.day, i.plan_fact, i.spendings, i.sum_of_spendings, i.notation, i.created_at)
    return render_template('db.html') #TODO name='John', products=products)


@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'GET':
        return render_template('auth.html')
    login = request.form.get('login')
    password = request.form.get('password')
    user = LogPassContainer.query.filter_by(login=login, password=password).first()
    if user:
        login_user(user)
        return redirect(url_for('account'))
    flash("Вы ввели неверный логин или пароль. Попробуйте ещё раз.", 'error')
    return render_template('auth.html', access=False)


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    if request.method == 'GET':
        return render_template('account.html')


    return render_template('account.html')


@app.route('/account_plan', methods=['GET', 'POST'])
@login_required
def account_plan():
    if request.method == 'GET':
        project = request.args.get('project')
        return render_template('account_plan.html', project=project)
    project = request.form.get('project')
    week = request.form.get('week')
    calendar = {
        "02.01 - 07.01": 1,
        "09.01 - 13.01": 2,
        "16.01 - 20.01": 3,
        "23.01 - 27.01": 4,
    }
    week = calendar[week]

    for j in range(1, 6):
        for i in range(1, 4):
            spendings = request.form.get('type_of_spendings_' + str(j) + '_' + str(i))
            sum_of_spendings = request.form.get('spendings_' + str(j) + '_' + str(i))
            #notation = request.form.get('notation_' + str(j) + '_' + str(i)) TODO Добавить комментарий в шаблон
            if spendings and sum_of_spendings:
                plan = PlansAndReports(project=project, week=week, day=j, plan_fact="Plan",
                                       spendings=spendings, sum_of_spendings=sum_of_spendings)
                db.session.add(plan)
    db.session.commit()
    return render_template('plan_send.html')

@app.route('/account_report', methods=['GET', 'POST'])
@login_required
def account_report():
    if request.method == 'GET':
        project = request.args.get('project')
        week = request.args.get('week')
        calendar = {
            "Понедельник": 1,
            "Вторник": 2,
            "Среда": 3,
            "Четверг": 4,
            "Пятница": 5,
            "02.01 - 07.01": 1,
            "09.01 - 13.01": 2,
            "16.01 - 20.01": 3,
            "23.01 - 27.01": 4,
        }
        week = calendar[week]
        line = PlansAndReports.query.filter_by(project=project, week=week, plan_fact="Plan").all()

        return render_template('account_report.html', project=project, week=week, line=line)


    project = request.form.get('project')
    week = request.form.get('week')
    day = request.form.get('day')
    calendar = {
        "Понедельник": 1,
        "Вторник": 2,
        "Среда": 3,
        "Четверг": 4,
        "Пятница": 5,
        "02.01 - 07.01": 1,
        "09.01 - 13.01": 2,
        "16.01 - 20.01": 3,
        "23.01 - 27.01": 4,
    }
    # week = calendar[week]
    # day = calendar[day]
    for j in range(1, 6):
        for i in range(1, 4):
            spendings = request.form.get('type_of_spendings_' + str(j) + '_' + str(i))
            sum_of_spendings = request.form.get('spendings_' + str(j) + '_' + str(i))
            notation = request.form.get('notation_' + str(j) + '_' + str(i))
            plan = PlansAndReports(project=project, week=week, day=j, plan_fact="Fact",
                                   spendings=spendings, sum_of_spendings=sum_of_spendings, notation=notation)
            db.session.add(plan)
        db.session.commit()
    return redirect(url_for('report_send'))


@app.route('/report_send', methods=['GET', 'POST'])
@login_required
def report_send():

    return render_template('report_send.html')


@app.route('/plan_send', methods=['GET', 'POST'])
@login_required
def plan_send():
    return render_template('plan_send.html')


@app.route('/manager', methods=['GET', 'POST'])
@login_required
def manager():
    user_data = LogPassContainer.query.all()
    main_data = PlansAndReports.query.all()
    if request.method == 'GET':
        return render_template('manager.html', user_data=user_data, main_data=main_data)


@app.route('/week_summary', methods=['GET', 'POST'])
@login_required
def week_summary():
    week_summary = request.form.get('week_summary')
    project = request.form.get('project')
    date = {
        "02.01 - 07.01": 1,
        "09.01 - 13.01": 2,
        "16.01 - 20.01": 3,
        "23.01 - 27.01": 4,
    }

    week = date[week_summary]
    line = PlansAndReports.query.filter_by(week=week, project=project, plan_fact='Plan').all()
    plan_sum = 0
    for i in line:
        plan_sum += i.sum_of_spendings
    line = PlansAndReports.query.filter_by(week=week, project=project, plan_fact='Fact').all()
    fact_sum = 0
    for i in line:
        fact_sum += i.sum_of_spendings

    return render_template('week_summary.html', plan_sum=round(plan_sum, 0),
                           fact_sum=round(fact_sum, 0), week_summary=week_summary)


@app.route('/month_summary', methods=['GET', 'POST'])
@login_required
def month_summary():
    month_summary = request.form.get('month_summary')
    project = request.form.get('project')
    date = {
        "январь": 1,
        "февраль": 2,
        "март": 3,
        "апрель": 4,
    }

    month = date[month_summary]
    line = PlansAndReports.query.filter_by(month=month, project=project, plan_fact='Plan').all()
    plan_sum = 0
    for i in line:
        plan_sum += i.sum_of_spendings
    line = PlansAndReports.query.filter_by(month=month, project=project, plan_fact='Fact').all()
    fact_sum = 0
    for i in line:
        fact_sum += i.sum_of_spendings

    return render_template('month_summary.html', plan_sum=round(plan_sum, 0),
                           fact_sum=round(fact_sum, 0), month_summary=month_summary)

@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_login():

    return render_template('chatgpt_lp.html')

@app.route('/delete', methods=['POST'])
@login_required
def delete_login():
    id = request.form.get('id')
    line = LogPassContainer.query.filter_by(id=id).first()
    db.session.delete(line)
    db.session.commit()
    return redirect(url_for('manager'))

@app.route('/edit_data', methods=['POST'])
@login_required
def edit_data():
    id = request.form.get('id')
    project = request.form.get('project')
    week = request.form.get('week')
    day = request.form.get('day')
    plan_fact = request.form.get('plan_fact')
    spendings = request.form.get('spendings')
    sum_of_spendings = request.form.get('sum_of_spendings')
    notation = request.form.get('notation')
    line = PlansAndReports.query.filter_by(id=id).first()
    if project:

        line.project = project
        line.week = week
        line.day = day
        line.plan_fact = plan_fact
        line.spendings = spendings
        line.sum_of_spendings = sum_of_spendings
        line.notation = notation
        db.session.commit()
        return redirect(url_for('manager'))

    return render_template('edit_data.html', line=line)

@app.route('/delete_data', methods=['POST'])
@login_required
def delete_data():
    id = request.form.get('id')
    line = PlansAndReports.query.filter_by(id=id).first()
    db.session.delete(line)
    db.session.commit()
    return redirect(url_for('manager'))

@app.after_request
def redirect_to_sign(response):
    if response.status_code == 401:
        return redirect(url_for('auth'))
    return response


if __name__ == '__main__':
#    from controller import *
    app.run(debug=True)