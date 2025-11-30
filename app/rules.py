from typing import Dict, List


def _clamp(x):
    return max(0.0, min(100.0, x))


def analyze_group(stats: Dict):
    causes = []
    n = stats.get('n', 1)
    dp = stats.get('diseases_pct', {})

    # Rule 1: Высокая распространенность респираторных заболеваний -> возможные инфекции/плохая вентиляция
    if dp.get('respiratory', 0) > 20 and stats.get('avg_missed_lesson', 0) > 3:
        conf = _clamp(
            dp.get('respiratory', 0) * 0.8 + stats.get('avg_missed_lesson', 0) * 5
        )

        causes.append({
            'name': 'Респираторные инфекции',
            'confidence': round(conf, 1),
            'recommendation': 'Провести профилактичский осмотр, улучшить проветривание аудиторий, рекомендовать вакцинацию и ношение масок при вспышках.'
        })

    # Rule 2: Высокий процент курящих -> ухудшение состояния дыхательной системы
    if stats.get('pct_smoking', 0) > 15:
        conf = _clamp(
            stats.get('pct_smoking', 0) * 0.9
        )
        causes.append({
            'name': 'Вред воздействия курения',
            'confidence': round(conf, 1),
            'recommendation': 'Запустить программы отказа от курения, консультации, информационные кампании.'
        })

    # Rule 3: Большое время у экрана -> проблемы со зрением и осанкой
    if stats.get('avg_screen_time', 0) > 6 and dp.get('vision', 0) > 15 or stats.get('avg_screen_time', 0) > 6 and dp.get('musculoskeletal', 0) > 15:
        conf = _clamp(
            stats.get('avg_screen_time', 0) * 8 + dp.get('vision', 0) * 1.5 + dp.get('musculoskeletal', 0) * 1.5
        )
        causes.append({
            'name': 'Длительное время перед монитором: проблемы зрения и опорно-двигательного аппарата',
            'confidence': round(conf,1),
            'recommendation': 'Рекомендовать перерывы 5-10 минут каждый час, упражнения для глаз и спины, регулировка рабочего места.'
        })

    # Rule 4: Низкая физическая активность -> иммунитет и ЖКТ
    if stats.get('avg_physical_activity', 0) < 3:
        conf = _clamp((3 - stats.get('avg_physical_activity', 0)) * 20)
        causes.append({
            'name': 'Низкая физическая активность',
            'confidence': round(conf,1),
            'recommendation': 'Организовать спортивные активности, мотивационные программы, доступ к инфраструктуре.'
        })

    # Rule 5: Высокая доля проживающих в общежитии -> риск инфекций и стресса
    if stats.get('pct_dorm', 0) > 10:
        conf = _clamp(
            stats.get('pct_dorm', 0) * 0.5 + dp.get('allergic', 0) * 0.3
        )
        causes.append({
            'name': 'Условия общежития: инфекции, стресс, аллергии',
            'confidence': round(conf,1),
            'recommendation': 'Проверить санитарное состояние общежития, проводить просветительскую работу, улучшать условия проживания.'
        })

    # Rule 6: Частые пропуски и большая средняя длительность -> хронические или серьезные заболевания
    if stats.get('avg_miss_duration', 0) > 5 or stats.get('avg_missed_lesson', 0) > 6:
        conf = _clamp(stats.get('avg_miss_duration', 0) * 6 + stats.get('avg_missed_lesson', 0) * 4)
        causes.append({
            'name': 'Хронические/серьезные заболевания / частые длительные болезни',
            'confidence': round(conf,1),
            'recommendation': 'Организовать углубленные медицинские обследования, направить в поликлинику.'
        })    

    # Rule 7: Аллергии: высокая доля аллергиков -> сезонные/средовые факторы
    if dp.get('allergic',0) > 10:
        conf = _clamp(dp.get('allergic',0) * 0.8)
        causes.append({
            'name': 'Аллергические реакции (возможно средовые или сезонные)',
            'confidence': round(conf,1),
            'recommendation': 'Определить аллергенные факторы, рекомендовать обследование и методы избегания контакта.'
        })   

    # Rule 8: Психические заболевания/стресс распространены -> стрессовые факторы в среде обучения
    if dp.get('mental',0) > 10 and stats.get('avg_missed_lesson',0) > 4:
        conf = _clamp(dp.get('mental',0) * 2 + stats.get('avg_missed_lesson',0) * 5)
        causes.append({
            'name': 'Стресс и психосоциальные факторы',
            'confidence': round(conf,1),
            'recommendation': 'Организовать психологическую поддержку, семинары по тайм-менеджменту и снижению стресса.'
        })

    # Rule 9: ЖКТ проблемы -> питание и стресс
    if dp.get('gi',0) > 10:
        conf = _clamp(dp.get('gi',0) * 0.9)
        causes.append({
            'name': 'Заболевания ЖКТ (возможны проблемы с питанием и стресс)',
            'confidence': round(conf,1),
            'recommendation': 'Проверить режим питания, провести консультации по питанию, снизить стрессовые факторы.'
        })

    # Rule 10: Дерматовенерологические заболевания -> гигиена и бытовые условия
    if dp.get('derm',0) > 5:
        conf = _clamp(dp.get('derm',0) * 1.0)
        causes.append({
            'name': 'Дерматовенерологические проблемы (возможны проблемы гигиены или инфекций)',
            'confidence': round(conf,1),
            'recommendation': 'Провести мероприятия по профилактике, информирование о гигиене, при необходимости медицинская помощь.'
        })

    # Если причин нет — дать общие рекомендации
    if not causes:
        causes.append({
            'name': 'Нет явных причин высокого риска',
            'confidence': 30.0,
            'recommendation': 'Поддерживать здоровый режим: спать 7-8 часов, сбалансированное питание, физическая активность, профилактические медосмотры.'
        }) 

    causes.sort(key = lambda x: x['confidence'], reverse = True)
    return causes


