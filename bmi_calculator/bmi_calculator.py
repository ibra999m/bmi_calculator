class BMICalculator:
    @staticmethod
    def calculate_bmi(weight, height):
        if height <= 0:
            raise ValueError("Рост должен быть положительным числом")
        return round(weight / (height ** 2), 2)

    @staticmethod
    def get_category(bmi):
        if bmi < 18.5:
            return {
                'category': 'underweight',
                'description': 'Недостаточный вес',
                'color': '#3498db'
            }
        elif 18.5 <= bmi < 25:
            return {
                'category': 'normal',
                'description': 'Нормальный вес',
                'color': '#2ecc71'
            }
        elif 25 <= bmi < 30:
            return {
                'category': 'overweight',
                'description': 'Избыточный вес',
                'color': '#e67e22'
            }
        else:
            return {
                'category': 'obese',
                'description': 'Ожирение',
                'color': '#e74c3c'
            }

    @staticmethod
    def get_normal_weight_range(height_cm):
        height_m = height_cm / 100
        lower = round(18.5 * (height_m ** 2), 1)
        upper = round(24.9 * (height_m ** 2), 1)
        return lower, upper

    @staticmethod
    def get_weight_status(weight, normal_min, normal_max):
        if weight < normal_min:
            diff = normal_min - weight
            return {
                'icon': '↓',
                'class': 'text-blue',
                'text': f'Ниже нормы на {diff:.1f} кг'
            }
        elif weight > normal_max:
            diff = weight - normal_max
            return {
                'icon': '↑',
                'class': 'text-red',
                'text': f'Выше нормы на {diff:.1f} кг'
            }
        else:
            return {
                'icon': '✓',
                'class': 'text-green',
                'text': 'В пределах нормы'
            }

    @classmethod
    def calculate_full_report(cls, weight, height_cm):
        height_m = height_cm / 100
        bmi = cls.calculate_bmi(weight, height_m)
        category = cls.get_category(bmi)
        normal_min, normal_max = cls.get_normal_weight_range(height_cm)
        status = cls.get_weight_status(weight, normal_min, normal_max)

        return {
            'bmi': bmi,
            **category,
            'normal_min': normal_min,
            'normal_max': normal_max,
            'status': status
        }