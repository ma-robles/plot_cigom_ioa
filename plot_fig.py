'''
genera las figuras para el proyecto CIGOM
requiere:
    -figname. nombre de la figura de acuerdo a la nomenclatura requerida
    -ifilename. nombre y ruta del archivo donde se encuentran los datos
'''
import os
import sys
import numpy as np
import netCDF4 as nc
from map_plots import map_pcolor, map_quiver, add_quiverPlot
import json
import argparse as ap
from configparser import ConfigParser
import shlex

def parse_name(figname):
    '''
    comprueba estructura del nombre de figura y regresa valores
    '''
    fig_dic={
            'tipo':["clim","mensual","estacional"],
            'var':["capa-mezcla",
                "nivel-mar",
                "temperatura",
                "salinidad",
                #"corrientes-vectores", 
                "velocidad", 
                "nitratos", 
                "carbono" ,
                "clorofila",
                ],
            'stat':["media",
                "desviacion-estandar",
                "maximos",
                "minimos",
                "promedio",
                ] ,
            'estacion':["invierno",
                "primavera",
                "otoño",
                "verano",
                ],
            }
    info_dic={
            #componentes del nombre para tipo climatológico
            'clim':['id','tipo','var','stat','depth',],
            #componentes del nombre para tipo mensual
            'mensual':['id','tipo', 'var', 'stat','depth','mes' ],
            #componentes del nombre para tipo estacional
            'estacional':['id','tipo', 'var', 'stat','estacion','depth' ],
            }


    split_name=figname.split('_')
    if len(split_name)<5:
        return 1
    cmp_struct=info_dic[split_name[1]];
    compo={}
    for i in range(len(cmp_struct)):
        #id
        if i==0:
            compo[cmp_struct[i]]=split_name[i]
        elif cmp_struct[i]=='depth': 
            val=split_name[i].split('m')
            if len(val)!=2 and len(val)!=1:
                return 1
            if len(val)==1:
                compo[cmp_struct[i]]=int(-1)
                split_name.append(split_name[-1])
            else:
                compo[cmp_struct[i]]=int(val[0])
        elif cmp_struct[i]=='mes':
            val=split_name[i].split('M')
            if len(val)!=2:
                return 1
            compo[cmp_struct[i]]=int(val[1][0:2])
        else:
            if split_name[i] in fig_dic[cmp_struct[i]]:
                compo[cmp_struct[i]]=split_name[i]
            else:
                return 1
    return compo

def create_tree(struct_val):
    path='Figuras/'
    path+=struct_val.tipo+'/'
    path+=struct_val.var_name+'/'
    path+=struct_val.stat+'/'
    os.makedirs(path,exist_ok=True)
    return(path)

def parse_units(units):
    if units=="degC":
        return "°C"
    else:
        return units

