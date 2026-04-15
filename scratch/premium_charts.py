import json
import os

file_path = r'c:\Users\allandiniz\Desktop\Data-Analytics-Grupo-24\1 - Projeto-Olist-KPIs\notebooks\Tech_Challenge_Grupo24_Allan.ipynb'

with open(file_path, 'r', encoding='utf-8-sig') as f:
    nb = json.load(f)

# Hardened search and replace for Premium Visuals
for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        source_text = "".join(cell.get('source', []))
        
        # 5.1 Pie Chart
        if "labels=['Venda Única', 'Recorrência (Fidelizados)']" in source_text or "labels=['Venda Ãšnica', 'Recorrentes']" in source_text:
            cell['source'] = [
                "# Taxa de Recompra - Visual Premium\n",
                "pedidos_por_cliente = df_consolidado.groupby('customer_unique_id')['order_id'].nunique().reset_index(name='qtd_pedidos')\n",
                "total_cl, recorrentes = len(pedidos_por_cliente), len(pedidos_por_cliente[pedidos_por_cliente['qtd_pedidos'] > 1])\n",
                "taxa_recompra = (recorrentes / total_cl) * 100\n",
                "\n",
                "plt.figure(figsize=(10, 7))\n",
                "plt.pie([total_cl - recorrentes, recorrentes], \n",
                "        labels=['Venda Única', 'Recorrência'], \n",
                "        autopct=lambda p: '{:.1f}%\\n({:,.0f})'.format(p, p * total_cl / 100), \n",
                "        startangle=140, colors=['#d1d8e0', '#20bf6b'], explode=(0, 0.1), shadow=True, \n",
                "        textprops={'fontsize': 12, 'fontweight': 'bold', 'color': '#2d3436'})\n",
                "\n",
                "plt.title('Taxa de Recompra: Fidelização de Clientes', fontsize=18, pad=30, fontweight='bold', color='#2d3436')\n",
                "plt.annotate(f'Taxa Global: {taxa_recompra:.2f}%', xy=(0.8, -0.9), fontsize=14, color='#27ae60', fontweight='bold')\n",
                "plt.show()"
            ]

        # 5.2 Churn Histplot
        if "ax = sns.histplot(ultima['meses']" in source_text or "sns.histplot(ultima['meses']" in source_text:
             cell['source'] = [
                "# Detecção de Churn (Inatividade) - Visual Premium\n",
                "plt.figure(figsize=(12, 6))\n",
                "sns.set_style(\"whitegrid\")\n",
                "ax = sns.histplot(ultima['meses'], bins=30, color='#3498db', kde=True, alpha=0.6)\n",
                "plt.axvline(6, color='#e74c3c', linestyle='--', linewidth=3, label='Alerta de Churn (6 meses)')\n",
                "\n",
                "plt.title('Tempo de Inatividade dos Clientes', fontsize=18, pad=20, fontweight='bold')\n",
                "plt.xlabel('Meses sem Comprar', fontsize=13)\n",
                "plt.ylabel('Volume de Clientes', fontsize=13)\n",
                "plt.legend(fontsize=12)\n",
                "\n",
                "# Anotação de Insight\n",
                "plt.annotate('Zona de Risco', xy=(8, plt.ylim()[1]*0.8), fontsize=14, color='#e74c3c', fontweight='bold')\n",
                "plt.show()"
             ]

        # 6. Bar Plots
        if "sns.barplot(data=df_primeira, x='recorrente_nome'" in source_text or "sns.barplot(data=df_primeira, x='recorrente'" in source_text:
             cell['source'] = [
                "# Fatores de Fidelização: O que divide os clientes?\n",
                "df_primeira = df_consolidado.sort_values('order_purchase_timestamp').groupby('customer_unique_id').first().reset_index()\n",
                "df_primeira['recorrente_nome'] = df_primeira['customer_unique_id'].isin(pedidos_por_cliente[pedidos_por_cliente['qtd_pedidos'] > 1]['customer_unique_id']).map({True: 'Fidelizado', False: 'Venda Única'})\n",
                "\n",
                "fig, ax = plt.subplots(1, 2, figsize=(16, 7))\n",
                "sns.set_palette([\"#b2bec3\", \"#20bf6b\"])\n",
                "\n",
                "# Atrasos\n",
                "sns.barplot(data=df_primeira, x='recorrente_nome', y='atrasado', ax=ax[0])\n",
                "ax[0].set_title('Impacto do Atraso Logístico', fontsize=15, fontweight='bold', pad=15)\n",
                "ax[0].set_ylabel('% de Pedidos com Atraso', fontsize=12)\n",
                "ax[0].set_xlabel('', fontsize=12)\n",
                "ax[0].set_yticklabels(['{:.0%}'.format(x) for x in ax[0].get_yticks()])\n",
                "\n",
                "# Satisfação (Review)\n",
                "sns.barplot(data=df_primeira, x='recorrente_nome', y='review_score', ax=ax[1], palette=[\"#b2bec3\", \"#3498db\"])\n",
                "ax[1].set_title('Impacto da Satisfação (Review)', fontsize=15, fontweight='bold', pad=15)\n",
                "ax[1].set_ylabel('Nota Média (1-5)', fontsize=12)\n",
                "ax[1].set_xlabel('', fontsize=12)\n",
                "ax[1].set_ylim(0, 5)\n",
                "\n",
                "plt.suptitle('Comparativo: O que gera a Recompra?', fontsize=20, fontweight='bold', y=1.02)\n",
                "plt.tight_layout()\n",
                "plt.show()"
             ]

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=1)

print("Notebook visual aesthetics upgraded to Premium.")
