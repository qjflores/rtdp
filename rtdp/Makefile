build:
	docker build --target=dev-rtdp --tag dev-rtdp:latest .

bash:
	docker-compose run --rm publisher /bin/bash

test:
	docker-compose run --rm consumer /opt/rtdp/scripts/pytest.sh

lint:
	docker-compose run --rm consumer /opt/rtpd/scripts/pylint.sh