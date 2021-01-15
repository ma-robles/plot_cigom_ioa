import numpy as np
import matplotlib
import matplotlib.pyplot as plt 
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.colors as colors

def map_pcolor(loncoords, latcoords, zvar, title='',
                                           colorbar_label='', 
                                           cmap='viridis', 
                                           plot_land=True, 
                                           plot_bathy=True, 
                                           land_dataset='GSHHS', 
                                           tickBins=4,
                                           extent=None,
                                           vmin=None,
                                           vmax=None,
                                           norm=None,
                                           colorbar_orientation='horizontal',
                                           crs=ccrs.PlateCarree()):
    """
       -
       Crea un gráfico tipo pcolormesh sobre un mapa, agrega linea de costas, lineas 
       batimetricas, marcadores de la malla lat,lon y devuelve la el objeto figura de 
       matplotlib

       Recibe variables de coordenadas longitud, latitud y magnitud a graficar

       Parametros requeridos:
        loncoords            - Arreglo ndarray 1D o 2D con variable de coordenadas 
                               longitud
        latcoords            - Arreglo ndarray 1D o 2D con variable de coordenadas 
                               latitud
        zvar                 - Arreglo ndarray 2D con variable a graficar.

       Parametros opcionales:
        title                - Titulo del plot
        colorbar_label       - Etiqueta para la barra de color 
        cmap                 - Estilo de la barra de color, los estilos disponibles se pueden 
                               consultar en https://matplotlib.org/3.3.3/tutorials/colors/colormaps.html
        plot_land            - Bandera para graficar tierra
        plot_bathy           - Bandera para graficar lineas batimetricas
        land_dataset         - Fuente de la cual seleccionar los poligonos de costa, las opciones 
                               posibles son: NaturalEarth y GSHHS
        tickBins             - Número de marcadores de malla lat,lon a incluir.
        extent               - Lista con 4 elementos para definir el dominio del plot 
                               [lonmin, lonmax, latmin, latmax]
        vmin                 - Valor mínimo para escala de color
        vmax                 - Valor máximo para escala de color
        norm                 - Recibe instancia Normalize para el mapeo de escala de color
        colorbar_orientation - Orientación de la barra de color
        crs                  - Proyección, ver 
                               https://scitools.org.uk/cartopy/docs/v0.15/crs/projections.html


        La función regresa el eje matplotlib del grafico y la figura.
    """

    # Global
    matplotlib.rcParams['font.family'] = "serif"
    fig = plt.figure(figsize=(8, 8))
    
    ax = plt.subplot(111, projection=crs)
    plt.title(title)

    colormeshObj = ax.pcolormesh(loncoords, latcoords, np.squeeze(zvar), cmap=plt.get_cmap(cmap), norm=norm, vmin=vmin, vmax=vmax)

    # Colorbar
    # Las siguientes dos lineas se encargan de agregar un eje del lado derecho de la figura
    # para depositar dentro de este eje la barra de color. 
    # Con este metodo aseguramos que la barra de color vertical sea de la misma altura que el
    # plot de pcolormesh
    # Ref: https://stackoverflow.com/questions/18195758/set-matplotlib-colorbar-size-to-match-graph
    if colorbar_orientation == 'vertical':
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.08, axes_class=matplotlib.pyplot.Axes)    
        plt.colorbar(colormeshObj, label=colorbar_label, cax=cax)
    else:
        plt.colorbar(colormeshObj, label=colorbar_label, orientation='horizontal', pad=0.08)

    #    
    addCoastlines(ax, plot_land, land_dataset)
    addBathy(ax, plot_bathy)
    addCoordinateTicks(ax, loncoords, latcoords, tickBins)

    #
    if extent is None:
        ax.set_extent([loncoords.min(), loncoords.max(), latcoords.min(), latcoords.max()], crs=crs)
    else:
        ax.set_extent(extent, crs=crs)
    #
    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(8,8)    
    return ax, fig


