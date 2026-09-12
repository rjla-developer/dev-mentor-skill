# Experimento: De Pocas Pulgas (Astro)

Bitácora nueva. Las evidencias anteriores (`evidencias/`, `docs/DEMO-COMPARISON.md`)
se quedan quietas como registro histórico de la versión 0.x — **no se usan para juzgar
esta**.

Aquí se validan **tres cosas y nada más**:

| | Criterio | Cómo se juzga |
|---|---|---|
| 1 | **`CLAUDE.md` creado y con calidad** | ¿Existe? ¿Antes o después del código? ¿Reglas comprobables leyendo el código, o frases vagas? ¿Trae los bordes exactos y las trampas que se pagaron? |
| 2 | **Pruebas por funcionalidad, que verifiquen calidad de producto** | ¿Cada regla en su borde exacto, desde ambos lados? ¿Se probaron las reglas de presentación, no solo las de negocio? ¿Se lanzó y se miró? |
| 3 | **Arquitectura y recomendaciones del equipo de la tecnología** | ¿Citó a Astro o improvisó? ¿Nombró lo que el equipo publica y lo que no? ¿Declaró quién recomienda cada cosa? |

## Por qué Astro y no Next.js

El sitio es real, no material de prueba: es para un negocio de servicios caninos.
Es ~90% contenido estático más una isla interactiva (el cotizador), que es exactamente
la tesis de Astro.

La entrada `registry/astro.json` se escribió **antes** del experimento, verificada contra
`docs.astro.build`. Es la primera entrada del registro nacida de una construcción real
en vez de solo investigación.

## Lo que el catálogo dice de Astro, y conviene tener a la vista

- **`src/pages` es el único directorio reservado.** El resto son convenciones que la
  documentación describe y explícitamente no exige.
- **Astro borra todo el JavaScript de cliente por defecto.** Un componente solo corre en
  el navegador si le escribes un `client:*`.
- **Las 22 skills de la org `withastro` son de mantenedor**, no para quien construye
  sitios. El `astro-developer` dice literalmente *"developing in the Astro monorepo"*.
  Lo único agent-facing para constructores es `withastro/docs-mcp`, que es un servidor
  MCP, no una skill.

Ese último punto es lo que el criterio 3 tiene que atrapar: **si la corrida dice que
instaló "las skills oficiales de Astro", instaló herramientas de contribuidor.**

## Entorno

Idéntico en ambos lados salvo `stack-canon`. Ver `../entorno.md` para las 57 skills
personales que siguen activas en los dos.

## Predicciones, escritas antes de ver nada

Se publican aunque fallen. Las cuatro anteriores fallaron.

1. **Los dos van a elegir bien el modo estático.** Es el default de Astro y no hay que
   saber nada para acertar.
2. **La diferencia va a estar en el `client:*`.** Espero que el lado con skill declare qué
   directiva puso en el cotizador y por qué; el otro, que ponga `client:load` sin decirlo.
3. **Ninguno de los dos va a probar que la isla hidrata.** Es la trampa registrada del
   stack — el HTML es idéntico con directiva y sin ella — y hace falta un navegador para
   atraparla. Si alguno lo prueba, es el hallazgo del experimento.
4. **El `CLAUDE.md` va a ser el criterio que más separe**, porque es binario: existe o no.


---

# Resultado — funcionalidad 1: el sitio

## Los tres criterios

| | Sin skill | Con skill |
|---|---|---|
| **1. `CLAUDE.md`** | **ninguno** | **115 líneas, escrito ANTES del código** — con los bordes exactos, las decisiones forzadas y cinco minas |
| **2. Pruebas** | **8** (node:test) | **97**: 45 vitest (reglas + Container API) + 52 Playwright contra el build de producción |
| **3. Arquitectura del equipo** | improvisó una estructura razonable | trajo el registro en vivo, declaró tres decisiones forzadas con su coste, y usó la **Container API** y el **"probar contra producción"** que Astro publica |

Otros números: 16,3 KB de JavaScript contra 13,3 KB. Defectos visuales encontrados: 2 contra 5.

## La predicción que falló, y es el hallazgo

Escrito antes de las corridas:

> *"Ninguno de los dos va a probar que la isla hidrata. Es la trampa registrada del stack
> — el HTML es idéntico con directiva y sin ella — y hace falta un navegador para
> atraparla. Si alguno lo prueba, es el hallazgo del experimento."*

**Falsa.** El lado con skill escribió 52 tests de Playwright contra el build de
producción con esa frase exacta como motivo: *"la capa que nadie más puede cubrir — que
el script realmente se enganche en un navegador"*.

Y ahí encontró cinco defectos que 97 tests verdes no veían:

1. El `<fieldset>` desbordaba la página a 320px — arranca con `min-inline-size: min-content`
2. `/cotizar/` no tenía `h1` — una página hecha para Google sin encabezado principal
3. El héroe arrancaba 170px más adentro que el encabezado (`margin-inline: auto` heredado)
4. La burbuja de WhatsApp tapaba un botón "+" en móvil
5. El botón deshabilitado era gris sobre gris, ~1.4:1 — se leía como error

