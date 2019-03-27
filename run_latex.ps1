docker pull miktex/miktex
docker volume create --name miktex
docker run -ti -v miktex:/miktex/.miktex -v "${PWD}:/miktex/work" miktex/miktex pdflatex main.tex