# Plots
def map_quiver(loncoords, latcoords, uvar, vvar,
                                           title='',
                                           slice_interval=8,
                                           quiverkeysize=None,
                                           quiverkeyunits='m s$^{-1}$)',
                                           plot_land=True, 
                                           plot_bathy=True, 
                                           land_dataset='GSHHS', 
                                           tickBins=4,
                                           extent=None,
                                           crs=ccrs.PlateCarree()):
    """
       - 
       Crea un gráfico tipo quiver y quiverkey sobre un mapa, agrega linea de costas, lineas 
       batimetricas, marcadores de la malla lat,lon y devuelve la el objeto figura de 
       matplotlib

       Recibe variables de coordenadas longitud, latitud componente U y V a graficar
       Parametros requeridos:
        loncoords            - Arreglo ndarray 1D o 2D con variable de coordenadas 
                               longitud
        latcoords            - Arreglo ndarray 1D o 2D con variable de coordenadas 
                               latitud
        uvar                 - Arreglo ndarray 2D con el los componentes U del mapa de
                               vectores
        vvar                 - Arreglo ndarray 2D con el los componentes V del mapa de
                               vectores                               

       Parametros opcionales:
        title          - titulo del plot
        slice_interval - Número de puntos de malla a omitir en el graficado de vectores 
                         de dirección
        quiverkeysize  - Tamaño del vector de referencia que se usa en quiverkey
        quiverkeyunits - Etiqueta para el vector de referencia
        plot_land      - Bandera para gráficar tierra
        plot_bathy     - Bandera para gráficar lineas batimetricas
        land_dataset   - Fuente de la cual seleccionar los poligonos de costa, las 
                         opciones posibles son: NaturalEarth y GSHHS
        tickBins       - Numero de marcadores de malla lat,lon a incluir.
        extent         - Lista con 4 elementos para definir el dominio del plot 
                         [lonmin, lonmax, latmin, latmax]
        crs            - Proyección, ver 
                         https://scitools.org.uk/cartopy/docs/v0.15/crs/projections.html
    """                                           
        
    # Global
    matplotlib.rcParams['font.family'] = "serif"
    #

    fig = plt.figure(figsize=(8, 8))
    ax = plt.subplot(111, projection=crs)
    plt.title(title)

    # Contenido grafico
    add_quiverPlot(ax, loncoords, latcoords, uvar, vvar, crs, 
                                                         slice_interval=slice_interval, 
                                                         quiverkeysize=quiverkeysize, 
                                                         quiverkeyunits=quiverkeyunits)
    addCoastlines(ax, plot_land, land_dataset)
    addBathy(ax, plot_bathy)
    addCoordinateTicks(ax, loncoords, latcoords, tickBins, crs=crs)

    # 
    if extent is None:
        ax.set_extent([loncoords.min(), loncoords.max(), latcoords.min(), latcoords.max()], crs=crs)
    else:
        ax.set_extent(extent, crs=crs)    

    #
    fig = matplotlib.pyplot.gcf()
    fig.set_size_inches(8,8)    
    return ax, fig


def add_quiverPlot(ax, xx, yy, u, v, crs=ccrs.PlateCarree(), slice_interval=8, quiverkeysize=None, quiverkeyunits='m s$^{-1}$)'):
    """
     Agrega un grafico tipo quiver y quiverkey al eje 'ax'
    """
    # El slice skip sirve para reducir el numero de flechas de vectores que se muestran en el plot
    # omitiendo elementos con un salto del factor 'slice_interval'
    # Este numero puede variar dependiendo de la resolución de las variables uvar, vvar
    skip = slice(None, None, slice_interval)
    quiverObj = ax.quiver(xx[skip], yy[skip], u[skip,skip], v[skip,skip], transform=crs)

    # Calcular el tamano de quiverkey
    if quiverkeysize is None:
        speed = np.sqrt(np.power(u,2) + np.power(v,2))
        quiverkeysize = np.round(np.nanmax(speed))/2.0

    plt.quiverkey(quiverObj, 0.55, -0.08, quiverkeysize, '(' + str(quiverkeysize) + ' ' + quiverkeyunits,
                   labelpos='W',
                   transform=crs,
                   color='black')




