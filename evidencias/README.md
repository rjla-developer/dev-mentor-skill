# Evidencias

Bitácora de las pruebas hechas sobre `stack-canon`. Todo lo que aquí se afirma tiene
una medición o un transcript detrás, y lo que no se midió está marcado como no medido.


> **Nota de nombre.** Los experimentos de este registro se corrieron cuando la skill se llamaba `dev-mentor`. El nombre cambió a `stack-canon` en 1.0.0, al recortar el alcance a los dos pilares que la evidencia sostiene. Los transcripts originales dicen `dev-mentor`; es la misma herramienta.

## Qué hay

| Archivo | Contiene |
|---|---|
| `entorno.md` | Las condiciones exactas de las pruebas. Léelo antes que nada: sin esto, ningún número de aquí significa lo que parece. |
| `brief-linkedin.md` | Documento de contexto para dar a un chat sin historial, con los ángulos de publicación y los activos disponibles. |
| `capturas/` | Imágenes y video de las corridas. |
| `../docs/DEMO-COMPARISON.md` | El registro técnico completo, corrida por corrida, con las predicciones fallidas. |

## La regla de esta carpeta

**Las derrotas se publican con el mismo detalle que las victorias.** No es modestia: es
lo único que hace creíbles las victorias. Un lector que ve tres predicciones fallidas
admitidas te cree la cuarta que sí salió.

Hasta hoy se han publicado cuatro fallos propios:

1. El plugin cargaba sin su hook, y el tope de `CLAUDE.md` quedaba sin aplicar.
2. La doctrina nunca decía "corre la app", así que una corrida entregó 68 pruebas
   verdes y un encabezado encimado en pantalla.
3. El mismo prompt se comportaba de dos maneras distintas porque nombrar un stack
   sacaba a la skill de modo `guided`.
4. Una corrida reportó "ninguna señal cruzó umbral" sin haber contado: su propio
   `build()` estaba en 103 líneas contra un umbral de 100.

Los cuatro se corrigieron. Los cuatro salieron de una prueba, no de una revisión.

## Cómo añadir un experimento

1. Anota el entorno en `entorno.md` si cambió algo.
2. Corre los dos lados con **el mismo prompt literal** y el mismo modo de permisos.
3. Mide antes y después. Sin medición no entra.
4. Escribe qué esperabas que pasara **antes** de mirar el resultado, y publícalo aunque
   falle.
