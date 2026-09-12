# De Pocas Pulgas — registro vigente

La única evidencia que sirve para juzgar **`stack-canon` 1.0**. Se mide contra los tres
criterios que la herramienta declara cumplir, y contra nada más.

Lo anterior a 1.0 está en [`../historico-0.x/`](../historico-0.x/) y midió una herramienta
distinta, con siete capacidades que ya no existen.

## El método

Misma app construida dos veces desde el mismo prompt literal, y después la misma
funcionalidad añadida a las dos. Una sola variable: `stack-canon` habilitado o no.

**La baseline no es Claude a secas.** Los dos lados corren con las mismas **57 skills
personales** activas (ver [`../entorno.md`](../entorno.md)). Esto mide valor marginal sobre
un montaje ya bueno, que es la pregunta que un lector técnico se hace de verdad.

- **Funcionalidad 1** — el sitio: siete servicios, cotizador con cinco reglas de borde
  exacto, cierre por WhatsApp, páginas para el buscador.
- **Funcionalidad 2** — un hero de scrollytelling: la van del negocio bajando en zigzag
  sobre canvas, 41–45 cuadros renderizados desde un `.glb`.

Stack: Astro. El catálogo tiene entrada `astro` verificada contra `docs.astro.build`,
escrita **antes** del experimento.

---

# Criterio 1 — `CLAUDE.md` creado y de calidad

| | Sin skill | Con skill |
|---|---|---|
| Tras la funcionalidad 1 | **no existe** | **115 líneas, escrito antes del código** |
| Tras la funcionalidad 2 | **no existe** | **208 líneas** |

**Veredicto: la skill, sin discusión.** Es el único de los tres criterios binario, y el
único que no se ha movido en ninguna comparación de toda la serie.

## Lo que contiene, que es lo que decide la "calidad"

Escrito **antes del código**, con el motivo dicho: *"para que las reglas estructurales
queden fijadas"*. Eso cambia la naturaleza del archivo — pasa de describir lo que se hizo a
restringir lo que se va a hacer.

Dentro: los bordes exactos de cada regla de negocio, las decisiones forzadas con su coste,
y las trampas que se pagaron durante el trabajo. Entre ellas las tres de medir memoria en
Chromium (sumar todos los procesos, mediana de varias lecturas, comparar sólo contra el
mismo recorrido de scroll) y la aritmética RGBA que falló por 25×.

## El efecto que sólo se ve con dos funcionalidades

En la funcionalidad 2, la skill se desvió del stack pedido —no usó GSAP— y lo justificó
así: ***"tu `CLAUDE.md` ya rechaza runtime de cliente con ese mismo argumento"***.

**Esa regla la escribió la funcionalidad 1.** Es una decisión anterior restringiendo una
posterior sin que nadie la recordara. Es el argumento entero del criterio 1, y hasta esa
corrida sólo existía como teoría.

---

# Criterio 2 — pruebas por funcionalidad que verifiquen calidad de producto

| | Sin skill | Con skill |
|---|---|---|
| Tras la funcionalidad 1 | 8 casos | **97** |
| Tras la funcionalidad 2 | 54 casos · 653 líneas | **127 casos · 1.281 líneas** |
| Archivos de test | 3 | **9** |

**Veredicto: la skill en volumen y en mecanismo. La baseline tuvo el mejor hallazgo
individual.**

## Lo que sólo hizo la skill

**Usó la Container API** — el mecanismo que el propio equipo de Astro publica para probar
componentes `.astro` renderizándolos a string.

**Probó contra el build de producción**, que es la regla que Astro publica textualmente:
*"Run your tests against your production code to more closely resemble your live, deployed
site."*

**Probó que el script hidrata.** Es la trampa registrada del stack: un componente sin
`client:*` produce **HTML idéntico** a uno que sí lo tiene, así que toda aserción de markup
pasa mientras el botón no hace nada. Sólo un navegador lo atrapa. 52 pruebas de Playwright
escritas con ese motivo explícito.

**Encontró cinco defectos que 97 pruebas verdes no veían**, al mirar la pantalla: el
`<fieldset>` desbordando a 320px, `/cotizar/` sin `h1`, el héroe 170px desalineado, la
burbuja de WhatsApp tapando un botón, y un botón deshabilitado a 1.4:1 de contraste — que
se lee como error, no como instrucción. La baseline encontró dos.

