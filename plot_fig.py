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
    path+=struct_val['tipo']+'/'
    path+=struct_val['var']+'/'
    path+=struct_val['stat']+'/'
    os.makedirs(path,exist_ok=True)
    return(path)

def parse_units(units):
    if units=="degC":
        return "°C"
    else:
        return units

def plot(filename, figname):
    info=parse_name(figname)
    print('info:',info)
    if info==1:
        print('***¡Sintaxis de nombre incorrecta!***')
        exit(1)
    path=os.path.join(create_tree(info),figname)
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
    with open('config_plot.json','r') as ifile:
        data_cfg=json.load(ifile)
    if info['tipo']=='clim':
        per='0'
    elif info['tipo']=='mensual':
        per=str(info['mes'])
    cfg=data_cfg[info['var']][per][str(info['depth'])][info['stat']]
    print('cmap:',cfg)
    title='Climatología'
    #if info['tipo']=='mensual':
    #    title+='de '+month[info['mes']]
    #elif info['tipo']=='estacional':
    #    title+='de '+info['estacion']
    title+=' de '+info['var']
    title+=' ('+info['stat']+')'
    if info['depth']!=-1:
        title+=' a '+str(info['depth'])+' m '
    no_depth= False
    with nc.Dataset(filename, 'r') as root:
        try:
            z=root.variables['Depth'][:]
        except:
            no_depth = True
        if no_depth == False:
            idepth=np.argwhere(z==info['depth'])[0][0]
            var=root.variables[var_names[info['var']]][0][idepth]
        else:
            var=root.variables[var_names[info['var']]][0]
        try:
            lon=root.variables['Longitude'][:]
        except:
            lon=root.variables['longitude'][:]

        try:
            lat=root.variables['Latitude'][:]
        except:
            lat=root.variables['latitude'][:]
        #time=nc.num2date(root.variables['time'][:], root.variables['time'].units)
        units=root.variables[var_names[info['var']]].units

    units=parse_units(units)
    units='['+units+']'
    title+=units
    print(title)

    ax, figure = map_pcolor(lon, lat, var,
            title=title,
            tickBins={
                'x':[-98,-95,-92,-89,-86,-83,-80,-77],
                'y':[18,20,22,24,26,28,30,32],
                },
            cmap=cfg['cmap'],
            plot_land=True, vmin=cfg['vmin'], vmax=cfg['vmax'])
    if info['tipo']=='mensual':
        ax.annotate(month[info['mes']],xy=(0.02,0.94), xycoords='axes fraction')
    figure.savefig(path, bbox_inches='tight', dpi=200)

figname=sys.argv[1]
ifilename=sys.argv[2]
plot(ifilename, figname)
