from datetime import datetime

#validate all data before adding it to the database 
def validate_event_data(data):
    errors = []
    
    titlu = data.get('titlu', '')
    if len(titlu) < 4 or len(titlu) > 200:
        errors.append("Titlu trebuie să conțină între 4-200 caractere.")

    descriere = data.get('descriere', '')
    if not descriere.strip():
        errors.append("Completați Descrierea.")
    elif len(descriere) > 500:
        errors.append("Descrierea nu poate depăși 500 de caractere.")

    data_str = data.get('data', '')
    try:
        event_date = datetime.strptime(data_str, '%Y-%m-%d')
        if event_date <= datetime.now():
            errors.append("Data trebuie prezentată in viitor.")
    except ValueError:
        errors.append("Formatul datelor este greșit, urmează formatul YYYY-MM-DD.")

    ora_str = data.get('ora', '')
    if ora_str:
        try:
            start_time_str, end_time_str = ora_str.split(' - ')
            start_time = datetime.strptime(start_time_str, '%H:%M:%S').time()
            end_time = datetime.strptime(end_time_str, '%H:%M:%S').time()
            if start_time >= end_time:
                errors.append("Timpul de start trebuie să fie mai devreme decât cel final")
        except ValueError:
            errors.append("Ora trebuie să fie de format 'HH:MM:SS - HH:MM:SS'.")
    else:
        errors.append("Ora este necesară, și trebuie să fie de formatul 'HH:MM:SS - HH:MM:SS'.")

    for field in ['raion', 'oras', 'strada']:
        if len(data.get(field, '')) < 4:
            errors.append(f"{field.capitalize()} Denumirea trebuie sa conțină cel puțin 4 caractere")
        elif len(data.get(field, '')) > 100:
            errors.append(f"{field.capitalize()} Denumirea nu poate depăși 100 de caractere.")

    nume = data.get('nume', '')
    if not nume.strip():
        errors.append("Indicați Numele Organizatorului.")
    elif len(nume) > 100:
        errors.append("Numele organizatorului nu poate depăși 100 de caractere.")


    domeniu = data.get('domeniu', '')
    if not domeniu.strip():
        errors.append("Indicați Domeniul Evenimentului.")
    elif len(nume) > 50:
        errors.append("Domeniul nu poate depăși 50 de caractere.")



    tip = data.get('tip', '')  
    if tip.strip().lower() not in ['obligatoriu', 'opțional']:
        errors.append("Tipul trebuie să fie 'obligatoriu' sau 'opțional'")

    if errors:
        return False, errors
    return True, "Validarea sa realizat cu success."
