# Valuation Model - WEG S.A. (WEGE3)

## Visão Geral

Este modelo de avaliação financeira foi desenvolvido para determinar o valor justo das ações da **WEG S.A. (WEGE3)** , uma das maiores empresas de equipamentos elétricos e eletrônicos do mundo. O modelo incorpora uma análise detalhada das demonstrações financeiras históricas, projeções futuras baseadas em cenários (Base, Bull, Bear), cálculo do custo de capital (WACC), e múltiplos métodos de valuation para chegar a um preço-alvo para a ação.

O trabalho foi realizado pelo **Grupo 2**, composto por:
- Augusto Schuster Franco
- Carlos Henrique Amorim
- Rafael Martone Regazzo
- Nicolas Beer

## Metodologia e Estrutura do Modelo

O modelo é construído no Microsoft Excel e está estruturado em múltiplas abas, cada uma com um propósito específico no processo de valuation. As principais etapas são:

1.  **Projeções de Receita e Custos:** Projeção detalhada dos resultados da empresa por segmento de negócio.
2.  **Demonstrações Financeiras Projetadas:** Construção da DRE, Balanço Patrimonial e Fluxo de Caixa para os próximos 5 anos.
3.  **Cálculo do Custo de Capital (WACC):** Determinação da taxa de desconto apropriada para o fluxo de caixa.
4.  **Valuation:** Utilização de métodos de fluxo de caixa descontado (DCF) e múltiplos de mercado (Múltiplos).
5.  **Análise de Sensibilidade e Cenários:** Avaliação do impacto de diferentes premissas no preço da ação.

## Estrutura das Abas do Arquivo

### `Cover`
*   **Propósito:** Página de rosto do modelo.
*   **Conteúdo:** Apresenta o título do projeto ("Valuation CJE Challenge"), a empresa analisada (WEG), os autores e a legenda de cores utilizada no modelo (Inputs, Formulas, Reference, Assumptions).

### `Model`
*   **Propósito:** O núcleo do modelo financeiro. É onde todas as projeções das demonstrações financeiras são construídas.
*   **Principais Funcionalidades:**
    *   **Seleção de Cenário:** O usuário pode escolher entre os cenários `Base`, `Bull` e `Bear` na célula `F5`. Isso aciona diferentes premissas de crescimento, taxas de câmbio e preços de commodities em todo o modelo.
    *   **Macroeconomia:** Incorpora premissas de inflação (IPCA), taxa de juros (SELIC), crescimento do PIB e taxa de câmbio (BRL/USD) fornecidas pelo Itaú BBA e IMF.
    *   **Receita por Segmento:** A receita líquida é projetada para quatro segmentos principais:
        *   Industrial Electrical and Electronic Equipment (IEE)
        *   Generation, Transmission and Distribution (GTD)
        *   Commercial Motors and Appliance (CMA)
        *   Paints and Varnishes (P&V)
        Cada segmento tem suas receitas domésticas e estrangeiras projetadas separadamente, com taxas de crescimento específicas por cenário.
    *   **Custo dos Produtos Vendidos (COGS):** Projetado com base em componentes como materiais (incluindo impacto do preço do cobre), despesas com pessoal, depreciação e outros custos.
    *   **Demonstração de Resultados (DRE):** Projeção de receita, lucro bruto, EBIT, EBT e lucro líquido, com todas as margens calculadas.
    *   **Balanço Patrimonial e Fluxo de Caixa:** Projeções completas do balanço (ativo, passivo e patrimônio líquido) e do fluxo de caixa, incluindo o cálculo do Capital de Giro Líquido (NOWC), CAPEX e um mecanismo de "revolver" para ajustar a posição de caixa.
    *   **Depreciação:** Cálculo detalhado da depreciação de ativos imobilizados (PP&E), intangíveis e direitos de uso (leasings), utilizando uma metodologia de *waterfall*.

