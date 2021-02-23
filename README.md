# plot_cigom_ioa
Generación de figuras para cigom usando como "núcleo" el script map_plots.py (https://gitlab.com/hmedrano/scripts-modelos-cigom/).
De manera automática se genera la estructura(árbol) de almacenamiento requerido en la carpeta actual. 

  
## Requerimientos
* matplotlib, netCDF4, cartopy, xarray (Los mismos que requiera map_plots.py)

## Sintaxis
~~~
usage: plot_fig.py [-h] [--tipo {clim,mensual,estacional}]
                   [--var_name {capa-mezcla,nivel-mar,temperatura,salinidad,viento,nitratos,carbono,clorofila}]
                   [--var_name_title VAR_NAME_TITLE] [--var_alias VAR_ALIAS]
                   [--stat {media,desviacion-estandar,maximos,minimos,promedio}]
                   [--filename FILENAME] [--ID ID] [--level LEVEL] [--mes MES]
                   [--root ROOT] [--cmap CMAP] [--vmin VMIN] [--vmax VMAX]
                   [--title TITLE] [--xcomp XCOMP] [--xfilename XFILENAME]
                   [--ycomp YCOMP] [--yfilename YFILENAME] [--lat LAT]
                   [--long LONG] [--depth DEPTH] [--units UNITS]
                   [--modelo MODELO] [-i CONFIG_FILE]

optional arguments:
  -h, --help            show this help message and exit
  --tipo {clim,mensual,estacional}
                        Tipo de figura
  --var_name {capa-mezcla,nivel-mar,temperatura,salinidad,viento,nitratos,carbono,clorofila}
                        Nombre de la variable
  --var_name_title VAR_NAME_TITLE
                        Nombre de la variable que se colocará en el título
  --var_alias VAR_ALIAS
                        Nombre de la variable en el archivo
  --stat {media,desviacion-estandar,maximos,minimos,promedio}
                        Operación estadística aplicada
  --filename FILENAME   Nombre del archivo
  --ID ID               Clave del modelo
  --level LEVEL         Profundidad en m
  --mes MES             Número del mes
  --root ROOT           Path de la carpeta raíz
  --cmap CMAP           Paleta de la barra de colores
  --vmin VMIN           Valor mínimo en la barra de colores
  --vmax VMAX           Valor máximo en la barra de colores
  --title TITLE         Título en la gráfica
  --xcomp XCOMP         Componente X en variables vectoriales
  --xfilename XFILENAME
                        Archivo con la componente X
  --ycomp YCOMP         Componente Y en variables vectoriales
  --yfilename YFILENAME
                        Archivo con la componente Y
  --lat LAT             Nombre de la variable de latitud
  --long LONG           Nombre de la variable de longitud
  --depth DEPTH         Nombre de la variable de profundidad
  --units UNITS         Especifica unidades de la variable
  --modelo MODELO       Especifica el modelo usado
  -i CONFIG_FILE, --input CONFIG_FILE
                        Archivo(s) de entrada
~~~
## Ejemplos:

python3 plot_fig.py -i mensual.inf


