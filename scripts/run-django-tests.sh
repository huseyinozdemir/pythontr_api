#!/usr/bin/env bash

# kod icerisinde herhangi bir dosya hata dondururse cık ve olusan hatayi döndur
set -e

# hangi dizinde olursak olalım uygulamamızın kok dizini uzerinden calismasi icin
cd "${0%/*}/.."

echo "Running unit test and flake 8 for Django Framework on Docker Container"
echo "............................."
docker-compose run -T --rm app sh -c "python manage.py test && flake8"
