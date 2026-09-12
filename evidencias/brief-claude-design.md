# Brief para un chat sin historial

Contexto autocontenido. Todo lo que aquí se afirma está medido y tiene transcript,
código en disco o captura detrás. Lo que no se midió está marcado como no medido, y eso
no se quita al presentarlo.

## Qué es el repositorio

**stack-canon** — https://github.com/rjla-developer/stack-canon · MIT · v1.0.0

Un plugin de Claude Code que hace dos cosas y se niega a hacer más:

1. **Aplica la arquitectura que cada equipo de framework publica para su propio stack.**
   No la que al agente le parezca. Para Flutter eso es MVVM en capas, feature-first,
   repositorios que no se conocen entre sí y una capa de dominio que no existe hasta que
   un segundo view model la necesite — verificado contra `docs.flutter.dev`, no contra un
   blog. Nueve stacks con el mismo tratamiento.

2. **Se asegura de que las reglas de negocio y las de presentación estén probadas en su
   borde exacto — y de que alguien haya mirado la pantalla.** Una suite verde prueba lo
   que se te ocurrió afirmar, no lo que no.

Más una regla por encima de las dos: **si no está claro dónde vive algo —qué plataforma,
qué proyecto, qué capa— pregunta una vez, y luego construye.**

Empezó haciendo nueve cosas. Cinco experimentos medidos sostuvieron dos, y el resto se
borró.

## El catálogo

Vive fuera del plugin y se descarga en cada ejecución, así que un PR aprobado llega a
todos sin reinstalar nada. Nueve stacks: Flutter, Next.js, **Astro**, Angular, React
Native/Expo, NestJS, FastAPI, Spring Boot, .NET.

Cada uno carga la arquitectura que su equipo recomienda, las reglas y trampas de prueba
específicas de ese stack, y las decisiones que el stack obliga a tomar sin dar un default.

## El método de las pruebas

Siete comparaciones. Siempre: **el mismo prompt literal, dos veces, cambiando una sola
variable.** Ambos lados corren con las mismas 57 skills personales activas — mide valor
marginal sobre un montaje ya bueno, no contra un Claude desnudo.

Dos aplicaciones construidas dos veces cada una:

- **Flutter** — app de eventos de baile en CDMX, más dos funcionalidades encima
- **Astro** — sitio de servicios caninos "De Pocas Pulgas", más un hero de scrollytelling

## Los resultados, con las derrotas dentro

### Lo que se sostiene en las siete comparaciones

**El `CLAUDE.md` del proyecto.** Existe o no existe, y el resultado no se ha movido nunca.
En Astro: 208 líneas contra ninguna. Y en la segunda funcionalidad se vio componer — una
decisión se justificó citando una regla que la funcionalidad anterior había escrito.

**Las pruebas.** 127 casos contra 54 en Astro. En Flutter, 68 contra 29.

### Lo que se sostuvo en Flutter y no en Astro

**La forma del código.** En Flutter, tres mediciones seguidas: bloques duplicados 8 → 17 →
18 sin skill, contra 6 → 6 → 5 con skill; función más larga 111 → 140 → 166 contra
91 → 103 → 99. En Astro salió al revés: 197 contra 258 la función más larga.

Con una corrida por lado, esto es varianza. No se presenta como ley.

### Los seis fallos propios, corregidos

1. El plugin cargaba **sin su hook** y nada lo delataba.
2. La doctrina **nunca decía "corre la app"** — una corrida entregó 68 pruebas verdes y un
   encabezado encimado en pantalla.
3. El mismo prompt se comportaba de dos formas según si nombrabas el stack.
4. Reportó "ninguna señal cruzó umbral" **sin haber contado**.
5. Un simulador bloqueado se leyó como límite permanente cuando era una carrera de 3
   segundos.
