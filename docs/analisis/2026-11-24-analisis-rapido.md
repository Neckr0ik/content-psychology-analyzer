# Análisis rápido: content-psychology-analyzer (24-nov-2026)

Diagnóstico, sin cambios de código. Pedido de Giovanni.

## Estado
- `pip install -r requirements.txt` y `pytest -q`: **22 pruebas pasan**, sin red.
- `python main.py --no-charts` reproduce los números del README (41, 55, 63 en las muestras citadas). El README no miente.
- Contexto previo (Graphiti, Qdrant): el repo es público, parte del portafolio Hybrid Intelligence; la memoria no tenía hallazgos técnicos de este código.

## Nemotron
`opencode_run` está en línea (`opencode_status`), pero toda llamada falla con `Unrecognized flag: --dir in command opencode run`: el envoltorio añade una opción que el CLI de OpenCode no acepta, y la herramienta sólo expone `message`, `model` y `session_id`. El mismo fallo se anotó el mismo día en otro repo. **No hubo revisión de Nemotron**, así que no hay aciertos que anotar. La revisión de abajo es mía y está comprobada ejecutando el código.

## Hallazgos comprobados (de mayor a menor)

| # | Hallazgo | Prueba |
|---|---|---|
| 1 | **El «arousal» usa `abs(compound)` de VADER.** Eso es intensidad de valencia, no activación. Un texto triste y apagado puntúa alto, justo lo contrario de lo que dice la descripción (tristeza = baja activación). | «A quiet, sad, lonely story of grief and loss.» → Arousal 45.7 |
| 2 | **Sin plurales ni derivados.** La coincidencia es de palabra completa, sin lematizar: «awards», «nominations», «thrilled» no cuentan. | «won an award» → Social 17; «won three awards» → 0 |
| 3 | **Sesgo por longitud.** El puntaje es cobertura de la lista, así que un texto largo acumula más claves distintas. Afecta directo a `--compare` si A y B difieren en largo. | misma pregunta con 8 claves de misterio más → Curiosity 28.8 → 100 |
| 4 | **Una sola palabra puede inflar el total.** «love» cuenta en dos pilares PERMA y dispara el bono de amplitud. | «love» → PERMA 32, Arousal 50, total 27 |
| 5 | **Palabras funcionales como señal**: «why», «how», «when», «then», «but», «i/he/she», «series», «season», «hit», «only», «first». Un texto de 3 palabras sale como «Prestige Signal». | «A new series.» → perfil Prestige Signal (total 5.8) |
| 6 | **Las descripciones de perfil prometen causalidad** que el README niega: «Built to spread», «Drives clicks», «Creates binge behavior», «Creates loyal audiences» (`frameworks.py`, impresas en CLI y reporte). | contradice «describe el texto, no predice» |
| 7 | **Detector de números**: el comentario dice que «3 Emmy Awards» cuenta, pero la regex exige unidad (million, fans…). «5k fans» da 0. | «Won 3 Emmy Awards» → sólo suma «emmy» |
| 8 | **Marco ganancia/pérdida sin negación**: «You will not lose money» sale como *loss*. (La negación general ya está documentada como límite.) | `compare(...)` → `loss` / `gain` |
| 9 | **CLI**: `--threshold` acepta negativos (todo «difiere» con 0 pts); `--text ""` cae en silencio al modo lote. | probado |

## Rigor de las citas
- **Bien ancladas**: Berger & Milkman 2012 (arousal y compartir), Loewenstein 1994 (brecha de información), Cialdini 1984 (prueba social), Tversky & Kahneman 1981 (marco ganancia/pérdida) y la distinción énfasis/equivalencia de Chong & Druckman 2007.
- **Russell 1980 (círculo)**: valencia y activación son ejes distintos; usar `|valence|` como activación es el hallazgo 1. Cambiar a un léxico de activación (p. ej. Warriner et al. 2013, a verificar) o quitar el término VADER.
- **Kahneman & Tversky 1979 para escasez**: la aversión a la pérdida no es el efecto de escasez. La base habitual es la teoría de la mercancía (Brock 1968) y Worchel, Lee & Adewole 1975 (a verificar antes de citar). Hoy es la cita más débil.
- **Green & Brock 2000**: el «transporte» es un estado del lector medido con escala; los marcadores textuales (pronombres, «but») son una operacionalización propia, no del artículo.
- **Markus & Wurf 1987 / Seligman 2011**: son teorías de la persona; que el texto diga «you» o «purpose» es un proxy. Está bien como heurística si el README lo dice (ya dice «text cues»).
- **Chong & Druckman**: sus «consideraciones» son creencias del tema (libertad vs. seguridad), no mecanismos retóricos. Tratar cada dimensión como una familia de consideraciones es una analogía; conviene decirlo en una línea.

## Mejoras (en orden de retorno)
1. Normalizar por longitud o usar densidad por 100 palabras; mínimo, avisar en `--compare` cuando A y B difieren mucho en largo.
2. Raíces simples (plurales y -ed/-ing) o listas con variantes.
3. Quitar `abs(compound)` del arousal, o sustituirlo por léxico de activación, y actualizar README y pruebas fijadas.
4. Podar palabras funcionales y repetidas entre dimensiones («love», «discover», «first», «why»).
5. Reescribir `CONTENT_PROFILE_TYPES` en lenguaje descriptivo.
6. Validar `--threshold > 0` y `--text` vacío; corregir el comentario de la regex de números.
7. Pruebas para cada hallazgo anterior (plural, longitud, tristeza).

Cada cambio de fórmula exige actualizar las tablas del README en el mismo PR (regla del CLAUDE.md).

## Ideas para KALEIDO (híbrida), sin copiar código de motor
Opinión breve, basada en lo que la memoria dice de KALEIDO/SKRIPT; no vi su código.
- **Línea base barata**: la prueba propuesta para SKRIPT pide un «lector genérico» contra el que ganar. Un puntaje de claves transparente y sin red es esa base ideal; si las teselas con INRA no la superan, no hay número de «potencial».
- **Patrón A/B**: salida «qué enfatiza cada redacción» con claves visibles, en vez de un puntaje único. Encaja con «¿viaja?» entre países.
- **Límites como producto**: la sección Limitations y las pruebas que fijan fórmulas documentadas son el mismo patrón de «Lo que no es» de la página de confianza.
- **Qué evitar**: los hallazgos 1, 2 y 3 son los errores típicos de cualquier lector por léxico; vale como lista de revisión.
- No reutilizar el léxico: es inglés, sin calibrar.

## Conectores (sin activar)
1. **Replit o Vercel para una demo pública**: caja de texto → siete barras y comparador A/B con claves. En Vercel iría como función Python sin matplotlib; en Replit, una app pequeña con el mismo motor. Conviene hacerlo después de corregir 1 a 4, para no exhibir los defectos.
2. **Skills de psicología de marketing**: servirían para revisar las citas de escasez y para redactar pares A/B del demo. No aparecen entre las skills de esta sesión; no las busqué ni las activé.