def plot(args):
    path=os.path.join(create_tree(args),args.figname)
    print(path)
    #define names in netCDF file
    var_names={
            "capa-mezcla":"CapaMezcla",
            "nivel-mar":"ssh",
            "temperatura":"pot_temp",
            "salinidad":"salinity",
            #"corrientes-vectores", 
            "velocidad":"speed", 
            "nitratos":"", 
            "carbono":"",
            "clorofila":"",
            }
    month={
            1:'Enero',
            2:'Febrero',
            3:'Marzo',
            4:'Abril',
            5:'Mayo',
            6:'Junio',
            7:'Julio',
            8:'Agosto',
            9:'Septiembre',
            10:'Octubre',
            11:'Noviembre',
            12:'Diciembre',
            }
    title=args.stat
    title=title[0].upper()+title[1:]
    if args.stat=='media':
        title=''
    if args.tipo=='mensual':
        title+=' mensual de la '
    elif args.tipo=='clim':
        title+='Climatología (1992-2012) de la '
    title+=args.var_name
    if args.depth!=None:
        title+=' a '+str(args.depth)+' m '
    if args.var_alias!=None:
        var_name=args.var_alias
    else:
        var_name=args.var_name
    with nc.Dataset(args.filename, 'r') as root:
        if args.depth!=None:
            z=root.variables['Depth'][:]
            idepth=np.argwhere(z==args.depth)[0][0]
            var=root.variables[var_name][0][idepth]
        else:
            var=root.variables[var_name][0]
        lon=root.variables[args.long][:]
        lat=root.variables[args.lat][:]
        #time=nc.num2date(root.variables['time'][:], root.variables['time'].units)
        if args.units==None:
            units=root.variables[args.units].units
        else:
            units=args.units

    units='['+units+']'
    title+=units
    title+=' Modelo '+args.modelo
    print(title)

    ax, figure = map_pcolor(lon, lat, var,
            title=title,
            tickBins={
                'x':[-98,-95,-92,-89,-86,-83,-80,-77],
                'y':[18,20,22,24,26,28,30,32],
                },
            cmap=args.cmap,
            plot_land=True,
            vmin=args.vmin,
            vmax=args.vmax)
    if args.tipo=='mensual':
        ax.annotate(month[args.mes],xy=(0.02,0.94), xycoords='axes fraction')
    figure.savefig(path, bbox_inches='tight', dpi=200)

#parsing args
parser= ap.ArgumentParser()
group=parser.add_mutually_exclusive_group()
parser.add_argument("--tipo", help="Tipo de figura",
        choices=["clim","mensual","estacional"],
        )
group.add_argument("--var_name", help="Nombre de la variable",
        choices=["capa-mezcla","nivel-mar", "temperatura", "salinidad", "viento",
        "nitratos","carbono","clorofila"],
        )
parser.add_argument("--var_alias", help="Nombre de la variable en el archivo")
parser.add_argument("--stat", help="Operación estadística aplicada",
        choices=["media","desviacion-estandar","maximos","minimos","promedio"],
        )
parser.add_argument("--filename", help="Nombre del archivo")
parser.add_argument("--ID", help="Clave del modelo",
        default="gom-unam-hycom-ioa-gom-phy-025",
        )
parser.add_argument("--depth", type=int, help="Profundidad en m")
parser.add_argument("--mes", type=int, help="Número del mes")
parser.add_argument("--root", help="Path de la carpeta raíz")
parser.add_argument("--cmap", help="Paleta de la barra de colores")
parser.add_argument("--vmin", type=float, help="Valor mínimo en la barra de colores")
parser.add_argument("--vmax", type=float, help="Valor máximo en la barra de colores")
parser.add_argument("--title", help="Título en la gráfica")
parser.add_argument("--xcomp", help="Componente X en variables vectoriales")
parser.add_argument("--xfilename", help="Archivo con la componente X")
parser.add_argument("--ycomp", help="Componente Y en variables vectoriales")
parser.add_argument("--yfilename", help="Archivo con la componente Y")
parser.add_argument("--lat", default="latitude", help="Nombre de la variable de latitud")
parser.add_argument("--long", default="longitude",help="Nombre de la variable de longitud")
parser.add_argument("--units", help="Especifica unidades de la variable")
parser.add_argument("--modelo", help="Especifica el modelo usado")
group.add_argument('-i',"--input", help="Archivo(s) de entrada", dest='config_file')

#parser.add_argument("--figname", help="Nombre de la figura")
args=parser.parse_args()
if args.config_file!=None:
    print('Reading:',args.config_file)
    file_parser=ConfigParser()
    file_parser.read(args.config_file)
    for section_name in file_parser.sections():
        print('  Variable:', section_name)
        arg_list=shlex.split('--var_name='+section_name+' '+\
                file_parser.get(section_name,'options'))
        args=parser.parse_args(arg_list)
figname='_'.join([args.ID,args.tipo,args.var_name,args.stat])
if args.depth!=None:
    figname+='_'+'{:04d}'.format(args.depth)+'m'
if args.mes!=None:
    figname+='_M'+'{:02d}'.format(args.mes)
args.figname=figname
plot(args)
