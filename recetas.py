# recetas.py

# Generación algorítmica de más de 100 recetas cruzando el inventario base
# para simular un volumen masivo de datos B2C / SaaS.

_ingredientes_base = [
    "huevos", "champiñones", "pechuga de pavo", "avena", "leche", "platano", 
    "pechuga de pollo", "cebolla", "base de pizza", "nata ligera", "bacon de pavo",
    "arroz", "pan integral", "atun en lata", "aguacate", "miel", "espinacas",
    "lomo de cerdo", "lentejas en bote", "garbanzos en bote", "filete de merluza",
    "pasta", "tortillas de trigo", "queso batido", "queso rallado", "tomate"
]

BASE_DE_DATOS_RECETAS = []

# 1. Añadimos bloques sistemáticos de combinaciones lógicas de cocina (Desayunos, Almuerzos, Cenas)
categorias = ["Alta en Proteína / Fuerza", "Bajo en Carbohidratos / Definición", "Energía / Cardio", "Permitido / Cheat Meal Sano"]

# Generación de 104 recetas cruzando proteínas, bases y vegetales
contador = 1
for cat in categorias:
    for proteina in ["pechuga de pollo", "pechuga de pavo", "atun en lata", "huevos", "lomo de cerdo", "filete de merluza"]:
        for base in ["arroz", "pasta", "pan integral", "tortillas de trigo", "avena", "lentejas en bote", "garbanzos en bote", "base de pizza"]:
            for vegetal in ["champiñones", "cebolla", "espinacas", "tomate", "aguacate"]:
                
                # Reglas lógicas básicas para descartar combinaciones incomibles (Ej: pescado con avena)
                if proteina == "filete de merluza" and base in ["avena", "base de pizza"]: continue
                if proteina == "atun en lata" and base == "avena": continue
                if base == "base de pizza" and cat != "Permitido / Cheat Meal Sano": continue
                if cat == "Bajo en Carbohidratos / Definición" and base in ["arroz", "pasta", "base de pizza"]: continue
                
                nombre_receta = f"Plato Fit #{contador}: {proteina.capitalize()} con {base} y {vegetal}"
                
                BASE_DE_DATOS_RECETAS.append({
                    "nombre": nombre_receta,
                    "ingredientes": list(set([proteina, base, vegetal])),
                    "categoria": cat,
                    "instrucciones": f"1. Prepara la base ({base}) adecuadamente cocida o tostada. 2. Cocina la proteína ({proteina}) a la plancha o salteada con un toque de aceite. 3. Añade el vegetal ({vegetal}) picado limpio como acompañamiento fresco o salteado conjunto. Sazona al gusto."
                })
                contador += 1
                if contador > 110: break
            if contador > 110: break
        if contador > 110: break

INGREDIENTES_PLATAFORMA = sorted(_ingredientes_base)