# Utils

def addCoastlines(ax, plot_land=True, land_dataset='GSHHS'):
    """
     Agrega lineas de costas y poligonos de tierra, al grafico de cartopy. Los datos son consultados de los 
     datasets que hospedan NaturalEarth o GSHHS, este ultimo teniendo los poligonos de costa con mas 
     resolución. 
     Nota: La primera vez que se solicita agregar lineas de costa puede tomar algunos minutos
           pues hace la descarga de los datasets mundiales.
    """
    # CFeature Coastlines, and land HighRes
    if plot_land:
        if land_dataset=='GSHHS':
            ax.add_feature(cfeature.GSHHSFeature(scale='full', levels=[1], linewidth=0.25, edgecolor='black', facecolor='lightgray') )
        elif land_dataset=='NaturalEarth':
            ax.add_feature(cfeature.NaturalEarthFeature('physical', 'land', '10m', edgecolor='face', facecolor='lightgray'))
        else:
            ax.coastlines(resolution='10m', color='black', linewidth=0.5)

def addBathy(ax, plot_bathy=True):
    """
     Agrega lineas batimetricas al grafico de cartopy. Los datos son consultados
     de los datasets batimetricos que hospeda NaturalEarth https://www.naturalearthdata.com/downloads/10m-physical-vectors/10m-bathymetry/
    """
    # Bathy
    if plot_bathy:
        ax.add_feature(cfeature.NaturalEarthFeature(name='bathymetry_K_200',  scale='10m', category='physical',linewidth=0.5, edgecolor='gray', facecolor='None', label='etiqueta'))
        ax.add_feature(cfeature.NaturalEarthFeature(name='bathymetry_J_1000', scale='10m', category='physical',linewidth=0.5, edgecolor='gray', facecolor='None', label='etiqueta'))
        ax.add_feature(cfeature.NaturalEarthFeature(name='bathymetry_I_2000', scale='10m', category='physical',linewidth=0.5, edgecolor='gray', facecolor='None', label='etiqueta'))
        ax.add_feature(cfeature.NaturalEarthFeature(name='bathymetry_H_3000', scale='10m', category='physical',linewidth=0.5, edgecolor='gray', facecolor='None', label='etiqueta'))
        ax.add_feature(cfeature.NaturalEarthFeature(name='bathymetry_G_4000', scale='10m', category='physical',linewidth=0.5, edgecolor='gray', facecolor='None', label='etiqueta'))
        ax.add_feature(cfeature.NaturalEarthFeature(name='bathymetry_F_5000', scale='10m', category='physical',linewidth=0.5, edgecolor='gray', facecolor='None', label='etiqueta'))

def addCoordinateTicks(ax, loncoords, latcoords, tickBins=4, decimals=1, crs=ccrs.PlateCarree()):
    """
     Agrega etiquetas de coordenadas para latitud, longitud.
    """
    #
    yticksBins=tickBins
    xticksBins=tickBins
    ax.set_yticks(np.round(np.linspace(latcoords.min(), latcoords.max(), yticksBins), decimals=decimals), crs=crs)
    ax.yaxis.set_major_formatter(LATITUDE_FORMATTER)
    for tick in ax.get_xticklabels():
        tick.set_fontfamily("serif")

    ax.set_xticks(np.round(np.linspace(loncoords.min(), loncoords.max(), xticksBins), decimals=decimals), crs=crs)
    ax.xaxis.set_major_formatter(LONGITUDE_FORMATTER)
    for tick in ax.get_yticklabels():
        tick.set_fontfamily("serif")  