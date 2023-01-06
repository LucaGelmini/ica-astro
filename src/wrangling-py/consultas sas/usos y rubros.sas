%let p_anio_comu = 2022;
%let p_anio=2022;
%let p_mes_comu = 11;

filename entrada1 "/srv/sas/secex/home/comunicado/tablas/rubro.xlsx";
filename entrada2 "/srv/sas/secex/home/comunicado/tablas/uso.xlsx";

PROC IMPORT 
datafile = entrada1
OUT=work.rubro_original DBMS=XLSX REPLACE;
PROC IMPORT 
datafile = entrada2
OUT=work.uso_original DBMS=XLSX REPLACE;

proc sql;
create table work.expo_por_rubro1 as
select distinct
   b.nanio,
   b.nmes,
   b.ccod_rubro,
   sum(b.NFOB_E) as fob
 from 
   secex.ce_eresumen b,
   secex.ce_cifras_comu a
 where 
        b.cpublicado='S' 
    AND b.nmarca IN (1,3)
    and a.nanio_comu = &p_anio_comu
    AND a.nmes_comu= &p_mes_comu
    AND  a.cdepto='E'
    and b.nanio_proceso = a.nanio_proceso
    and b.nnro_proceso = a.nnro_proceso
    and b.nanio = a.nanio_conc
    and b.nmes = a.nmes_conc

	and b.nanio between &p_anio -1 and  &p_anio
/*    AND b.nmes <= &p_mes*/
  group by 
  b.nanio,
   b.nmes,
   b.ccod_rubro
  
;quit;

proc sql;
 create table work.expo_por_rubro2 as 
 select distinct
   put(b.nanio,z4.) as fech_aaaa,
   put(b.nmes,z2.) as fech_mm,
/*   SUBSTR(b.ccod_rubro,1,1) as rubro_cod,*/
   a.cdescri as rubro_descri,
   sum(b.fob) as fob

 from work.expo_por_rubro1 b

left join work.rubro_original a
on SUBSTR(b.ccod_rubro,1,1)= a.ccod_moai

 group by 
   b.nanio,
   b.nmes,
   rubro_descri
;quit;


proc sql;
create table work.impo_por_uso as
select distinct
a.fech_aaaa as anio,
a.fech_mm as mes, 
SUBSTR(a.uso,1,1) as uso,
b.cdescri,
sum(a.val_dol) as cif

from secexh.ce_tm3a a
left join work.uso_original b
on SUBSTR(a.uso,1,1)= b.ccod_uso

where a.fech_aa >='21'

group by
a.fech_aaaa,
a.fech_mm,
SUBSTR(a.uso,1,1)
/*b.cdescri*/
order by a.fech_aaaa
;quit;

proc sql;
create table work.expo_impo as
select
'Exportaciones' as comercio,
a.fech_aaaa as anio,
a.fech_mm as mes,
a.rubro_descri as rubro_uso,
a.fob as valor

from work.expo_por_rubro2 a 
union all
select 
'Importaciones' as comercio,
a.anio,
a.mes,
a.cdescri as rubro_uso,
a.cif as valor
from work.impo_por_uso a
;quit;

PROC export data= work.expo_impo
DBMS=CSV
outfile = "/srv/sas/secex/home/mbasualdo/ICA_web/expo_impo_rubros_usos.csv"
replace ;
;