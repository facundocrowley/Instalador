from db import *
def BackOffice(fantasia,cuit,RazonSocial,Direccion,CantCajas,ClienteID):

    #Esto es para declarar el valor de la sucursal donde estoy
    con=conexion() #Conecta sólo para el primer select
    con.execute("select sucursal from sistema") #################################Despues modificar para que te pregunte la sucursal, si no existe crearla y si ya existe tomar el valor de la variable
    Sucursal = con.fetchone()[0] #Esto guarda el primer valor de la primera fila
    con.execute("select EmpresaDefecto from sistema")
    Empresa = con.fetchone()[0] #Declara la empresa sobre la que trabajamos

    updClienteId=(f"update sistema set ClienteWeb={ClienteID}")# Se guarda el update en una variable
    updFantasia=(f"update sucursales set Descripcion='{fantasia}' where codigo={Sucursal}")# Se guarda el update en una variable
    updItemFactura=(f"update ConfigFacturacion set ItemsFactura=100")#
    updCompCant=(f"update ConfigFacturacion set ComprobantesCant=1")#
    updEmpresas=(f"update Empresas set Nombre='{fantasia}', cuit={cuit},RazonSocial='{RazonSocial}',Direccion='{Direccion}'  where Numero={Empresa}") #
    updClientes=(f"update Clientes set Documento=111111, TipoIva='C',TipoDocumento=1 where Nombre like '%Consumidor Final%' and Sucursal={Sucursal}")
    updModulos=(f"update Modulos set Descripcion ='*** '+(select descripcion from Sucursales where Codigo=(select Sucursal from Sistema))+' ***' where Modulo='PPP'")
    CrearCajas=(f" declare @cantidadcajas int set @cantidadcajas={CantCajas};declare @empresa int set @empresa={Empresa}; declare @sucursal int set @sucursal={Sucursal}; while @cantidadcajas>0 begin insert into cajas select @empresa,@sucursal,@cantidadcajas,@cantidadcajas,'H',9923,9930,'caja'+convert(nvarchar(1),@cantidadcajas),0,0 set @cantidadcajas=@cantidadcajas-1 end")

    update=updClienteId+updFantasia+updItemFactura+updCompCant+updEmpresas+updClientes+updModulos+CrearCajas
    con.execute(update) #Se ejecuta la secuencia guardada
    con.commit() #Afirma los cambios, sin esto no hace nada

    desconexion(con)
    #Declara las variables


fantasia=input('Nombre Fantasia: ')
cuit=input('CUIT: ')
RazonSocial=input('Razon Social: ')
Direccion=input('Dirección: ')
CantCajas=input('Cantidad de cajas: ')
ClienteID=input('Cliente ID: ')

BackOffice(fantasia,cuit,RazonSocial,Direccion,CantCajas,ClienteID)