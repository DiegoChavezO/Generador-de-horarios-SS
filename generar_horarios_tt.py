import pandas as pd
from itertools import product

def generate_tt_schedule(professor_schedule, tt_data, tt_slots):
    """
    Genera los horarios de los trabajos terminales (TT) basándose en la disponibilidad de profesores y los slots disponibles.
    
    Parameters:
        professor_schedule (pd.DataFrame): Horarios transformados de los profesores.
        tt_data (pd.DataFrame): Lista de trabajos terminales con sus sinodales y directores.
        tt_slots (pd.DataFrame): Rango de fechas y disponibilidad de slots para TT.
    
    Returns:
        pd.DataFrame: Horario generado con las asignaciones de TT.
    """
    
    assigned_tt = []
    professor_occupancy = {}
    professor_schedule.columns = professor_schedule.columns.str.upper().str.strip()
    
    for _, tt in tt_data.iterrows():
        tt_id = tt['TT']
        participants = [tt['DIRECTOR 1'], tt['DIRECTOR 2'], tt['SINODAL 1'], tt['SINODAL 2'], tt['SINODAL 3']]
        participants = [p for p in participants if pd.notna(p)]  # Remover valores nulos
        print(f"working...")
        for _, slot in tt_slots.iterrows():
            
            date = f"{slot['Inicio']} - {slot['Fin']}"
            for time_slot in ["8-10", "10-12", "12-2", "2-4", "4-6", "6-8"]:
                
                if slot[time_slot] > 0:  # Hay espacio disponible
                    #print("Columnas en professor_schedule:", professor_schedule.columns)
                    availability = {p: check_availability(professor_schedule, p, time_slot) for p in participants}
                    available_count = sum(availability.values())
                    
                    if available_count >= len(participants) - 1:  # Priorizar con más coincidencias
                        # Verificar que el profesor no esté ya ocupado en este horario
                        if not any(professor_occupancy.get((p, date, time_slot), False) for p in participants):
                            
                            # Registrar ocupación
                            for p in participants:
                                professor_occupancy[(p, date, time_slot)] = True
                            
                            # Registrar el TT
                            assigned_tt.append([
                                tt_id, tt['DIRECTOR 1'], tt['DIRECTOR 2'], tt['SINODAL 1'],
                                tt['SINODAL 2'], tt['SINODAL 3'], date, time_slot,
                                availability.get(tt['DIRECTOR 1'], False),
                                availability.get(tt['DIRECTOR 2'], False),
                                availability.get(tt['SINODAL 1'], False),
                                availability.get(tt['SINODAL 2'], False),
                                availability.get(tt['SINODAL 3'], False)
                            ])
                            print(assigned_tt)
                            
                            # Reducir disponibilidad del slot
                            slot[time_slot] -= 1
                            break
    
    return pd.DataFrame(assigned_tt, columns=[
        "ID_TT", "DIRECTOR 1", "DIRECTOR 2", "SINODAL 1", "SINODAL 2", "SINODAL 3", "FECHA", "HORARIO", 
        "DIR1 DISPONIBLE", "DIR2 DISPONIBLE", "SIN1 DISPONIBLE", "SIN2 DISPONIBLE", "SIN3 DISPONIBLE"
    ])

def check_availability(professor_schedule, professor, time_slot):
    """
    Verifica si un profesor está disponible en un slot de horario.
    """
    if professor in professor_schedule['PROFESOR'].values:
        prof_row = professor_schedule[professor_schedule['PROFESOR'] == professor].iloc[0]
        return any(time_slot in str(prof_row[day]) for day in ['LUNES', 'MARTES', 'MIÉRCOLES', 'JUEVES', 'VIERNES'])
    return False
