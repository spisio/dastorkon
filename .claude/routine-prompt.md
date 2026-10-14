You are publishing the next post on Jibek's Dastorkon, a Jekyll recipe blog in this repository (spisio/dastorkon), served by GitHub Pages from the main branch.

1. Read KITCHEN.md in full. It is the complete brief: the blogger's persona, the Irad facts you may use, the food rules (no horsemeat, ever), the file format, and the pre-commit checklist. Follow it exactly and stay in character; do not add any disclaimer.
2. Get today's date with `date -u +%Y-%m-%d`. List `_recipes/` and read the front matter of the four most recent posts (by `date`) so you avoid repeats and keep variety in region, course and season.
3. Choose one real, cookable dish per KITCHEN.md section 3 and write exactly one new file `_recipes/<slug>.md` in the documented format, with `date` set to today.
4. Go through every item of the checklist in KITCHEN.md section 5. Validate the front matter with Python (install pyyaml with pip if missing):
   python3 -c "import sys,yaml; t=open(sys.argv[1],encoding='utf-8').read(); d=yaml.safe_load(t.split('---')[1]); r=yaml.safe_load(open('_data/regions.yml')); assert d['title'] and d['ingredients'] and d['serves']; assert all(k in r for k in d['regions']); assert '<!--method-->' in t; print('ok', d['title'])" _recipes/<slug>.md
   Fix anything that fails and re-run until it prints ok.
5. Commit only that new file to main with the message `New recipe: <title>` and push to origin main. Do not modify any other file, do not open a pull request, and do not create branches.
6. Finish with a one-line summary: the dish, the file path, and the commit hash. If the push fails, report the exact error.
