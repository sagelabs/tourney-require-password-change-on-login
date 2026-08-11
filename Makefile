lint:
	ruff check --select E,F,W,B,C4,I --ignore E402,E501,E712,B904,B905,I001 --exclude=Tourney/uploads Tourney/ migrations/ tests/
	isort --profile=black --check-only --skip=Tourney/uploads --skip-glob **/node_modules Tourney/ tests/
	yarn --cwd Tourney/themes/admin lint
	black --check --diff --exclude=Tourney/uploads --exclude=node_modules .
	prettier --check 'Tourney/themes/*/assets/**/*'
	prettier --check '**/*.md'

format:
	isort --profile=black --skip=Tourney/uploads --skip-glob **/node_modules Tourney/ tests/
	black --exclude=Tourney/uploads --exclude=node_modules .
	prettier --write 'Tourney/themes/**/assets/**/*'
	prettier --write '**/*.md'

test:
	pytest -rf --cov=Tourney --cov-context=test --cov-report=xml \
		--ignore-glob="**/node_modules/" \
		--ignore=node_modules/ \
		-W ignore::sqlalchemy.exc.SADeprecationWarning \
		-W ignore::sqlalchemy.exc.SAWarning \
		-n auto
	bandit -r Tourney -x Tourney/uploads --skip B105,B322
	pipdeptree

coverage:
	coverage html --show-contexts

serve:
	python serve.py

shell:
	python manage.py shell

translations-init:
	# make translations-init lang=af
	pybabel init -i messages.pot -d Tourney/translations -l $(lang)

translations-extract:
	pybabel extract -F babel.cfg -k lazy_gettext -k _l -o messages.pot .

translations-update:
	pybabel update --ignore-obsolete -i messages.pot -d Tourney/translations

translations-compile:
	pybabel compile -f -d Tourney/translations

translations-lint:
	dennis-cmd lint Tourney/translations