### `DRE`
*   **Propósito:** Consolida as informações de Demonstração de Resultados do ano de 2020 em diante.
*   **Conteúdo:** Apresenta de forma resumida e clara a Receita Líquida, COGS, Lucro Bruto, SG&A, EBIT, Resultado Financeiro, EBT e Lucro Líquido, juntamente com as principais margens (Bruta, EBIT, EBITDA, Líquida), todas referenciadas da aba `Model`.

### `WACC` e `WACC forecast`
*   **Propósito:** Calcular o Custo Médio Ponderado de Capital (WACC) para descontar os fluxos de caixa.
*   **Metodologia:**
    *   **Custo de Capital Próprio (Ke):** Calculado pelo modelo CAPM.
        *   **Risk Free Rate (Rf):** 4,49% (10Y Treasury Yield dos EUA).
        *   **Equity Risk Premium (ERP):** 4,33% (Damodaran).
        *   **Beta (β):** 0,53 (calculado na aba `BETA & CRP`).
        *   **Country Risk Premium (CRP):** 3,34% (calculado na aba `BETA & CRP`).
        *   **Fórmula:** `Ke = Rf + β * (ERP) + CRP`
    *   **Custo de Capital de Terceiros (Kd):** Calculado como a média ponderada das taxas de juros efetivas sobre a dívida da empresa, considerando diferentes indexadores (CDI, TR, Euribor, etc.) e moedas.
    *   **Estrutura de Capital (We/Wd):** Ponderada pelo valor de mercado do patrimônio líquido e pelo valor contábil da dívida.
    *   **WACC Nominal:** `WACC = We * Ke + Wd * Kd * (1 - Tax Rate)`. O resultado é um WACC nominal em BRL.

### `BETA & CRP`
*   **Propósito:** Calcular o beta da WEG e o Country Risk Premium (CRP) ajustado pela exposição geográfica da empresa.
*   **Metodologia:**
    *   **Beta:** Calculado através de uma regressão dos retornos mensais da ação da WEG (WEGE3) contra os retornos do índice Ibovespa (IBOV) dos últimos 5 anos. O beta bruto é ajustado para aproximar um beta futuro (`Adj. Beta = 0,67 * Beta + 0,33`).
    *   **Country Risk Premium (CRP):** Começa com o CRP do Brasil (0,0334), conforme tabela do Damodaran, e é ponderado pela receita da WEG em diferentes regiões geográficas (Brasil, Europa, Ásia, etc.), reduzindo o risco país pelo percentual da receita obtida fora do Brasil.

### `DCF`
*   **Propósito:** Calcular o valor da empresa (Enterprise Value) e o preço justo da ação através do método do Fluxo de Caixa Livre para a Firma (FCFF).
*   **Metodologia:**
    *   **Projeção do FCFF:** O fluxo de caixa é projetado para 5 anos, usando dados da aba `Model`. A fórmula base é: `FCFF = NOPAT + D&A - Δ NOWC - CAPEX`.
    *   **Valor Terminal (Perpetuidade):** Calculado usando o modelo de crescimento em perpetuidade: `FCFF_TV = (FCFF_Ano_5 * (1+g)) / (WACC - g)`, onde `g` é a taxa de crescimento em perpetuidade (calculada na aba `Growth in perpetuity`).
    *   **Desconto:** Todos os fluxos de caixa são descontados a valor presente usando o WACC calculado.
    *   **Equity Value:** O valor da empresa (Enterprise Value) é reduzido pela dívida líquida (`Net Debt`) e pela participação de acionistas não-controladores (`Non-controlling shareholders`) para se chegar ao valor do patrimônio líquido (`Equity Value`).
    *   **Preço por Ação:** O valor do patrimônio líquido é dividido pelo número de ações em circulação (4,197 bilhões de ações).
    *   **Análise de Sensibilidade:** A aba `DCF` inclui uma análise de sensibilidade do preço da ação em relação a diferentes combinações de WACC e taxa de crescimento em perpetuidade (g).

### `Trading Comps`
*   **Propósito:** Realizar uma avaliação por múltiplos, comparando a WEG com empresas similares (peers).
*   **Peers Utilizados:** Siemens, GE, Nidec, Schneider, Rockwell, Regal Rexnord, ABB, Intelbrás, Eletrobrás, Hitachi e Emerson.
*   **Múltiplos Analisados:**
    *   **EV/EBITDA:** Histórico e projetado para os anos de 2020 a 2029.
    *   **P/E:** Histórico e projetado para os anos de 2020 a 2029.