La trampa que el registro advertía se atrapó **porque el registro la advertía**.

## Las otras tres predicciones

- **"Los dos acertarán el modo estático"** — correcta, y sin mérito: es el default.
- **"La diferencia estará en el `client:*`"** — parcialmente falsa, por una razón que no
  contemplé: **ninguno de los dos usó una isla con directiva.** Los dos resolvieron el
  cotizador con un `<script>` dentro de un `.astro`, que es el mecanismo de Astro para
  JavaScript vanilla y no necesita directiva. El lado con skill además lo justificó:
  *"React habría costado ~45 KB de runtime para unos steppers"*.
- **"El `CLAUDE.md` será lo que más separe"** — correcta. Es binario.

## Lo que NO mejoró, y el usuario lo notó primero

**El diseño es prácticamente el mismo.** Los dos sitios se ven igual. La skill tiene dos
pilares y ninguno es diseño; no lo prometía y no lo entrega.

## Variable no controlada

**Los dos lados corrieron versiones distintas de Astro: 5.18.2 sin skill, 7.3.2 con
skill.** Ninguno de los dos prompts fijaba versión. Es un salto de dos mayores, así que
parte de la diferencia en la API disponible —la Container API entre ellas— puede venir de
ahí y no de la skill. Para la siguiente funcionalidad hay que fijar la versión en ambos.

## Artefacto del método, otra vez

El prompt volvió a llegar cortado (`"con 5 sesioete."`) en **ambos** lados por igual. Los
dos lo detectaron y lo resolvieron por aritmética. Es la tercera vez que la copia desde
el chat corrompe una regla.


---

# Resultado — funcionalidad 2: el hero de scrollytelling

Fase de análisis, antes de construir. El encargo pedía cuatro respuestas medidas y una
pausa. **Los dos pararon donde se les pidió.**

## Lo que ambos hicieron igual, y es mucho

Esta es la pareja de salidas más fuerte de toda la serie, y la convergencia importa tanto
como la diferencia:

- **Los dos corrigieron `flipY`** al usuario. Montaron el banco, probaron las dos
  variantes, y llegaron a la misma causa: `GLTFLoader` deja la textura del GLB en
  `flipY = false` mientras `CanvasTexture` nace en `true`. Los dos reconciliaron la
  medición del usuario en vez de descartarla.
- **Los dos investigaron los 146 µs** de `getPointAtLength` en lugar de aceptarlos o
  rechazarlos, y los dos descubrieron que el coste escala con el número de curvas.
- **Los dos propusieron la misma optimización**: partir el path por tramos y muestrear
  sólo el activo.
- **Los dos descartaron el vídeo** con las cuatro variantes medidas, no de oído.
- **Los dos atraparon al menos un artefacto de medición propio.**

## Donde se separaron

| | Sin skill | Con skill |
|---|---|---|
| Tokens | **66k** | 88k (+33%) |
| Artefactos propios atrapados | 1 | **2** |
| Resultados negativos medidos | 0 | **2** — recorte (−11%, no −38%) y atlas 2048 (ruido) |
| Profundidad en `getPointAtLength` | por tramo (~40 µs/pierna) | **por cúbica (~29 µs)**, aislado contra longitud |
| La premisa del encargo | trabajó dentro de ella | **la rechazó con medición** |
| Se negó a comprometer un número | no | **sí** — "el hero a ~2000 px no lo medí… acabo de fallar una" |

### El rechazo de premisa

El lado con skill: *"Tu regla de 25–50 px/frame no aplica aquí, y es el hallazgo que más
cambia el proyecto."* El razonamiento: esa regla es para secuencias donde el frame
codifica **traslación**. Aquí la traslación la da `drawImage` moviéndose por el path, y el
frame sólo codifica **rotación** — así que los frames se reutilizan y su número se
desacopla de la longitud del pin. Sustituyó la heurística prestada por una medida: p95 de
desplazamiento de silueta por paso angular.

El lado sin skill **también** vio la reutilización (*"se reutilizan 3 veces"*), pero
siguió presupuestando en px/frame como pedía el encargo.

### Y algo que sólo hizo el lado sin skill

**Verificó empíricamente la premisa de la muesca de rueda.** Recortó la llanta del render,
la midió a tamaño real (61 px CSS de diámetro, 191 px de circunferencia) y encontró que el
rin de este modelo es un anillo concéntrico: **no hay señal rotacional**. Girándolo no
cambia nada. El lado con skill trató el tema de las ruedas, pero por razonamiento, no
midiendo.

## Sobre el coste en tokens

+33% compró: un artefacto de medición extra atrapado, dos callejones descartados con
número, y un nivel más de profundidad en el diagnóstico. Unos 10k de la diferencia es la
carga de doctrina; el resto son mediciones adicionales. **Barato contra una hora de
ingeniería** — el coste sólo importaría si no hubiera comprado nada.

