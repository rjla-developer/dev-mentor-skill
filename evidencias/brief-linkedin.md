# Brief para el chat de publicaciones

Documento de contexto para un chat sin historial previo. Todo lo que aquí se afirma
está medido y tiene transcript o captura detrás. **Lo que no se midió está marcado
como no medido, y eso no se quita al publicar.**

## 1. Qué es

`stack-canon` es un plugin de Claude Code. No genera código: **decide cómo se va a
construir antes de que se escriba**, aplicando la doctrina publicada por el equipo que
mantiene cada framework.

Repositorio: https://github.com/rjla-developer/stack-canon · MIT · versión 0.2.0

## 2. El problema que ataca

Los equipos oficiales — Flutter, Angular, Expo, Vercel, Microsoft, .NET, Trail of Bits —
han publicado cientos de "agent skills". Casi nadie las instala, nada las orquesta, y
ninguna enseña criterio: son capacidades ("cómo hacer un layout responsivo"), no juicio
("llevas cuarenta widgets duplicando el mismo botón").

Y todas tienen huecos. Las skills oficiales de Flutter cubren layouts, routing y
serialización JSON. **No cubren estrategia de pruebas.** Alguien tiene que detectar eso
y llenarlo.

## 3. Qué hace, en concreto

- Detecta el stack y consulta un **catálogo vivo** (se descarga en cada ejecución, así
  que un cambio aprobado llega a todos sin reinstalar nada).
- Aplica la arquitectura que recomienda el equipo del framework. Para Flutter: MVVM en
  capas, feature-first, repositorios que no se conocen entre sí — verificado contra
  `docs.flutter.dev/app-architecture/guide`, no contra un blog.
- Trae **reglas de prueba específicas del stack**, no doctrina genérica. Ejemplo real:
  *"un test que necesita `pumpWidget` está probando la View; si la misma aserción se
  puede hacer contra el view model, bájalo de capa"*.
- Registra **las trampas que ya pagó** en el `CLAUDE.md` del proyecto, para que el
  siguiente no las pague.
- Exige lanzar la app y **mirar la pantalla**. Una suite verde prueba lo que se te
  ocurrió afirmar; una pantalla renderizada muestra lo que no.

## 4. La ventaja, dicha con precisión

**No es "produce mejor código".** Esa afirmación se probó y no se sostiene: la baseline
escribe buen código.

Es esto: **las decisiones salen a la superficie antes de quedar horneadas, la
herramienta declara dónde termina lo que sabe, y el proyecto conserva memoria.**

## 5. Los experimentos

Tres, todos con el mismo método: el mismo prompt literal, dos veces, cambiando una sola
variable. **Importante: la baseline no es Claude a secas** — ambos lados corren con 57
skills personales activas. Mide valor marginal sobre un montaje ya bueno.

### Experimento 1 — Skill de Alexa (tutor de inglés)

**stack-canon perdió en lo más importante.** No lanzó la app; la baseline sí, y encontró
un defecto visual. Ganó en estructura y memoria, pero perdió en verificación empírica.

Ese fallo produjo una regla nueva. Es el experimento más valioso de los tres.

### Experimento 2 — App Flutter de eventos de baile

Mismo prompt, dos construcciones completas.

| | Sin skill | Con skill |
|---|---|---|
| Líneas de código | 1 505 | **1 476** |
| Líneas de prueba | 406 | **876** |
| `build()` más largo | **111** | **91** |
| Defectos visuales encontrados | 1 | **3** |
| `CLAUDE.md` | ninguno | 122 líneas, escrito **antes** del código |

El umbral del catálogo para partir un widget es **100 líneas**. Uno lo cruzó sin
enterarse; el otro se quedó debajo y avisó que lo vigilaba.

Dos de los tres defectos solo aparecieron **al mirar la pantalla**: el conteo encimándose
con una insignia, y "ya tienes lugar" comunicado únicamente con un botón deshabilitado —
que se lee como error. El widget renderizaba exactamente como estaba escrito.

Documento visual: https://claude.ai/code/artifact/07e670fe-40ec-4245-9dee-4d3be59e00da

