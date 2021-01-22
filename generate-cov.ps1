#!/bin/bash
pytest --cov-report term --cov=environment --cov=extractor --cov-report term-missing --cov=loader --cov=rdf -cov=turtleParser