*   **Cálculo do Preço Justo:** O modelo calcula um preço justo implícito para a WEG com base na mediana ou média dos múltiplos dos pares para os anos projetados, utilizando os dados de EBITDA e Lucro Líquido da WEG.
*   **ROIC, ROA, ROE:** As principais métricas de rentabilidade da WEG são calculadas para os anos projetados.

### `Growth in perpetuity`
*   **Propósito:** Calcular a taxa de crescimento em perpetuidade (g) usada no modelo DCF.
*   **Metodologia:** Utiliza a distribuição geográfica da receita da WEG e projeções de crescimento do PIB real para cada região, ajustadas pela inflação local para chegar a um crescimento nominal ponderado.

### Análises Adicionais

*   **`Reverse DCF`:** Calcula a taxa de crescimento implícita dos fluxos de caixa que justifica o preço atual da ação no mercado. É uma ferramenta para entender o que o mercado já está precificando.
*   **`Football field`:** Consolida os preços-alvo obtidos por diferentes métodos (DCF, Múltiplos, Preço dos analistas de mercado ("Broker")) em um único gráfico, fornecendo uma visão consolidada das avaliações.
*   **`Tornado`:** Realiza uma análise de sensibilidade do preço da ação em relação a variações em fatores-chave como WACC, crescimento na perpetuidade, taxa de câmbio e preço do cobre.
*   **`TIR`:** Calcula a Taxa Interna de Retorno (TIR) de um possível investimento, baseado nos fluxos de caixa projetados e na venda da empresa no final do período, utilizando um múltiplo de saída (EV/EBITDA).
*   **`Total shareholder return`:** Calcula o retorno total para o acionista (TSR) combinando a valorização das ações com os dividendos recebidos ao longo do período de projeção.
*   **Outras Abas (COGS, Staff Expense, Copper, etc.):** Fornecem suporte analítico detalhado para as principais premissas do modelo, como a evolução dos custos de mão de obra e a sensibilidade aos preços do cobre.

## Principais Premissas e Inputs

*   **Cenários:** Base (cenário mais provável), Bull (otimista) e Bear (pessimista).
*   **Taxa de Crescimento em Perpetuidade (g):** Calculada na aba `Growth in perpetuity`.
*   **Custo de Capital (WACC):** 11,0% (aproximadamente, no cenário Base).
*   **Preço do Cobre:** Varia de acordo com o cenário, impactando diretamente o COGS.
*   **Taxa de Câmbio (BRL/USD):** Projetada com base em premissas macroeconômicas e varia por cenário.
*   **Payout de Dividendos:** Baseado na média histórica dos anos projetados.

## Como Utilizar Este Modelo

1.  **Selecionar Cenário:** Na aba `Model`, altere a célula `F5` para "Base", "Bull" ou "Bear".
2.  **Verificar Premissas:** Revise as premissas macroeconômicas na aba `Model` e as premissas específicas (como crescimento dos segmentos e preço do cobre) que mudam automaticamente com o cenário selecionado.
3.  **Executar Análise:** O modelo recalculará automaticamente todas as projeções e o valuation. O preço justo por ação estará na aba `DCF`.
4.  **Consultar Sensibilidades:** Utilize as abas `Tornado`, `Football field` e `Sensitivity Analysis` na aba `DCF` para entender o impacto das variáveis no resultado final.

## Conclusão

Este modelo de valuation oferece uma análise robusta e detalhada da WEG S.A., combinando projeções financeiras bottom-up com metodologias de avaliação de mercado. A estrutura modular, com cenários e análises de sensibilidade, permite aos usuários uma compreensão aprofundada dos drivers de valor da empresa e dos riscos associados às suas premissas. O preço-alvo final é obtido como resultado de uma integração harmoniosa entre o fluxo de caixa descontado e a avaliação relativa por múltiplos.
