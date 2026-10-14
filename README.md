# Jibek's Dastorkon

Recipe blog: https://spisio.github.io/dastorkon/

A Jekyll site built by GitHub Pages from the `main` branch. Nothing to install to publish: push a change and Pages rebuilds.

## Adding a recipe

Add one Markdown file to `_recipes/`. The format, voice and rules are in [KITCHEN.md](KITCHEN.md). A scheduled Claude routine follows that guide and adds a new recipe every Wednesday and Sunday.

## Layout

- `_recipes/` one file per recipe
- `_data/regions.yml` the region filters and badge labels
- `_layouts/` page templates (`default.html`, `recipe.html`)
- `index.html` home page and recipe index
- `assets/` CSS, JS and the star icon
- RSS feed: `/feed/recipes.xml`

## Previewing locally (optional)

Needs Ruby. Then:

```
gem install bundler jekyll
jekyll serve --baseurl /dastorkon
```
