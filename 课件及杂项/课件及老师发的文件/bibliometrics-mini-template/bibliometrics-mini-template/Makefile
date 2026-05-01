.PHONY: sample test fetch run wos

sample:
	PYTHONPATH=src python -m bmmini.pipeline --config config/query.yaml --use-sample

fetch:
	PYTHONPATH=src python -m bmmini.fetch_openalex --config config/query.yaml

run:
	PYTHONPATH=src python -m bmmini.pipeline --config config/query.yaml

wos:
	PYTHONPATH=src python -m bmmini.pipeline --config config/query.yaml --use-wos

test:
	PYTHONPATH=src pytest -q