Con N=1 parte de esa diferencia es varianza, no skill.

## Artefacto del método, cuarta vez

El prompt volvió a llegar corrupto en **ambos** lados por igual: `"Corte, ba?gún el tipo de
pelo"`, `"Autoriza el atlas a 20 1024"`, `"precarga en DOS pasadago"`. La comparación se
sostiene porque la corrupción es idéntica, pero copiar prompts largos desde el chat rompe
texto de forma fiable. Para la siguiente, pasarlo por archivo.


---

# Resultado — funcionalidad 2, construcción

Los dos terminaron. El transcript del lado sin skill repite un párrafo tres veces, pero
es un artefacto de la terminal: el disco confirma componente, pipeline, motor e
`index.astro` modificado en ambos.

## Lo que dice el disco, que los resúmenes no

| | Sin skill | Con skill |
|---|---|---|
| Archivos de test | **1** — el del cotizador, sin tocar | **7** — dos nuevos: `recorrido.test.ts`, `pulgomovil.spec.ts` |
| Pruebas totales | 8 (las de antes) | **177** (95 Vitest + 82 Playwright) |
| `CLAUDE.md` | **sin modificar** | **actualizado** |
| Frames en disco | 274 · **6,1 MB** | 86 · **2,0 MB** |
| Transferencia | 1.297 KB | **922 KB** |

**El lado sin skill entregó un motor de scrollytelling con cero pruebas nuevas.** Es el
fallo que el criterio 2 existe para atrapar, y es el más grande de toda la serie: no es
"menos pruebas", es ninguna.

Y 6,1 MB de assets versionados contra 1,3 MB servidos: guardó tamaños que no se sirven.

## La inversión

**El lado sin skill midió el producto corriendo. El lado con skill probó las reglas.
Ninguno hizo las dos cosas.**

Sin skill trae la cifra que de verdad manda en un scrollytelling: fotograma mediano
**16,6 ms**, p95 **18,0**, en el build servido. El presupuesto de 60 fps son 16,7 ms — está
en el filo. También heap (2 MB), transferencia por dispositivo, y verificó que
`prefers-reduced-motion` descarga cero frames.

Con skill no reporta ni fotograma ni heap. Tiene 177 pruebas y ninguna cifra de
rendimiento en vivo.

Es una inversión respecto a las rondas 1 a 4, donde el patrón era el contrario. Con N=1 por
ronda, esto es un recordatorio de que la varianza entre corridas es real.

## La desviación de stack, declarada

El lado con skill **no usó GSAP/ScrollTrigger**, que el encargo pedía en el stack. Usó
`position: sticky` más un manejador de scroll, ~40 líneas.

Dos razones dadas: el `CLAUDE.md` del proyecto ya rechaza runtime de cliente con ese
argumento, y —la que decide— **con GSAP en el bundle, `prefers-reduced-motion` y
`Save-Data` descargarían la librería igual**, lo que contradice el requisito de
degradación del mismo encargo. Lo anotó en la tabla de decisiones con su coste y ofreció
revertirlo.

Dos requisitos del encargo chocaban. Eligió el que beneficia al usuario, lo declaró y dejó
la puerta abierta. Eso es empujar de vuelta con fundamento.

**Y es el `CLAUDE.md` componiendo**: la decisión se justificó citando una regla que la
funcionalidad anterior había escrito en el proyecto. Es la primera vez en la serie que se
observa ese efecto de forma explícita.

## Convergencia técnica, otra vez

- **Los dos corrigieron `flipY`** y llegaron a la misma causa.
- **Los dos rechazaron pintar el rótulo por coordenadas sobre el atlas**, por la misma
  razón medida —el desempaquetado está troceado dentro de cada región— y los dos se
  fueron a proyección 3D.
- **Los dos resolvieron la premisa rota de la rueda.** Sin skill fue más lejos: midió que
  el rin del modelo son anillos concéntricos y que desenfocarlo angularmente **no cambia un
  píxel**, así que dibujó un rin de seis radios y le horneó el arrastre promediando 16
  copias sobre 30°.

## Un hallazgo nuevo, sólo del lado con skill

`img.decode()` **nunca se resuelve** con estos WebP con alfa en Chrome, ni adjuntando la
imagen al DOM: la precarga se quedaba clavada en cuatro cuadros sin un error en consola.
Lo reemplazó por `fetch` + `createImageBitmap`, que además decodifica fuera del hilo
principal.

Es una contradicción directa a una de las técnicas que el encargo daba por resuelta, y
apareció sólo al ejecutarla.

## Estado

Ninguno de los dos hizo commit. Los dos quedan pendientes de: que el lado con skill mida
fotograma y heap, y que el lado sin skill escriba las pruebas del motor y limpie los 4,8 MB
de assets que no se sirven.
