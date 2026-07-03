# ilyautov.github.io

User-site (корневой сайт GitHub Pages для `https://ilyautov.github.io/`).

Мини-визитка со ссылками на проекты. Держит:

- `yandex-verification` мета-тег для подтверждения хоста в Яндекс.Вебмастере;
- host-level `robots.txt` со ссылкой на sitemap проекта `humanizer-ru`.

Проектные сайты (например `humanizer-ru`) живут в своих репозиториях и
отдаются по `https://ilyautov.github.io/<repo>/` независимо от этого репо.

## Локальный просмотр

```
python3 -m http.server 8000
```

Чистый HTML5, без сборки, без внешних скриптов и трекеров.
