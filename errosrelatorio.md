ModalGerarImagem.vue:180 [Vue warn]: Unhandled error during execution of render function 
  at <RelatorioImpressao key=0 dados-relatorio= 
{data_abate: '06/08/2025 a 06/09/2025', unidade: 'Todas as unidades', quantidade_aves: 85117, peso_total_vivo: 185190, peso_total_processado: 146017.90000000002, …}
 valores-calculados= 
{receita_bruta: 1661231.63, lucro_liquido: 439191.6299999999, rendimento: 78.847615961985}
  ... > 
  at <ModalGerarImagem is-visible=true dados-consolidados= 
{totalAves: 85117, pesoTotalVivo: 185190, pesoTotalProcessado: 146017.90000000002, receitaTotal: 1661231.63, custoTotal: 1222040, …}
 filtros= 
{dataInicio: '2025-08-07', dataFim: '2025-09-07', unidade: '', tipoRelatorio: 'produtos'}
  ... > 
  at <Relatorios key=3 > 
  at <BaseTransition mode="out-in" appear=false persisted=false  ... > 
  at <Transition name="fade" mode="out-in" > 
  at <App>
ModalGerarImagem.vue:180 [Vue warn]: Unhandled error during execution of component update 
  at <ModalGerarImagem is-visible=true dados-consolidados= 
{totalAves: 85117, pesoTotalVivo: 185190, pesoTotalProcessado: 146017.90000000002, receitaTotal: 1661231.63, custoTotal: 1222040, …}
 filtros= 
{dataInicio: '2025-08-07', dataFim: '2025-09-07', unidade: '', tipoRelatorio: 'produtos'}
  ... > 
  at <Relatorios key=3 > 
  at <BaseTransition mode="out-in" appear=false persisted=false  ... > 
  at <Transition name="fade" mode="out-in" > 
  at <App>
RelatorioImpressao.vue:502 Uncaught (in promise) TypeError: Cannot read properties of undefined (reading 'data_abate')
    at ComputedRefImpl.fn (RelatorioImpressao.vue:502:23)
    at Proxy._sfc_render (RelatorioImpressao.vue:15:37)

﻿