**Y midió el rendimiento con instrumentación real**: `mouse.wheel` en vez de `scrollTo`
—*"saltar el scroll se salta justo el trabajo que se quiere medir"*—, parcheando la
callback de `requestAnimationFrame`, con CPU a 4× y 6× y 219–233 muestras por escenario.
Ni un fotograma por encima del presupuesto de 16,7 ms en ninguno de los cuatro.

Corrigió además un error propio de 25×: sospechó un problema de memoria (121,6 MB sobre el
papel), el primer A/B pareció confirmarlo (89 contra 200 MB), y al aislarlo los deltas
salían negativos contra su propia línea base. Chrome no guarda esos bitmaps como RGBA
residente; el coste real son ~5 MB.

Y se negó a dar un número: *"el intervalo entre fotogramas no te lo doy como prueba: sale
16.7 clavado, que es la cadencia sintética de headless, no 60 fps en un teléfono."*

## Lo que la baseline hizo mejor

**Entregó el hero con cero pruebas** — hubo que pedírselas. Pero al escribirlas, **una
falló de verdad**: 180° no son un número entero de cuadros de 8° (son 22,5), así que las
paradas pares caen en 256° en vez de su pose nominal de 252°. **Cuatro grados de desvío
sistemático**, invisible a ojo, ahora documentado.

Es el mejor argumento del criterio 2 de toda la serie, y lo produjo el otro lado: **las
pruebas no se escriben para que pasen, se escriben para que una falle.**

---

# Criterio 3 — arquitectura y recomendaciones del equipo de la tecnología

| | Sin skill | Con skill |
|---|---|---|
| Consultó doctrina publicada | no | **sí, descargada en vivo** |
| Declaró decisiones con su coste | no | **sí, tres en la funcionalidad 1** |
| Assets servidos | 2,1 MB | **1,0 MB** |
| Transferencia del hero | 1.297 KB | **922 KB** |
| Líneas de `src/` | 3.191 | **2.948** |
| **Función más larga** | **197** | **258** |
| **Archivo más grande** | **545** | **627** |

**Veredicto: mixto, y hay que decirlo así.**

## A favor de la skill

Trajo el registro en vivo y declaró tres decisiones forzadas con su coste: salida
estática (el default que Astro recomienda hasta estar seguro de necesitar otra cosa),
**ningún framework de UI en las islas** —*"React habría costado ~45 KB de runtime para unos
steppers"*— y la convención de carpetas documentada, admitiendo que reparte una feature en
tres sitios.

Y un hallazgo que el catálogo carga precisamente para esto: **las 22 skills de la
organización `withastro` son herramientas de mantenedor**, no para quien construye sitios.
La que se llama `astro-developer` dice literalmente *"developing in the Astro monorepo"*.
Los agregadores las listan como "skills de Astro", que es como alguien acaba instalando
herramientas de contribuidor creyendo que le van a ayudar.

## En contra de la skill

**La baseline ganó las dos métricas de forma del código.** Y no por poco: 258 líneas en una
sola función es el doble de cualquier umbral razonable.

Peor: esa función vive **dentro del `<script>` del componente**. La skill separó bien las
*reglas* (`src/lib/recorrido.ts`) y dejó el motor pegado a la pantalla, mientras la
baseline sacó el suyo a `src/scripts/` como archivos aparte.

---

# Lo que no está probado

- **Una corrida por lado.** La salida de un modelo varía. Es una anécdota, no una
  medición; harían falta tres por lado para publicar cualquier tasa.
- **Nadie evaluó la experiencia** de los dos sitios, sólo el código y las métricas.
- **El diseño es prácticamente idéntico** en ambos. La herramienta tiene dos pilares y
  ninguno es diseño; no lo prometía y no lo entrega.
- **Ocho de los nueve stacks del catálogo** nunca se han probado en una corrida.

# Ruido conocido del método

- **Versiones distintas de Astro** en la funcionalidad 1: 5.18.2 sin skill contra 7.3.2 con
  skill. Ningún prompt fijaba versión. Se corrigió en la funcionalidad 2, donde ambos
  corrieron 7.3.2.
- **El prompt llegó corrupto** en las dos funcionalidades, idéntico en ambos lados —
  copiarlo desde el chat rompe texto de forma fiable. Los dos lo detectaron y lo
  resolvieron. Para lo siguiente, pasarlo por archivo.
