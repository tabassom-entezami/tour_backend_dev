# Use bash as default shell
SHELL := /bin/bash
IMAGES := tour_gateway \
          tour_processor


# build docker images
build:
	for image in $(IMAGES) ; do make -C $$image build-image; done

# Run unit tests for all projects
unit-test:
	@for image in $(IMAGES); do \
		if [[ "$$image" == "tour_gateway" ]]; then \
			continue; \
		fi; \
		echo "### RUNNING TESTS FOR $$image"; \
		docker-compose --log-level ERROR run --no-deps --rm -T $${image##tour_} pytest -q; \
	done