6. Optimiza para lo comprobable: **ninguna regla pregunta si la cosa sirve** a quien la
   va a usar. Registrado sin arreglar, porque un décimo gate sería un checklist
   haciéndose pasar por criterio.

### Cinco predicciones publicadas antes de medir, y falladas

- "Sin la skill elige el stack en silencio" → preguntó
- "La baseline no correrá sus tests" → los corrió
- "La baseline no encontrará hallazgos arquitectónicos" → encontró el mejor de todos
- "La skill escribirá mejores tests" → los de la baseline eran más amplios
- "Ninguno probará que la isla hidrata" → la skill escribió 52 pruebas para eso

## Los momentos que mejor lo cuentan

**Argumentó en contra de su propio catálogo.** Encontró las skills oficiales de Flutter,
dio los comandos, y dijo que en esa app no valían la pena: dos rutas y sin backend, así
que routing y serialización JSON casi no existen ahí.

**Descubrió que las skills "oficiales" de Astro no son para ti.** Las 22 de la
organización `withastro` son herramientas de mantenedor — triage, releases, revisión de
PRs. La que se llama `astro-developer` dice literalmente *"developing in the Astro
monorepo"*. Los agregadores las listan como "skills de Astro", que es como alguien acaba
instalando herramientas de contribuidor.

**Corrigió al usuario con medición, no con opinión.** El encargo del hero daba dos trampas
"ya medidas". Las dos corridas montaron el banco, probaron las dos variantes y encontraron
que una estaba al revés — con la causa: `GLTFLoader` deja la textura en `flipY = false`
mientras `CanvasTexture` nace en `true`.

**Corrigió un error propio de 25×.** Sospechó un problema de memoria (121,6 MB sobre el
papel), el primer A/B pareció confirmarlo, y al aislarlo los deltas salían negativos.
Tres instrumentos después: Chrome no guarda esos bitmaps como RGBA residente; el coste
real son ~5 MB.

**Se negó a dar un número.** *"El intervalo entre fotogramas no te lo doy como prueba: sale
16.7 clavado, que es la cadencia sintética de headless, no 60 fps en un teléfono."*

**Y la baseline encontró lo que nadie más.** Al escribir las pruebas que le faltaban, una
falló de verdad: 180° no son un número entero de cuadros de 8° (son 22,5), así que las
paradas pares caen cuatro grados desviadas. Invisible a ojo, sistemático.

## Lo que NO hace

**No mejora el diseño.** Los dos sitios de Astro se ven prácticamente igual. Tiene dos
pilares y ninguno es diseño; no lo prometía y no lo entrega.

**No produce mejor código por sí solo.** Esa afirmación se probó y no se sostiene.

## Lo que todavía no está probado

- Una corrida por lado. Es una anécdota, no una medición.
- Nadie evaluó la **experiencia** de las apps, sólo el código y las métricas.
- Siete de los nueve stacks nunca se han probado en una corrida.

## Evidencia disponible

| | Dónde |
|---|---|
| Registro técnico completo, con las derrotas | `docs/DEMO-COMPARISON.md` y `evidencias/react/README.md` |
| Entorno exacto de las pruebas (las 57 skills) | `evidencias/entorno.md` |
| Capturas de las corridas de Flutter | `evidencias/capturas/` |
| Documento visual con las métricas de Flutter | https://claude.ai/code/artifact/07e670fe-40ec-4245-9dee-4d3be59e00da |
| Los cuatro proyectos construidos | dos Flutter, dos Astro, en disco |

## Tono al presentarlo

Cero superlativos. Los números hablan solos y **las derrotas dan más credibilidad que las
victorias**: cualquiera puede clonar el repo y reproducir esto en una tarde. Que te
encuentren siendo honesto vale más que un A/B impecable.

La historia real no es "construí una herramienta que gana". Es: **construí nueve cosas,
medí siete veces, borré siete de las nueve porque los datos no las sostenían, y publiqué
las cinco predicciones que fallé.**