### Experimento 3 — La misma feature, a los dos códigos

*"¿En cuál preferiría meter una feature dentro de seis meses?"* no hay que imaginarlo.
Se le pidió a ambos: **el organizador puede cancelar un evento**.

| | Sin skill | Con skill |
|---|---|---|
| Líneas para la misma feature | **+227** | **+105** |
| Bloques duplicados | **8 → 17** | **6 → 6** |
| Archivo más grande | 289 → **402** | 286 → 318 |

**Un código absorbió la feature duplicando; el otro no tuvo que hacerlo.** Ese es el
resultado más fuerte de los tres experimentos, y es el que responde la pregunta de los
seis meses con números.

## 6. Los fallos propios, que se publican igual

Sin esta sección lo anterior no vale nada.

1. **El plugin cargaba sin su hook.** El tope de líneas del `CLAUDE.md` quedaba sin
   aplicar y nada lo delataba. Apareció en la primera instalación real desde el
   marketplace; la CI nunca instalaba el plugin.
2. **La doctrina nunca decía "corre la app".** Una corrida entregó 68 pruebas verdes,
   analizador limpio y build compilando — con un encabezado encimado en pantalla.
3. **El mismo prompt se comportaba de dos formas**, porque nombrar un stack sacaba a la
   skill de modo automático. El usuario lo notó antes que nosotros.
4. **Una corrida reportó "ninguna señal cruzó umbral" sin haber contado.** Su propio
   `build()` estaba en 103 líneas contra un umbral de 100.

Los cuatro se corrigieron. Los cuatro salieron de una prueba, no de una revisión.

## 7. Lo que todavía no está probado

- **Una corrida por lado.** Es una anécdota, no una medición. Harían falta tres.
- **Nadie evaluó la experiencia de las apps**, solo el código.
- **El catálogo tiene ocho stacks, pero solo Flutter se ha probado en una corrida.**
- La instalación de skills oficiales **nunca se ejercitó** en una construcción real: en
  las dos corridas de Flutter la propia skill argumentó en contra de instalarlas.

## 8. Lo que se le pide a la comunidad

El catálogo envejece rápido: los equipos oficiales publican cada semana. Falta:

- **22 stacks** listos para adoptar, con plantilla — están en `docs/ROADMAP.md`.
- Umbrales mal calibrados. Si uno hace ruido en código real, cámbialo con la evidencia.
- Comandos de instalación que cambiaron o repositorios que se movieron.

La única regla: **un dato que no puedes verificar se marca `needs_verification: true`,
nunca se inventa.** La CI rechaza lo contrario.

## 9. Activos disponibles

| | Dónde |
|---|---|
| Documento visual con las métricas | https://claude.ai/code/artifact/07e670fe-40ec-4245-9dee-4d3be59e00da |
| Capturas de las tres corridas | `evidencias/capturas/` (ver `MANIFIESTO.md`) |
| Registro técnico completo | `docs/DEMO-COMPARISON.md` |
| Repositorio | https://github.com/rjla-developer/stack-canon |
| Video de pantalla de las corridas | lo aporta el autor |

## 10. Ángulos sugeridos, uno por día

1. **El problema.** Cientos de skills oficiales publicadas, casi nadie las instala.
2. **El experimento.** Mismo prompt, dos veces, una variable. Enseñar los dos árboles de
   carpetas — se entiende sin saber programar.
3. **El fallo propio.** 68 pruebas verdes y un encabezado roto. Por qué la regla estaba
   incompleta y cómo se corrigió.
4. **La feature.** +227 líneas contra +105, y la duplicación que se duplicó de un lado.
5. **El "no".** La skill argumentando en contra de instalar sus propias
   recomendaciones, y negándose a añadir una capa de arquitectura que un checklist
   habría exigido.
6. **La llamada a la comunidad.** Los 22 stacks y la regla de no inventar datos.

**Tono:** cero superlativos. Los números hablan solos y las derrotas dan más credibilidad
que las victorias. Cualquiera puede clonar el repo y reproducir esto en una tarde — que
te encuentren siendo honesto vale más que un A/B impecable.
