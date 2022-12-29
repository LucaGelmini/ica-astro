%let p_anio_comu = 2022;
%let p_anio=2022;
%let p_mes_comu = 11; 

proc sql;
create table work.socios_impo1 as
select distinct
b.fech_aaaa,
b.fech_mm,
b.pdest_final,
sum(b.cif) as cif

from (
select
a.fech_aaaa,
a.fech_mm,
case
	when missing(c.ccod_asoc) then a.porg
	else c.ccod_asoc
	end as pdest_final,
a.val_dol as cif

from secexh.ce_tm3a a

left join secex.ce_pais c
	on (a.porg = c.ccod_pais)

where a.fech_aa between '21' and '22' ) b

group by
b.fech_aaaa,
b.fech_mm,
b.pdest_final

;quit;

proc sql;
create table work.socios_impo2 as
select
a.fech_aaaa as anio,
a.fech_mm as mes,
a.pdest_final as pais_cod,
b.cdescri as pais_descri,
a.cif

from work.socios_impo1 a

left join secex.ce_pais b
	on (a.pdest_final=b.ccod_pais)

;quit;

proc sql;
create table work.socios_expo1 as
select distinct
   b.nanio,
   b.nmes,
   b.CCOD_PDES,
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

proc sql;
 create table work.socios_expo2 as 
 select distinct
   put(b.nanio,z4.) as fech_aaaa,
   put(b.nmes,z2.) as fech_mm,
   case 
     when missing(a.ccod_asoc) then  b.CCOD_PDES
	 else a.ccod_asoc
   end as pdest_final,
   sum(b.fob) as fob
 from work.socios_expo1 b

  left join secexh.ce_pais a
 on (b.ccod_pdes = a.ccod_pais)

 group by 
   b.nanio,
   b.nmes,
   pdest_final
;quit;

proc sql;
create table work.socios_expo3 as
select
a.fech_aaaa as anio,
a.fech_mm as mes,
a.pdest_final as pais_cod,
b.cdescri as pais_descri,
a.fob



from work.socios_expo2 a
left join secex.ce_pais b
	on (a.pdest_final=b.ccod_pais)
;quit;





