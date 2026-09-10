# Entorno de las pruebas

Sin esto, ningún número de la bitácora significa lo que parece.

## Lo más importante

**La baseline no es Claude a secas.** Las dos corridas de cada experimento se ejecutan
con **57 skills personales activas** más el plugin `swift-lsp`. La única diferencia entre
los lados es `dev-mentor`.

Esto mide **valor marginal sobre un montaje ya bueno**, que es la pregunta que un lector
técnico tiene de verdad: *"ya tengo mis skills, ¿esto me suma algo?"*. Una comparación
contra cero skills respondería una pregunta que nadie se hace, y además saldría
favorecida artificialmente.

## Las 57 skills activas en ambos lados

**Suite gstack (56):** `_gstack-command`, `autoplan`, `benchmark`, `benchmark-models`,
`browse`, `canary`, `careful`, `codex`, `connect-chrome`, `context-restore`,
`context-save`, `cso`, `design-consultation`, `design-html`, `design-review`,
`design-shotgun`, `devex-review`, `diagram`, `document-generate`, `document-release`,
`freeze`, `frontend-design`, `gstack`, `gstack-upgrade`, `guard`, `health`,
`investigate`, `ios-clean`, `ios-design-review`, `ios-fix`, `ios-qa`, `ios-sync`,
`land-and-deploy`, `landing-report`, `learn`, `make-pdf`, `office-hours`,
`open-gstack-browser`, `pair-agent`, `plan-ceo-review`, `plan-design-review`,
`plan-devex-review`, `plan-eng-review`, `plan-tune`, `qa`, `qa-only`, `retro`, `review`,
`scrape`, `setup-browser-cookies`, `setup-deploy`, `setup-gbrain`, `ship`, `skillify`,
`spec`, `sync-gbrain`, `unfreeze`

**Plugin:** `swift-lsp@claude-plugins-official`

Varias de esas se solapan con lo que hace `dev-mentor` — `review`, `health`, `qa`,
`plan-eng-review`, `design-review`, `document-generate`. Eso **endurece** la prueba: el
lado sin dev-mentor no está desarmado, tiene herramientas para casi todo lo que dev-mentor
promete.

## Constantes en ambos lados

| | |
|---|---|
| Modelo | Opus 5 (1M context), Claude Max |
| Claude Code | 2.1.243 – 2.1.265 según la corrida (anotado por experimento) |
| Modo de permisos | auto mode, idéntico en ambos lados |
| Flutter | 3.41.7 estable · Dart 3.11.5 |
| Prompt | literal, carácter por carácter, el mismo en ambos |
| Datos | locales, sin backend, sin autenticación, sin despliegue |

## Fuentes de ruido conocidas

- **Una corrida por lado.** La salida de un modelo varía. Un par es una anécdota;
  harían falta tres por lado para publicar cualquier tasa.
- **El prompt llegó corrupto** en dos experimentos: una regla perdió texto al copiarse.
  Idéntico en ambos lados, así que la comparación se sostiene — pero las dos corridas
  también estaban siendo probadas en cómo manejan un requisito roto, lo cual no era
  la intención.
- **Ninguno de los dos proyectos es un repositorio git**, así que las diferencias se
  midieron comparando el árbol antes y después, no con `git diff`.
- **La versión de la skill cambió entre corridas.** El experimento de Flutter se corrió
  con 0.1.x y se repitió con 0.2.0 después de corregir un fallo que la primera expuso.
  Ambas están registradas por separado.
