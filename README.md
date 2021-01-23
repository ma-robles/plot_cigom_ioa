# plot_cigom_ioa
Generación de figuras para cigom usando como "núcleo" el script map_plots.py (https://gitlab.com/hmedrano/scripts-modelos-cigom/).
De manera automática se genera la estructura(árbol) de almacenamiento requerido en la carpeta actual. 

## Sintaxis
plot_fig.py < nombre de la figura > < nombre del archivo .nc >
  * Nombre de la figura es el nombre usando la nomenclatura solicitada. Si la nomenclatura es incorrecta, el script arrojará un error.
  * Nombre del archivo .nc es el nombre (y ruta) del archivo de donde se obtendrán los datos para realizar las gráficas.
  
## Requerimientos
* matplotlib, netCDF4, cartopy, xarray (Los mismos que requiera map_plots.py)

## Ejemplos:

python3 plot_fig.py gom-unam-hycom-ioa-gom-phy-025_mensual_temperatura_promedio_0000m_M07.png climmensual_hycom_temp_07.nc

python3 plot_fig.py gom-unam-hycom-ioa-gom-phy-025_clim_temperatura_media_0000m.png climanual_hycom_temp_nc7.nc

Nota: en los ejemplos anteriores no se incluye la ruta de los archivos .nc, por lo que deberá ser agregada.
