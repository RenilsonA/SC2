import math as m

def define_equacoes(mapa, nivel, x, y, u, funcoes = True):
    const = 0.65
    if(mapa == 1):
        if(nivel == 1):
            const = 0.4
            l1 = - 5.2*x + 2.5*y + 3.2*u
            l2 = - 9.0*x - 0.8*y + 5.0*u
             
        elif(nivel == 2):
            const = 0.5
            l1 =   5.0*y
            l2 = - 9.0*x - 0.9*y + 5.0*u
            
        elif(nivel == 3):
            const = 0.25
            l1 = - 1.2*x + 2.0*y
            l2 =   3.6*x - 0.4*y - 5.0*u
            
        elif(nivel == 4):
            const = 0.25
            l1 =   1.0*x - 0.4*y + 0.6*u
            l2 =   1.8*x + 0.2*y - 5.0*u
            
        
    elif(mapa == 2):
        const = 0.2
        if(nivel == 1):
            l1 =   3.0*y + 1.0*u
            l2 = - 3.0*m.sin(8*x) - y
            
        elif(nivel == 2):
            l1 = - 2.0*x + m.atan(3.0*x) + 2.0*y + 2.0*u
            l2 =   2.0*x - 2.0*y
            
        elif(nivel == 3):
            l1 =   3.0*x*(0.5*x + 1.5*y) + 2.0*u
            l2 =   3.0*(x - y) + 1.0*u*u
            
        elif(nivel == 4):
            const = 0.05
            l1 = - 10.0*(x - 0.7)*(x + 0.7) + 5.0*u
            l2 = - 1.0*y + 2.0*u
                    
    elif(mapa == 3):
        if(nivel == 1):
            const = 0.2
            x = 10*x
            y = 10*y
            u  = 5*u
            l1 = 1.0*y + 0.5*u
            l2 = - 0.5*(x - y) + 0.8*u
            if x > y:
                l1 = l1 + 3
            else:
                l1 = l2 - 3.0
            
            l1 = l1/3.0
            l2 = l2/3.0
        
        elif(nivel == 2):
            const = 0.25
            l1 = -1.0*y
            l2 = -0.25*x
            if x > 0:
                l2 = l2 + 2*u
            else:
                l2 = l2 - 2*u
                    
        elif(nivel == 3):
            const = 0.25
            x = 10*x
            y = 10*y
            u  = 5*u
            l1 = -1.0*y
            l2 = 1.0*x
            if x < y:
                l2 = l2 + 4.0 + u
            else:
                l2 = l2 - 4.0 - u

            l1 = l1/4.0
            l2 = l2/4.0
            
        elif(nivel == 4):
            const = 0.3
            x = 10*x
            y = 10*y
            u  = 5*u
            z = 1.2759
            l1 = 0.7578*x - 1.9796*y
            l2 = 1.7454*x - 0.3350*y
            if (-0.1582*x + 1.8467*y) > 0:
                l1 = l1 + 0.1005*z*u 
                l2 = l2 - 2.16*z*u
            else:
                l1 = l1 - 0.1005*z*u 
                l2 = l2 + 2.16*z*u

            l1 = l1/6.0
            l2 = l2/6.0
        
    elif(mapa == 4):
        if(nivel == 1):
            const = 0.2
            x = 10*x
            y = 10*y
            u  = 5*u
            l1 = 1.0*y + 0.5*u
            l2 = - 0.5*(x + y) + 0.8*u
            if l1 > 0:
                l1 = 4.0
            else:
                l1 = - 4.0
            if l2 > 0:
                l2 = 4.0
            else:
                l2 = - 4.0

            l1 = l1/5.0
            l2 = l2/5.0
        
        elif(nivel == 2):
            const = 0.35
            x = 10*x
            y = 10*y
            u  = 5*u
            l1 = - 1.0*y
            l2 = 1.0*x + 1.0*u
            if (l1 > 0.0) and (l1 < 2.0):
                l1 = 2.0
            if (l1 < 0.0) and (l1 > -2.0):
                l1 = -2.0
            if (l1 > 2.0):
                l1 = 4.0
            if (l1 < -2.0):
                l1 = -4.0
        
            if (l2 > 0.0) and (l2 < 2.0):
                l2 = 2.0
            if (l2 < 0.0) and (l2 > -2.0):
                l2 = -2.0
            if (l2 > 2.0):
                l2 = 4.0
            if (l2 < -2.0):
                l2 = -4.0

            l1 = l1/5.0
            l2 = l2/5.0
        
        elif(nivel == 3):
            const = 0.2
            x = 10*x
            y = 10*y
            u  = 5*u
            l1 = 1.0*y
            l2 = 1.0*x + 2.0*u
            if (l1 > 0.0) and (l1 < 2.0):
                l1 = 2.0
            if (l1 < 0.0) and (l1 > -2.0):
                l1 = -2.0
            if (l1 > 2.0):
                l1 = 4.0
            if (l1 < -2.0):
                l1 = -4.0
        
            if (l2 > 0.0) and (l2 < 2.0):
                l2 = 2.0
            if (l2 < 0.0) and (l2 > -2.0):
                l2 = -2.0
            if (l2 > 2.0):
                l2 = 4.0
            if (l2 < -2.0):
                l2 = -4.0
                
            l1 = l1/5.0
            l2 = l2/5.0
        
        elif(nivel == 4):
            const = 0.2
            x = 10*x
            y = 10*y
            u  = 5*u
            l1 = 1.0*y + 1.0*u
            l2 = -(9.8/1.0)*m.sin(x) - 1.0*y
            if l1 >= 0:
                l1 = 2.0
            else:
                l1 = -2.0
            if l2 >= 0:
                l2 = 2.0
            else:
                l2 = -2.0
            l1 = l1/5.0
            l2 = l2/5.0
            
    if funcoes:
        return (l1, l2)
    return const
