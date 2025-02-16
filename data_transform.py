import pandas as pd
import re

def clean_professor_name(name):
    # Eliminar caracteres especiales y títulos innecesarios
    name = re.sub(r'\(.*?\)|-|int|Mtro', '', name, flags=re.IGNORECASE).strip()
    # Separar nombre y apellidos correctamente si están en formato Apellido, Nombre
    parts = name.split()
    if "," in name:
        last_name, first_name = name.split(",")
        name = first_name.strip() + " " + last_name.strip()
    return name.title()

def transform_professor_schedule(df):
    # Seleccionar solo las columnas relevantes y hacer una copia para evitar el warning
    df = df[['profesor', 'lunes', 'martes', 'miércoles', 'jueves', 'viernes']].copy()
    
    # Limpiar los nombres de los profesores
    df.loc[:, 'profesor'] = df['profesor'].apply(clean_professor_name)
    
    # Eliminar la 'L' que aparece en algunos horarios
    for day in ['lunes', 'martes', 'miércoles', 'jueves', 'viernes']:
        df.loc[:, day] = df[day].astype(str).str.replace('L', '', regex=True).str.strip()
        df.loc[:, day] = df[day].replace('', None)
    
    # Agrupar horarios por profesor
    grouped = df.groupby('profesor').agg(lambda x: [h for h in x.dropna()])
    
    # Crear horario consolidado
    processed_data = []
    for prof, row in grouped.iterrows():
        daily_schedule = {}
        for day in ['lunes', 'martes', 'miércoles', 'jueves', 'viernes']:
            schedules = row[day]
            if schedules:
                times = [list(map(str.strip, h.split('-'))) for h in schedules if '-' in h]
                if times:
                    start_times = [t[0] for t in times]
                    end_times = [t[1] for t in times]
                    start_min = min(start_times)
                    end_max = max(end_times)
                    daily_schedule[day] = f"{start_min}-{end_max}"
                else:
                    daily_schedule[day] = None
            else:
                daily_schedule[day] = None
        
        # Clasificación de horario basado en el horario más extendido
        all_times = sum([row[day] for day in ['lunes', 'martes', 'miércoles', 'jueves', 'viernes'] if row[day]], [])
        
        if all_times:
            valid_times = [h.split('-') for h in all_times if '-' in h]
            if valid_times:
                start_times = sorted([h[0] for h in valid_times])
                end_times = sorted([h[1] for h in valid_times])
                final_start = start_times[0]
                final_end = end_times[-1]
                
                # Asegurar que el formato de hora es válido antes de convertirlo a entero
                def extract_hour(time_str):
                    return int(re.search(r'\d+', time_str).group()) if re.search(r'\d+', time_str) else 0
                
                final_start_hour = extract_hour(final_start)
                final_end_hour = extract_hour(final_end)
                
                # Determinar el tipo de horario más cercano
                schedule_types = {"7-2": (7, 14), "9-3": (9, 15), "2-9": (14, 21), "3-10": (15, 22)}
                best_match = min(schedule_types.items(), key=lambda x: abs(final_start_hour - x[1][0]) + abs(final_end_hour - x[1][1]))[0]
            else:
                best_match = "Sin horario"
        else:
            best_match = "Sin horario"
        
        processed_data.append([prof, daily_schedule['lunes'], daily_schedule['martes'], daily_schedule['miércoles'], 
                               daily_schedule['jueves'], daily_schedule['viernes'], best_match])
    
    # Crear DataFrame final
    final_df = pd.DataFrame(processed_data, columns=['Profesor', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Clasificación Horaria'])
    return final_df