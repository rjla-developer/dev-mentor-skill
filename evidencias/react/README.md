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
