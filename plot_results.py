# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 17:48:21 2013

@author: nipun
"""

import matplotlib.pyplot as plt
import matplotlib


matplotlib.rcParams.update({'font.size': 24})



def draw_table(MNE, RE, filename='temp123', path=''):
    
    #Creating table header for markdown table to be rendered by github
    file_contents="|Appliance|Case0|Case0|Case1|Case1|Case2|Case2|Case3|Case3|\n"
    file_contents+="|--"*9+"|\n"
    for appliance in MNE[0]:
        temp=""
        temp="|"+appliance
        for i in range(4):
            temp=temp+"|"+str(round(RE[i][appliance],2))
            temp=temp+"|"+str(round(MNE[i][appliance]*100,2))
        temp=temp+"|\n"
        file_contents+=temp
    with open("%s%s.md" %(path,filename), 'wa+') as outfile:
        outfile.write(file_contents)
    
    
    '''
    fig, ax = plt.subplots()
    ax.set_axis_off()
    
    column_header=('RE', 'MNE', 'RE', 'MNE','RE', 'MNE','RE', 'MNE')
    row_header=[appliance for appliance in MNE[0]]
    results=[]
    for appliance in MNE[0]:
        row=[]
        for i in range(4):
            row.append(str(RE[i][appliance]))
            row.append(str(MNE[i][appliance]*100))
        results.append(row)
    ax.table(cellText=results,rowLabels=row_header,colLabels=column_header,loc='center')
    plt.savefig(path+filename+'.md')
    '''

