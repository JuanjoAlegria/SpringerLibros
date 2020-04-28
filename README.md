# SpringerLibros
Script en python para descargar libros de Springer liberados durante pandemia

## Preparación
Desde una consola:

```
git clone git@github.com:JuanjoAlegria/SpringerLibros.git
cd SpringerLibros
pip install -r requirements.txt
```

## Uso
Desde una consola, y en la carpeta SpringerLibros:
```
python script_libros.py --doc_links links.txt --doc_format {DOC_FORMAT}
```

`{DOC_FORMAT}` puede ser `pdf` o `epub`. El script tratará de descargar el documento en el formato elegido, y si no funciona,
probará con el otro formato.