def analyze_individual(student: Dict):
    causes = []
    add = student.get('additional', {})
    dis = student.get('diseases', {})

    # Rule 1: Если курит и есть респираторные симптомы
    if add.get('smoking') and dis.get('respiratory'):
        causes.append({
            'name': 'Курение усугубляет респираторные заболевания',
            'confidence': 90.0,
            'recommendation': 'Рекомендовать программу отказа от курения, обследование легких.'
        })

    # Rule 2: Долгое время у монитора и жалобы на зрение
    if add.get('screen_time', 0) > 8 and dis.get('vision'):
        causes.append({
            'name': 'Перегрузка глаз из-за длительной работы за монитором',
            'confidence': 85.0,
            'recommendation': 'Следовать правилу 20-20-20, сделать проверку зрения и скорректировать рабочее место.'
        })

    # Rule 3: Низкая физическая активность и боли в ОДА
    if add.get('physical_activity', 0) < 3 and dis.get('musculoskeletal'):
        causes.append({
            'name': 'Недостаток движения ведет к проблемам опорно-двигательного аппарата',
            'confidence': 80.0,
            'recommendation': 'Рекомендовать упражнения для спины, плавание, консультация физиотерапевта.'
        })  

    # Rule 4: Частые пропуски и длительность -> возможные хронические заболевания
    if add.get('missed_lesson', 0) > 10 or add.get('avg_miss_duration', 0) > 7 or dis.get('chronic'):
        causes.append({
            'name': 'Вероятность хронического или тяжелого заболевания',
            'confidence': 88.0,
            'recommendation': 'Назначить углубленное медицинское обследование, направить к специалистам.'
        }) 

    # Rule 5: Проживание в общежитии + аллергии
    if add.get('dorm') and dis.get('allergic'):
        causes.append({
            'name': 'Аллергены в условиях проживания',
            'confidence': 70.0,
            'recommendation': 'Проверить условия проживания, рекомендовать средства по снижению аллергенной нагрузки.'
        })

    # Rule 6: Психические заболевания/стресс
    if dis.get('mental'):
        causes.append({
            'name': 'Стресс / психические проблемы',
            'confidence': 90.0,
            'recommendation': 'Предложить консультацию психолога, снизить нагрузку, техники релаксации.'
        })

    # Rule 7: Аллергические реакции без явных триггеров
    if dis.get('allergic') and not add.get('dorm'):
        causes.append({
            'name': 'Сезонные или пищевые аллергии',
            'confidence': 65.0,
            'recommendation': 'Провести аллерготесты, вести дневник питания и контактов с возможными аллергенами.'
        })

    # Rule 8: Высокое экранное время без проблем зрения -> риск будущих проблем
    if add.get('screen_time', 0) > 8 and not dis.get('vision'):
        causes.append({
            'name': 'Риск ухудшения зрения из-за длительной работы за монитором',
            'confidence': 60.0,
            'recommendation': 'Профилактика: перерывы, гимнастика для глаз, проверка зрения.'
        })

    # Rule 9: Курение и низкая физическая активность
    if add.get('smoking') and add.get('physical_activity', 0) < 2:
        causes.append({
            'name': 'Сочетание курения и малоподвижного образа жизни',
            'confidence': 75.0,
            'recommendation': 'Ввести программу по отказу от курения и постепенному увеличению активности.'
        })

    # Rule 10: Частые пропуски + психические
    if add.get('missed_lesson', 0) > 5 and dis.get('mental'):
        causes.append({
            'name': 'Пропуски на фоне психоэмоционального состояния',
            'confidence': 80.0,
            'recommendation': 'Психологическая поддержка, оценка академической нагрузки.'
        })

    # Если причин нет — дать общие рекомендации
    if not causes:
        causes.append({
            'name': 'Нет явных причин высокого риска',
            'confidence': 30.0,
            'recommendation': 'Поддерживать здоровый режим: спать 7-8 часов, сбалансированное питание, физическая активность, профилактические медосмотры.'
        })  

    # Сортируем
    causes.sort(key=lambda x: x['confidence'], reverse=True)
    return causes
    