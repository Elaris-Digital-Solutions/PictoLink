# Expansión de Frases Especiales - Resumen

## Objetivo
Pensar como el usuario final y predefinir respuestas para combinaciones importantes de palabras que mapeen a pictogramas existentes en el catálogo.

## Frases Especiales Agregadas

### Saludos y Expresiones Coloquiales (10 nuevas)
| Expresión | Mapea a | IDs | Uso |
|-----------|---------|-----|-----|
| `qué tal` / `que tal` | cómo, estar | 22619, 5465 | Saludo informal |
| `cómo estás` | cómo, estar | 22619, 5465 | Saludo formal |
| `gracias` | gracias | 8128 | Agradecimiento |
| `por favor` | por favor | 8194 | Cortesía |
| `de nada` | de, nada | 7074, 29839 | Respuesta a gracias |
| `no sé` / `no se` | no, sé | 5526, 2652 | Desconocimiento |

### Conjugaciones Verbales Problemáticas (2 nuevas)
| Conjugación | Mapea a | ID | Problema Resuelto |
|-------------|---------|-----|-------------------|
| `dormiste` | dormir | 2369 | spaCy lemmatiza a "dormistar" ❌ |
| `durmiendo` | dormir | 2369 | Gerundio directo |

### Expresiones de Tiempo (3 nuevas)
| Expresión | Mapea a | IDs |
|-----------|---------|-----|
| `qué hora es` / `que hora es` | qué, hora, ser | 22620, 7129, 5581 |
| `ahora` | ahora | 13026 |
| `después` | después | 13080 |

## Resultados de Pruebas

### ✅ Caso Exitoso: "que tal"
```
Input: "que tal"
Output: ['cómo', 'estar']
Status: ✅ FUNCIONA CORRECTAMENTE
```

### ⚠️ Caso Parcial: "que tal dormiste?"
```
Input: "que tal dormiste?"
Current Output: ['qué']  
Expected: ['cómo', 'estar', 'dormir']
Problem: Sistema busca coincidencia EXACTA de frase completa
```

**Explicación**: El sistema de frases especiales busca coincidencia exacta. "que tal dormiste?" no coincide con "que tal" porque tiene palabras adicionales.

## Soluciones Propuestas

### Opción 1: Búsqueda de Subcadenas (Recomendada)
Modificar la lógica para buscar frases especiales como subcadenas:
- "que tal dormiste?" → encuentra "que tal" → mapea "cómo, estar" + procesa "dormiste" → "dormir"
- Resultado: `['cómo', 'estar', 'dormir']` ✅

### Opción 2: Agregar Más Combinaciones
Agregar frases completas específicas:
- "que tal dormiste" → "cómo, estar, dormir"
- "que tal estás" → "cómo, estar"
- etc.

**Problema**: Explosión combinatoria (demasiadas variantes)

### Opción 3: Híbrido
- Buscar primero coincidencia exacta
- Si no hay match, buscar subcadenas de frases especiales
- Procesar palabras restantes normalmente

## Estadísticas Finales

- **Frases especiales totales**: 23 (antes: 13)
- **Nuevas expresiones coloquiales**: 10
- **Conjugaciones verbales**: 2
- **Expresiones de tiempo**: 3
- **Cobertura mejorada**: +77% (10/13 frases nuevas)

## Próximos Pasos Recomendados

1. ✅ **Implementar búsqueda de subcadenas** para frases especiales
2. Agregar más conjugaciones problemáticas según se identifiquen
3. Expandir con expresiones regionales/coloquiales según feedback de usuarios
4. Considerar sistema de sinónimos para frases (ej: "qué onda" → "qué tal")
