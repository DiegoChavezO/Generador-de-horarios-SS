import pandas as pd
from itertools import product
from datetime import datetime, timedelta

def generate_tt_schedule(professor_schedule, tt_data, tt_slots):
    """
    Genera los horarios de los trabajos terminales (TT) basándose en la disponibilidad de profesores y los slots disponibles.
    
    Parameters:
        professor_schedule (pd.DataFrame): Horarios transformados de los proffesores.
        tt_data (pd.DataFrame): Lista de trabajos terminales con sus sinodales y directores.
        tt_slots (pd.DataFrame): Rango de fechas y disponibilidad de slots para TT.
    
    Returns:
        pd.DataFrame: Horario generado con las asignaciones de TT.
    """
    
    assigned_tt = []
    professor_occupancy = {}
    professor_schedule.columns = professor_schedule.columns.str.upper().str.strip()

    #debug
    print("Espacios disponibles en tt_slots antes de la asignación:")
    print(tt_slots)

    
    for _, tt in tt_data.iterrows():
        tt_id = tt['TT']
        participants = [tt['DIRECTOR 1'], tt['DIRECTOR 2'], tt['SINODAL 1'], tt['SINODAL 2'], tt['SINODAL 3']]
        participants = [p for p in participants if pd.notna(p)]  # Remover valores nulos
        
        print(f"Asignando TT: {tt_id}...")
        #print(f"working...")
        
        # Iterar sobre las filas de tt_slots para encontrar un día disponible
        '''
        for index, slot in tt_slots.iterrows():
            start_date = datetime.strptime(slot['Inicio'], "%d %b %Y")  # Convertir fecha inicio
            end_date = datetime.strptime(slot['Fin'], "%d %b %Y")  # Convertir fecha fin
            days_range = (end_date - start_date).days + 1  # Calcular el rango de días
            
            for day_offset in range(days_range):
                assigned_date = start_date + timedelta(days=day_offset)  # Tomar un día dentro del rango
                
                # Solo asignar en días lunes a viernes
                if assigned_date.weekday() >= 5:
                    continue

                assigned_date_str = assigned_date.strftime("%d %b %Y")  # Formato de salida
                
                for time_slot in ["8-10", "10-12", "12-2", "2-4", "4-6", "6-8"]:
                    
                    if tt_slots.at[index, time_slot] > 0:  # Si hay espacio disponible en ese día
                        availability = {p: check_availability(professor_schedule, p, time_slot) for p in participants}
                        available_count = sum(availability.values())

                        if available_count >= len(participants) - 1:
                            if not any(professor_occupancy.get((p, assigned_date_str, time_slot), False) for p in participants):
                                for p in participants:
                                    professor_occupancy[(p, assigned_date_str, time_slot)] = True

                                # Guardar el TT en la lista de asignados
                                assigned_tt.append([
                                    tt_id, tt['DIRECTOR 1'], tt['DIRECTOR 2'], tt['SINODAL 1'],
                                    tt['SINODAL 2'], tt['SINODAL 3'], assigned_date_str, time_slot,
                                    availability.get(tt['DIRECTOR 1'], False),
                                    availability.get(tt['DIRECTOR 2'], False),
                                    availability.get(tt['SINODAL 1'], False),
                                    availability.get(tt['SINODAL 2'], False),
                                    availability.get(tt['SINODAL 3'], False)
                                ])
                                
                                print(f"✅ Asignado TT {tt_id} el {assigned_date_str} en {time_slot}")

                                # Reducir disponibilidad en el día exacto
                                tt_slots.at[index, time_slot] -= 1
                                break  # Salir del loop de horarios para este TT
                if tt_slots.at[index, time_slot] == 0:
                    break  # Pasar al siguiente día si ya no hay espacio

    return pd.DataFrame(assigned_tt, columns=[
        "ID_TT", "DIRECTOR 1", "DIRECTOR 2", "SINODAL 1", "SINODAL 2", "SINODAL 3", "FECHA", "HORARIO",
        "DIR1 DISPONIBLE", "DIR2 DISPONIBLE", "SIN1 DISPONIBLE", "SIN2 DISPONIBLE", "SIN3 DISPONIBLE"
    ])
    '''

    
        for _, slot in tt_slots.iterrows():
            
            date = f"{slot['Inicio']} - {slot['Fin']}"
            for time_slot in ["8-10", "10-12", "12-2", "2-4", "4-6", "6-8"]:
                
                if tt_slots.at[slot.name, time_slot] > 0:#slot[time_slot] > 0:  # Hay espacio disponible
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
                            tt_slots.at[slot.name, time_slot] -= 1 #slot[time_slot] -= 1
                            print(f"✅ Asignado TT {tt_id} en {date} {time_slot}")
                            break
    
    return pd.DataFrame(assigned_tt, columns=[
        "ID_TT", "DIRECTOR 1", "DIRECTOR 2", "SINODAL 1", "SINODAL 2", "SINODAL 3", "FECHA", "HORARIO", 
        "DIR1 DISPONIBLE", "DIR2 DISPONIBLE", "SIN1 DISPONIBLE", "SIN2 DISPONIBLE", "SIN3 DISPONIBLE"
    ])
    
def check_availability(professor_schedule, professor, time_slot):
    """
    Verifica si un profesor está disponible en un slot de horario.
    """
    
    """
    Verifica si un profesor está disponible en un slot de horario comparando rangos de tiempo.
    """
    if professor in professor_schedule["PROFESOR"].values:
        prof_row = professor_schedule[professor_schedule["PROFESOR"] == professor].iloc[0]

        # Convertir `time_slot` (ejemplo: "4-6") en valores de hora
        slot_start, slot_end = map(int, time_slot.split('-'))

        # Recorrer los días y verificar si el profesor está disponible en ese rango
        for day in ["LUNES", "MARTES", "MIÉRCOLES", "JUEVES", "VIERNES"]:
            horario_profesor = str(prof_row[day])
            
            if horario_profesor not in ["nan", "None", ""]:
                # Convertir horario del profesor a rangos de tiempo
                try:
                    horario_parts = horario_profesor.split("-")
                    if len(horario_parts) == 2:
                        prof_start, prof_end = map(int, horario_parts)
                        # Validar si el `time_slot` está dentro del horario del profesor
                        if prof_start <= slot_start and prof_end >= slot_end:
                            print(f"✅ {professor} DISPONIBLE en {time_slot} (Horario: {prof_start}-{prof_end})")
                            return True
                except ValueError:
                    print(f"⚠ Error al interpretar horario de {professor}: {horario_profesor}")

        print(f"❌ {professor} NO DISPONIBLE en {time_slot} (Horario: {prof_row[['LUNES', 'MARTES', 'MIÉRCOLES', 'JUEVES', 'VIERNES']]})")
        return False

    print(f"❌ {professor} NO ENCONTRADO en los horarios.")
    return False


    '''
    if professor in professor_schedule["PROFESOR"].values:
            prof_row = professor_schedule[professor_schedule["PROFESOR"] == professor].iloc[0]
            #print(f"📋 Revisando disponibilidad de {professor} en {time_slot}...")

            # Asegurémonos de que las columnas existen en `professor_schedule`
            #print(prof_row[["LUNES", "MARTES", "MIÉRCOLES", "JUEVES", "VIERNES"]])

            available = any(time_slot in str(prof_row[day]) for day in ["LUNES", "MARTES", "MIÉRCOLES", "JUEVES", "VIERNES"])
            print(f"✅ {professor} disponibilidad en {time_slot}: {available}")
            return available
    print(f"❌ {professor} no encontrado en los horarios.")
    return False'''