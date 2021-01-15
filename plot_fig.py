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
            if len(val)!=2:
                return 1
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
    path+=struct_val['tipo']+'/'
    path+=struct_val['var']+'/'
    path+=struct_val['stat']+'/'
    os.makedirs(path,exist_ok=True)
    return(path)

def plot(filename, figname):
    info=parse_name(figname)
    print('info:',info)
    path=os.path.join(create_tree(info),figname)
    print(path)
    var_names={
            "temperatura":"pot_temp",
            }
    month={
            1:'enero',
            2:'febrero',
            3:'marzo',
            4:'abril',
            5:'mayo',
            6:'junio',
            7:'julio',
            8:'agosto',
            9:'septiembre',
            10:'octubre',
            11:'noviembre',
            12:'diciembre',
            }
    with open('config_plot.json','r') as ifile:
        data_cfg=json.load(ifile)
    per=str(info['mes'])
    cfg=data_cfg[info['var']][per][str(info['depth'])][info['stat']]
    print('cmap:',cfg)
    title='Climatología '
    if info['tipo']=='mensual':
        title+='de '+month[info['mes']]
    elif info['tipo']=='estacional':
        title+='de '+info['estacion']
    title+=' de '+info['var']
    title+=' ('+info['stat']+')'
    title+=' a '+str(info['depth'])+' m'
    with nc.Dataset(filename, 'r') as root:
        z=root.variables['Depth'][:]
        idepth=np.argwhere(z==info['depth'])[0][0]
        lon=root.variables['Longitude'][:]
        lat=root.variables['Latitude'][:]
        #time=nc.num2date(root.variables['time'][:], root.variables['time'].units)
        var=root.variables[var_names[info['var']]][0][idepth]
        units=root.variables[var_names[info['var']]].units

    units='['+units+']'
    print(title)
    ax, figure = map_pcolor(lon, lat, var,
            title=title,
            colorbar_label=units,
            cmap=cfg['cmap'],
            plot_land=True, vmin=cfg['vmin'], vmax=cfg['vmax'])
    figure.savefig(path, bbox_inches='tight', pad_inches=0.4,dpi=120)

figname=sys.argv[1]
ifilename=sys.argv[2]
plot(ifilename, figname)
