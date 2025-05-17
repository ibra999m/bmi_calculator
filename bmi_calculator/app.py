from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from forms import BMIForm
from bmi_calculator import BMICalculator
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                                                    'bmi.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your-secret-key-here'

db = SQLAlchemy(app)


class BMIRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    weight = db.Column(db.Float, nullable=False)
    height = db.Column(db.Float, nullable=False)
    bmi = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


with app.app_context():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def index():
    form = BMIForm()
    show_history = session.get('show_history', False)

    if form.validate_on_submit():
        try:
            weight = form.weight.data
            height = form.height.data
            result = BMICalculator.calculate_full_report(weight, height)

            record = BMIRecord(
                fullname=form.fullname.data,
                weight=weight,
                height=height,
                bmi=result['bmi'],
                category=result['category']
            )
            db.session.add(record)
            db.session.commit()

            session['last_result'] = {
                'fullname': form.fullname.data,
                'weight': weight,
                'height': height,
                'bmi': result['bmi'],
                'description': result['description'],
                'color': result['color'],
                'normal_min': result['normal_min'],
                'normal_max': result['normal_max'],
                'status_icon': result['status']['icon'],
                'status_class': result['status']['class'],
                'status_text': result['status']['text']
            }

            return redirect(url_for('index'))
        except Exception as e:
            flash(f"Ошибка: {str(e)}", "danger")

    records = []
    if show_history:
        records = BMIRecord.query.order_by(BMIRecord.created_at.desc()).all()

    return render_template(
        'index.html',
        form=form,
        last_result=session.pop('last_result', None),
        records=records,
        show_history=show_history
    )


@app.route('/toggle_history')
def toggle_history():
    session['show_history'] = not session.get('show_history', False)
    return redirect(url_for('index'))


@app.route('/delete_record/<int:id>')
def delete_record(id):
    try:
        record = BMIRecord.query.get_or_404(id)
        db.session.delete(record)
        db.session.commit()
        flash('Запись успешно удалена', 'success')
    except Exception as e:
        flash(f'Ошибка при удалении: {str(e)}', 'danger')
    return redirect(url_for('index'))


@app.route('/clear_history')
def clear_history():
    try:
        db.session.query(BMIRecord).delete()
        db.session.commit()
        flash('История очищена', 'success')
    except Exception as e:
        flash(f'Ошибка при очистке: {str(e)}', 'danger')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)