from db import *


--Todos los datos en Empresas, Sistema,cajas y Clientes deben estar correctos

declare @puntoventa nvarchar(1000) set @puntoventa='1'
declare @NombreServer nvarchar(50) set @NombreServer='SERVER'
declare @esfacturaelectronica nvarchar(1) set @esfacturaelectronica='1'
declare @CorregirNumeracion nvarchar(1) set @CorregirNumeracion='1'



declare @nrocaja nvarchar(1000) set @nrocaja=(select Caja from Cajas where PuntoVenta=@puntoventa) --Numero de caja
declare @puntoventaNoFiscal nvarchar(5) set @puntoventanofiscal=(select puntoventa+1000 from Cajas where PuntoVenta=@puntoventa) --Punto de venta No fiscal
declare @empresa nvarchar(2)  set @empresa=(select empresadefecto from Sistema) --Numero de Empresa
declare @razonsocial nvarchar(50) set @razonsocial=(select razonsocial from Empresas where Numero=@empresa) --Razon social
declare @cuit nvarchar(max) set @cuit=(select cuit from Empresas where numero=@empresa) -- Cuit de Empresa
declare @cliente nvarchar(6) set @cliente=(select top 1 codigo from clientes where nombre	like '%Consumidor Final%' and Sucursal=(select sucursal from Sistema)) --Cliente Consumidor Final
declare @encabezado nvarchar(max)
declare @query nvarchar(max)
declare @configcae nvarchar(max)
declare @config nvarchar(max)
declare @numeracion nvarchar(max)
--	Config general	--
set @config= (select
'update pos_config set Nrocaja='+@nrocaja+';'+
'update pos_config set VentaImporteMinimo=1;'+
'update pos_config set VentaImporteMinimoCbte=1;'+
'update pos_config set PuertoFiscal='+char(39)+'\\127.0.0.1\POS-80'+char(39)+';'+
'update pos_config set FiscalMarca='+char(39)+'GENERICO_ANCHO'+char(39)+';'+
'update pos_config set FiscalModelo='+char(39)+'TMU220'+char(39)+';'+
'update pos_config set ModoItem='+char(39)+'T'+char(39)+';'+
'update pos_config set PuertoNoFiscal='+char(39)+'\\127.0.0.1\POS-80'+char(39)+';'+
'update pos_config set NoFiscalMarca='+char(39)+'GENERICO_ANCHO'+char(39)+';'+
'update pos_config set NoFiscalModelo='+char(39)+'TMU220'+char(39)+';'+
'update pos_config set PuntoVentaFiscal='+@puntoventa+';'+
'update pos_config set PuntoVentaNoFiscal='+@puntoventaNoFiscal+';'+
'update pos_config set NombreSvrLocalMP='+char(39)+@NombreServer+char(39)+';'+
'update pos_config set ClienteDefectoFC='+@cliente+';'+
'update pos_config set VerifNumCbtes=0;'+
'update pos_NumerosComprobantes set FormatoImpresion=2 where TipoCbte in ('+char(39)+'FA'+char(39)+','+char(39)+'CA'+char(39)+');'+
'update pos_NumerosComprobantes set FormatoImpresion=3 where TipoCbte in ('+char(39)+'RM'+char(39)+');'

)
--	Config CAE	--
set @configcae=''
if @esfacturaelectronica=1
begin
set @configcae= (select
'update pos_config set PuntoVenta_CAE='+@puntoventa+';'+
'update pos_config set esfacturaelectronica=1;'+
'update pos_config set Empresa_Cae='+@empresa+';'+
'update pos_config set Cuit_Empresa_Cae='+@cuit+';'
)
end
--	Encabezado	--
set @encabezado=
(select
'Delete from Encabezado;'+
'insert into Encabezado
select	1 as Linea,'+char(39)+(select Nombre from Empresas where Numero=@empresa)+char(39)+' as Texto,1 as Doble;'+
'insert into Encabezado '+
'select 2 as Linea,'+char(39)+(select RazonSocial from Empresas where Numero=@empresa)+char(39)+' as Texto,0 as Doble;'+
'insert into Encabezado '+
'select 3 as Linea,'+char(39)+'C.U.I.T.:'+(select CUIT from Empresas where Numero=@empresa)+char(39)+' as Texto,0 as Doble;'+
'insert into Encabezado '+
'select 4 as Linea,'+char(39)+'Ing. Brutos.:'+(select CUIT from Empresas where Numero=@empresa)+char(39)+' as Texto,0 as Doble;'+
'insert into Encabezado '+
'select 5 as Linea,'+char(39)+(select Direccion from Empresas where Numero=@empresa)+char(39)+' as Texto,0 as Doble;'+
'insert into Encabezado '+
'select 6 as Linea,'+char(39)+(select 'IVA Responsable Inscripto' from Empresas where Numero=@empresa)+char(39)+' as Texto,0 as Doble;'
)
--	Corregir numeracion	--
set @numeracion=''
if @CorregirNumeracion=1
begin
set @numeracion='update pos_NumerosComprobantes set NroSiguienteCbte=1 where TipoCbte not in ('+char(39)+'RC'+char(39)+','+char(39)+'RT'+char(39)+');'
end
--	Traer Query completa
set @query=@config+@configcae+@encabezado+@numeracion
select @query  as Query
