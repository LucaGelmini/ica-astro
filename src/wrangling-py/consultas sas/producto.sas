%let p_mes = 11; 
%let p_anio=2022;

filename entrada2 "/srv/sas/secex/home/comunicado/tablas/cenice_enm_descri.xlsx";
PROC IMPORT 
datafile = entrada2
OUT=work.cenice DBMS=XLSX REPLACE;

proc sql;
create table work.ppales_prod_impo_mensual as
select 
b.fech_aaaa as fech_aaaa,
b.fech_mm as fech_mm,
b.nomen as ncm_cod, 
b.cdescri_red as ncm_descri, 
b.cif as cif

from (
select distinct
a.fech_aaaa,
a.fech_mm,
a.nomen,
c.cdescri_red,
sum(a.VAL_DOL) as cif,
sum(a.FOB_DOL) as fob
from secexh.ce_tm3a a

left join work.cenice c
	on (a.cnro_enmienda = c.cnro_enmienda
	and a.nomen = c.ccod_capi||c.ccod_part||c.ccod_subp||c.cnomen)

where (a.fech_aa >= substr(put(&p_anio -1,4.),3,2)) and
a.fech_mm = put(&p_mes,2.)

group by
a.fech_aaaa,
a.fech_mm,
a.nomen,
c.cdescri_red
) b
;quit;

proc sql;
create table work.ppales_prod_impo_acumulado as
select 
b.fech_aaaa as fech_aaaa,
b.fech_mm as fech_mm,
b.nomen as ncm_cod, 
b.cdescri_red as ncm_descri, 
b.cif as cif

from (
select distinct
a.fech_aaaa,
a.fech_mm,
a.nomen,
c.cdescri_red,
sum(a.VAL_DOL) as cif,
sum(a.FOB_DOL) as fob
from secexh.ce_tm3a a

left join SECEXH.CE_CENICE_ENMIENDA c
	on (a.cnro_enmienda = c.cnro_enmienda
	and a.nomen = c.ccod_capi||c.ccod_part||c.ccod_subp||c.cnomen)

where (a.fech_aa >= substr(put(&p_anio -1,4.),3,2)) and
a.fech_mm >= put(&p_mes,2.)


group by
a.fech_aaaa,
a.fech_mm,
a.nomen,
c.cdescri_red
) b
;quit;

proc sql;
create table work.ppales_prod_impo_mensual as
select 
b.fech_aaaa as fech_aaaa,
b.fech_mm as fech_mm,
b.nomen as ncm_cod, 
b.cdescri_red as ncm_descri, 
b.cif as cif

from (
select distinct
a.fech_aaaa,
a.fech_mm,
a.nomen,
c.cdescri_red,
sum(a.VAL_DOL) as cif,
sum(a.FOB_DOL) as fob
from secexh.ce_tm3a a

left join SECEXH.CE_CENICE_ENMIENDA c
	on (a.cnro_enmienda = c.cnro_enmienda
	and a.nomen = c.ccod_capi||c.ccod_part||c.ccod_subp||c.cnomen)

where (a.fech_aa >= substr(put(&p_anio -1,4.),3,2)) and
a.fech_mm = put(&p_mes_comu,2.)

group by
a.fech_aaaa,
a.fech_mm,
a.nomen,
c.cdescri_red
) b
;quit;

proc sql;
create table work.ppales_prod_expo as 
 select distinct
   b.nanio,
   b.nmes,
/*   b.CCOD_PDES,*/
   b.
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
   b.CCOD_PDES
  
;quit;